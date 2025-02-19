from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import mysql.connector

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
    return RedirectResponse(url="/preguntas", status_code=303)

@app.get("/preguntas", response_class=HTMLResponse)
def mostrar_preguntas():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Preguntas Adicionales</title>
    </head>
    <body>
        <h1>Responde las siguientes preguntas:</h1>
        <form action="/guardar_respuestas" method="post">
            <label>1. ¿Cuál es tu color favorito?</label>
            <input type="text" name="color_favorito" required><br>
            
            <label>2. ¿Cuál es tu comida favorita?</label>
            <input type="text" name="comida_favorita" required><br>
            
            <label>3. ¿Cuál es tu pasatiempo favorito?</label>
            <input type="text" name="pasatiempo_favorito" required><br>
            
            <label>4. ¿Cuál es tu deporte favorito?</label>
            <input type="text" name="deporte_favorito" required><br>
            
            <label>5. ¿Cuál es tu animal favorito?</label>
            <input type="text" name="animal_favorito" required><br>
            
            <button type="submit">Enviar Respuestas</button>
        </form>
    </body>
    </html>
    """

@app.post("/guardar_respuestas")
def guardar_respuestas(
    color_favorito: str = Form(...),
    comida_favorita: str = Form(...),
    pasatiempo_favorito: str = Form(...),
    deporte_favorito: str = Form(...),
    animal_favorito: str = Form(...),
):
    return {"message": "Respuestas guardadas", "respuestas": {
        "color_favorito": color_favorito,
        "comida_favorita": comida_favorita,
        "pasatiempo_favorito": pasatiempo_favorito,
        "deporte_favorito": deporte_favorito,
        "animal_favorito": animal_favorito
    }}
