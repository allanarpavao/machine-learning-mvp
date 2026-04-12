from urllib.parse import unquote
import uuid
from flask_openapi3 import APIBlueprint, Tag
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from flask import abort

from models.machine_learning import Pipeline, Preprocessador
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
# TODO: adicionar try/except para modelo de ML
@estudantes_bp.post('/criar', responses={"201": EstudanteViewSchema})
def predict_estudante(body: EstudanteSchema):
    """Adiciona um novo estudante à base de dados.
    
    Recebe os atributos do aluno,
    salva no banco de dados e retorna a resposta do modelo.
    """
    # usa o modelo de machine learning
    preprocessador = Preprocessador()
    dados_in = preprocessador.preparar_form(body)
    best_pipeline = Pipeline()
    best_pipeline.carrega_pipeline()
    nova_avaliacao_estudante = best_pipeline.preditor(dados_in)
    resultado = nova_avaliacao_estudante[0]
    
    try:
        dados_estudante = body.model_dump()
        estudante = Estudante(**dados_estudante)
        estudante.situacao_academica = resultado

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



@estudantes_bp.get('/listar', responses={"200": EstudanteViewSchema})
def get_estudantes():
    """Lista todos os estudantes cadastrados no db

    """

    try:
        estudantes = Session.query(Estudante).all()
        if not estudantes:
            return {
                    "status": "success",
                    "mensagem": "Nenhum usuário encontrado.",
                    "usuarios": [],
                    "quantidade": 0
                }, HTTPStatus.OK
        return [EstudanteViewSchema.model_validate(estudante).model_dump() for estudante in estudantes], HTTPStatus.OK
   
    except Exception as e:
        return {"status": "error", "mensagem": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    finally:
        Session.remove()

##---------------------------##

# TODO: apagar estudante
# @estudantes_bp.delete()