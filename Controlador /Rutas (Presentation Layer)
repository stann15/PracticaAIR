# app/controllers/incidencia_controller.py
from flask import Blueprint, request, jsonify
from app.services.incidencia_service import IncidenciaService

incidencia_bp = Blueprint('incidencia_bp', __name__)

@incidencia_bp.route('/api/incidencias', methods=['POST'])
def reportar_incidencia():
    """
    Reporta una nueva incidencia en el campus.
    Permite registrar incidencias físicas marcando sus coordenadas exactas (latitud y longitud).
    ---
    tags:
      - Incidencias
    parameters:
      - in: body
        name: body
        description: Datos geográficos y descriptivos de la incidencia.
        required: true
        schema:
          type: object
          required:
            - usuario_id
            - tipo
            - lon
            - lat
          properties:
            usuario_id:
              type: integer
              example: 1
            tipo:
              type: string
              example: "Farola fundida"
              enum: ["Farola fundida", "Zona solitaria/miedo", "Obstáculo en la vía", "Punto con dificultad"]
              description: Tipo tipificado según el ERS.
            lon:
              type: number
              format: float
              example: -3.8741
              description: Longitud geográfica.
            lat:
              type: number
              format: float
              example: 40.3364
              description: Latitud geográfica.
            descripcion:
              type: string
              example: "La farola parpadea intermitentemente y el área está oscura."
              description: Detalles opcionales.
    responses:
      201:
        description: Incidencia reportada correctamente en el sistema y mapa.
      400:
        description: Faltan campos o el tipo de incidencia es inválido.
      500:
        description: Error interno del servidor.
    """
    datos = request.get_json()
    
    campos_requeridos = ['usuario_id', 'tipo', 'lon', 'lat']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": "Faltan campos obligatorios (usuario_id, tipo, lon, lat)"}), 400

    resultado = IncidenciaService.crear_incidencia(
        usuario_id=datos['usuario_id'],
        tipo=datos['tipo'],
        lon=datos['lon'],
        lat=datos['lat'],
        descripcion=datos.get('descripcion', '')
    )
    
    status_code = resultado.pop('status')
    return jsonify(resultado), status_code

@incidencia_bp.route('/api/incidencias/cercanas', methods=['GET'])
def incidencias_cercanas():
    """
    Busca incidencias cercanas (Consulta Espacial Radial).
    Ejecuta un barrido geográfico (ST_DWithin en PostGIS) indicando un punto central y un radio de alcance en metros.
    ---
    tags:
      - Incidencias
    parameters:
      - in: query
        name: lon
        type: number
        required: true
        description: Longitud del punto central de búsqueda.
      - in: query
        name: lat
        type: number
        required: true
        description: Latitud del punto central de búsqueda.
      - in: query
        name: radio
        type: number
        required: false
        default: 500
        description: Radio de búsqueda en metros.
    responses:
      200:
        description: Lista de incidencias encontradas dentro del radio solicitado.
      400:
        description: Parámetros inválidos u omitidos.
      500:
        description: Error interno en la consulta espacial.
    """
    try:
        lon = float(request.args.get('lon'))
        lat = float(request.args.get('lat'))
        radio = float(request.args.get('radio', 500))
    except (TypeError, ValueError):
        return jsonify({"error": "Los parámetros 'lon' y 'lat' son obligatorios y deben ser numéricos"}), 400

    resultado = IncidenciaService.obtener_incidencias_cercanas(lon, lat, radio)
    status_code = resultado.pop('status')
    
    return jsonify(resultado), status_code
