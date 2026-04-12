from urllib.parse import unquote
import uuid
from flask_openapi3 import APIBlueprint, Tag
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError

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


# TODO: cadastrar estudante
@estudantes_bp.post('/criar', responses={"201": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
# TODO: try/except com rollback()
def criar_usuario(form: UsuarioSchema):
    """Adiciona um novo usuário à base de dados

    Retorna uma representação dos usuários.
    """
    try:
        usuario = Usuario(
            nome_usuario = form.nome_usuario,
            email = form.email,
            senha = form.senha
        )

        Session.add(usuario)
        Session.commit()

        return apresenta_usuario(usuario), HTTPStatus.CREATED


# TODO: listagem para aparecer no front end
# @estudantes_bp.get()

# TODO: apagar estudante
# @estudantes_bp.delete()