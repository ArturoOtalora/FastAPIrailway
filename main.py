from fastapi import FastAPI, Form, Request,Query 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import mysql.connector
import random


# Configurar la conexión a MySQL desde Railway
DB_HOST = "shuttle.proxy.rlwy.net"
DB_USER = "root"
DB_PASSWORD = "umzzdISTaNglzBNhBcTqxNMamqkCUJfs"
DB_NAME = "railway"
DB_PORT = 17125


app = FastAPI()

app.mount("/statics", StaticFiles(directory="statics"), name="statics")

preguntas_lista = [
    "¿Consideras que tu alimentación te nutre lo suficientemente bien?", "¿Practicas semanal mínimo tres veces algún tipo de ejercicio?", "¿Consideras que tus habito de sueño te dan el descanso necesario?", "¿Durante los últimos seis meses has visitado o realizado un chequeo médico?",
    "Piensas que los hábitos que hoy ocupan gran parte de tu tiempo te ayudan para tener un cuerpo más saludable?", "¿Cuando sabes que estás siendo evaluado por los demás, ¿consigues mantenerte tranquila/o?",
    "¿Consideras que tus experiencias vividas te han ayudado a crecer como ser humano?", "¿A pesar de las dificultades sientes que te han ayudado a tener mejor calidad de vida?",
    "Cada que obtienes un logro practicas la celebración de la victoria?", "¿Te adaptas fácil a diferentes situaciones o nuevas ideas?",
    "¿Tu bienestar personal es prioridad en tu vida?", "¿Te has sentido impotente y dudando de ti por algún momento prolongado?",
    "¿Sientes que tu circulo cercano te animan a lograr tus metas?", "¿te sientes agradecido por los logros obtenidos?",
    "¿Durante los últimos seis meses has visitado o realizado un chequeo médico?", "¿Te siente valorado y respetado por los demás?",
    "¿Sientes que la autoimagen que tienes de ti representa tu más alto valor como ser humano?", "¿Cuándo reflexionas de tu valor personal que tan consciente eres del valor que aportas al mundo?",
    "¿Desde lo que hoy haces que pasión te motiva para seguir haciendolo por un tiempo más?", "¿Los pensamientos que más tienes sustentan la vida que hoy tienes?","Cuándo encuentras una verdad personal, por difícil que sea logras hacerla parte de ti","De tus ingresos dejas mínimo un 10% para ahorro","Realizas un presupuesto familiar mensual para tener una idea clara de tus ingresos y gastos","Tienes una o más inversiones de largo plazo que me permitan tener una base económica","Calculas la calidad de tus deudas sin poner en riesgo tu salud financiera","Con los ingresos que tienes podrías tener los gastos de subsistencia de 3 a 6 meses"
]

@app.get("/")
def home():
    return RedirectResponse(url="/mostrar_pagina")

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
    

    return RedirectResponse(url=f"/preguntas?usuario_id={numero_identificacion}", status_code=303)


@app.get("/mostrar_pagina", response_class=HTMLResponse)
def mostrar_pagina():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Turing - Registro de Usuario</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

      body {
            font-family: Arial, sans-serif;
            background: url('/statics/VITAL.png') no-repeat center center fixed;
            background-size: contain;  /* No estira la imagen */
            background-attachment: fixed; /* Mantiene la imagen en su lugar */
            background-color: #f4f4f4; /* Color de respaldo en caso de que la imagen no cargue */
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
          }
        .title-container {
            background: rgba(0, 0, 0, 0.7); /* Fondo oscuro semitransparente */
            color: white;
            padding: 15px 40px;
            border-radius: 10px;
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
            width: 90%;
            max-width: 500px;
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
            width: 100%;
        }

        button:hover {
            background: #1e5bc6;
        }
    </style>
</head>
<body>
    <div class="title-container">
        <h1>Registro de Usuario</h1>
    </div>
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
            <select id="rango_edad" name="rango_edad" required>
                <option value="18-25">18 a 25 años</option>
                <option value="26-40">26 a 40 años</option>
                <option value="41-55">41 a 55 años</option>
                <option value="56-76">56 a 76 años</option>
            </select>
            
            <label for="grado_escolaridad">Grado de Escolaridad:</label>
            <select id="grado_escolaridad" name="grado_escolaridad" required>
                <option value="Basica Primaria">Básica Primaria</option>
                <option value="Bachiller">Bachiller</option>
                <option value="Pregado">Pregrado</option>
                <option value="Posgrado">Posgrado</option>
                <option value="Doctorado">Doctorado</option>
            </select>
            
            <label for="antiguedad">Antigüedad laborando en la compañía:</label>
            <select id="antiguedad" name="antiguedad" required>
                <option value="Menos de 1 año">Menos de 1 año</option>
                <option value="Entre 1 y 2 años ">Entre 1 y 2 años </option>
                <option value="Entre 2 y 5 años">Entre 2 y 5 años</option>
                <option value="Mas de 5 años">Mas de 5 añoso</option>
            </select>
            
            <label for="ciudad">Ciudad:</label>
            <input type="text" id="ciudad" name="ciudad" required>
            
            <button type="submit">Registrar</button>
        </form>
    </div>
