# app/services/ruta_service.py
from app.models.ruta import Ruta
from app.repositories.ruta_dao import RutaDAO
from app.repositories.incidencia_dao import IncidenciaDAO

class RutaService:
    @staticmethod
    def guardar_ruta(usuario_id: int, origen_wkt: str, destino_wkt: str, indice_seguridad: float, trazado_wkt: str = None) -> dict:
        try:
            origen_geom = f'SRID=4326;{origen_wkt}'
            destino_geom = f'SRID=4326;{destino_wkt}'
            
            # Incorporamos el trazado opcional para no romper APIs anteriores
            trazado_geom = f'SRID=4326;{trazado_wkt}' if trazado_wkt else None

            nueva_ruta = Ruta(
                usuario_id=usuario_id,
                origen=origen_geom,
                destino=destino_geom,
                trazado=trazado_geom,
                indiceSeguridad=indice_seguridad,
                estaActiva=True
            )
            
            RutaDAO.guardar(nueva_ruta)
            
            return {"mensaje": "Ruta segura guardada correctamente en PostGIS", "id_ruta": nueva_ruta.id, "status": 201}
        except Exception as e:
            return {"error": f"Error interno al guardar la ruta: {str(e)}", "status": 500}

    # NUEVO: Lógica de evaluación de seguridad
    @staticmethod
    def evaluar_seguridad_ruta(ruta_id: int) -> dict:
        ruta = RutaDAO.obtener_por_id(ruta_id)
        if not ruta:
            return {"error": "Ruta no encontrada", "status": 404}
        if not ruta.trazado:
            return {"error": "La ruta seleccionada no cuenta con un trazado guardado para ser evaluada", "status": 400}

        try:
            # 50 metros de tolerancia de impacto respecto al trazado según ERS
            resultados = IncidenciaDAO.buscar_activas_cercanas_a_ruta(ruta_id, radio_metros=50.0)
            
            conteo_incidencias = len(resultados)
            
            # Algoritmo de evaluación base (Categorización)
            if conteo_incidencias == 0:
                nivel_seguridad = "Alta"
            elif 1 <= conteo_incidencias <= 2:
                nivel_seguridad = "Media"
            else:
                nivel_seguridad = "Baja"

            incidencias_formateadas = []
            for incidencia, lon, lat in resultados:
                incidencias_formateadas.append({
                    "id": incidencia.id,
                    "tipo": incidencia.tipoIncidencia,
                    "estado": incidencia.estado,
                    "coordenadas": {"lon": lon, "lat": lat}
                })

            return {
                "ruta_id": ruta_id,
                "nivel_seguridad": nivel_seguridad,
                "incidencias_activas_en_trayecto": conteo_incidencias,
                "detalle_incidencias": incidencias_formateadas,
                "status": 200
            }
        except Exception as e:
            return {"error": f"Error interno en la evaluación espacial: {str(e)}", "status": 500}
