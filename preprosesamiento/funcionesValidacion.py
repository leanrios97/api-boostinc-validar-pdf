import os  # Importa el módulo os para trabajar con el sistema de archivos.
import PyPDF2  # Importa PyPDF2 para el procesamiento de archivos PDF.
import nltk  # Importa la biblioteca nltk para el procesamiento de lenguaje natural.
from nltk.corpus import stopwords  # Importa la lista de stopwords de nltk.
import re  # Importa el módulo re para expresiones regulares.
from unidecode import unidecode  # Importa unidecode para normalizar palabras.
import pandas as pd  # Importa pandas para trabajar con datos tabulares.
import spacy  # Importa Spacy para el procesamiento de lenguaje natural.
from spacy.language import Language  # Importa Language de Spacy.
from spacy_langdetect import LanguageDetector  # Importa el detector de idioma de spacy-langdetect.
import base64  # Importa base64 para la codificación y decodificación en base64.
import io 


# Función para codificar un archivo PDF a base64
def encode_pdf_to_base64(pdf_path):
    import base64  # Importa base64 para la codificación y decodificación en base64.
    
    try:
        with open(pdf_path, 'rb') as pdf_file:  # Abre el archivo PDF en modo lectura binaria.
            pdf_bytes = pdf_file.read()  # Lee el contenido del archivo PDF.
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')  # Codifica el contenido en base64.
            return pdf_base64  # Devuelve el contenido codificado en base64.
    except Exception as e:
        return None  # En caso de error, devuelve None.

# Función para agregar un detector de idioma a Spacy
def language_detector(nlp, name):
    return LanguageDetector()  # Devuelve un detector de idioma para Spacy.

# Función para contar coincidencias de palabras clave "lorem ipsum"
def lorem_matches(text):
    matches = [word for word in text.split() if re.match(r'lorem ipsum|loremipsum|lorem|ipsum|amet|etiam|quis', word, re.IGNORECASE)]
    return len(matches)  # Devuelve el número de coincidencias encontradas.

# Función para contar coincidencias de palabras ofensivas
def dirty_matches(text):
    df = pd.read_csv("preprosesamiento/data/bad_words_es.csv")["word"].apply(lambda x: unidecode(x))  # Lee una lista de palabras ofensivas.
    bad_words = list(df)  # Crea una lista de palabras ofensivas normalizadas.
    matches = [word for word in text.split() if re.match("|".join(bad_words), unidecode(word), re.IGNORECASE)]  # Busca coincidencias con palabras ofensivas.
    return len(matches)  # Devuelve el número de coincidencias encontradas.

# Función para contar enlaces web en el texto
def enlaces_web(text):
    matches = re.findall(r'(http[s]?://|www.)\S+', text)  # Busca enlaces web utilizando una expresión regular.
    return len(matches)  # Devuelve el número de enlaces encontrados.

# Descargar stopwords en español
nltk.download('stopwords')  # Descarga la lista de stopwords en español.
stopwords = stopwords.words('spanish') + ["-", ")", "(", "``", "''", ":", "?", "'", ";", "/"]  # Agrega stopwords adicionales.

# Cargar modelo de lenguaje en_core_web_sm y agregar el detector de idioma a Spacy
nlp = spacy.load("en_core_web_sm")  # Carga el modelo de lenguaje en_core_web_sm de Spacy.
Language.factory("language_detector", func=language_detector)  # Crea un detector de idioma personalizado.
nlp.add_pipe('language_detector', last=True)  # Agrega el detector de idioma a Spacy como último paso.

# Función principal
def validacion(pdf_base64):
    pdf_bytes = base64.b64decode(pdf_base64)  # Decodifica el archivo PDF en base64.

    # Crear un objeto StringIO a partir de los bytes del PDF
    pdf_stream = io.BytesIO(pdf_bytes)  # Crea un objeto StringIO con los bytes del PDF.

    pdf_reader = PyPDF2.PdfReader(pdf_stream)  # Lee el PDF con PyPDF2.

    text = ""  # Inicializa una variable para almacenar el texto del PDF.

    num_pages = len(pdf_reader.pages)  # Obtiene el número de páginas del PDF.

    if num_pages == 0:
        return {"Estado":False, "Messague":"El documento está vacío."}  # Si el documento está vacío, devuelve falso y un mensaje.

    for i in range(num_pages):
        page = pdf_reader.pages[i]  # Obtiene una página del PDF.
        text += page.extract_text()  # Extrae el texto de la página y lo agrega a la variable de texto.

    patron = r'\n+|\s+'
    text = re.sub(patron, ' ', text)  # Normaliza el texto, reemplazando saltos de línea y espacios múltiples por un solo espacio.

    if len(text.split()) < 350:
        return {"Estado":False, "Messague":"Archivo muy corto."}  # Si el texto es demasiado corto, devuelve falso y un mensaje.

    ipsum_words = lorem_matches(text)  # Llama a la función para contar coincidencias de palabras clave "lorem ipsum".

    if ipsum_words > 10:
        return {"Estado":False, "Messague":"Archivo potencialmente autogenerado."}  # Si hay demasiadas coincidencias, devuelve falso y un mensaje.

    dirty_words = dirty_matches(text)  # Llama a la función para contar coincidencias de palabras ofensivas.

    if dirty_words > 10:
        return {"Estado":False, "Messague":"Archivo potencialmente agresivo."}  # Si hay demasiadas coincidencias de palabras ofensivas, devuelve falso y un mensaje.

    enlaces_web_count = enlaces_web(text)  # Llama a la función para contar enlaces web en el texto.

    if enlaces_web_count > 0:
        return {"Estado":False, "Messague":"Archivo contiene un enlace a externo, por favor remover." } # Si hay enlaces web, devuelve falso y un mensaje.

    doc = nlp(text)  # Tokeniza el texto con Spacy.

    if doc._.language["language"] != "es" and doc._.language["language"] != "en":
        return {"Estado":False, "Messague":"El idioma del archivo debe ser Español o Inglés"}  # Si el idioma no es español ni inglés, devuelve falso y un mensaje.

    return {"Estado":True, "Messague":"Documento valido."}  # Si todas las comprobaciones son satisfactorias, devuelve verdadero y un mensaje de "Válido".