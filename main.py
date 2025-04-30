from fastapi import FastAPI, Form, Request,Query, HTTPException 
from fastapi.responses import HTMLResponse, RedirectResponse,FileResponse
from fastapi.staticfiles import StaticFiles
import mysql.connector
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, ListFlowable,KeepTogether,Spacer
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from matplotlib.patches import Rectangle, FancyBboxPatch
import os
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import textwrap
import pandas as pd
from reportlab.lib.enums import TA_JUSTIFY

import mysql.connector


# Configurar la conexión a MySQL desde Railway
DB_HOST = "gondola.proxy.rlwy.net"
DB_USER = "root"
DB_PASSWORD = "nwzXTMUHabRgDchrDIQtXGsNhaNgFnrR"
DB_NAME = "railway"
DB_PORT = 53433


app = FastAPI()



app.mount("/statics", StaticFiles(directory="statics"), name="statics")

preguntas_lista = [
    "¿Consideras que tu alimentación te nutre lo suficientemente bien?", "¿Realizas ejercicio físico al menos tres veces por semana?", "¿Sientes que tus habito de sueño te dan el descanso necesario?",
    "¿En los últimos seis meses te has realizado chequeos médicos?", "¿Piensas que los hábitos que hoy ocupan gran parte de tu tiempo te ayudan para tener un cuerpo más saludable?",
    "¿Consideras que tus experiencias han contribuido a tu calidad de vida o crecimiento personal?", "¿Celebras tus logros o victorias?",
    "¿Cuando siento una emoción intensa, soy capaz de calmarme antes de actuar o tomar decisiones?", "¿Sientes que te adaptas a cambios o nuevas situaciones con facilidad?",
    "¿Tu bienestar emocional es prioridad en tu vida?", "¿Consideras que has manejado bien los sentimientos de impotencia o duda prolongados?",
    "¿Sientes que tu círculo cercano te anima a lograr tus metas?", "¿te sientes agradecido por los logros obtenidos?",
    "¿Has reflexionado personalmente o con un profesional sobre tu salud mental en los últimos seis meses?", "¿En qué medida te sientes valorado y respetado por otros?",
    "¿Sientes que la autoimagen que tienes de ti representa tu más alto valor como ser humano?", "¿Cuándo reflexionas de tu valor personal que tan consciente eres del valor que aportas al mundo?",
    "¿Desde lo que hoy haces, lo consideras tu pasión y te motiva para seguir haciéndolo ?", "¿Los pensamientos que más tienes sustentan tu valor mas alto?","¿Cuándo conoces una verdad sobre tu vida la aceptas con facilidad?",
    "¿De tus ingresos mensuales ahorras al menos el 10%?","¿En la actualidad tienes y sigues un presupuesto mensual?","¿Tienes una o más inversiones de largo plazo que me permitan tener una base económica?",
    "¿Tienes un plan para gestionar tus deudas sin afectar tu salud financiera?","¿Hoy tienes un plan de ahorro que cubra tus gastos básicos por 3 a 6 meses?","¿Consideras que la calidad del aire en los espacios donde vives, trabajas o transitas diariamente apoya tu salud?",
    "¿Incorporas prácticas sostenibles como el reciclaje, la reducción de residuos o la reutilización de materiales en tu día a día?","¿Confías en que el agua que consumes (para beber, cocinar o higiene) es segura y cumple con estándares que protegen tu salud?","¿Conoces o tomas acciones para reducir tu huella de carbono en actividades como transporte, alimentación o consumo energético?",
    "¿Reconoces cómo tus decisiones y hábitos cotidianos contribuyen al cambio climático y, a su vez, cómo este fenómeno afecta tu calidad de vida?"
]
nombre_completo_global = ""
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
    Profesion: str = Form(...),
    
):
    

    conn = get_db_connection()
    cursor = conn.cursor()  
    
    # Verificar si el número de identificación ya existe
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE numero_identificacion = %s", (numero_identificacion,))
    (existe,) = cursor.fetchone()
    
    if existe:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="El número de identificación ya está registrado.")
        
    cursor.execute(
        """
         INSERT INTO usuarios (nombre, apellidos, tipo_documento, numero_identificacion, correo, sexo, rango_edad, grado_escolaridad, antiguedad, ciudad, Profesion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (nombre, apellidos, tipo_documento, numero_identificacion, correo, sexo, rango_edad, grado_escolaridad, antiguedad, ciudad, Profesion)
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
            background-size: contain;
            background-attachment: fixed;
            background-color: #f4f4f4;
            display: flex;
            flex-direction: column;
            align-items: center;    
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }

            .title-container {
            text-align: center;
            font-size: 25px;
            font-weight: bold;
            margin-bottom: 30px;
            margin-top: -20px;
            color: #2C3E50;
        }

        .container {
            background: rgba(255, 255, 255, 0.9);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 800px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        label {
            font-weight: bold;
            margin-bottom: 5px;
            font-size: 14px;
        }

        input, select {
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 14px;
        }

        button {
            background: #2575fc;
            color: white;
            padding: 12px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 20px;
            width: 100%;
            transition: background 0.3s ease;
        }

        button:hover {
            background: #1e5bc6;
        }

        @media (max-width: 768px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="title-container">
        <h1>Registro de Usuario</h1>
    </div>
    <div class="container">
        <form action="/guardar_usuario" method="post">
            <div class="form-grid">
                <div class="form-group">
                    <label for="nombre">Nombre:</label>
                    <input type="text" id="nombre" name="nombre" required>
                </div>
                <div class="form-group">
                    <label for="apellidos">Apellidos:</label>
                    <input type="text" id="apellidos" name="apellidos" required>
                </div>
                <div class="form-group">
                    <label for="tipo_documento">Tipo de Documento:</label>
                    <select id="tipo_documento" name="tipo_documento" required>
                        <option value="CC">Cédula de Ciudadanía</option>
                        <option value="TI">Tarjeta de Identidad</option>
                        <option value="CE">Cédula de Extranjería</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="numero_identificacion">Número de Identificación:</label>
                    <input type="text" id="numero_identificacion" name="numero_identificacion" required>
                </div>
                <div class="form-group">
                    <label for="correo">Correo Electrónico:</label>
                    <input type="email" id="correo" name="correo" required>
                </div>
                <div class="form-group">
                    <label for="sexo">Sexo:</label>
                    <select id="sexo" name="sexo" required>
                        <option value="Masculino">Masculino</option>
                        <option value="Femenino">Femenino</option>
                        <option value="Otro">Otro</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="rango_edad">Rango de Edad:</label>
                    <select id="rango_edad" name="rango_edad" required>
                        <option value="18-25">18 a 25 años</option>
                        <option value="26-40">26 a 40 años</option>
                        <option value="41-55">41 a 55 años</option>
                        <option value="56-76">56 a 76 años</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="grado_escolaridad">Grado de Escolaridad:</label>
                    <select id="grado_escolaridad" name="grado_escolaridad" required>
                        <option value="Basica Primaria">Básica Primaria</option>
                        <option value="Bachiller">Bachiller</option>
                        <option value="Pregado">Pregrado</option>
                        <option value="Posgrado">Posgrado</option>
                        <option value="Doctorado">Doctorado</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="antiguedad">Antigüedad laborando en la compañía:</label>
                    <select id="antiguedad" name="antiguedad" required>
                        <option value="Menos de 1 año">Menos de 1 año</option>
                        <option value="Entre 1 y 2 años ">Entre 1 y 2 años </option>
                        <option value="Entre 2 y 5 años">Entre 2 y 5 años</option>
                        <option value="Mas de 5 años">Mas de 5 años</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="ciudad">Ciudad:</label>
                    <input type="text" id="ciudad" name="ciudad" required>
                </div>
                <div class="form-group">
                    <label for="Profesion">Profesión:</label>
                    <input type="text" id="Profesion" name="Profesion" required>
                </div>
            </div>
            <div class="form-group" style="grid-column: 1 / -1; margin-top: 10px;">
                <label style="font-weight: normal;">
                    <input type="checkbox" name="autorizacion_datos" required>
                    Autorizo de manera libre, voluntaria, previa, explícita e informada a Vital Value, para que en 
                    los términos legales establecidos realice la recolección, almacenamiento, uso, circulación,
                    supresión y, en general, el tratamiento de mis datos personales que he proporcionado o
                    proporcionaré, con la finalidad de análisis y caracterización. Conozco que tengo derecho a
                    conocer, actualizar, rectificar y suprimir mis datos personales, así como a revocar la
                    autorización otorgada, de conformidad con la Ley 1581 de 2012 y demás normas aplicables.
                </label>
            </div>
            <button type="submit">Registrar</button>
        </form>
    </div>
</body>
</html>
    """
@app.get("/preguntas", response_class=HTMLResponse)
def mostrar_preguntas(usuario_id: int, pagina: int = Query(1, alias="pagina")):
    # Definición de categorías y preguntas asociadas
    categorias_preguntas = {
        "Salud Vital Corporal": preguntas_lista[0:5],
        "Salud Emocional": preguntas_lista[5:10],
        "Salud Mental": preguntas_lista[10:15],
        "Sentido Existencial": preguntas_lista[15:20],
        "Salud Financiera": preguntas_lista[20:25],
        "Salud Ambiental": preguntas_lista[25:30]
    }

    total_preguntas = len(preguntas_lista)
    preguntas_por_pagina = 10
    inicio = (pagina - 1) * preguntas_por_pagina
    fin = min(inicio + preguntas_por_pagina, total_preguntas)
    es_ultima_pagina = fin >= total_preguntas
    progreso = (fin / total_preguntas) * 100

    # Generación dinámica de HTML para preguntas organizadas por categorías
   # Generación dinámica de HTML para preguntas organizadas por categorías
    preguntas_html = ""
    contador = 0

    bloque_textos = {
        1: ("Bienestar Físico ","Explorarás el camino de la autogestión de cómo el movimiento, la nutrición y el descanso se entrelazan para potenciar tu energía y resistencia. Este espacio te invita a escuchar las señales de tu organismo y diseñar rutinas que respeten tu ritmo único, porque cuidar tu salud física es el cimiento para una vida plena y activa."),
        2: ("Bienestar Emocional", "Aquí reflexionarás sobre cómo gestionas lo que sientes, cómo te relacionas contigo y con los demás, y qué prácticas te ayudan a encontrar calma en medio del caos. Reconocer tus emociones no es debilidad: es la clave para construir resiliencia y conexiones auténticas."),
        3: ("Bienestar Mental", "Este espacio te invita a observar cómo piensas, qué creencias guían tus decisiones y de qué manera tu enfoque mental influye en tu bienestar. Cultivar una mente clara, flexible y presente te permite adaptarte a los cambios, tomar decisiones conscientes y vivir con mayor plenitud interior."),
        4: ("Sentido Existencial", "Profundizarás en tus propósitos, creencias y las preguntas que dan sentido a tu existencia. Más allá de lo cotidiano, aquí explorarás cómo tus acciones se conectan con un legado personal, porque vivir con intención es la base de la plenitud duradera."),
        5: ("Bienestar Financiero", "En esta dimensión entenderás tu coeficiente intelectual financiero: comprenderás cómo funciona el dinero, de dónde nacen tus decisiones económicas y qué conocimientos necesitas para autogestionarlo con claridad."),
        6: ("Bienestar Ambiental", "Reflexionarás sobre tu conexión con la naturaleza, tu impacto en el entorno y cómo pequeños cambios en tus hábitos pueden nutrir positivamente al planeta. Cuidar tu relación con la Tierra no solo es un acto colectivo, sino una forma de honrar tu propio hogar vital.."),
    }

    ultimo_bloque_insertado = None  # Para evitar repetir el mensaje

    for categoria, preguntas in categorias_preguntas.items():
        for pregunta in preguntas:
            if inicio <= contador < fin:
                bloque_actual = (contador // 5) + 1  # 👈 Calcula el bloque basado en la posición global

                # Mostrar mensaje del bloque solo una vez por página
                if bloque_actual != ultimo_bloque_insertado:
                    titulo_bloque, mensaje_bloque = bloque_textos.get(
                        bloque_actual,
                        (f"Bloque {bloque_actual}", "Reflexiona con atención sobre los siguientes aspectos.")
                    )
                    preguntas_html += f'''
                    <div class="bloque-intro">
                        <h2>{titulo_bloque}</h2>
                        <p>{mensaje_bloque}</p>
                    </div>
                    '''
                    ultimo_bloque_insertado = bloque_actual

                preguntas_html += f'''
                <div class="pregunta-container">
                    <p class="pregunta">{pregunta}</p>
                    <div class="star-rating">
                        {"".join([
                            f'<input type="radio" id="star{j}_{contador}" name="respuesta_{contador}" value="{j}" required>'
                            f'<label for="star{j}_{contador}" class="star">&#9733;</label>'
                            for j in range(10, 0, -1)
                        ])}
                    </div>
                </div>
                
                    '''
            contador += 1

    return f'''
   <!DOCTYPE html>
<html>
<head>
    <title>Preguntas</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: url('/statics/VITALV.jpg') no-repeat center center fixed;
            background-size: contain;
            background-attachment: fixed;
            background-color: #f4f4f4;
            text-align: center;
            padding: 20px;
        }}
        h1, h2 {{
            color: #333;
        }}
        .modal {{
            display: none; /* oculto por defecto */
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.6);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }}
        .modal-content {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            max-width: 700px;
            width: 100%;
            text-align: justify;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            max-height: 90vh;
            overflow-y: auto;
            line-height: 1.6;
            font-size: 17px;
        }}
        .modal-content p strong  {{
           font-size: 18px;
            color: #007bff;
        }}
         .modal-content button {{
            display: block;
            margin: 20px auto 0;
            background-color: #007bff;
            color: white;
            font-size: 16px;
            padding: 10px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }}
        .modal-content button:hover {{
            background-color: #007bff;
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
            background: linear-gradient(90deg, #007bff, #0056b3);
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
            background-color: #007bff;
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
        #contenido {{
            display: none;
        }}
        .bloque-intro {{
            background-color: #f8f9fa;
            padding: 20px;
            margin: 30px auto 10px;
            border-left: 5px solid #007bff;
            width: 80%;
            border-radius: 10px;
            text-align: left;
        }}

        .bloque-intro h2 {{
            color: #0056b3;
            margin-bottom: 10px;
        }}

        .bloque-intro p {{
            font-size: 16px;
            color: #444;
        }}
         .error-message {{
            color: #dc3545;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            padding: 10px;
            border-radius: 5px;
            margin: 15px auto;
            width: 80%;
            display: none;
        }}
    </style>
</head>
<body>
    <h1>Bienvenidos a un lugar seguro donde tus pensamientos y emociones pueden ser escuchados y comprendidos:</h1>
    <div class="modal" id="error-modal">
    <div class="modal-content">
        <p><strong>Atención</strong><br><br>
        Por favor, responde todas las preguntas antes de continuar. Asegúrate de calificar cada una con una estrella del 1 al 10. 🌟</p>
        <button onclick="cerrarErrorModal()">Aceptar</button>
    </div>
</div>
    <div class="modal" id="modal">
        <div class="modal-content">
            <p><strong></strong><br><br>
            ¡Bienvenido/a a <strong>CIMA</strong>, tu espacio para el crecimiento consciente!<br><br>
            Al responder las preguntas que encontrarás a continuación, estarás dando el primer paso hacia un viaje de <strong>autoconocimiento profundo</strong>. Este proceso no solo te ayudará a identificar patrones, hábitos y emociones que definen tu día a día y realidad, sino que también creará una base sólida para impulsar tu <strong>transformación personal interior</strong>.<br><br>
            ¿Por qué es importante? Porque solo cuando nos observamos con Consciencia podemos entender qué aspectos de nuestra vida necesitan atención, cuidado o cambio. Cada respuesta que compartas será como una semilla: desde aquí, nuestra plataforma te guiará con herramientas, recursos y recomendaciones adaptadas a tus necesidades únicas, para que cultives <strong>bienestar integral</strong>.<br><br>
            Este no es un cuestionario, sino un <strong>mapa hacia la mejor versión de ti</strong>. Te invitamos a abordarlo con <strong>curiosidad, sin juicios</strong> y con la certeza de que cada reflexión es un paso hacia la libertad de reinventarte.<br><br>
            <em>Tu viaje empieza aquí. 🌱</em>
            </p>
            <button onclick="cerrarModal()">Aceptar</button>
        </div>
    </div>
    <div id="error-message" class="error-message">
    Por favor, responde todas las preguntas antes de continuar.
    </div>
    <!-- Contenido oculto -->
    <div id="contenido">
        <p class="instrucciones">Selecciona el número de estrellas que mejor represente tu opinión: 1 ⭐ significa 'Muy Bajo' y 10 ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ significa 'Muy Alto'</p>
        <div class="progress-bar-container">
            <div class="progress-bar"></div>
            <div class="progress-text">{progreso:.0f}%</div>
        </div>
        <form id="form-preguntas" action="/guardar_respuestas" method="post">
            <input type="hidden" name="usuario_id" value="{usuario_id}">
            <input type="hidden" name="pagina" value="{pagina}">
            {preguntas_html}
            <button type="button" onclick="validarFormulario()">{'Finalizar' if es_ultima_pagina else 'Siguiente'}</button>
        </form>
    </div>

    <script>
            function cerrarModal() {{
                
                document.getElementById('modal').style.display = 'none';
                document.getElementById('contenido').style.display = 'block';
                localStorage.setItem("modalVisto", "true");
            }}

           function validarFormulario() {{
    const preguntas = document.querySelectorAll('.pregunta-container');
    let todasRespondidas = true;

    preguntas.forEach(pregunta => {{
        const inputs = pregunta.querySelectorAll('input[type="radio"]');
        let respondida = false;

        inputs.forEach(input => {{
            if (input.checked) {{
                respondida = true;
            }}
        }});

        if (!respondida) {{
            todasRespondidas = false;
            pregunta.style.border = "2px solid #dc3545";
            pregunta.style.animation = "shake 0.5s";

            setTimeout(() => {{
                pregunta.style.border = "";
                pregunta.style.animation = "";
            }}, 500);
        }}
    }});

    if (todasRespondidas) {{
        document.getElementById('form-preguntas').submit();
    }} else {{
        document.getElementById('error-modal').style.display = 'flex';
    }}
}}

function cerrarErrorModal() {{
    document.getElementById('error-modal').style.display = 'none';
}}

            window.onload = function() {{
                const modal = document.getElementById('modal');
                const contenido = document.getElementById('contenido');
                const yaVisto = localStorage.getItem("modalVisto");

                if (yaVisto === "true") {{
                    contenido.style.display = 'block';  // Solo muestra el contenido si ya fue visto
                }} else {{
                    modal.style.display = 'flex';  // Muestra el modal solo la primera vez
                }}
                
                // Agregar animación shake al CSS
                const style = document.createElement('style');
                style.innerHTML = `
                    @keyframes shake {{
                        0%, 100% {{ transform: translateX(0); }}
                        20%, 60% {{ transform: translateX(-5px); }}
                        40%, 80% {{ transform: translateX(5px); }}
                    }}
                `;
                document.head.appendChild(style);
            }}
        </script>
    </body>
    </html>

    '''
def generar_graficos_por_categoria(valores_respuestas):
    categorias = ["Ambiental","Vital", "Emocional", "Mental", "Existencial", "Financiera"]
    dimensiones = {
        "Vital": ["Alimentación", "Descanso", "Ejercicio", "Hábitos Saludables", "Salud Vital Corporal"],
        "Emocional": ["Autoconocimiento", "Autoregulación", "Cuidado Personal", "Motivación", "Resiliencia"],
        "Mental": ["Disfruta De La Realidad", "Manejo Del Stress", "Relaciones Saludables", "Conexión Con Otros", "Seguridad Y Confianza"],
        "Existencial": ["Autenticidad Conmigo Mismo", "Lo Que Piensas Te Motiva", "Por Qué Estoy Aquí?", "Propósito De Vida", "Quién Soy"],
        "Financiera": ["Ahorro", "Deuda", "Ingresos", "Inversión", "Presupuesto"],
        "Ambiental": ["Autocuidado", "Armonía ambiental", "Accesibilidad Ambiental", "Atención preventiva", "Conciencia ambiental"]
    }

    # Interpretaciones
    interpretaciones = {
        
    }

    inicio = 0
    promedios_categorias = []
    for categoria in categorias:
        dim = dimensiones[categoria]
        respuestas_categoria = valores_respuestas[inicio:inicio + len(dim)]
        inicio += len(dim)
        
        # Normalización
        valores = np.interp(respuestas_categoria, (1, 10), (0, 1))
        promedio = np.mean(valores)
        promedios_categorias.append(promedio)
        # Tabla de porcentajes
        porcentajes = [f"{int(v * 100)}%" for v in valores]
        tabla = pd.DataFrame({
            "Dimensión": dim,
            "Porcentaje": porcentajes
        })

        # Interpretación basada en el promedio de la categoría
        promedio = np.mean(valores)
        if promedio <= 0.2:
            nivel = "muy_bajo"
        elif promedio <= 0.4:
            nivel = "bajo"
        elif promedio <= 0.6:
            nivel = "medio"
        elif promedio <= 0.8:
            nivel = "alto"
        else:
            nivel = "muy_alto"
        interpretacion = interpretaciones.get(categoria, {}).get(nivel, "")
        
        
        angulos = [n / float(len(dim)) * 2 * pi for n in range(len(dim))]
        angulos += angulos[:1]
        valores = np.append(valores, valores[0])

        # Aumentar el tamaño de la figura para dar más espacio
        fig, ax = plt.subplots(figsize=(8, 10), subplot_kw=dict(polar=True))  # Aumenté el ancho y alto
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)
        ax.fill(angulos, valores, color="#90EE90", alpha=0.5)
        ax.plot(angulos, valores, color="#2E8B57", linewidth=2.5)

        # Ajustar posición de las etiquetas y espacio alrededor
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(dim, fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylim(0, 1)

        # Añadir más espacio entre las etiquetas y el gráfico
        ax.tick_params(pad=15)  # Aumenta este valor si necesitas más espacio

        # Ajustar posición del título si lo tienes
        # ax.set_title(f"Perfil en {categoria}", fontsize=16, fontweight='bold', color="#2F4F4F", pad=30)

        ax.set_yticklabels([])

        # Recuadro alrededor del gráfico
        for spine in ax.spines.values():
            spine.set_edgecolor("#333333")
            spine.set_linewidth(1.5)

        # Ajustar posición y tamaño de la tabla
        tabla_estilo = plt.table(
            cellText=tabla.values,
            colLabels=tabla.columns,
            cellLoc='center',
            loc='bottom',
            bbox=[-0.25, -0.7, 1.5, 0.6]  # Ajusta estos valores para posicionar mejor la tabla
        )

        # Resto del estilo de la tabla (igual que antes)
        tabla_estilo.auto_set_font_size(False)
        tabla_estilo.set_fontsize(14)
        tabla_estilo.scale(1.9, 1.9)

        for (i, j), cell in tabla_estilo.get_celld().items():
            cell.set_edgecolor('grey')
            cell.set_linewidth(0.6)
            if i == 0:
                cell.set_facecolor('#E0F7FA')
                cell.set_text_props(weight='bold', color='#1E88E5')
            else:
                cell.set_facecolor('#ffffff' if i % 2 == 0 else '#f2f2f2')

        # # Ajustar posición de la interpretación
        # plt.text(
        #     0.5,  # centro horizontal
        #     -0.9,  # posición vertical relativa a la tabla
        #     interpretacion,
        #     ha='center',
        #     va='top',
        #     fontsize=12,
        #     color='#333333',
        #     wrap=True,
        #     transform=ax.transAxes  # Usar coordenadas relativas al eje
        # )

        # Ajustar el layout con más padding
        plt.tight_layout(pad=3.0)  # Aumenta este valor si necesitas más espacio general
        # # Recuadro alrededor de la tabla
        # plt.gca().add_patch(Rectangle(
        #     (0.1, -0.5), 0.5, 0.45,  # Posición y tamaño del recuadro
        #     fill=False, edgecolor='#333333', linewidth=1.5, linestyle='-'
        # ))

        # # Ajuste de espacio vertical
        # plt.subplots_adjust(bottom=0.4)

        # Interpretación más cerca de la tabla
        # plt.figtext(
        #     0.5, -0.25,
        #     interpretacion,
        #     ha="center",
        #     fontsize=16,
        #     bbox={"facecolor": "whitesmoke", "edgecolor": "black", "boxstyle": "round,pad=0.5", "alpha": 0.8}
        # )
        # fig = plt.gcf()
        # ax = plt.gca()
        # bbox = ax.get_position()

        # padding_x = 0.4
        # padding_y = 0.05

        # fig.patches.append(FancyBboxPatch(
        #     (bbox.x0 - padding_x, bbox.y0 - padding_y),
        #     bbox.width + 2 * padding_x,
        #     bbox.height + 2 * padding_y,
        #     boxstyle="round,pad=0.02",
        #     edgecolor="#00BCD4",
        #     linewidth=2.5,
        #     fill=False,
        #     transform=fig.transFigure
        # ))
        # Guardar imagen
        # fig.patches.append(Rectangle(
        # (0.1, 0.25), 0.8, 0.70,  # Ajusta estas coordenadas y dimensiones
        # transform=fig.transFigure,
        # fill=False,
        # edgecolor="#00BCD4",  # Puedes cambiar el color si deseas
        # linewidth=3
        # ))

        plt.savefig(f"statics/radar_{categoria.lower()}.png", dpi=300, bbox_inches="tight")
        plt.close()
      # Gráfico radar consolidado
    tabla_promedios = promedios_categorias[:]    
    angulos_global = [n / float(len(categorias)) * 2 * pi for n in range(len(categorias))]
    angulos_global += angulos_global[:1]
    promedios_categorias.append(promedios_categorias[0])
    # Convertir datos en porcentaje para la tabla
    tabla = {
        "Categoría": categorias,
        "Porcentaje": [f"{v * 100:.1f}%" for v in tabla_promedios]
            }
    tabla_df = pd.DataFrame(tabla)
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.fill(angulos_global, promedios_categorias, color="#90EE90", alpha=0.5)
    ax.plot(angulos_global, promedios_categorias, color="#2E8B57", linewidth=2.5)
    ax.set_xticks(angulos_global[:-1])
    ax.set_xticklabels(categorias, fontsize=14, fontweight='bold', color='#333333')
    ax.set_ylim(0, 1)
    ax.set_yticklabels([])
        # Agregar tabla debajo del gráfico
    tabla_estilo = plt.table(
        cellText=tabla_df.values,
        colLabels=tabla_df.columns,
        cellLoc='center',
        loc='bottom',
        bbox=[-0.25, -1.05, 1.5, 0.8]
    )
    tabla_estilo.auto_set_font_size(False)
    tabla_estilo.set_fontsize(12)
    tabla_estilo.scale(1.5, 1.5)

    # Estilo de la tabla
    for (i, j), cell in tabla_estilo.get_celld().items():
        cell.set_edgecolor('grey')
        cell.set_linewidth(0.6)
        if i == 0:
            cell.set_facecolor('#E0F7FA')
            cell.set_text_props(weight='bold', color='#1E88E5')
        else:
            cell.set_facecolor('#ffffff' if i % 2 == 0 else '#f2f2f2')

    # Ajuste de espacio vertical para acomodar la tabla
    plt.subplots_adjust(bottom=0.3)

    # Obtener la figura actual
    fig = plt.gcf()

# Añadir un rectángulo en coordenadas de figura (como fondo decorativo)
    # fig.patches.append(Rectangle(
    # (0.1, 0.25), 0.8, 0.70,  # Ajusta estas coordenadas y dimensiones
    # transform=fig.transFigure,
    # fill=False,
    # edgecolor="#00BCD4",  # Puedes cambiar el color si deseas
    # linewidth=3
    # ))
    # Guardar imagen del gráfico unificado
    plt.savefig("statics/radar_general.png", dpi=300, bbox_inches="tight")
    plt.close()

      
def agregar_fondo(c, width, height, background_path):
    """Dibuja la imagen de fondo en cada página."""
    if os.path.exists(background_path):
        bg = ImageReader(background_path)
        img_width = width  # Ancho igual al de la página
        img_height = height * 0.10  # Alto del 25% de la página
        c.drawImage(bg, 0, height - img_height, width=img_width, height=img_height)

        
def agregar_fondopiepagina(c, width, height, background_path_pie):
    """Dibuja la imagen pie de pagina de fondo en cada página."""
    if os.path.exists(background_path_pie):
        bg = ImageReader(background_path_pie)
        img_width = width*0.95  # Ancho igual al de la página
        img_height = height * 0.07 # Alto del 25% de la página
        c.drawImage(bg, x=0, y=0, width=img_width, height=img_height, preserveAspectRatio=True, anchor='s')

def agregar_pie_pagina(c, width, page_num):
    """Dibuja el número de página en la parte inferior."""
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawCentredString(width - 40, 30, f"Página {page_num}")       
     
    
def generar_pdf_con_analisis(usuario_id):
    """Genera un PDF con un análisis de las respuestas del usuario."""
    pdf_path = f"statics/analisis_usuario_{usuario_id}.pdf"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, apellidos  FROM usuarios WHERE numero_identificacion = %s", (usuario_id,))
    nombre_completo_global = cursor.fetchone()
    nombre_completo = f"{nombre_completo_global[0]} {nombre_completo_global[1]}"  # Concatena nombre y apellido

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    background_path = "statics/BKVITAL.PNG"
    background_path_pie = "statics/pie.PNG"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    page_num = 1
    # Dibujar imagen de fondo en la primera página
    agregar_fondo(c, width, height, background_path)
    agregar_fondopiepagina(c, width, height, background_path_pie)
        # Obtener respuestas de la base de datos

    # Texto introductorio
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor("#2E4053"))
    c.drawCentredString(width / 2, height - 90, "ANÁLISIS DE PERCEPCIÓN DE BIENESTAR")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor("#2E4053"))
    c.drawCentredString(width / 2, height - 110, f"{nombre_completo.upper()}")
    # Resto del texto
    c.setFont("Helvetica", 18)
    c.setFillColor(colors.black)
        
       # Configurar estilos
    styles = getSampleStyleSheet()
    estilo_justificado = ParagraphStyle(
        "Justificado",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        alignment=4,  # 4 es para justificar el texto
    )
    
    texto_intro = (  
    "Este informe refleja tu percepción personal sobre las dimensiones clave que conforman tu bienestar integral. "
    "Los resultados muestran fortalezas destacadas en múltiples dimensiones del Ser humano, evidenciando áreas donde te sientes confianza, motivación y alineación con tus propósitos. "
    "Además, identifica oportunidades de mejora que, al abordarse, pueden potenciar tu crecimiento y estabilidad en el largo plazo.\n\n"

    "Este documento no solo es una radiografía de tu percepción actual, sino también una herramienta de autoconocimiento diseñada para inspirar reflexión y acción. "
    "Tu nivel de energía, interpretado como un indicador de tu capacidad para interactuar con desafíos y oportunidades, complementa esta visión, resaltando tu disposición para responder de manera consciente y proactiva. "
    "Recuerda que el bienestar es un camino dinámico: celebrar tus logros y explorar áreas de desarrollo te acercará a una vida más plena y adaptativa. "
    "Utiliza este informe como una guía para seguir cultivando tu equilibrio, reconociendo que cada dimensión es un paso hacia la versión más auténtica y realizada de ti.\n\n"
    
    "Este informe es, ante todo, una herramienta para que sigas explorando y potenciando aquellas áreas que te acerquen a la versión más auténtica y realizada de ti mismo(a)."
    )
    parrafo_intro = Paragraph(texto_intro, estilo_justificado)
     # Definir el marco de texto en el PDF
    frame = Frame(60, height - 560, width - 120, 400)
    frame.addFromList([parrafo_intro], c)
    page_num += 1
    c.showPage()
    # Dibujar imagen de fondo en la primera página
    agregar_fondo(c, width, height, background_path)
    agregar_fondopiepagina(c, width, height, background_path_pie)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pregunta, respuesta FROM respuestasForm WHERE usuario_id = %s", (usuario_id,))
    respuestas = cursor.fetchall()
    conn.close()

    if not respuestas:
        return None  # Si no hay respuestas, no generamos el PDF.

    # Convertir respuestas a valores numéricos
    valores_respuestas = np.array([int(respuesta) for _, respuesta in respuestas])
    generar_graficos_por_categoria(valores_respuestas)
    # Análisis básico
    promedio = np.mean(valores_respuestas)
    min_valor = np.min(valores_respuestas)
    max_valor = np.max(valores_respuestas)

    # Determinar tendencias
    if promedio >= 8:
        interpretacion = "Se muestra con una alta capacidad de resiliencia, además puede soportar las demandas de la vida diaria. Tiene una percepción de bienestar que le proporciona la sensación de que todas las áreas de su vida se encuentran en un estado de aparente plenitud. Su energía vital se ubica por encima del promedio, lo que quiere decir que siente que todo en su vida marcha de la mejor manera. Tiende a tener un estado de ánimo elevado, lo cual representa una situación no retadora para la persona, pues puede llegar a no permitirse la expresión de emociones, así como la transformación de las mismas."
        recomendaciones = [
            "•	Permitirse identificar sus emociones y las reacciones que presenta cuando experimenta alguna situación desfavorable, gestionándolas y equilibrándolas.",
            "•	Ser consciente de sus oportunidades de mejora, con el propósito de tomar acciones para transformarlas",
            "•	Continuar potenciando sus capacidades y habilidades, a través del reconocimiento de otras facultades, y de herramientas del medio que pueda emplear para dicho fin",
            "•	Darse momentos de descanso, quietud y desconexión."
        ]
    elif promedio >= 7:
        interpretacion = "Tiene alta capacidad de percepción de los estímulos ambientales, puede responder de manera adecuada y oportuna frente a los mismos, lo cual la ubica en una posición de consciencia. En este nivel, se reconocen las oportunidades de mejora y se buscan estrategias que permitan transformarlas. La percepción de bienestar que tiene la persona sobre sí misma y el ambiente es óptima, reconoce que se encuentra en equilibrio y tiene todas las potencialidades para llevar una vida plena; lo anterior, le permite sentir vitalidad y motivación para emprender acciones que la lleven al logro de objetivos, así como para enfrentarse a nuevos retos relacionales, personales y/o laborales."
        recomendaciones = [
            "•	Continuar fortaleciendo la inteligencia emocional a través de la empatía, las habilidades sociales, la autoconsciencia y el autoconocimiento",
            "•	Seguir potenciando su proyecto de vida por medio de acciones asertivas que permitan el logro de objetivos",
            "•	Generar relaciones de valor con las personas a su alrededor; buscando que la relación consigo mismo y los demás, sean motivadores para seguir cargando de sentido las áreas de su vida, encontrando en ellas equilibrio"
        ]
    elif promedio >= 5:
        interpretacion = "Puede experimentar cambios en el estado de ánimo por periodos de tiempo intermitente, llevándola a tener sensación de cansancio y malestar frente algunos acontecimientos de la vida diaria. Si bien puede reconocer tener cierta capacidad para enfrentar diferentes situaciones, esta persona puede experimentar sensaciones de impotencia y una consciencia moderada frente al sentido de vida, sin embargo, resalta la importancia de la integralidad del ser (cuerpo, mente, emociones y espíritu), aunque se le dificulta tomar acción para resolver determinados momentos de crisis. Su proceso de aprendizaje resulta más efectivo, debido a la capacidad de autorreflexión y la búsqueda de mejoras continuas."
        recomendaciones = [
            "•	Gestionar sus emociones, identificando reacciones frente a situaciones y buscando alternativas para su manejo",
            "•	Transformar pensamientos limitantes o negativos",
            "•	Practicar actividades de interés personal, y donde se vincule sus relaciones interpersonales",
            "•	Identificar los propios recursos psicológicos y las herramientas empleadas en otros momentos de la vida, para hace frente a situaciones adversas",
            "•	Tener consciencia del aquí y el ahora, viviendo en el presente",
            "•	Buscar técnicas para aumentar la productividad",
        ]
    elif promedio >= 3:
        interpretacion = "Puede actuar de manera lenta para captar situaciones o demandas del entorno; se percibe con agotamiento y falta de energía, lo que hace que se presenten alteraciones a nivel físico, emocional, mental y espiritual, que producen sensación de malestar, poca actividad, desmotivación y baja productividad. Puede no estar conectada con su sentido existencial y su fuente de energía, es decir, repite comportamientos que la hacen permanecer en el mismo ciclo, dificultándosele encontrar motivadores alineados con su propósito de vida."
        recomendaciones = [
            "•	Mejorar hábitos alimenticios y del sueño",
            "•	Buscar motivadores para encontrar su propósito y trabajar en su proyecto de vida",
            "•	Exteriorizar y gestionar sus emociones.",
            "•	Realizar actividades que solía hacer y disfrutar; tener un diario de bienestar donde se consigne la rutina diaria",
            "•	Practicar acciones para el autocuidado, tales como: actividad física, chequeos médicos, dedicarse momentos de esparcimiento, darse regalos, etc.",
            "•	Emplear técnicas de meditación",
            "•	Trabajar la gestión del tiempo"
        ]
    else:
        interpretacion = "Puede experimentar una alta resistencia para resolver situaciones que se le presentan en la vida cotidiana, adicional a ello, puede presentar una escasa consciencia para comprender y actuar ante situaciones nuevas e inesperadas. Puede presentarse agotamiento físico, mental, emocional y espiritual de carácter extremo y persistente en el tiempo, perjudicando a la persona en las diferentes esferas de la vida. La desesperanza y frustración continúan en un crecimiento exponencial."
        recomendaciones = [
            "•	Dedicarse tiempos de descanso y reposo acordes a la necesidad identificada",
            "•	Emplear técnicas de respiración, relajación muscular y meditación (consciencia plena)",
            "•	Llevar una dieta balanceada.",
            "•	Higiene del sueño",
            "•	Diseñar y emplear un cronograma de actividades gratificantes y/o rutina diaria.",
            "•	Propiciar la autorreflexión, buscando fortalecer su dimensión espiritual.",
            "•	Trabajar el sentido de vida, buscando motivadores, encontrando su misión, pasión y vocación de vida",
            "•	Identificar/transformar creencias y patrones de comportamiento.",
            "•	Buscar y establecer redes de apoyo.",
            "•	Practicar actividades artísticas tales como: dibujo, pintura, escritura, baile."
        ]
        
    
        # Crear el PDF
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor("#2E4053"))  # Color azul oscuro para el título principal
    c.drawCentredString(width / 2, height - 90, "Análisis de tus Respuestas")

    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)  # Color negro para el contenido
    y_position = height - 120
    max_width = width - 150  
    lineas_interpretacion = simpleSplit(interpretacion, "Helvetica", 12, max_width)

     # Estilos de párrafo
    styles = getSampleStyleSheet()
    estilo_justificado = ParagraphStyle(
        "Justificado",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        alignment=4,  # 4 es para justificar el texto
    )
       # Texto de interpretación
    parrafo_interpretacion = Paragraph(interpretacion, estilo_justificado) 

        # Definir un marco para el párrafo
    frame = Frame(80, height - 450, width - 160, 300)
    frame.addFromList([parrafo_interpretacion], c)

    y_position = height - 350  # Ajustar espacio después de la interpretación
    y_position -= 20
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#1F618D"))  # Color azul medio para subtítulos
    c.drawString(85, y_position, "Recomendaciones:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)  # Regresar a color negro para el contenido

    for recomendacion in recomendaciones:
        lineas_recomendacion = simpleSplit(recomendacion, "Helvetica", 12, max_width)
        for linea in lineas_recomendacion:
            c.drawString(85, y_position, linea)
            y_position -= 20
        y_position -= 10

    y_position -= 20
    # Verificar si hay suficiente espacio en la página para la imagen
    img_width = 300
    img_height = 300
    x_position = (width - img_width) / 2
   
    # if y_position - img_height < 50:  # Si no hay suficiente espacio, crear nueva página
    c.showPage()
    page_num += 1
    agregar_fondo(c, width, height, background_path)
    agregar_fondopiepagina(c, width, height, background_path_pie)
    agregar_pie_pagina(c, width, page_num)
    y_position = height - 120  # Reiniciar posición en la nueva página

    # Dibujar la imagen de análisis general
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor("#2E4053"))
    c.drawCentredString(width / 2, y_position, "Análisis General")

    y_position -= 40  # Ajuste de espacio para la imagen
    image_path = "statics/radar_general.png"
    c.drawImage(image_path, x_position, y_position - img_height, width=img_width, height=img_height)

    # Agregar número de página
    agregar_pie_pagina(c, width, page_num) 
    # Saltar a una nueva página para los gráficos si no hay suficiente espacio
    #c.showPage()    
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor("#2E4053"))  # Título principal para gráficos
    #c.drawCentredString(width / 2, height - 60, "Gráficos por Categoría")

    y_position = height - 120
    img_width = 250
    img_height = 250
    x_position = (width - img_width) / 2
    # Agregar número de página
    agregar_pie_pagina(c, width, page_num) 
    descripciones = {
    "vital": "Tu cuerpo es el lienzo donde se plasma tu historia. Los hábitos que has construido —desde la nutrición hasta el descanso— revelan cómo dialogas con tu energía física. Este análisis no juzga, sino que ilumina oportunidades para alinear tus acciones con las necesidades únicas de tu organismo. Aquí descubrirás cómo fortalecer tu vitalidad para que cada día sea una expresión de cuidado consciente.",
    "emocional": "Las emociones son ventanas a tu mundo interno. Tus respuestas reflejan cómo navegas la alegría, el estrés o la incertidumbre, y cómo estas experiencias moldean tus relaciones y decisiones. Este espacio te invita a observar patrones, celebrar tus avances y reconocer dónde puedes cultivar mayor equilibrio emocional para vivir con autenticidad y serenidad.",
    "mental": "Tu mente es un jardín: sus pensamientos y creencias dan forma a tu realidad. Este análisis explora cómo cultivas flexibilidad ante los desafíos, gratitud frente a los logros y claridad en tus decisiones. Descubrirás si tus patrones mentales te acercan a la plenitud o si hay terrenos fértiles para sembrar nuevas perspectivas",
    "existencial": "¿Qué huella quieres grabar en el mundo? Tus respuestas revelan cómo conectas tus acciones diarias con un propósito más profundo. Aquí explorarás si tu vida actual resuena con tus valores esenciales y cómo puedes alinear decisiones futuras para que cada paso contribuya a un legado auténtico y significativo",
    "financiera": "El dinero no solo se cuenta: se gestiona con mente y corazón. Tus elecciones financieras —desde el ahorro hasta la inversión— hablan de tus valores y tu capacidad para equilibrar lo práctico con lo emocional. Este análisis te guiará a identificar fortalezas y áreas donde transformar preocupaciones en estrategias claras, construyendo seguridad material y paz interior.",
    "ambiental": "Tu relación con la Tierra es un reflejo de tu conexión con la vida. Tus hábitos cotidianos —desde el consumo hasta el manejo de recursos— muestran cómo honras el ecosistema del que formas parte. Esta evaluación te ayudará a identificar acciones para transformar tu impacto, no solo como un acto ecológico, sino como un compromiso con tu propio bienestar integral"
                   }
    # Estilo de párrafo justificado
    paragraph_style = ParagraphStyle(
        name="Justificado",
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        alignment=TA_JUSTIFY,
        textColor=colors.black,
    )
    interpretaciones = {
        "vital": {
        "muy_bajo": "⚠️ Nivel crítico de energía. Tus resultados indican un agotamiento físico significativo que puede manifestarse como fatiga crónica, dificultad para concentrarte o mayor susceptibilidad a enfermedades. Es esencial que priorices tu descanso, cuides tu alimentación y realices actividad física ligera. Un sueño reparador de al menos 7 a 9 horas, una dieta rica en hierro y vitamina B12, y caminatas cortas pueden ayudarte a comenzar tu recuperación. También es recomendable realizar chequeos médicos para descartar posibles deficiencias nutricionales.",
        
        "bajo": "🔄 Energía por debajo del óptimo. Experimentas fluctuaciones de energía que afectan tu productividad diaria. La recuperación tras esfuerzos físicos o mentales puede ser más lenta de lo deseable, lo que genera un ritmo de vida inestable. Incorporar horarios regulares de alimentación, técnicas de respiración, evitar estimulantes en exceso y fortalecer tu cuerpo con ejercicios suaves puede ayudarte a restaurar tu vitalidad de manera progresiva.",
        
        "medio": "✅ Base sólida con potencial. Tu nivel de energía es estable en general, pero aún se perciben bajones ocasionales que podrían ser optimizados. Con pequeños ajustes en tus hábitos puedes lograr un mejor rendimiento físico y mental. Técnicas de trabajo por ciclos, una mejor hidratación, mayor atención a tu alimentación diaria y el uso de suplementos naturales pueden marcar una gran diferencia en tu bienestar corporal.",
        
        "alto": "🌟 Vitalidad notable. Tienes una buena respuesta física y mental frente a las demandas del día a día. Te recuperas con facilidad, mantienes un ritmo activo y tu cuerpo funciona con eficiencia. Para mantener este estado, es importante variar tus rutinas de ejercicio, cuidar la calidad de tus alimentos y sostener prácticas de autocuidado como el descanso adecuado o actividades regenerativas como la sauna o los baños de contraste.",
        
        "muy_alto": "🔥 Energía excepcional. Demuestras hábitos altamente efectivos que sostienen tu vitalidad de manera continua. Este nivel de energía no solo te permite enfrentar tus retos personales con entusiasmo, sino que también impacta positivamente en quienes te rodean. Puedes explorar nuevas dimensiones como el entrenamiento de alto rendimiento, mentoría en bienestar, técnicas de biohacking o terapias avanzadas de regeneración celular para llevar tu salud al siguiente nivel."
            },
        "emocional": {
        "muy_bajo": "⚠️ Estado emocional crítico. Tus emociones están desreguladas y es posible que sientas tristeza profunda, desesperanza o una falta de motivación constante. Este estado puede impactar gravemente tu salud mental y física si no se atiende. Es prioritario buscar espacios de contención emocional, hablar con un profesional de la salud mental y reconectar con actividades que te brinden paz y seguridad.",
        
        "bajo": "🔄 Altibajos emocionales. Vives momentos de ánimo variable que afectan tu estabilidad diaria. Aunque logras gestionar algunas situaciones, hay una dificultad latente para mantener la calma o expresar adecuadamente lo que sientes. Es un buen momento para fortalecer tu inteligencia emocional, aprender a identificar tus emociones y desarrollar estrategias para canalizarlas de manera saludable.",
        
        "medio": "✅ Bien, pero con áreas a mejorar. En general manejas tus emociones de forma aceptable, aunque en ciertas situaciones puedes sentirte sobrecargado, ansioso o desconectado. Aprender a cultivar el equilibrio emocional, practicar la autocompasión y mantener relaciones saludables te permitirá avanzar hacia un mayor bienestar emocional.",
        
        "alto": "🌟 Gran equilibrio emocional. Tu nivel de madurez emocional es alto y se refleja en tu capacidad para afrontar los desafíos con serenidad, comunicarte con claridad y mantener vínculos estables. Este balance te ayuda a mantener tu motivación, reducir el estrés y construir un entorno emocionalmente saludable.",
        
        "muy_alto": "🔥 Fortaleza emocional sobresaliente. Posees una gran inteligencia emocional que te permite mantener la calma bajo presión, ofrecer apoyo a otros y transformar experiencias negativas en aprendizajes significativos. Tu presencia emocional tiene un efecto positivo en tu entorno y eres una fuente de inspiración para quienes te rodean."
        },
        "mental": {
        "muy_bajo": "⚠️ Confusión mental y bajo enfoque. Tus respuestas reflejan una carga cognitiva significativa, con dificultad para concentrarte, tomar decisiones y organizar tus pensamientos. Esta situación puede estar influenciada por el estrés, la fatiga, la sobreestimulación o la falta de descanso mental adecuado.",
        
        "bajo": "🔄 Nivel bajo de agilidad mental. Aunque logras mantener cierto control sobre tus pensamientos, es probable que experimentes dispersión, estrés acumulado o problemas para sostener tu atención durante períodos largos. Esto puede interferir en tu productividad y en la calidad de tus decisiones cotidianas. ",
        
        "medio": "✅ Funcionamiento mental adecuado con margen de mejora. En general, tu capacidad cognitiva se mantiene estable, pero puedes experimentar ocasionalmente fatiga mental, indecisión o pensamientos repetitivos. Aprovecha este punto de equilibrio para desarrollar habilidades como la planificación estratégica, la visualización positiva y la resolución de problemas.",
        
        "alto": "🌟 Gran claridad y agudeza mental. Tus resultados indican que gestionas de forma eficiente tus recursos cognitivos, con buena capacidad para analizar, planificar y resolver situaciones. Esto se refleja en una mayor eficacia para aprender, adaptarte y mantener una visión objetiva ante los desafíos. Mantén este estado reforzando hábitos como la lectura regular.",
        
        "muy_alto": "🔥 Dominio mental excepcional. Estás en un nivel avanzado de rendimiento cognitivo, lo cual se manifiesta en una mente ágil, clara y adaptable. Tu capacidad para enfocarte, aprender rápidamente y tomar decisiones acertadas es notable, y probablemente has desarrollado una excelente autorregulación de tus pensamientos."
         },
       "existencial": {
        "muy_bajo": "⚠️ Falta de propósito o conexión. Actualmente te sientes perdido, sin una dirección clara en la vida, lo cual puede provocar desmotivación, vacío o desconexión personal. Es fundamental que te tomes un momento para reflexionar profundamente sobre lo que te importa, te mueve y te genera sentido. Explorar tu historia personal, tus valores, y dialogar con otros puede ayudarte a comenzar a reconectar con tu propósito.",
        
        "bajo": "🔄 En búsqueda de sentido. Aunque existen momentos de claridad, a menudo sientes que lo que haces carece de un significado profundo. Esta sensación puede generar frustración o una constante búsqueda externa de validación. Dedicar tiempo a descubrir lo que realmente valoras, lo que te hace feliz y establecer metas alineadas contigo mismo puede marcar un cambio significativo.",
        
        "medio": "✅ Conexión parcial con el propósito. Tienes claridad en algunas áreas de tu vida, pero aún quedan aspectos importantes que podrías definir mejor. Este nivel te permite avanzar, pero también es una invitación a revisar tus decisiones, prioridades y creencias para asegurar que estén en sintonía con tu verdadera esencia.",
        
        "alto": "🌟 Buena conexión con tus valores. Has logrado alinear gran parte de tus acciones con lo que realmente valoras, lo cual se traduce en satisfacción personal y sentido de dirección. Siguiendo este camino, puedes potenciar tu crecimiento y desarrollar una vida más consciente y coherente.",
        
        "muy_alto": "🔥 Plenitud existencial. Tu propósito está bien definido y lo manifiestas con autenticidad en tu vida diaria. Esta conexión profunda contigo mismo te brinda estabilidad, alegría duradera y un impacto positivo en tu entorno. Estás en condiciones de inspirar a otros, guiar procesos de cambio y construir una vida con propósito elevado."
       },
        "financiera": {
        "muy_bajo": "⚠️ Inseguridad financiera alta. Tu situación económica actual genera altos niveles de estrés, inestabilidad y preocupación. Es posible que enfrentes deudas, gastos inesperados o falta de planificación. Es urgente que comiences por revisar tus ingresos y egresos, establecer prioridades básicas y buscar apoyo educativo o profesional en temas financieros. Un cambio de hábitos puede marcar la diferencia.",
        
        "bajo": "🔄 Necesidad de organización financiera. Manejas tus recursos, pero con dificultades para ahorrar o mantener un control eficiente de tus gastos. Hay decisiones que podrían estar afectando tu estabilidad futura. Aprender sobre planificación financiera, establecer presupuestos claros y reducir gastos innecesarios puede ayudarte a mejorar tu panorama económico.",
        
        "medio": "✅ Buen manejo financiero con áreas de mejora. Tienes cierto control sobre tus finanzas, aunque aún puedes optimizar tus ingresos, ahorrar con mayor constancia o generar nuevas fuentes de ingreso. Revisar tus metas económicas a corto y largo plazo puede ayudarte a tomar mejores decisiones y alcanzar mayor estabilidad.",
        
        "alto": "🌟 Finanzas saludables. Tu nivel de control financiero es alto, lo cual te permite vivir con tranquilidad, planificar tu futuro y tomar decisiones inteligentes sobre tu dinero. Mantener este nivel requiere seguir aprendiendo, invirtiendo con criterio y diversificando tus fuentes de ingreso.",
        
        "muy_alto": "🔥 Excelente estabilidad financiera. Has alcanzado una visión clara y estratégica sobre tus finanzas. No solo cubres tus necesidades y ahorras con constancia, sino que además inviertes, generas ingresos pasivos y piensas en el largo plazo. Este nivel te permite construir riqueza, impactar en otros y dejar un legado financiero sólido."
    },
        "ambiental": {
        "muy_bajo": "⚠️ Impacto ambiental alto. Tus hábitos actuales tienen consecuencias negativas sobre el medio ambiente. Es posible que haya un bajo nivel de conciencia sobre reciclaje, uso de recursos o contaminación. Es importante que tomes responsabilidad y comiences con acciones pequeñas como reducir residuos, evitar el uso excesivo de plásticos y optar por medios de transporte sostenibles.",
        
        "bajo": "🔄 Hábitos ecológicos mejorables. Aunque hay cierta intención de cuidar el ambiente, aún no se refleja de forma concreta en tu estilo de vida. Adoptar prácticas como reutilizar productos, consumir local y reducir tu huella de carbono puede ayudarte a alinear tus valores con tu comportamiento diario.",
        
        "medio": "✅ Compromiso moderado con el medioambiente. Has adoptado algunos hábitos sostenibles, pero hay áreas que puedes seguir mejorando. Revisar tu consumo energético, el origen de los productos que usas y tu forma de desechar materiales te permitirá avanzar hacia una vida más respetuosa con el entorno.",
        
        "alto": "🌟 Excelente conciencia ambiental. Llevas un estilo de vida en armonía con el planeta, aplicando principios de sostenibilidad, consumo responsable y respeto por los recursos naturales. Este nivel te posiciona como un ejemplo para otros, y puedes seguir creciendo al compartir tu experiencia y apoyar causas ecológicas.",
        
        "muy_alto": "🔥 Gran impacto positivo en el planeta. Eres un agente de cambio con un compromiso profundo por la protección del medioambiente. Tus acciones diarias no solo son sostenibles, sino también inspiradoras para quienes te rodean. Estás en condiciones de liderar proyectos ecológicos, educar a otros y promover políticas ambientales transformadoras."
    },
        }   
    categorias = ["vital", "emocional", "mental", "existencial", "financiera", "ambiental"]

    # Validar que hay 30 respuestas
    if len(valores_respuestas) != 30:
        raise ValueError("Se esperaban exactamente 30 respuestas (6 categorías x 5 preguntas)")

    # Calcular promedios por categoría
    promedios = [np.mean(valores_respuestas[i:i+5]) for i in range(0, 30, 5)]

    # Process first 5 categories in the loop
    for idx, categoria in enumerate(categorias[:5]): 
        promedio = promedios[idx]

        if promedio <= 1.6:
            nivel = "muy_bajo"
        elif promedio <= 2.2:
            nivel = "bajo"
        elif promedio <= 6.8:
            nivel = "medio"
        elif promedio <= 9.0:
            nivel = "alto"
        else:
            nivel = "muy_alto"

    
    for categoria in ["vital", "emocional", "mental", "existencial", "financiera","ambiental"]:
        image_path = f"statics/radar_{categoria}.png"
        
        if os.path.exists(image_path):
            c.showPage()
            page_num += 1
            agregar_fondo(c, width, height, background_path)
            agregar_fondopiepagina(c, width, height, background_path_pie)
            agregar_pie_pagina(c, width, page_num)

            margen_horizontal = 50
            margen_vertical = 100

            # Título
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(colors.HexColor("#1F618D"))
            titulo = f"Salud {categoria.capitalize()}"
            c.drawCentredString(width / 2, height - margen_vertical, titulo)

            # Descripción
            descripcion = descripciones.get(categoria.lower(), "")
            p = Paragraph(descripcion, paragraph_style)

            bloque_top = height - margen_vertical - 30
            frame_width = width - 2 * margen_horizontal
            frame_height = 100

            frame = Frame(
                margen_horizontal,
                bloque_top - frame_height,
                frame_width,
                frame_height,
                showBoundary=0
            )
            frame.addFromList([p], c)

            # Imagen
            separacion = 20
            img_width = 280
            img_height = 280
            x_position = (width - img_width) / 2
            y_position = bloque_top - frame_height - separacion

            c.drawImage(image_path, x_position, y_position - img_height, width=img_width, height=img_height)

            # Interpretación
            interpretacion = interpretaciones.get(categoria.lower(), {}).get(nivel, "")
            p = Paragraph(interpretacion, paragraph_style)

            separacion_interpretacion = 20
            interpretacion_y = y_position - img_height - separacion_interpretacion

            frame = Frame(
                margen_horizontal,
                interpretacion_y - 100,
                frame_width,
                100,
                showBoundary=0
            )
            frame.addFromList([p], c)

    # Add Ambiental section separately (6th category)
