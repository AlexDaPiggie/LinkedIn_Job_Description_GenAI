"""Session state for the question-by-question intake flow."""

from pydantic import BaseModel, Field

from src.agent.questions import QUESTIONS, IntakeQuestion, get_next_question
from src.schema.job_description import JobDescriptionDraft
from src.schema.job_info import JobInfo, parse_list_answer


class QuestionAnswer(BaseModel):
    """The recorded answer to one intake question.

    Attributes:
        question_name: Identifier of the answered question.
        question_text: Text of the question as shown to the user.
        answer_text: The cleaned answer, or None if left blank.
        skipped: True when the answer is blank.
    """

    question_name: str
    question_text: str
    answer_text: str | None = None
    skipped: bool = True


class SessionState(BaseModel):
    """Progress of one intake session and its latest generated draft.

    Attributes:
        job_info: Hiring details gathered so far.
        answers: Recorded answers keyed by question name.
        question_index: Position of the next unanswered question.
        current_draft: Latest generated draft, if any.
        current_draft_markdown: Latest rendered Markdown, if any.
        draft_outdated: True when answers changed after the draft was made.
    """

    job_info: JobInfo = Field(default_factory=JobInfo)
    answers: dict[str, QuestionAnswer] = Field(default_factory=dict)
    question_index: int = 0
    current_draft: JobDescriptionDraft | None = None
    current_draft_markdown: str | None = None
    draft_outdated: bool = False

    def _require_current_question(self) -> IntakeQuestion:
        """Returns the current question.

        Raises:
            ValueError: If every question has already been answered.
        """
        question = self.current_question()
        if question is None:
            raise ValueError("No remaining questions")
        return question

    def _find_question(self, question_name: str) -> IntakeQuestion:
        """Looks up a question by its identifier.

        Args:
            question_name: Identifier of the question.

        Returns:
            The matching question.

        Raises:
            ValueError: If no question has that identifier.
        """
        for question in QUESTIONS:
            if question.question_name == question_name:
                return question
        raise ValueError(f"Unknown field name: {question_name}")

    def _set_job_info_field(self, question: IntakeQuestion, answer: str) -> None:
        """Writes an answer into the matching `JobInfo` field.

        A blank answer resets the field to its empty value (None for
        optional text fields, [] for lists, "" otherwise).

        Args:
            question: Question the answer belongs to.
            answer: Cleaned answer text.
        """
        field_name = question.question_name
        # equal_opportunity is not collected through the questionnaire.
        if field_name == "equal_opportunity":
            return

        if not answer:
            if question.answer_type == "list":
                empty_value = []
            elif field_name in {"company_description", "salary_range"}:
                empty_value = None
            else:
                empty_value = ""
            setattr(self.job_info, field_name, empty_value)
            return

        value = parse_list_answer(answer) if question.answer_type == "list" else answer
        setattr(self.job_info, field_name, value)

    def _record_answer(self, question: IntakeQuestion, cleaned_answer: str) -> None:
        """Stores an answer in both `job_info` and `answers`.

        Args:
            question: Question being answered.
            cleaned_answer: Answer with surrounding whitespace removed.
        """
        self._set_job_info_field(question, cleaned_answer)
        self.answers[question.question_name] = QuestionAnswer(
            question_name=question.question_name,
            question_text=question.question_text,
            answer_text=cleaned_answer or None,
            skipped=not cleaned_answer,
        )

    def current_question(self) -> IntakeQuestion | None:
        """Returns the question awaiting an answer, or None when finished."""
        return get_next_question(self.question_index)

    def submit_answer(self, answer: str) -> None:
        """Answers the current question and advances to the next one.

        Args:
            answer: Raw answer text from the input box.

        Raises:
            ValueError: If there are no remaining questions.
        """
        question = self._require_current_question()
        self._record_answer(question, answer.strip())
        self.question_index += 1

    def edit_answer(self, question_name: str, answer: str) -> None:
        """Replaces a previously submitted answer.

        Marks the draft as outdated if one already exists.

        Args:
            question_name: Identifier of the question to change.
            answer: New raw answer text.

        Raises:
            ValueError: If the question identifier is unknown.
        """
        question = self._find_question(question_name)
        self._record_answer(question, answer.strip())
        if self.current_draft or self.current_draft_markdown:
            self.draft_outdated = True

    def missing_required_questions(self) -> list[IntakeQuestion]:
        """Returns the required questions that have no real answer yet."""
        missing_questions = []
        for question in QUESTIONS:
            answer = self.answers.get(question.question_name)
            if question.required and (answer is None or answer.skipped):
                missing_questions.append(question)
        return missing_questions

    def skipped_fields(self) -> list[str]:
        """Returns the names of all questions unanswered or left blank."""
        skipped_names = []
        for question in QUESTIONS:
            answer = self.answers.get(question.question_name)
            if answer is None or answer.skipped:
                skipped_names.append(question.question_name)
        return skipped_names
