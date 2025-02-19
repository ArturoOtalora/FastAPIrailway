from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
import mysql.connector
import os

# Configurar la conexión a MySQL desde Railway
DB_HOST = "shuttle.proxy.rlwy.net"
DB_USER = "root"
DB_PASSWORD = "umzzdISTaNglzBNhBcTqxNMamqkCUJfs"
DB_NAME = "railway"
DB_PORT = 17125

app = FastAPI()

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

@app.post("/guardar_usuario")
def guardar_usuario(
    nombre: str = Form(...),
    apellidos: str = Form(...),
    tipo_documento: str = Form(...),
    numero_identificacion: int = Form(...),
    correo: str = Form(...),
    sexo: str = Form(...),
    rango_edad: str = Form(...),
    grado_escolaridad: str = Form(...),
    antiguedad: str = Form(...),
    ciudad: str = Form(...),
):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO usuarios (nombre, apellidos, tipo_documento, numero_identificacion, correo, sexo, rango_edad, grado_escolaridad, antiguedad, ciudad)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (nombre, apellidos, tipo_documento, numero_identificacion, correo, sexo, rango_edad, grado_escolaridad, antiguedad, ciudad)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Usuario guardado", "usuario": {"nombre": nombre, "apellidos": apellidos, "correo": correo}}

@app.get("/", response_class=HTMLResponse)
def mostrar_pagina():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Turing - Registro de Usuario</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                text-align: center;
                padding: 50px;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
                display: inline-block;
                text-align: left;
                width: 50%;
            }
            input, select {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            label {
                font-weight: bold;
                display: block;
                margin-top: 10px;
            }
            button {
                background: #2575fc;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 15px;
            }
            button:hover {
                background: #1e5bc6;
            }
        </style>
    </head>
    <body>
        <h1>Registro de Usuario</h1>
        <div class="container">
            <form action="/guardar_usuario" method="post">
                <label for="nombre">Nombre:</label>
                <input type="text" id="nombre" name="nombre" required>
                
                <label for="apellidos">Apellidos:</label>
                <input type="text" id="apellidos" name="apellidos" required>
                
                <label for="tipo_documento">Tipo de Documento:</label>
                <select id="tipo_documento" name="tipo_documento" required>
                    <option value="CC">Cédula de Ciudadanía</option>
                    <option value="TI">Tarjeta de Identidad</option>
                    <option value="CE">Cédula de Extranjería</option>
                </select>
                
                <label for="numero_identificacion">Número de Identificación:</label>
                <input type="text" id="numero_identificacion" name="numero_identificacion" required>
                
                <label for="correo">Correo Electrónico:</label>
                <input type="email" id="correo" name="correo" required>
                
                <label for="sexo">Sexo:</label>
                <select id="sexo" name="sexo" required>
                    <option value="Masculino">Masculino</option>
                    <option value="Femenino">Femenino</option>
                    <option value="Otro">Otro</option>
                </select>
                
                <label for="rango_edad">Rango de Edad:</label>
                <input type="text" id="rango_edad" name="rango_edad" required>
                
                <label for="grado_escolaridad">Grado de Escolaridad:</label>
                <input type="text" id="grado_escolaridad" name="grado_escolaridad" required>
                
                <label for="antiguedad">Antigüedad:</label>
                <input type="text" id="antiguedad" name="antiguedad" required>
                
                <label for="ciudad">Ciudad:</label>
                <input type="text" id="ciudad" name="ciudad" required>
                
                <button type="submit">Registrar</button>
            </form>
        </div>
    </body>
    </html>
    """

