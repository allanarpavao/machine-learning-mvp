from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class EstudanteSchema(BaseModel):
    """Define os atributos de um estudante para predição de risco de evasão
    """
    father_qualification: int = 1
    mother_qualification: int = 1
    father_occupation: int = 1
    mother_occupation: int = 1

    education_special_needs: int = 0
    debtor: int = 0
    tuition_fees_up_to_date: int = 1
    scholarship_holder: int = 0
    marital_status: int = 1
    nationality: int = 1
    displaced: int = 1
    gender: int = 0
    age_at_enrollment: int = 19
    international: int = 0

    application_mode: int = 1
    application_order: int = 4
    course: int = 1
    daytime_evening_attendance: int = 1
    previous_qualification: int = 1
    previous_qualification_grade: float = 95
    admission_grade: float = 95

    curricular_units_1st_sem_credited: int = 0
    curricular_units_1st_sem_enrolled: int = 6
    curricular_units_1st_sem_evaluations: int = 8
    curricular_units_1st_sem_approved: int = 5
    curricular_units_1st_sem_grade: float = 14.333
    curricular_units_1st_sem_without_evaluations: int = 0

    curricular_units_2nd_sem_credited: int = 0
    curricular_units_2nd_sem_enrolled: int = 6
    curricular_units_2nd_sem_evaluations: int = 7
    curricular_units_2nd_sem_approved: int = 5
    curricular_units_2nd_sem_grade: float = 13.500
    curricular_units_2nd_sem_without_evaluations: int = 0

class EstudanteViewSchema(BaseModel):
    """Define como o estudante será retornado
    """
    model_config = ConfigDict(from_attributes=True)
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

