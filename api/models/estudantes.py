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

#TODO: criar matricula automaticamente
class Estudante(Base):
    __tablename__ = "estudantes"
    
    # matricula: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    matricula: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    
    # Dados familiares
    father_qualification: Mapped[int] = mapped_column(Integer, nullable=False, doc="Nível de educação do pai (1–34)")
    mother_qualification: Mapped[int] = mapped_column(Integer, nullable=False, doc="Nível de educação da mãe (1–29)")
    father_ocupation: Mapped[int] = mapped_column(Integer, nullable=False, doc="Ocupação profissional do pai (1–46)")
    mother_ocupation: Mapped[int] = mapped_column(Integer, nullable=False, doc="Ocupação profissional da mãe (1–32)")
    
    # Informações Pessoais
    education_special_needs: Mapped[int] = mapped_column(Integer, nullable=False, doc="Necessidades educacionais especiais (0=Não, 1=Sim)")
    debtor: Mapped[int] = mapped_column(Integer, nullable=False, doc="Inadimplente (0=Não, 1=Sim)")
    tuiton_fees_up_to_date: Mapped[int] = mapped_column(Integer, nullable=False, doc="Mensalidades em dia (0=Não, 1=Sim)")
    scholarship_holder: Mapped[int] = mapped_column(Integer, nullable=False, doc="Bolsista (0=Não, 1=Sim)")
    marital_status: Mapped[int] = mapped_column(Integer, nullable=False, doc="Estado civil do aluno (1–6)")
    nationality: Mapped[int] = mapped_column(Integer, nullable=False, doc="Nacionalidade do aluno (1–21)")
    displaced: Mapped[int] = mapped_column(Integer, nullable=False, doc="Proveniente de outra região (0=Não, 1=Sim)")
    gender: Mapped[int] = mapped_column(Integer, nullable=False, doc="Gênero do aluno (0=Feminino, 1=Masculino)")
    age_at_enrollment: Mapped[int] = mapped_column(Integer, nullable=False, doc="Idade do aluno na matrícula (17–70)")
    international: Mapped[int] = mapped_column(Integer, nullable=False, doc="Estudante internacional (0=Não, 1=Sim)")
    
    # Dados durante matricula
    application_mode: Mapped[int] = mapped_column(Integer, nullable=False, doc="Modo de candidatura (1–18)")
    application_order: Mapped[int] = mapped_column(Integer, nullable=False, doc="Ordem de preferência na candidatura (1–9)")
    course: Mapped[int] = mapped_column(Integer, nullable=False, doc="Curso matriculado (1–17)")
    school_time: Mapped[int] = mapped_column(Integer, nullable=False, doc="Turno do curso (0=Noturno, 1=Diurno)")
    previous_qualification: Mapped[int] = mapped_column(Integer, nullable=False, doc="Qualificação anterior (1–17)")
    
    # Desempenho Acadêmico - 1o Sem
    # UC = unidades curriculares
    curricular_units_1st_sem_credited: Mapped[int] = mapped_column(Integer, nullable=False, doc="Disciplinas creditadas 1º sem (0–20)")
    curricular_units_1st_sem_enrolled: Mapped[int] = mapped_column(Integer, nullable=False, doc="Disciplinas matriculadas 1º sem (0–26)")
    curricular_units_1st_sem_evaluations: Mapped[int] = mapped_column(Integer, nullable=False, doc="Avaliações realizadas 1º sem (0–45)")
    curricular_units_1st_sem_approved: Mapped[int] = mapped_column(Integer, nullable=False, doc="Disciplinas aprovadas 1º sem (0–26)")
    curricular_units_1st_sem_grade: Mapped[float] = mapped_column(Float, nullable=False, doc="Média de notas 1º sem (0.000–18.875)")
    curricular_units_1st_sem_without_evaluations: Mapped[int] = mapped_column(Integer, nullable=False, doc="Disciplinas sem avaliação 1º sem (0–12)")
    
    # Desempenho Acadêmico - 2o Sem
    curricular_units_2nd_sem_credited: Mapped[int] = mapped_column(Integer, nullable=False, doc="Disciplinas creditadas 2º sem (0–19)")
    curricular_units_2nd_sem_enrolled: Mapped[int] = mapped_column(Integer, nullable=False, doc="Disciplinas matriculadas 2º sem (0–23)")
    curricular_units_2nd_sem_evaluations: Mapped[int] = mapped_column(Integer, nullable=False, doc="Avaliações realizadas 2º sem (0–33)")
    curricular_units_2nd_sem_approved: Mapped[int] = mapped_column(Integer, nullable=False, doc="Disciplinas aprovadas 2º sem (0–20)")
    curricular_units_2nd_sem_grade: Mapped[float] = mapped_column(Float, nullable=False, doc="Média de notas 2º sem (0.000–18.571)")
    curricular_units_2nd_sem_without_evaluations: Mapped[int] = mapped_column(Integer, nullable=False, doc="Disciplinas sem avaliação 2º sem (0–12)")
    
    # Data do cadastro do estudante no banco de dados
    data_insercao: Mapped[Optional[datetime]] = mapped_column(DateTime(), default=lambda: datetime.now(), server_default=func.now())
    situacao_academica: Mapped[str] = mapped_column(String, nullable=False, doc="Situação acadêmica do modelo")