</body>
</html>

    """
@app.get("/preguntas", response_class=HTMLResponse)
def mostrar_preguntas(usuario_id: int, pagina: int = Query(1, alias="pagina")):
    total_preguntas = len(preguntas_lista)
    preguntas_por_pagina = 10
    inicio = (pagina - 1) * preguntas_por_pagina
    fin = min(inicio + preguntas_por_pagina, total_preguntas)
    preguntas = preguntas_lista[inicio:fin]

    es_ultima_pagina = fin >= total_preguntas
    progreso = (fin / total_preguntas) * 100

    preguntas_html = "".join([
        f'''
        <div class="pregunta-container">
            <p class="pregunta">{pregunta}</p>
            <div class="star-rating">
                {"".join([
                    f'<input type="radio" id="star{j}_{inicio + i}" name="respuesta_{inicio + i}" value="{j}" required>'
                    f'<label for="star{j}_{inicio + i}" class="star">&#9733;</label>'
                    for j in range(10, 0, -1)
                ])}
            </div>
        </div>
        '''
        for i, pregunta in enumerate(preguntas)
    ])

    return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Preguntas</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: url('/statics/VITALV.jpg') no-repeat center center fixed;
            background-size: contain;  /* No estira la imagen */
            background-attachment: fixed; /* Mantiene la imagen en su lugar */
            background-color: #f4f4f4; /* Color de respaldo en caso de que la imagen no cargue */
            
                    background-color: #f4f4f4;
                    text-align: center;
                    padding: 20px;
                }}
                h1 {{
                    color: #333;
                }}
                .pregunta-container {{
                    background: white;
                    padding: 15px;
                    margin: 15px auto;
                    border-radius: 10px;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                    width: 80%;
                    text-align: left;
                }}
                .pregunta {{
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .star-rating {{
                    display: flex;
                    flex-direction: row-reverse;
                    justify-content: flex-start;
                    gap: 5px;
                }}
                .star-rating input {{
                    display: none;
                }}
                .star-rating label {{
                    font-size: 30px;
                    color: gray;
                    cursor: pointer;
                    transition: color 0.3s;
                }}
                .star-rating input:checked ~ label,
                .star-rating label:hover,
                .star-rating label:hover ~ label {{
                    color: gold;
                }}
                .progress-bar-container {{
                    width: 80%;
                    background-color: #e0e0e0;
                    border-radius: 15px;
                    margin: 20px auto;
                    overflow: hidden;
                    position: relative;
                    height: 25px;
                    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
                }}
                .progress-bar {{
                    height: 100%;
                    width: {progreso}%;
                    background: linear-gradient(90deg, #28a745, #218838);
                    transition: width 0.5s;
                    border-radius: 15px;
                }}
                .progress-text {{
                    position: absolute;
                    width: 100%;
                    text-align: center;
                    font-weight: bold;
                    top: 0;
                    left: 0;
                    line-height: 25px;
                    color: #fff;
                    font-size: 14px;
                }}
                button {{
                    background-color: #28a745;
                    color: white;
                    font-size: 16px;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background 0.3s;
                }}
                button:hover {{
                    background-color: #218838;
                }}
            </style>
        </head>
        <body>
             <h1>Bienvenidos a un lugar seguro donde tus pensamientos y emociones pueden ser escuchados y comprendidos:</h1>
        <p class="instrucciones">Selecciona el número de estrellas que mejor represente tu opinión: 1 ⭐ significa 'Muy Bajo' y 10 ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ significa 'Muy Alto</p>
    <div class="progress-bar-container">
        <div class="progress-bar"></div>
        <div class="progress-text">{progreso:.0f}%</div>
    </div>
    <form action="/guardar_respuestas" method="post">
        <input type="hidden" name="usuario_id" value="{usuario_id}">
        <input type="hidden" name="pagina" value="{pagina}">
        {preguntas_html}
        <button type="submit">{'Finalizar' if es_ultima_pagina else 'Siguiente'}</button>
            </form>
        </body>
        </html>
        '''



@app.post("/guardar_respuestas")
async def guardar_respuestas(request: Request, usuario_id: int = Form(...), pagina: int = Form(...)):
    form_data = await request.form()
    respuestas = {}

    for key, value in form_data.items():
        if key.startswith("respuesta_"):
            index = int(key.split("_")[1])
            pregunta = preguntas_lista[index]
            respuestas[pregunta] = value

    conn = get_db_connection()
    cursor = conn.cursor()

    for pregunta, respuesta in respuestas.items():
        cursor.execute(
            "INSERT INTO respuestasForm (usuario_id, pregunta, respuesta) VALUES (%s, %s, %s) "
            "ON DUPLICATE KEY UPDATE respuesta = VALUES(respuesta)",
            (usuario_id, pregunta, respuesta)
        )

    conn.commit()
    cursor.close()
    conn.close()

    total_preguntas = len(preguntas_lista)
    preguntas_por_pagina = 10
    es_ultima_pagina = (pagina * preguntas_por_pagina) >= total_preguntas

    if es_ultima_pagina:
        return HTMLResponse(content='''
            <!DOCTYPE html>
            <html>
            <head>
                <title>¡Buen trabajo!</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding: 50px;
                        background-color: #d4edda;
                    }}
                    .mensaje {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #155724;
                    }}
                    .container {{
                        background: white;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                        display: inline-block;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <p class="mensaje">¡Buen trabajo! Has completado todas las preguntas.</p>
                    <p>Gracias por tu tiempo y esfuerzo.</p>
                </div>
            </body>
            </html>
        ''')
    else:
        return RedirectResponse(url=f"/preguntas?usuario_id={usuario_id}&pagina={pagina+1}", status_code=303)

      
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
