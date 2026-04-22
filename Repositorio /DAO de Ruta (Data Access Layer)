# app/repositories/ruta_dao.py
from app.models.ruta import Ruta
from app.extensions import db

class RutaDAO:
    @staticmethod
    def guardar(ruta: Ruta) -> Ruta:
        db.session.add(ruta)
        db.session.commit()
        return ruta

    # NUEVO: Obtener ruta por ID para la validación
    @staticmethod
    def obtener_por_id(ruta_id: int) -> Ruta:
        return Ruta.query.get(ruta_id)
