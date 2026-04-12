from urllib.parse import unquote
import uuid
from flask_openapi3 import APIBlueprint, Tag
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from flask import abort

from models import Session
from models.estudantes import Estudante
from schemas.estudantes import EstudanteSchema, EstudanteViewSchema

# from models import Session
# from models.usuario import Usuario
# from schemas.error import ErrorSchema
# from schemas.usuario import ListagemUsuariosSchema, UsuarioBuscaSchema, UsuarioSchema, UsuarioViewSchema, apresenta_usuario, apresenta_usuarios

estudantes_bp = APIBlueprint(
    'estudantes',
    __name__,
    url_prefix='/estudantes',
    abp_tags=[Tag(name='Estudantes', description='Operações do estudante')]
)


# TODO: adicionar ErrorSchema
# TODO: try/except com rollback()
# TODO: return apresenta_estudante para documentaçao
@estudantes_bp.post('/criar', responses={"201": EstudanteViewSchema})
def criar_estudante(form: EstudanteSchema):
    """Adiciona um novo estudante à base de dados.
    
    Recebe os atributos do aluno,
    salva no banco de dados e retorna a resposta do modelo.
    """
    try:
        dados_estudante = form.model_dump() 
        estudante = Estudante(**dados_estudante)
        estudante.situacao_academica = "Pendente de Predição"

        # Persistência no banco de dados
        Session.add(estudante)
        Session.commit()
        return EstudanteViewSchema.model_validate(estudante).model_dump(), HTTPStatus.CREATED
    

    except IntegrityError as e:
        Session.rollback()
        abort(HTTPStatus.CONFLICT)
        
    except Exception as e:
        Session.rollback()
        return {"erro": str(e), "tipo": type(e).__name__}, HTTPStatus.BAD_REQUEST






##---------------------------##

# TODO: listagem para aparecer no front end
# @estudantes_bp.get()

# TODO: apagar estudante
# @estudantes_bp.delete()