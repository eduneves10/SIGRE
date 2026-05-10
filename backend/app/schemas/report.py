"""
Conjunto de Schemas Pydantic para padronização dos Payloads de Relatório.
"""

from pydantic import BaseModel
from typing import List, Optional
from .professor import ProfessorOut
from .discipline import DisciplineOut
from .course import CourseOut
from .room import RoomOut

class BaseDataReportOut(BaseModel):
    """
    Schema de resposta para a agregação de todos os cadastros base do sistema.
    Utilizado na exportação de planilhas de gestão inicial.
    """
    professors: List[ProfessorOut]
    disciplines: List[DisciplineOut]
    courses: List[CourseOut]
    rooms: List[RoomOut]

class UserReportOut(BaseModel):
    """
    Schema simplificado para o relatório de usuários, 
    seguindo a nomenclatura esperada pelo componente de exportação frontend.
    """
    Nome: str
    Email: str
    Papel: str
    Curso: Optional[str] = None
    Status: str

class HistoryReportOut(BaseModel):
    """
    Schema detalhado para o relatório de histórico de alocações.
    Contém dados formatados como strings para facilitar a renderização em PDF/Excel.
    Os nomes dos campos são intencionalmente capitalizados em português para corresponder
    diretamente às chaves JSON lidas pelo componente de exportação do frontend.
    """
    Data: str
    Horário: str
    Professor: str
    Disciplina: str
    Curso: Optional[str] = None
    Sala: str
