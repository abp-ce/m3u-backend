from datetime import datetime

from pydantic import BaseModel


class PersonalList(BaseModel):
    title: str
    value: str


class ProgrammeResponse(BaseModel):
    disp_name: str | None = None
    pstart: datetime
    pstop: datetime
    title: str
    pdesc: str | None = None

    class Config:
        orm_mode = True
