# app/repositories/usuario_dao.py
from app.models.usuario import Usuario
from app.extensions import db

class UsuarioDAO:
    @staticmethod
    def guardar(usuario: Usuario) -> Usuario:
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def obtener_por_correo(correo: str) -> Usuario:
        return Usuario.query.filter_by(correoCorporativo=correo).first()
