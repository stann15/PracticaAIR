# app/controllers/ruta_controller.py
from flask import Blueprint, request, jsonify
from app.services.ruta_service import RutaService

ruta_bp = Blueprint('ruta_bp', __name__)

@ruta_bp.route('/api/rutas', methods=['POST'])
def crear_ruta():
    """
    Guarda una nueva ruta segura.
    Almacena una ruta con sus puntos de origen y destino en formato espacial WKT (Well-Known Text).
    ---
    tags:
      - Rutas
    parameters:
      - in: body
        name: body
        description: Datos espaciales e información de la ruta.
        required: true
        schema:
          type: object
          required:
            - usuario_id
            - origen
            - destino
            - indice_seguridad
          properties:
            usuario_id:
              type: integer
              example: 1
            origen:
              type: string
              example: "POINT(-3.8741 40.3364)"
              description: Coordenadas de origen en WKT.
            destino:
              type: string
              example: "POINT(-3.8765 40.3378)"
              description: Coordenadas de destino en WKT.
            trazado:
              type: string
              example: "LINESTRING(-3.8741 40.3364, -3.8750 40.3370, -3.8765 40.3378)"
              description: Línea completa del trayecto en formato WKT (Opcional).
            indice_seguridad:
              type: number
              format: float
              example: 8.5
    responses:
      201:
        description: Ruta segura guardada correctamente en PostGIS.
      400:
        description: Faltan campos obligatorios.
      500:
        description: Error interno del servidor.
    """
    datos = request.get_json()
    
    campos_requeridos = ['usuario_id', 'origen', 'destino', 'indice_seguridad']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": "Faltan campos obligatorios. Se requiere usuario_id, origen, destino e indice_seguridad"}), 400

    resultado = RutaService.guardar_ruta(
        usuario_id=datos['usuario_id'],
        origen_wkt=datos['origen'],
        destino_wkt=datos['destino'],
        indice_seguridad=datos['indice_seguridad'],
        trazado_wkt=datos.get('trazado', None)
    )
    
    status_code = resultado.pop('status')
    return jsonify(resultado), status_code

@ruta_bp.route('/api/rutas/<int:ruta_id>/evaluacion', methods=['GET'])
def evaluar_ruta(ruta_id):
    """
    Evalúa el nivel de seguridad de una ruta.
    Calcula mediante funciones espaciales (ST_DWithin) el nivel de seguridad de una ruta en base a las incidencias que intersectan su trazado a menos de 50 metros.
    ---
    tags:
      - Rutas
    parameters:
      - in: path
        name: ruta_id
        type: integer
        required: true
        description: Identificador numérico de la ruta a evaluar.
    responses:
      200:
        description: Evaluación espacial procesada exitosamente. Devuelve el nivel de seguridad y el detalle de las incidencias impactadas.
      400:
        description: La ruta seleccionada no cuenta con un trazado de tipo LINESTRING válido.
      404:
        description: Ruta no encontrada.
      500:
        description: Error interno del motor PostGIS.
    """
    resultado = RutaService.evaluar_seguridad_ruta(ruta_id)
    status_code = resultado.pop('status')
    
    return jsonify(resultado), status_code
