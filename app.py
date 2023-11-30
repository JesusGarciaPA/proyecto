from flask import Flask, render_template, request
import pandas as pd
from statistics import mode, median
from scipy.stats import mode

app = Flask(__name__)

def leer_contenido_archivo(archivo_excel):
    try:
        df = pd.read_excel(archivo_excel)
        contenido = df.to_html()
        return contenido
    except Exception as e:
        return f"Error al leer el archivo: {str(e)}"

def calcular_suma_columna(archivo_excel, nombre_columna):
    df = pd.read_excel(archivo_excel)
    suma = df[nombre_columna].sum()
    return suma

def calcular_estadisticas(archivo_excel, nombre_columna):
    df = pd.read_excel(archivo_excel)

    # Calcular la media
    media = df[nombre_columna].mean()

    # Calcular la moda (puede haber más de una moda)
    modas = df[nombre_columna].mode()

    # Si hay múltiples modas, se devuelve una lista; de lo contrario, se devuelve el valor único.
    moda = modas.values.tolist() if not modas.empty else None

    # Calcular la mediana
    mediana = df[nombre_columna].median()

    return media, moda, mediana


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verificar si se envió un archivo
        if 'archivo' not in request.files:
            return render_template('index.html', error='No se ha proporcionado ningún archivo.')

        archivo = request.files['archivo']

        # Verificar si el archivo tiene un nombre
        if archivo.filename == '':
            return render_template('index.html', error='No se ha proporcionado ningún archivo.')

        # Verificar si el archivo es de tipo Excel
        if not archivo.filename.endswith('.xlsx'):
            return render_template('index.html', error='El archivo debe ser de tipo Excel (.xlsx).')

        # Obtener el nombre de la columna para calcular estadísticas
        nombre_columna = request.form.get('columna')

        # Verificar si se proporcionó un nombre de columna
        if not nombre_columna:
            return render_template('index.html', error='Ingrese un nombre de columna para calcular estadísticas.')

        # Calcular las estadísticas y mostrar los resultados
        contenido_archivo = leer_contenido_archivo(archivo)
        suma = calcular_suma_columna(archivo, nombre_columna)
        media, moda, mediana = calcular_estadisticas(archivo, nombre_columna)
        return render_template('index.html',contenido_archivo=contenido_archivo, suma=suma, media=media, moda=moda, mediana=mediana)

    return render_template('index.html')

@app.route('/diagrama')
def venn():
    return render_template("diagrama.html")

@app.route('/modelo')
def entidad():
    return render_template("modelo.html")

if __name__ == '__main__':
    app.run(debug=True)
