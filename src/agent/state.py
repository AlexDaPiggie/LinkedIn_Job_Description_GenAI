from pydantic import BaseModel, Field
from src.agent.questions import QUESTIONS, IntakeQuestion, get_next_question
from src.schema.job_description import JobDescriptionDraft
from src.schema.job_info import JobInfo, parse_list_answer

'''
Data Class to document the status of the answers
'''
class QuestionAnswer(BaseModel):
    question_name: str
    question_text: str
    answer_text: str | None = None
    skipped: bool = True

'''
Data Class to store the version of the drafts, with detailed status of each question
'''
class SessionState(BaseModel):
    job_info: JobInfo = Field (default_factory=JobInfo)
    answers: dict[str, QuestionAnswer] = Field(default_factory=dict)
    question_index: int = 0
    current_draft_json: JobDescriptionDraft | None = None
    current_draft_markdown: str | None = None
    draft_outdated: bool = False

    def _required_current_question(self):
        '''
        This function is to return the question text
        '''
        question = self.current_question()
        if question is None:
            raise ValueError("No remaining questions")
        return question
    
    def _question_by_question_name(self, question_name: str):
        '''
        This function is to return the question text, knowing the question id (question_name)
        '''
        for question in QUESTIONS:
            if question.question_name == question_name:
                return question
        raise ValueError(f"Unknown field name: {question_name}")
    
    def _answer_counts_as_skipped(self, question:IntakeQuestion, answer: str):
        
        if not answer:
            return True
        return False
        
    def _set_job_info_field (self, question: IntakeQuestion, answer: str):
        if not answer: 
            if question.question_name == "equal_opportunity": 
                return 
            if question.answer_type == "list":
                setattr(self.job_info, question.question_name, [])
                return 

            if question.question_name in {"company_description", "salary_range"}:
                setattr(self.job_info, question.question_name, None)
                return 
            setattr(self.job_info, question.question_name, "")
            return 
        
        if question.question_name == "equal_opportunity": 
            return 
        
        value = parse_list_answer(answer) if question.answer_type == "list" else answer 

        setattr(self.job_info, question.question_name, value)
    
    def current_question(self):
        '''
        This helper function is to iterate to the next question, knowing the current question index.
        '''
        return get_next_question(self.question_index)
    
    def submit_answer(self, answer: str): 
        '''
        This function submits the answer from the input box
        '''
        question = self._required_current_question()
        cleaned_answer = answer.strip()
        self._set_job_info_field (question, cleaned_answer)
        self.answers[question.question_name]  = QuestionAnswer(
            question_name = question.question_name,
            question_text = question.question_text,
            answer_text = cleaned_answer or None,
            skipped = self._answer_counts_as_skipped (question, cleaned_answer)
        )
        self.question_index += 1

    def edit_answer (self, question_name: str, answer: str): 
        '''
        This question is for editing the submnitted answer
        '''
        question = self._question_by_question_name(question_name)
        cleaned_answer = answer.strip()
        self._set_job_info_field(question, cleaned_answer)
        self.answers[question.question_name] = QuestionAnswer(
            question_name = question.question_name,
            question_text = question.question_text,
            answer_text = cleaned_answer or None,
            skipped = self._answer_counts_as_skipped(question, cleaned_answer),
        )
        if self.current_draft_json or self.current_draft_markdown:
            self.draft_outdated = True

    def missing_required_questions (self):
        '''
        This question is to return error when required questions are blank (without an answer)
        '''
        missing = []
        for question in QUESTIONS:
            answer = self.answers.get (question.question_name)
            if question.required and (answer is None or answer.skipped):
                missing.append (question)
        return missing
        
    def skipped_fields (self): 
        '''
        THis function is to record the fields that have been skipped by users
        '''
        skipped = []
        for question in QUESTIONS:
            answer = self.answers.get (question.question_name)
            if answer is None or answer.skipped: 
                skipped.append (question.question_name)
        return skipped
        