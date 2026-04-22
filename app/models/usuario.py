# app/models/usuario.py
from app.extensions import db

class Usuario(db.Model):
    """
    Modelo base de Usuario. Cumple estrictamente con el diagrama UML proporcionado.
    Se añade el atributo de la contraseña hasheada requerido para la autenticación local del prototipo.
    """
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    correoCorporativo = db.Column(db.String(120), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False) # Requerimiento técnico de la iteración
    tipo = db.Column(db.String(50)) # Preparado para herencia (Administrador, UsuarioComunidad, etc.)

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo
    }

    # Métodos definidos estrictamente según el diagrama de clases de análisis UML
    def iniciarSesion(self):
        pass

    def cerrarSesion(self):
        pass

    def gestionarPerfil(self):
        pass

    def cambiarIdioma(self):
        pass
