# app/services/incidencia_service.py
from app.models.incidencia import Incidencia
from app.repositories.incidencia_dao import IncidenciaDAO

class IncidenciaService:
    @staticmethod
    def crear_incidencia(usuario_id: int, tipo: str, lon: float, lat: float, descripcion: str) -> dict:
        # Validación tipificada según ERS (RF-INC-02)
        tipos_validos = ["Farola fundida", "Zona solitaria/miedo", "Obstáculo en la vía", "Punto con dificultad"]
        if tipo not in tipos_validos:
            return {
                "error": f"Tipo de incidencia inválido. Valores permitidos: {', '.join(tipos_validos)}", 
                "status": 400
            }
        
        try:
            # Formateamos coordenadas a WKT (Well-Known Text)
            punto_wkt = f'SRID=4326;POINT({lon} {lat})'
            
            nueva_incidencia = Incidencia(
                usuario_id=usuario_id,
                tipoIncidencia=tipo,
                ubicacionExacta=punto_wkt,
                descripcion=descripcion
            )
            
            IncidenciaDAO.guardar(nueva_incidencia)
            
            return {
                "mensaje": "Incidencia reportada correctamente en el sistema y mapa", 
                "id_incidencia": nueva_incidencia.id, 
                "status": 201
            }
        except Exception as e:
            return {"error": f"Error interno al guardar la incidencia: {str(e)}", "status": 500}

    @staticmethod
    def obtener_incidencias_cercanas(lon: float, lat: float, radio_metros: float) -> dict:
        try:
            resultados = IncidenciaDAO.buscar_en_radio(lon, lat, radio_metros)
            
            incidencias_formateadas = []
            for incidencia, lon_db, lat_db in resultados:
                incidencias_formateadas.append({
                    "id": incidencia.id,
                    "tipo": incidencia.tipoIncidencia,
                    "estado": incidencia.estado,
                    "descripcion": incidencia.descripcion,
                    "fecha_reporte": incidencia.fechaReporte.isoformat(),
                    "coordenadas": {
                        "lon": lon_db,
                        "lat": lat_db
                    }
                })
            
            return {
                "incidencias": incidencias_formateadas,
                "radio_busqueda_metros": radio_metros,
                "total": len(incidencias_formateadas),
                "status": 200
            }
        except Exception as e:
            return {"error": f"Error interno en la búsqueda espacial: {str(e)}", "status": 500}
