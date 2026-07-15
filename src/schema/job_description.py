from pydantic import BaseModel, Field
class JobDescriptionDraft (BaseModel): 
    title: str
    about_company: str
    about_role: str
    responsibilities: list[str] = Field(default_factory=list)
    requirements: list[str] = Field(default_factory=list)
    nice_to_haves: list[str] = Field (default_factory=list)
    benefits: list[str] = Field(default_factory=list)
    why_join_us: str = ""
    equal_opportunity: str = ""