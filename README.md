# PracticaAIR
Instrucciones de Ejecución
Asegúrate de tener Docker y Docker Compose instalados en tu sistema.

Abre una terminal, navega a la carpeta raíz del proyecto y ejecuta el siguiente comando para levantar la infraestructura:

Bash
docker-compose up --build
El servicio de base de datos tardará unos segundos en estar saludable y crear la extensión PostGIS. Acto seguido, la API en Flask estará disponible en http://localhost:5000.

Pruebas mediante cURL
1. Registro de Usuario (Éxito)
Recuerda que el sistema fuerza el uso de dominios corporativos.

Bash
curl -X POST http://localhost:5000/api/register \
-H "Content-Type: application/json" \
-d '{"correo": "alumno1@alumnos.urjc.es", "contrasena": "MiPasswordSeguro123"}'
2. Registro de Usuario (Fallo de dominio)

Bash
curl -X POST http://localhost:5000/api/register \
-H "Content-Type: application/json" \
-d '{"correo": "alumno1@gmail.com", "contrasena": "MiPasswordSeguro123"}'
3. Inicio de Sesión

Bash
curl -X POST http://localhost:5000/api/login \
-H "Content-Type: application/json" \
-d '{"correo": "alumno1@alumnos.urjc.es", "contrasena": "MiPasswordSeguro123"}'

# requirements.txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
GeoAlchemy2==0.14.3
psycopg2-binary==2.9.9
Werkzeug==3.0.1

Dado que hemos añadido nuevos modelos, si tenías el contenedor corriendo, es recomendable reiniciarlo para que SQLAlchemy detecte los cambios y cree la nueva tabla espacial:

Bash
docker-compose down
docker-compose up --build
Prueba 1: Registrar un usuario (Requisito Previo)
Primero necesitamos un usuario_id válido para la ForeignKey:

Bash
curl -X POST http://localhost:5000/api/register \
-H "Content-Type: application/json" \
-d '{"correo": "estudiante@alumnos.urjc.es", "contrasena": "secreto123"}'
(Anota el "id" devuelto, supongamos que es el 1).

Prueba 2: Guardar una Ruta Segura con Datos Espaciales (Iteración 2)
Para enviar geometrías espaciales mediante JSON, Senda URJC utiliza el formato estándar WKT (Well-Known Text). Ejemplo: POINT(longitud latitud).

Bash
curl -X POST http://localhost:5000/api/rutas \
-H "Content-Type: application/json" \
-d '{

3. Instrucciones de Prueba
Dado que hemos añadido la tabla de incidencias, te recomiendo hacer un docker-compose down y un docker-compose up --build para que SQLAlchemy detecte y cree la nueva tabla espacial en el arranque.

Aquí tienes los comandos de prueba listos para tu terminal:

1. Reportar una nueva incidencia (Endpoint POST)
(Recuerda que el usuario_id debe existir previamente en tu base de datos).

Bash
curl -X POST http://localhost:5000/api/incidencias \
-H "Content-Type: application/json" \
-d '{
      "usuario_id": 1,
      "tipo": "Farola fundida",
      "descripcion": "La farola del parking principal está parpadeando y casi apagada",
      "lon": -3.8741,
      "lat": 40.3364
    }'
2. Búsqueda Espacial con PostGIS (Endpoint GET)
Buscaremos todas las incidencias a un máximo de 1000 metros desde unas coordenadas cercanas (las de un usuario caminando, por ejemplo). PostGIS hará el cálculo geoespacial real descartando lo que esté más lejos de ese radio.

Bash
curl -X GET "http://localhost:5000/api/incidencias/cercanas?lon=-3.8745&lat=40.3370&radio=1000"
      "usuario_id": 1,
      "origen": "POINT(-3.8741 40.3364)", 
      "destino": "POINT(-3.8765 40.3378)",
      "indice_seguridad": 8.5
    }'
