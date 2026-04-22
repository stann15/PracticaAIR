# app/models/incidencia.py
from app.extensions import db
from geoalchemy2 import Geometry
from datetime import datetime

class Incidencia(db.Model):
    """
    Modelo de Incidencia. Cumple con el diagrama UML proporcionado (pág 74).
    Implementa tipos de datos espaciales nativos de PostGIS para marcar el punto exacto.
    """
    __tablename__ = 'incidencias'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Relación 0..* con Usuario según diagrama UML
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Atributos definidos en el UML y ERS
    estado = db.Column(db.String(50), default='Pendiente') # Pendiente, En Resolución, Resuelta, Rechazada
    tipoIncidencia = db.Column(db.String(100), nullable=False) 
    ubicacionExacta = db.Column(Geometry('POINT', srid=4326), nullable=False)
    fechaReporte = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Atributo extra solicitado en la iteración 3
    descripcion = db.Column(db.Text, nullable=True)

    # Relación bidireccional
    usuario = db.relationship('Usuario', backref=db.backref('incidencias', lazy=True))

    # Método definido estrictamente según el diagrama de clases UML
    def actualizarEstado(self, nuevo_estado: str):
        self.estado = nuevo_estado
