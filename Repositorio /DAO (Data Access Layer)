# app/repositories/incidencia_dao.py
from app.models.incidencia import Incidencia
from app.extensions import db
from sqlalchemy import func, cast
from geoalchemy2.types import Geography

class IncidenciaDAO:
    @staticmethod
    def guardar(incidencia: Incidencia) -> Incidencia:
        db.session.add(incidencia)
        db.session.commit()
        return incidencia

    @staticmethod
    def buscar_en_radio(lon: float, lat: float, radio_metros: float):
        """
        Realiza una búsqueda espacial nativa en PostGIS.
        Convierte la Geometría a Geografía para que ST_DWithin calcule la distancia en metros reales.
        Retorna la Incidencia y desglosa internamente la longitud y latitud.
        """
        punto_origen = f'SRID=4326;POINT({lon} {lat})'
        
        # Hacemos la query solicitando la entidad y extrayendo X e Y de la geometría nativa
        return db.session.query(
            Incidencia,
            func.ST_X(Incidencia.ubicacionExacta).label('lon'),
            func.ST_Y(Incidencia.ubicacionExacta).label('lat')
        ).filter(
            func.ST_DWithin(
                cast(Incidencia.ubicacionExacta, Geography),
                cast(func.ST_GeomFromText(punto_origen, 4326), Geography),
                radio_metros
            )
        ).all()
