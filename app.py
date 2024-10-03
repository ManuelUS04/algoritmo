from flask import Flask, render_template, request, redirect, url_for, flash
import os
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'

# Aqui se asegura de que la carpeta uploads existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def procesar_urls(ruta_archivo):
    urls_filtradas = set()  # Aqui estoy usando set para evitar duplicados
    patron = re.compile(r'https?://(.*shop.*?)/.*\.html$')  # Se una la expresión regular para filtrar URLs

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            url = linea.strip()  # Se quita espacios en blanco alrededor de la línea
            if patron.match(url):  # Verificacmos si la URL coincide con el patrón
                urls_filtradas.add(url)  # Lo agregamos al set

    return urls_filtradas

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Aqui esta verificando si el archivo fue subido
        if 'archivo' not in request.files:
            return "No se subió ningún archivo", 400

        archivo = request.files['archivo']

        # Aqui se esta verificando si el archivo tiene un nombre válido
        if archivo.filename == '':
            return "No se seleccionó ningún archivo", 400

        # Aqui verificamos si el archivo cargado es de tipo .txt
        if not archivo.filename.endswith('.txt'):
            flash("Archivo no válido. Por favor sube un archivo .txt", "error")
            return redirect(request.url)
        
        # Ahora aqui se esta guardando el archivo en la carpeta uploads
        ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], archivo.filename)
        archivo.save(ruta_archivo)

        # Aqui procesamos el archivo subido al UPLOADS
        resultado = procesar_urls(ruta_archivo)
        total_urls = len(resultado)

        # Al final retornamos los resultados
        return render_template("index.html", resultado=resultado, total_urls=total_urls)

    return render_template("index.html", resultado=None)

if __name__ == "__main__":
    app.run(debug=True)
