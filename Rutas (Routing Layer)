# app/controllers/usuario_controller.py
from flask import Blueprint, request, jsonify
from app.services.usuario_service import UsuarioService

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/api/register', methods=['POST'])
def register():
    datos = request.get_json()
    if not datos or not 'correo' in datos or not 'contrasena' in datos:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    resultado = UsuarioService.registrar_usuario(datos['correo'], datos['contrasena'])
    status_code = resultado.pop('status')
    
    return jsonify(resultado), status_code

@usuario_bp.route('/api/login', methods=['POST'])
def login():
    datos = request.get_json()
    if not datos or not 'correo' in datos or not 'contrasena' in datos:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    resultado = UsuarioService.iniciar_sesion(datos['correo'], datos['contrasena'])
    status_code = resultado.pop('status')
    
    return jsonify(resultado), status_code
