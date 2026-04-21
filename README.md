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
