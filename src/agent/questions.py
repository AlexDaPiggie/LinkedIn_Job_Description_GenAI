"""Definition of the intake questions asked to the user."""

from pydantic import BaseModel


class IntakeQuestion(BaseModel):
    """One question in the intake questionnaire.

    Attributes:
        question_name: Identifier matching a `JobInfo` field.
        question_text: Text shown to the user.
        required: Whether the user must answer.
        answer_type: "text" for a single value or "list" for several items.
        recommended: Optional, but answering it noticeably improves the
            draft (the UI nudges the user to fill it in).
    """

    question_name: str
    question_text: str
    required: bool
    answer_type: str = "text"
    recommended: bool = False

    @property
    def can_skip(self) -> bool:
        """Whether the user may leave this question unanswered."""
        return not self.required


QUESTIONS = [
    IntakeQuestion(
        question_name="company_name",
        question_text="What is your company name?",
        required=True,
    ),
    IntakeQuestion(
        question_name="role_title",
        question_text="What role are you hiring for?",
        required=True,
    ),
    IntakeQuestion(
        question_name="role_summary",
        question_text="Why is the company hiring this role, and what should this person help accomplish?",
        required=True,
    ),
    IntakeQuestion(
        question_name="responsibilities",
        question_text="What are the primary responsibilities for this role?",
        required=True,
        answer_type="list",
    ),
    IntakeQuestion(
        question_name="requirements",
        question_text="What skills, experience, or qualifications are required?",
        required=True,
        answer_type="list",
    ),
    IntakeQuestion(
        question_name="nice_to_haves",
        question_text="What skills or experience would be nice to have, but not required?",
        required=False,
        answer_type="list",
    ),
    IntakeQuestion(
        question_name="company_description",
        question_text="How would you describe the company in a few sentences?",
        required=False,
    ),
    IntakeQuestion(
        question_name="team_context",
        question_text="Who will this person work with? (team size, manager, partner teams)",
        required=False,
        recommended=True,
    ),
    IntakeQuestion(
        question_name="why_join_us",
        question_text="Why should candidates be excited to join this company or team?\n(mission, culture, growth, impact, or interesting work.)",
        required=False,
        recommended=True,
    ),
    IntakeQuestion(
        question_name="benefits",
        question_text="Are there any benefit, perk, or compensation details you would like to include?",
        required=False,
        answer_type="list",
    ),
]


def get_next_question(question_index: int) -> IntakeQuestion | None:
    """Returns the question at the given position.

    Args:
        question_index: Zero-based position in `QUESTIONS`.

    Returns:
        The question, or None when all questions have been asked.
    """
    if question_index >= len(QUESTIONS):
        return None
    return QUESTIONS[question_index]
