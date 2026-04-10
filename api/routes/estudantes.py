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