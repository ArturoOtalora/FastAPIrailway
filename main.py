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
import os
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import textwrap

# Configurar la conexión a MySQL desde Railway
DB_HOST = "shuttle.proxy.rlwy.net"
DB_USER = "root"
DB_PASSWORD = "umzzdISTaNglzBNhBcTqxNMamqkCUJfs"
DB_NAME = "railway"
DB_PORT = 17125


app = FastAPI()

app.mount("/statics", StaticFiles(directory="statics"), name="statics")

preguntas_lista = [
    "¿En qué medida consideras que tu alimentación te nutre adecuadamente?", "¿En qué medida realizas ejercicio físico al menos tres veces por semana?", "¿En qué medida tus hábitos de sueño te proporcionan un descanso óptimo?",
    "¿En qué medida has realizado chequeos médicos en los últimos seis meses?", "¿En qué medida tus hábitos diarios contribuyen a tu salud física?",
    "¿En qué medida tus experiencias pasadas han impulsado tu crecimiento personal?", "¿En qué medida las dificultades han mejorado tu calidad de vida?",
    "¿En qué medida celebras tus logros o victorias?", "¿En qué medida te adaptas a cambios o nuevas situaciones?",
    "¿En qué medida priorizas tu bienestar emocional?", "¿En qué medida experimentas sentimientos de impotencia o duda prolongados? (Invertida: Muy alto = negativo)",
    "¿En qué medida tu círculo cercano apoya tus metas?", "¿En qué medida te sientes agradecido por tus logros?",
    "¿En qué medida has evaluado tu salud mental con profesionales en los últimos seis meses?", "¿En qué medida te sientes valorado y respetado por otros?",
    "¿En qué medida tu autoimagen refleja tu valor como ser humano?", "¿En qué medida eres consciente del impacto positivo que aportas al mundo?",
    "¿En qué medida la pasión impulsa lo que haces actualmente?", "¿En qué medida tus pensamientos sostienen la vida que deseas tener?","¿En qué medida integras verdades personales difíciles en tu vida?","¿En qué medida ahorras al menos el 10% de tus ingresos mensuales?","¿En qué medida elaboras y sigues un presupuesto familiar?","¿En qué medida tienes inversiones a largo plazo para tu estabilidad económica?","¿En qué medida gestionas tus deudas sin afectar tu salud financiera?","¿En qué medida tus ahorros cubrirían gastos básicos por 3 a 6 meses?"
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
def generar_graficos_por_categoria(valores_respuestas):
    categorias = ["Vital", "Emocional", "Mental", "Existencial", "Financiera"]
    colores = ["red", "green", "blue", "purple", "orange"]
    valores = np.interp(valores_respuestas[:len(categorias)], (1, 10), (0, 1))  # Normalizar valores

    if len(valores) < len(categorias):
        print("Error: No hay suficientes respuestas para todas las categorías.")
        return

    angulos = [n / float(len(categorias)) * 2 * pi for n in range(len(categorias))]
    angulos.append(angulos[0])  # Cerrar la gráfica
    valores = np.append(valores, valores[0])  # Cerrar la gráfica con el primer valor

    interpretaciones = {
        "Vital": {
            "muy_bajo": "⚠️ Energía y vitalidad muy bajas. Es importante mejorar hábitos de sueño y alimentación.",
            "bajo": "🔄 Necesitas más actividad física y descanso adecuado.",
            "medio": "✅ Nivel aceptable, pero aún puedes optimizar tu bienestar físico.",
            "alto": "🌟 Te mantienes activo y con buena energía. ¡Sigue así!",
            "muy_alto": "🔥 Excelente estado físico y bienestar general."
        },
        "Emocional": {
            "muy_bajo": "⚠️ Estado emocional crítico. Considera buscar apoyo profesional.",
            "bajo": "🔄 Hay altibajos en tu estado emocional. Trabaja en tu inteligencia emocional.",
            "medio": "✅ Manejas bien tus emociones, pero aún puedes mejorar en resiliencia.",
            "alto": "🌟 Tienes un gran equilibrio emocional. Mantente atento a tu bienestar.",
            "muy_alto": "🔥 Fortaleza emocional sobresaliente. Inspiras a los demás."
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
        }
    } 

    for i, categoria in enumerate(categorias):
        fig = plt.figure(figsize=(6, 6), facecolor="white")  # Fondo del cuadrado en blanco
        ax = plt.subplot(111, polar=True)
        
        ax.set_facecolor("white")  # Fondo del gráfico en blanco
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)
        
        # Configuración de etiquetas en negro
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias, fontsize=12, fontweight="bold", color="black")

        # Configuración de la cuadrícula y bordes en gris claro
        ax.yaxis.grid(color="lightgray", linestyle="dashed", alpha=0.7)
        ax.spines["polar"].set_color("lightgray")

        # Resaltar la categoría actual
        valores_resaltados = np.zeros(len(valores) - 1)
        valores_resaltados[i] = valores[i]
        valores_resaltados = np.append(valores_resaltados, valores_resaltados[0])

        # Dibujar la gráfica con líneas en gris claro y área resaltada en azul claro
        ax.plot(angulos, valores, linewidth=1, linestyle='solid', color="gray", alpha=0.5)
        ax.fill(angulos, valores, 'gray', alpha=0.1)
        ax.plot(angulos, valores_resaltados, linewidth=2, linestyle='solid', color="blue")
        ax.fill(angulos, valores_resaltados, 'blue', alpha=0.3)

        # Determinar nivel e interpretación
        if valores[i] <= 0.2:
            nivel = "muy_bajo"
        elif valores[i] <= 0.4:
            nivel = "bajo"
        elif valores[i] <= 0.6:
            nivel = "medio"
        elif valores[i] <= 0.8:
            nivel = "alto"
        else:
            nivel = "muy_alto"

        interpretacion = interpretaciones[categoria][nivel]

        # Título alineado a la izquierda, fuera del gráfico
        plt.title(f"Perfil en {categoria}", fontsize=15, fontweight="bold", color="black", pad=40)

        # Agregar recomendación debajo del gráfico con ajuste para texto largo
        plt.figtext(
            0.5, -0.05,  # Ajuste en Y para evitar corte
            interpretacion, 
            ha="center", 
            fontsize=12, 
            fontweight="bold", 
            fontfamily="serif", 
            color="black",
            bbox={"facecolor": "whitesmoke", "edgecolor": "black", "boxstyle": "round,pad=0.5", "alpha": 0.8},
            wrap=True  # Ajuste para que no se corte el texto
        )

        # Guardar imagen con fondo blanco completo
        plt.savefig(f"statics/radar_{categoria.lower()}.png", transparent=False, dpi=300, facecolor="white", bbox_inches="tight")

        plt.close()

