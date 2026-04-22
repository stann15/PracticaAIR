# app/__init__.py
import os
from flask import Flask
from flasgger import Swagger
from app.extensions import db
from app.controllers.usuario_controller import usuario_bp
from app.controllers.ruta_controller import ruta_bp
from app.controllers.incidencia_controller import incidencia_bp

def create_app():
    app = Flask(__name__)
    
    # Configuración de conexión a PostgreSQL + PostGIS
    db_user = os.getenv('POSTGRES_USER', 'postgres')
    db_password = os.getenv('POSTGRES_PASSWORD', 'postgres')
    db_host = os.getenv('POSTGRES_HOST', 'db')
    db_name = os.getenv('POSTGRES_DB', 'senda_urjc')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Configuración e Inicialización de Swagger (Flasgger)
    swagger_template = {
        "info": {
            "title": "API REST - Senda URJC",
            "description": "Documentación interactiva de los endpoints del backend espacial para la aplicación Senda URJC.",
            "version": "1.0.0",
            "contact": {
                "name": "Equipo de Desarrollo - Senda URJC"
            }
        }
    }
    Swagger(app, template=swagger_template)

    # Registro de blueprints (Rutas / Endpoints)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(ruta_bp)
    app.register_blueprint(incidencia_bp)

    # Creación automática de tablas si no existen
    with app.app_context():
        # Extensión PostGIS necesaria para tablas espaciales
        db.session.execute(db.text('CREATE EXTENSION IF NOT EXISTS postgis;'))
        db.session.commit()
        
        # Importación de modelos para que SQLAlchemy los detecte
        from app.models.usuario import Usuario
        from app.models.ruta import Ruta 
        from app.models.incidencia import Incidencia
        
        db.create_all()

    return app
