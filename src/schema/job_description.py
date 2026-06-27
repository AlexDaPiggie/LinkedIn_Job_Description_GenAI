from pydantic import BaseModel, Field
class JobDescriptionDraft (BaseModel): 
    title: set
    about_company: str
    about_role: str
    responsibilities: list[str] = Field(default_factory=list)
    requirements: list[str] = Field(validate_default=list)
    benefits: list[str] = Field(default_factory=list)
    location: str
    equal_opportunity: str