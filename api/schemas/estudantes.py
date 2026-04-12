from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class EstudanteSchema(BaseModel):
    """Define os atributos de um estudante para predição de risco de evasão
    """
    Marital_status: int = 1
    Nationality: int = 1
    Displaced: int = 1
    Gender: int = 0
    Age_at_enrollment: int = 19
    International: int = 0

    Mothers_qualification: int = 1
    Fathers_qualification: int = 1
    Mothers_occupation: int = 1
    Fathers_occupation: int = 1
    Educational_special_needs: int = 0
    Debtor: int = 0
    Tuition_fees_up_to_date: int = 1
    Scholarship_holder: int = 0

    Application_mode: int = 1
    Application_order: int = 1
    Course: int = 1
    Daytime_evening_attendance: int = 1
    Previous_qualification: int = 1

    Curricular_units_1st_sem_credited: int = 0
    Curricular_units_1st_sem_enrolled: int = 6
    Curricular_units_1st_sem_evaluations: int = 8
    Curricular_units_1st_sem_approved: int = 5
    Curricular_units_1st_sem_grade: float = 14.333
    Curricular_units_1st_sem_without_evaluations: int = 0

    Curricular_units_2nd_sem_credited: int = 0
    Curricular_units_2nd_sem_enrolled: int = 6
    Curricular_units_2nd_sem_evaluations: int = 7
    Curricular_units_2nd_sem_approved: int = 5
    Curricular_units_2nd_sem_grade: float = 13.500
    Curricular_units_2nd_sem_without_evaluations: int = 0

class EstudanteViewSchema(BaseModel):
    """Define como o estudante será retornado
    """
    matricula: int
    situacao_academica: str

# class UsuarioBuscaSchema(BaseModel):
#     """ Define como deve ser a estrutura que representa a busca.
#         A busca será feita apenas com base no uuid do usuario.
#     """
#     id_usuario: str = "7a743fa4-57b5-4b0b-b97a-5da34a58bf62"

# class ListagemUsuariosSchema(BaseModel):
#     """ Define como uma listagem de produtos será retornada.
#     """
#     usuarios: List[UsuarioSchema]

