from flask_openapi3 import APIBlueprint, Tag
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from flask import abort

from models.machine_learning import Pipeline, Preprocessador
from models import Session
from models.estudantes import Estudante
from schemas.estudantes import EstudanteBuscaSchema, EstudanteSchema, EstudanteViewSchema


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
                    "mensagem": "Nenhum usuário encontrado.",
                    "usuarios": [],
                    "quantidade": 0
                }, HTTPStatus.OK
        
        return [EstudanteViewSchema.model_validate(estudante).model_dump() for estudante in estudantes], HTTPStatus.OK
   
    except Exception as e:
        return {"erro": str(e), "tipo": type(e).__name__}, HTTPStatus.INTERNAL_SERVER_ERROR

    finally:
        Session.remove()

@estudantes_bp.delete('/',
            responses={"200": EstudanteViewSchema})
def delete_estudante(query: EstudanteBuscaSchema):
    """Remove um estudante do sistema com base no id fornecido.
    Retorna uma resposta indicando o sucesso ou a falha da operação.
    """

    estudante_id = query.id_estudante
    try:
        estudante = Session.query(Estudante).filter(Estudante.matricula == estudante_id).first()
        
        if estudante:
            Session.query(Estudante).filter(Estudante.matricula == estudante_id).delete()
            Session.commit()
            return {
                "mensagem": f"Usuário removido com sucesso."
            }, HTTPStatus.OK
        else:
            return {"mensagem": f"Usuário não encontrado na base."
            }, HTTPStatus.NOT_FOUND
    
    except IntegrityError:
        Session.rollback()
        return {"mensagem": "Não é possível deletar"}, HTTPStatus.CONFLICT
    
    except Exception as e:
        Session.rollback()
        return {"erro": str(e), "tipo": type(e).__name__}, HTTPStatus.INTERNAL_SERVER_ERROR

    finally:
        Session.remove()