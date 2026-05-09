from pydantic import BaseModel, Field, ConfigDict, computed_field, AliasChoices
from typing import Optional

class ProfessorBase(BaseModel):
    nomeProf: str = Field(..., validation_alias=AliasChoices("nomeProf", "nome"), serialization_alias="nomeProf")
    emailProf: Optional[str] = Field(None, validation_alias=AliasChoices("emailProf", "email"), serialization_alias="emailProf")
    matriculaProf: Optional[str] = Field(None, validation_alias=AliasChoices("matriculaProf", "matricula"), serialization_alias="matriculaProf")
    siapeProf: Optional[str] = Field(None, validation_alias=AliasChoices("siapeProf", "siape"), serialization_alias="siapeProf")

class ProfessorCreate(BaseModel):
    """matriculaProf é a matrícula funcional; siapeProf é o código SIAPE federal."""

    nomeProf: str = Field(..., validation_alias=AliasChoices("nomeProf", "nome"))
    emailProf: str = Field(..., validation_alias=AliasChoices("emailProf", "email"))
    matriculaProf: Optional[str] = Field(None, validation_alias=AliasChoices("matriculaProf", "matricula"))
    siapeProf: Optional[str] = Field(None, validation_alias=AliasChoices("siapeProf", "siape"))

class ProfessorUpdate(BaseModel):
    nomeProf: Optional[str] = Field(None, validation_alias=AliasChoices("nomeProf", "nome"))
    emailProf: Optional[str] = Field(None, validation_alias=AliasChoices("emailProf", "email"))
    matriculaProf: Optional[str] = Field(None, validation_alias=AliasChoices("matriculaProf", "matricula"))
    siapeProf: Optional[str] = Field(None, validation_alias=AliasChoices("siapeProf", "siape"))

class ProfessorOut(ProfessorBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @computed_field
    @property
    def idProfessor(self) -> int:
        return self.id
