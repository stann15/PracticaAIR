# app/repositories/incidencia_dao.py
from app.models.incidencia import Incidencia
from app.models.ruta import Ruta
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
        Realiza una búsqueda espacial de proximidad contra un PUNTO.
        """
        punto_origen = f'SRID=4326;POINT({lon} {lat})'
        
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

    # NUEVO: Búsqueda espacial avanzada (PUNTO vs LÍNEA)
    @staticmethod
    def buscar_activas_cercanas_a_ruta(ruta_id: int, radio_metros: float):
        """
        Realiza un JOIN espacial nativo en PostGIS para encontrar incidencias activas 
        a lo largo de todo el trazado de un LINESTRING.
        """
        return db.session.query(
            Incidencia,
            func.ST_X(Incidencia.ubicacionExacta).label('lon'),
            func.ST_Y(Incidencia.ubicacionExacta).label('lat')
        ).join(
            Ruta, 
            func.ST_DWithin(
                cast(Incidencia.ubicacionExacta, Geography), 
                cast(Ruta.trazado, Geography), 
                radio_metros
            )
        ).filter(
            Ruta.id == ruta_id,
            Incidencia.estado.in_(['Pendiente', 'En Resolución']) # Filtramos cerradas o falsas
        ).all()
