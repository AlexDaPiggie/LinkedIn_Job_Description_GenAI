from pydantic import BaseModel, Field
def parse_list_answer (answer: str):
    '''
    THis function is for parsing  the text lines from user input, connecting them by ',' to match JSOn format
    '''
    pieces: list[str] = []
    for line in answer.splitlines():
        pieces.extend (line.split (','))
    return [piece.strip() for piece in pieces if piece.strip()]


'''
Data Class for Job Info
'''
class JobInfo (BaseModel): 
    company_name: str = ""
    role_title: str = ""
    role_summary: str = ""
    responsibilities: list[str] = Field(default_factory=list)
    requirements: list[str] = Field (default_factory=list)
    company_description: str | None = None
    nice_to_haves: list[str] = Field (default_factory=list)
    benefits: list[str] = Field(default_factory=list)
    why_join_us: str = ""
    equal_opportunity: str = ""
    tone: str = "professional"
    target_length: str = "medium"