from pydantic import BaseModel
from datetime import date


class AllSchema(BaseModel):
    unit: str


class AllVilaSchema(AllSchema):
    villa_count: int


class ALLProjectSchema(AllSchema):
    u_type: str
    project_count: int


class ProjectSearchSchema(AllSchema):
    beds: int
    u_type: str
    area: float
    price: int
    date: date