#     c.showPage()
#     page_num += 1
#     agregar_fondo(c, width, height, background_path)
#     agregar_fondopiepagina(c, width, height, background_path_pie)
#     agregar_pie_pagina(c, width, page_num)

#     descripcion_ambiental = (
#     "El entorno que habitas influye directamente en tu bienestar. "
#     "Aquí exploramos tu conexión con la naturaleza y el compromiso con prácticas "
#     "que promueven un mundo más saludable y equilibrado para todos."
#     )

#     c.setFont("Helvetica-Bold", 18)
#     c.setFillColor(colors.HexColor("#2E4053"))  # Título principal para gráficos
#     c.drawCentredString(width / 2, height - 90, "Salud Ambiental")

#     # Estilo de párrafo justificado
#     paragraph_style = ParagraphStyle(
#         name="Justificado",
#         fontName="Helvetica",
#         fontSize=11,
#         leading=15,
#         alignment=TA_JUSTIFY,
#         textColor=colors.black,
#     )

#     # Crear el párrafo
#     p = Paragraph(descripcion_ambiental, paragraph_style)

#     # Frame para el texto (posición y tamaño)
#     margen_horizontal = 50
#     frame_width = width - 2 * margen_horizontal
#     frame_height = 90  # altura del bloque de texto

#     frame_top = height - 120  # donde empieza el frame, debajo del título

