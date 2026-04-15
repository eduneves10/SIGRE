from pydantic import BaseModel, Field, ConfigDict, computed_field, AliasChoices
from typing import Optional, Union

class RoomBase(BaseModel):
    nomeSala: str = Field(..., validation_alias=AliasChoices("nomeSala", "codigo_sala"), serialization_alias="nomeSala")
    tipoSala: Optional[str] = Field(None, validation_alias=AliasChoices("tipoSala", "tipo_sala"), serialization_alias="tipoSala")
    tipoSalaId: Optional[int] = Field(None, validation_alias=AliasChoices("tipoSalaId", "fk_tipo_sala", "tipo_sala_id"), serialization_alias="tipoSalaId")
    descricao_sala: Optional[str] = None
    capacidade: Optional[int] = Field(None, validation_alias=AliasChoices("capacidade", "limite_usuarios"))

class RoomCreate(BaseModel):
    nomeSala: str
    tipoSalaId: int = Field(..., alias="tipoSalaId")
    descricao_sala: Optional[str] = None
    capacidade: Optional[int] = None

class RoomUpdate(BaseModel):
    nomeSala: Optional[str] = None
    tipoSalaId: Optional[int] = Field(None, alias="tipoSalaId")
    descricao_sala: Optional[str] = None
    capacidade: Optional[int] = None

class RoomOut(RoomBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @computed_field
    @property
    def idSala(self) -> int:
        return self.id
