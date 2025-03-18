from fastapi import FastAPI, Form, Request,Query 
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
from reportlab.platypus import Paragraph
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from matplotlib.patches import Rectangle
import os
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import textwrap
import pandas as pd

# Configurar la conexión a MySQL desde Railway
DB_HOST = "shuttle.proxy.rlwy.net"
DB_USER = "root"
DB_PASSWORD = "umzzdISTaNglzBNhBcTqxNMamqkCUJfs"
DB_NAME = "railway"
DB_PORT = 17125


app = FastAPI()

app.mount("/statics", StaticFiles(directory="statics"), name="statics")

preguntas_lista = [
    "¿Consideras que tu alimentación te nutre lo suficientemente bien?", "¿Realizas ejercicio físico al menos tres veces por semana?", "¿Sientes que tus habito de sueño te dan el descanso necesario?",
    "¿En los últimos seis meses te has realizado chequeos médicos?", "¿Piensas que los hábitos que hoy ocupan gran parte de tu tiempo te ayudan para tener un cuerpo más saludable?",
    "¿Consideras que tus experiencias han contribuido a tu calidad de vida o crecimiento personal?", "¿Celebras los tus logros o victorias?",
    "¿Cada que obtienes un logro practicas la celebración de la victoria?", "¿Sientes que te adaptas a cambios o nuevas situaciones con facilidad?",
    "¿Tu bienestar emocional es prioridad en tu vida?", "¿Consideras que has manejado bien los sentimientos de impotencia o duda prolongados?",
    "¿Sientes que tu círculo cercano te anima a lograr tus metas?", "¿te sientes agradecido por los logros obtenidos?",
    "¿Has reflexionado personalmente o con un profesional sobre tu salud mental en los últimos seis meses?", "¿En qué medida te sientes valorado y respetado por otros?",
    "¿Sientes que la autoimagen que tienes de ti representa tu más alto valor como ser humano?", "¿Cuándo reflexionas de tu valor personal que tan consciente eres del valor que aportas al mundo?",
    "¿Desde lo que hoy haces que pasión te motiva para seguir haciéndolo a futuro ?", "¿Los pensamientos que más tienes sustentan tu valor mas alto?","¿Cuándo conoces una verdad sobre tu vida la aceptas con facilidad?",
    "¿De tus ingresos mensuales ahorras al menos el 10%?","¿En la actualidad tienes y sigues un presupuesto mensual?","¿Tienes una o más inversiones de largo plazo que me permitan tener una base económica?",
    "¿Tienes un plan para gestionar tus deudas sin afectar tu salud financiera?","¿Hoy tienes un plan de ahorro que cubra tus gastos básicos por 3 a 6 meses?","¿Consideras que la calidad del aire en los espacios donde vives, trabajas o transitas diariamente apoya tu salud?",
    "¿Incorporas prácticas sostenibles como el reciclaje, la reducción de residuos o la reutilización de materiales en tu día a día?","¿Confías en que el agua que consumes (para beber, cocinar o higiene) es segura y cumple con estándares que protegen tu salud?","¿Conoces o tomas acciones para reducir tu huella de carbono en actividades como transporte, alimentación o consumo energético?",
    "¿Reconoces cómo tus decisiones y hábitos cotidianos contribuyen al cambio climático y, a su vez, cómo este fenómeno afecta tu calidad de vida?"
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
                <option value="Mas de 5 años">Mas de 5 años</option>
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
    preguntas_html = ""
    contador = 0
    for categoria, preguntas in categorias_preguntas.items():
        #preguntas_html += f'<h2>{categoria}</h2>'
        for pregunta in preguntas:
            if inicio <= contador < fin:
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
        <p class="instrucciones">Selecciona el número de estrellas que mejor represente tu opinión: 1 ⭐ significa 'Muy Bajo' y 10 ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ significa 'Muy Alto'</p>
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
def generar_graficos_por_categoria(valores_respuestas):
    categorias = ["Ambiental","Vital", "Emocional", "Mental", "Existencial", "Financiera"]
    dimensiones = {
        "Vital": ["Alimentación", "Descanso", "Ejercicio", "Hábitos Saludables", "Salud Vital Corporal"],
        "Emocional": ["Autoconocimiento", "Autoregulación", "Cuidado Personal", "Motivación", "Resiliencia"],
        "Mental": ["Disfruta De La Realidad", "Manejo Del Stress", "Relaciones Saludables", "Conexión Con Otros", "Seguridad Y Confianza"],
        "Existencial": ["Autenticidad Conmigo Mismo", "Lo Que Piensas Te Motiva", "Por Qué Estoy Aquí?", "Propósito De Vida", "Quién Soy"],
        "Financiera": ["Ahorro", "Deuda", "Ingresos", "Inversión", "Presupuesto"],
        "Ambiental": ["Autocuidado", "armonía ambiental", "Accesibilidad Ambiental", "Atención preventiva", "Conciencia ambiental"]
    }

    # Interpretaciones
    interpretaciones = {
        "Vital": {
            "muy_bajo": "⚠️ Energía y vitalidad muy bajas.",
            "bajo": "🔄 Necesitas más actividad física.",
            "medio": "✅ Nivel aceptable.",
            "alto": "🌟 Buena energía.",
            "muy_alto": "🔥 Excelente estado físico."
        },
        "Emocional": {
            "muy_bajo": "⚠️ Estado emocional crítico.",
            "bajo": "🔄 Altibajos emocionales.",
            "medio": "✅ Bien, pero se puede mejorar.",
            "alto": "🌟 Gran equilibrio emocional.",
            "muy_alto": "🔥 Fortaleza emocional sobresaliente."
        },
        "Mental": {
            "muy_bajo": "⚠️ Bajo enfoque y claridad mental. Evalúa técnicas para mejorar la concentración.",
            "bajo": "🔄 Necesitas fortalecer tu agilidad mental y manejo del estrés.",
            "medio": "✅ Buen nivel, pero podrías mejorar en gestión de pensamientos.",
            "alto": "🌟 Mente clara y activa. Excelente manejo de desafíos mentales.",
            "muy_alto": "🔥 Dominio mental excepcional. Gran capacidad de aprendizaje y análisis."
        },
        "Existencial": {
            "muy_bajo": "⚠️ Falta de propósito o conexión. Reflexiona sobre lo que te motiva.",
            "bajo": "🔄 Buscas sentido a tu vida, sigue explorando lo que te hace feliz.",
            "medio": "✅ Tienes claridad en algunos aspectos, pero aún puedes definir mejor tu propósito.",
            "alto": "🌟 Buena conexión con tus valores y propósitos. Continúa creciendo.",
            "muy_alto": "🔥 Plenitud y propósito bien definidos. Inspiras a los demás."
        },
        "Financiera": {
            "muy_bajo": "⚠️ Inseguridad financiera alta. Evalúa mejorar tu educación financiera.",
            "bajo": "🔄 Es momento de planificar mejor tus finanzas y controlar gastos.",
            "medio": "✅ Manejas bien tus finanzas, pero aún hay áreas de mejora.",
            "alto": "🌟 Finanzas saludables. Buen control de ingresos y gastos.",
            "muy_alto": "🔥 Excelente estabilidad financiera. Gran visión para inversiones."
        },
        "Ambiental": {
            "muy_bajo": "⚠️ Impacto ambiental alto. Es crucial reducir tu huella ecológica.",
            "bajo": "🔄 Hay margen de mejora en tus hábitos ecológicos. Reduce, reutiliza y recicla.",
            "medio": "✅ Buen compromiso con el medioambiente, pero aún puedes optimizar.",
            "alto": "🌟 Excelente conciencia ambiental. Sigues prácticas sostenibles.",
            "muy_alto": "🔥 Gran impacto positivo en el planeta. Inspiras con tu sostenibilidad."
        },
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
        
        
         # Gráfico Radar
        angulos = [n / float(len(dim)) * 2 * pi for n in range(len(dim))]
        angulos += angulos[:1]
        valores = np.append(valores, valores[0])
        

        fig, ax = plt.subplots(figsize=(6, 9), subplot_kw=dict(polar=True))
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)
        ax.fill(angulos, valores, color="#90EE90", alpha=0.5)
        ax.plot(angulos, valores, color="#2E8B57", linewidth=2.5)

        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(dim, fontsize=14, fontweight='bold', color='#333333')
        ax.set_ylim(0, 1) 
       # ax.set_title(f"Perfil en {categoria}", fontsize=16, fontweight='bold', color="#2F4F4F", pad=20)
        ax.set_yticklabels([])
        # Recuadro alrededor del gráfico
        for spine in ax.spines.values():
            spine.set_edgecolor("#333333")
            spine.set_linewidth(1.5)
        
        # Estilo mejorado para la tabla de porcentajes
        tabla_estilo = plt.table(
            cellText=tabla.values,
            colLabels=tabla.columns,
            cellLoc='center',
            loc='bottom',
            bbox=[-0.30, -1.10, 1.80, 0.90]
        )
        tabla_estilo.auto_set_font_size(False)
        tabla_estilo.set_fontsize(14)
        tabla_estilo.scale(1.9, 1.9)

        # Mejorar estilo de la tabla
        for (i, j), cell in tabla_estilo.get_celld().items():
            cell.set_edgecolor('grey')
            cell.set_linewidth(0.6)
            if i == 0:
                cell.set_facecolor('#E0F7FA')
                cell.set_text_props(weight='bold', color='#1E88E5')
            else:
                cell.set_facecolor('#ffffff' if i % 2 == 0 else '#f2f2f2')

        # Recuadro alrededor de la tabla
        plt.gca().add_patch(Rectangle(
            (0.1, -0.35), 0.8, 0.25,  # Posición y tamaño del recuadro
            fill=False, edgecolor='#333333', linewidth=1.5, linestyle='-'
        ))

        # Ajuste de espacio vertical
        plt.subplots_adjust(bottom=0.4)

        # Interpretación más cerca de la tabla
        plt.figtext(
            0.5, -0.25,
            interpretacion,
            ha="center",
            fontsize=16,
            bbox={"facecolor": "whitesmoke", "edgecolor": "black", "boxstyle": "round,pad=0.5", "alpha": 0.8}
        )

        # Guardar imagen
        plt.savefig(f"statics/radar_{categoria.lower()}.png", dpi=300, bbox_inches="tight")
        plt.close()
      # Gráfico radar consolidado
    angulos_global = [n / float(len(categorias)) * 2 * pi for n in range(len(categorias))]
    angulos_global += angulos_global[:1]
    promedios_categorias.append(promedios_categorias[0])
    # tabla = {"Categoría": categorias, "Porcentaje": [f"{v*100:.1f}%" for v in promedios_categorias]}
    # tabla_df = pd.DataFrame(tabla)
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.fill(angulos_global, promedios_categorias, color="#90EE90", alpha=0.5)
    ax.plot(angulos_global, promedios_categorias, color="#2E8B57", linewidth=2.5)
    ax.set_xticks(angulos_global[:-1])
    ax.set_xticklabels(categorias, fontsize=14, fontweight='bold', color='#333333')
    ax.set_ylim(0, 1)
    ax.set_yticklabels([])
    #     # Agregar tabla debajo del gráfico
    # tabla_estilo = plt.table(
    #     cellText=tabla_df.values,
    #     colLabels=tabla_df.columns,
    #     cellLoc='center',
    #     loc='bottom',
    #     bbox=[-0.25, -1.05, 1.5, 0.8]
    # )
    # tabla_estilo.auto_set_font_size(False)
    # tabla_estilo.set_fontsize(12)
    # tabla_estilo.scale(1.5, 1.5)

    # # Estilo de la tabla
    # for (i, j), cell in tabla_estilo.get_celld().items():
    #     cell.set_edgecolor('grey')
    #     cell.set_linewidth(0.6)
    #     if i == 0:
    #         cell.set_facecolor('#E0F7FA')
    #         cell.set_text_props(weight='bold', color='#1E88E5')
    #     else:
    #         cell.set_facecolor('#ffffff' if i % 2 == 0 else '#f2f2f2')

    # # Ajuste de espacio vertical para acomodar la tabla
    # plt.subplots_adjust(bottom=0.3)
        

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

def agregar_pie_pagina(c, width, page_num):
    """Dibuja el número de página en la parte inferior."""
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawCentredString(width - 40, 30, f"Página {page_num}")       
     

def generar_pdf_con_analisis(usuario_id):
    """Genera un PDF con un análisis de las respuestas del usuario."""
    pdf_path = f"statics/analisis_usuario_{usuario_id}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    background_path = "statics/BKVITAL.PNG"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    page_num = 1
    # Dibujar imagen de fondo en la primera página
    agregar_fondo(c, width, height, background_path)
        # Obtener respuestas de la base de datos

    # Texto introductorio
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor("#2E4053"))
    c.drawCentredString(width / 2, height - 90, "Análisis de percepción de bienestar")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)

    # Definir estilo de párrafo justificado
    styles = getSampleStyleSheet()
    style = ParagraphStyle(
        "Justify",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        textColor=colors.black,
        leading=14,  # Espaciado entre líneas
        alignment=10,  # 4 = Justificado
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
    p = Paragraph(texto_intro, style)
    y_position = height - 120
    max_width = width - 100
    lineas_intro = simpleSplit(texto_intro, "Helvetica", 12, max_width)
   
    page_num += 1
    for linea in lineas_intro:
        c.drawString(50, y_position, linea)
        y_position -= 20
    c.showPage()
    # Dibujar imagen de fondo en la primera página
    agregar_fondo(c, width, height, background_path)
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

    for linea in lineas_interpretacion:
        c.drawString(100, y_position, linea)
        y_position -= 20  

    y_position -= 20
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#1F618D"))  # Color azul medio para subtítulos
    c.drawString(100, y_position, "Recomendaciones:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)  # Regresar a color negro para el contenido

    for recomendacion in recomendaciones:
        lineas_recomendacion = simpleSplit(recomendacion, "Helvetica", 12, max_width)
        for linea in lineas_recomendacion:
            c.drawString(120, y_position, linea)
            y_position -= 20
        y_position -= 10

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

    # Agregar nueva página para el gráfico general
    c.showPage()
    page_num += 1
    agregar_fondo(c, width, height, background_path)
    agregar_pie_pagina(c, width, page_num)

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor("#2E4053"))  # Título principal para gráficos
    c.drawCentredString(width / 2, height - 90, "Análisis General")

    image_path = "statics/radar_ambiental.png"
    margen_horizontal = 50
    margen_vertical = 100
    img_width = 300  # Ajustar ancho de imagen
    img_height = 300  # Ajustar alto de imagen
    x_position = (width - img_width) / 2
    y_position = height - margen_vertical - 60  # Bajar la posición inicial para evitar cortes
    c.drawImage(image_path, x_position, y_position - img_height, width=img_width, height=img_height)
            
    for categoria in ["Ambiental","vital", "emocional", "mental", "existencial", "financiera"]:
        image_path = f"statics/radar_{categoria}.png"
        if os.path.exists(image_path):
            c.showPage()
            page_num += 1
            agregar_fondo(c, width, height, background_path)
            agregar_pie_pagina(c, width, page_num)
            # Márgenes y ajustes
            margen_horizontal = 50
            margen_vertical = 100

            # Título centrado y más abajo
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(colors.HexColor("#1F618D"))  # Color azul medio para subtítulos
            titulo = f"Análisis - Salud {categoria.capitalize()}"
            titulo_width = c.stringWidth(titulo, "Helvetica-Bold", 16)
            c.drawCentredString(width / 2, height - margen_vertical, titulo)

            # Ajustar posiciones y tamaños con más espacio
            img_width = 300  # Ajustar ancho de imagen
            img_height = 300  # Ajustar alto de imagen
            x_position = (width - img_width) / 2
            y_position = height - margen_vertical - 60  # Bajar la posición inicial para evitar cortes

            # Dibujar gráfico centrado y más abajo
            c.drawImage(image_path, x_position, y_position - img_height, width=img_width, height=img_height)

        # Página de Plan de Acción
    c.showPage()
    page_num += 1
    agregar_fondo(c, width, height, background_path)
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