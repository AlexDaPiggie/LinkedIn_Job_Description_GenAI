from pydantic import BaseModel

'''
Data Class to store the properties of the input wrapper
'''
class IntakeQuestion (BaseModel):
    question_name: str
    question_text: str
    required: bool
    answer_type: str = "text"

    @property
    def can_skip(self): 
        return not self.required
    
QUESTIONS = [
    IntakeQuestion(
        question_name = "company_name",
        question_text = "What is your company name?",
        required = True,
    ),
    IntakeQuestion(
        question_name ="role_title",
        question_text= "What role are you hiring for?",
        required = True
    ),
    IntakeQuestion(
        question_name = "role_summary",
        question_text = "Why is the company hiring this role, and what should this person help accomplish?",
        required = True,
    ),
    IntakeQuestion(
        question_name="responsibilities",
        question_text="What is the role the applicates with be responsible for?",
        required = True,
        answer_type = "list",
    ),
    IntakeQuestion(
        question_name = "requirements",
        question_text = "What skills, experience, or qualifications are required?",
        required = True,
        answer_type = "list",
    ),
    IntakeQuestion(
        question_name="nice_to_haves",
        question_text="What skills or experience would be nice to have, but not required?",
        required = False,
        answer_type = "list",
    ),
    IntakeQuestion(
        question_name="salary_range",
        question_text="What salary range you want to include?",
        required = False,
    ),
    IntakeQuestion(
        question_name="company_description",
        question_text="How would you describe the company in a few sentences?",
        required=False,
    ),
    IntakeQuestion (
        question_name="why_join_us",
        question_text="Why should candidates be excited to join this company or team? " "Mention things like mission, culture, growth, impact, or interesting work.",
        required = False,
    ),
    IntakeQuestion(
        question_name="benefits",
        question_text="Are there any benefit, perk, or compensation you would like  to include?",
        required = False,
        answer_type = "list",
    ),
    IntakeQuestion(
        question_name="tone",
        question_text="What tone do you want the job description to sound?",
        required = False,
    ),
    IntakeQuestion(
        question_name="target_length",
        question_text="How long should the job description be: short, medium, or long?",
        required = False,
    ),
    IntakeQuestion(
        question_name="equal_opportunity",
        question_text="Do you want to include an equal opportunity statement in the job description?",
        required = False,
    )
]

def get_next_question (index: int):
    '''
    This function is simply to return the next question in the list above, knowing the index
    '''
    if index >= len (QUESTIONS): 
        return None
    return QUESTIONS[index]