#     frame = Frame(
#         margen_horizontal,
#         frame_top - frame_height,
#         frame_width,
#         frame_height,
#         showBoundary=0  # pon 1 si quieres ver el cuadro mientras ajustas
#     )

#     frame.addFromList([p], c)
#     image_path = "statics/radar_ambiental.png"
#     img_width = 320
#     img_height = 320
#     x_position = (width - img_width) / 2
#     y_position = frame_top - frame_height - 30  # separación pequeña entre texto e imagen
#     c.drawImage(
#         image_path,
#         x_position,
#         y_position - img_height,
#         width=img_width,
#         height=img_height,
#         preserveAspectRatio=True,
#         mask='auto'
#     )

#    # Interpretación
#     interpretacion = interpretaciones.get("ambiental", {}).get(nivel, "")
#     p = Paragraph(interpretacion, paragraph_style)

#     separacion_interpretacion = 20
#     interpretacion_y = y_position - img_height - separacion_interpretacion

#     frame = Frame(
#                 margen_horizontal,
#                 interpretacion_y - 100,
#                 frame_width,
#                 100,
#                 showBoundary=0
#             )
#     frame.addFromList([p], c) 

    # Página de Plan de Acción
    c.showPage()
    page_num += 1
    agregar_fondo(c, width, height, background_path)
    agregar_fondopiepagina(c, width, height, background_path_pie)
    agregar_pie_pagina(c, width, page_num)

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#2E4053")) 
    c.drawCentredString(width / 2, height - 80, "PLAN DE ACCIÓN")
    c.setFont("Helvetica", 12)
    texto_plan_accion = [
    ("META (Qué es lo que quiero lograr)", 2),
    ("BENEFICIOS (Qué voy a obtener de lograr esta meta)", 2),
    ("PASOS PARA LOGRAR ESTA META (Qué debo hacer para lograr esta meta)", 2),
    ("PLAZOS ESTABLECIDOS (Cuándo voy a completar estas acciones)", 2),
    ("POSIBLES OBSTÁCULOS (Qué cosas podrían interferir en el logro de esta meta)", 2),
    ("POSIBLES SOLUCIONES (Cómo voy a lograr eliminar los obstáculos de mi camino)", 2),
    ("MÉTODO PARA MONITOREAR TU PROGRESO (¿Cómo sabré que estoy progresando?)", 2),
    ("¿VALE LA PENA GASTAR TIEMPO, ESFUERZO Y DINERO EN ESTA META?", 1),
]

    y_position = height - 110
    for titulo, lineas in texto_plan_accion:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y_position, titulo)
        y_position -= 18  # Espacio después del título

        c.setFont("Helvetica", 12)
        for _ in range(lineas):
            c.drawString(60, y_position, "_" * 80)
            y_position -= 24  # Espacio entre líneas

    # Última pregunta con opciones
    c.setFont("Helvetica", 12)
    c.drawString(60, y_position, "Sí _____   No _____   Sí, pero después _____   FECHA DE HOY ___________")
    c.showPage()
    page_num += 1
    agregar_fondo(c, width, height, background_path)
    agregar_fondopiepagina(c, width, height, background_path_pie)
    agregar_pie_pagina(c, width, page_num)

    # Título de la nueva sección
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#2E4053")) 
    c.drawCentredString(width / 2, height - 80, "SIETE AYUDAS PARA LA ACCIÓN")
    

    # Lista de consejos
    ayudas_accion = [
        ("1. Recuerde los beneficios que Ud. recibirá al alcanzar sus metas.",
        "Identifique los beneficios que Ud. recibirá: mayor efectividad en el trabajo, mejorar su satisfacción laboral, incrementar sus habilidades interpersonales, etc. ¿Cuáles serán los beneficios?"),
        
        ("2. Recuerde su disponibilidad de tiempo.",
        "Hay 525.600 minutos en un año. Si Ud. utiliza 15 minutos todos los días para desarrollarse, aplicará un total de 5.475 minutos por año. Esto da como resultado un 0,0104 de sus minutos anuales disponibles. ¿Puede Ud. ahorrar 0,0104 de sus minutos para desarrollarse?"),
        
        ("3. Haga las cosas de a una por vez.",
        "La gran tarea de autodesarrollarse está compuesta de pequeñas tareas. Divida y conquiste: divida la gran tarea en varias y pequeñas subtareas. Entonces concéntrese en una subtarea por vez y finalícela."),
        
        ("4. Practique, practique, practique.",
        "La práctica conduce al aprendizaje. Mientras más práctica, más aprende. Un poco de práctica todos los días es mejor que una gran sesión de práctica cada semana."),
        
        ("5. La perseverancia conquista.",
        "Aférrese a su Plan de Acción. La perseverancia es la conducta crítica necesaria para que Ud. logre sus metas. Las personas a menudo se detienen al acercarse al triunfo. Siga adelante... no pare. Si Ud. para, nunca logrará sus metas."),
        
        ("6. Responda eficazmente ante sus errores.",
        "Todos cometemos errores. Ud. los cometerá al llevar a cabo su Plan de Acción y al trabajar en el logro de sus metas. Responda eficazmente. Acepte la responsabilidad por sus errores, siéntase seguro a pesar de cometerlos, y aprenda de ellos. No piense que Ud. nunca debe cometer errores, no se preocupe y obsesione con ellos, y nunca se desanime por cometerlos."),
        
        ("7. Evoque sus 'recuerdos de éxitos'.",
        "Cuando se sienta presionado/a o frustrado/a o cuando sienta que no está progresando en su Plan de Acción, evoque una ''memoria de éxito''. Recuerde uno de sus éxitos o logros pasados. Inunde su mente con esa memoria y permita que la misma cree pensamientos, emociones e imágenes positivas. Ud. se sentirá bien, su confianza aumentará, y podrá continuar con su plan de acción y trabajar en el logro de sus metas."),
        ]

    y_position = height - 120
    max_width = width - 120  # Ajuste del margen

    for titulo, contenido in ayudas_accion:
        # Título en negrita
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y_position, titulo)
        y_position -= 18  # Espaciado después del título

        # Contenido en texto normal
        c.setFont("Helvetica", 12)
        for linea in simpleSplit(contenido, "Helvetica", 12, max_width):
            c.drawString(60, y_position, linea)
            y_position -= 18

        y_position -= 10  # Espacio adicional entre cada punto    


    c.save()
    return pdf_path


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
        # Generar el PDF con el análisis de respuestas

            contenido_html = f"""
            <html>
            <head>
                <title>¡Buen trabajo!</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
                <style>
                    body {{
                        font-family: 'Roboto', sans-serif;
                        text-align: center;
                        padding: 50px;
                        background-color: #f4f4f4;
                    }}
                    .container {{
                        background: white;
                        padding: 30px;
                        border-radius: 12px;
                        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
                        display: inline-block;
                        max-width: 500px;
                    }}
                    h1 {{
                        color: #333;
                    }}
                    p {{
                        font-size: 18px;
                        color: #666;
                    }}
                    button {{
                        background-color: #007bff;
                        color: white;
                        border: none;
                        padding: 15px 25px;
                        font-size: 18px;
                        border-radius: 8px;
                        cursor: pointer;
                        margin-top: 20px;
                        transition: background 0.3s ease-in-out;
                    }}
                    button:hover {{
                        background-color: #0056b3;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>¡Gracias por tu tiempo!</h1>
                    <p>Haz clic en el botón para generar y descargar tu análisis de respuestas:</p>
                    <button onclick="window.location.href='/descargar_pdf?usuario_id={usuario_id}'">Generar y Descargar Análisis</button>
                </div>
            </body>
            </html>
            """
            return HTMLResponse(content=contenido_html)
    else:
            return RedirectResponse(url=f"/preguntas?usuario_id={usuario_id}&pagina={pagina+1}", status_code=303)
@app.get("/descargar_pdf")
def descargar_pdf(usuario_id: int):
        pdf_path = generar_pdf_con_analisis(usuario_id)
        if pdf_path:
            return FileResponse(pdf_path, media_type="application/pdf", filename=f"Analisis_Respuestas_{usuario_id}.pdf")
        return HTMLResponse(content="<h1>Error al generar el PDF.</h1>")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)