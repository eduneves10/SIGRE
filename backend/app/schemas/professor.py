from pydantic import BaseModel, Field, ConfigDict, AliasChoices
from typing import Optional


class ProfessorBase(BaseModel):
    nomeProf: str = Field(..., validation_alias=AliasChoices("nomeProf", "nome"), serialization_alias="nomeProf")
    emailProf: Optional[str] = Field(None, validation_alias=AliasChoices("emailProf", "email"), serialization_alias="emailProf")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class ProfessorCreate(BaseModel):
    nomeProf: str = Field(..., validation_alias=AliasChoices("nomeProf", "nome"))
    emailProf: str = Field(..., validation_alias=AliasChoices("emailProf", "email"))

    model_config = ConfigDict(populate_by_name=True)


class ProfessorUpdate(BaseModel):
    nomeProf: Optional[str] = Field(None, validation_alias=AliasChoices("nomeProf", "nome"))
    emailProf: Optional[str] = Field(None, validation_alias=AliasChoices("emailProf", "email"))

    model_config = ConfigDict(populate_by_name=True)


class ProfessorOut(ProfessorBase):
    id: int
