# app/controllers/usuario_controller.py
from flask import Blueprint, request, jsonify
from app.services.usuario_service import UsuarioService

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/api/register', methods=['POST'])
def register():
    """
    Registro de un nuevo usuario.
    Permite registrar a un usuario de la URJC en el sistema. Restringido a dominios corporativos.
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: body
        description: Datos del usuario a registrar.
        required: true
        schema:
          type: object
          required:
            - correo
            - contrasena
          properties:
            correo:
              type: string
              example: alumno1@alumnos.urjc.es
              description: Correo corporativo de la URJC.
            contrasena:
              type: string
              example: MiPasswordSeguro123
              description: Contraseña del usuario.
    responses:
      201:
        description: Usuario registrado correctamente.
      400:
        description: Faltan campos obligatorios o el dominio del correo es inválido.
      409:
        description: El usuario ya existe en el sistema.
    """
    datos = request.get_json()
    if not datos or not 'correo' in datos or not 'contrasena' in datos:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    resultado = UsuarioService.registrar_usuario(datos['correo'], datos['contrasena'])
    status_code = resultado.pop('status')
    
    return jsonify(resultado), status_code

@usuario_bp.route('/api/login', methods=['POST'])
def login():
    """
    Inicio de sesión.
    Permite a un usuario autenticarse en el sistema utilizando su correo y contraseña.
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: body
        description: Credenciales de acceso del usuario.
        required: true
        schema:
          type: object
          required:
            - correo
            - contrasena
          properties:
            correo:
              type: string
              example: alumno1@alumnos.urjc.es
            contrasena:
              type: string
              example: MiPasswordSeguro123
    responses:
      200:
        description: Inicio de sesión exitoso.
      400:
        description: Faltan campos obligatorios.
      401:
        description: Credenciales inválidas.
    """
    datos = request.get_json()
    if not datos or not 'correo' in datos or not 'contrasena' in datos:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    resultado = UsuarioService.iniciar_sesion(datos['correo'], datos['contrasena'])
    status_code = resultado.pop('status')
    
    return jsonify(resultado), status_code
