from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import Float, ForeignKey, DateTime, Integer, func
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import uuid

from models import Base

class Estudantes(Base):
    __tablename__ = "estudantes"
    
    matricula: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    father_qualification = mapped_column() # Father's qualification,int,1–34,Nível de educa
    mother_qualification = mapped_column() # Mother's qualification,int,1–29,Nível de educa
    father_ocupation = mapped_column() # Father's occupation,int,1–46,Ocupação profissi
    mother_ocupation = mapped_column() # Mother's occupation,int,1–32,Ocupação profissi
    education_special_needs = mapped_column()
    debtor = mapped_column()
    tuiton_fees_up_to_date = mapped_column()
    scholarship_holder = mapped_column()
    marital_status = mapped_column()
    nationality = mapped_column()
    
    displaced = mapped_column()
    gender = mapped_column()
    age_at_enrollment = mapped_column()
    international = mapped_column()
    
    application_mode = mapped_column()
    application_order = mapped_column()
    course = mapped_column()
    school_time = mapped_column()
    previous_qualification = mapped_column()
    curricular_units_1st_sem_credited = mapped_column()
    curricular_units_1st_sem_enrolled = mapped_column()
    curricular_units_1st_sem_evaluations = mapped_column()
    curricular_units_1st_sem_approved = mapped_column()
    curricular_units_1st_sem_grade = mapped_column()
    curricular_units_1st_sem_without_evaluations = mapped_column()
    curricular_units_2nd_sem_credited = mapped_column()
    curricular_units_2nd_sem_enrolled = mapped_column()
    curricular_units_2nd_sem_evaluations = mapped_column()
    curricular_units_2nd_sem_approved = mapped_column()
    curricular_units_2nd_sem_grade = mapped_column()
    curricular_units_2nd_sem_without_evaluations = mapped_column()
    
    # nome: Mapped[str] = mapped_column(String(200), nullable=False)
    # endereco: Mapped[str] = mapped_column(String(50), nullable=False)
    # latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    # longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    # cuisine: Mapped[str] = mapped_column(String(100), nullable=True)
    # telefone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    # website: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    
    data_predictor: Mapped[Optional[datetime]] = mapped_column(DateTime(), default=lambda: datetime.now(), server_default=func.now()) 