def generar_pdf_con_analisis(usuario_id):
    """Genera un PDF con un análisis de las respuestas del usuario."""
    pdf_path = f"statics/analisis_usuario_{usuario_id}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
     # Establecer fondo de pantalla más pequeño y con transparencia
    background_path = "statics/VITAL.png"
    
    if os.path.exists(background_path):
        img_width, img_height = width * 0.1, height * 0.1  # Reducir tamaño
        x_position = width - img_width - 10  # Ajustar margen derecho
        y_position = height - img_height - 10  # Ajustar margen superior
        c.drawImage(background_path, x_position, y_position, width=img_width, height=img_height, mask=[255, 255, 255, 255, 255, 255])
        # Obtener respuestas de la base de datos
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
        interpretacion = "puede experimentar cambios en el estado de ánimo por periodos de tiempo intermitente, llevándola a tener sensación de cansancio y malestar frente algunos acontecimientos de la vida diaria. Si bien puede reconocer tener cierta capacidad para enfrentar diferentes situaciones, esta persona puede experimentar sensaciones de impotencia y una consciencia moderada frente al sentido de vida, sin embargo, resalta la importancia de la integralidad del ser (cuerpo, mente, emociones y espíritu), aunque se le dificulta tomar acción para resolver determinados momentos de crisis. Su proceso de aprendizaje resulta más efectivo, debido a la capacidad de autorreflexión y la búsqueda de mejoras continuas."
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
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Análisis de tus Respuestas")

    c.setFont("Helvetica", 12)
    y_position = height - 100
    max_width = width - 150  
    lineas_interpretacion = simpleSplit(interpretacion, "Helvetica", 12, max_width)

    for linea in lineas_interpretacion:
        c.drawString(100, y_position, linea)
        y_position -= 20  
    
    y_position -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position, "Recomendaciones:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    
    for recomendacion in recomendaciones:
        lineas_recomendacion = simpleSplit(recomendacion, "Helvetica", 12, max_width)
        for linea in lineas_recomendacion:
            c.drawString(120, y_position, linea)
            y_position -= 20
        y_position -= 10

    # Saltar a una nueva página para los gráficos si no hay suficiente espacio
    c.showPage()    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Gráficos por Categoría")

    y_position = height - 100
    img_width = 250
    img_height = 250
    x_position = (width - img_width) / 2

    for categoria in ["vital", "emocional", "mental", "existencial", "financiera"]:
        image_path = f"statics/radar_{categoria}.png"
        if os.path.exists(image_path):
            if y_position - img_height < 50:
                c.showPage()  # Crear una nueva página si no hay suficiente espacio
                y_position = height - 100
                c.setFont("Helvetica-Bold", 16)
                c.drawString(100, height - 50, "Gráficos por Categoría")
            
            c.drawImage(image_path, x_position, y_position - img_height, width=img_width, height=img_height)
            y_position -= img_height + 20  # Espacio entre gráficos

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
