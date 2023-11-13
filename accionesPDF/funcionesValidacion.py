import spacy
import pandas as pd
from unidecode import unidecode
import base64
import PyPDF2
import re
import string
import random
from spacy_langdetect import LanguageDetector
from spacy.language import Language
import io


class PDFValidator:

    def __init__(self):
        # Cargamos el modelo de lenguaje en español de SpaCy
        self.nlp = spacy.load("es_core_news_sm")
        # Inicializamos la lista de palabras ofensivas
        self._bad_words = self._load_badwords()
        # Inicializamos la variable para el contenido del PDF
        self.pdf = None

    def _load_badwords(self, bad_words_path="bad_words_es.csv"):
        try:
            # Lee el archivo CSV que contiene las palabras ofensivas
            df = pd.read_csv(bad_words_path)
            # Normaliza las palabras ofensivas
            bad_words = [unidecode(word) for word in df["word"]]
            return bad_words
        except Exception as e:
            print(f"Error loading bad words: {e}")
            return []

    def _get_lang_detector(self, nlp, name):
        # Crea un detector de idioma personalizado para SpaCy
        return LanguageDetector()

    def _language_detector(self):
        # Genera un nombre aleatorio para el detector de idioma personalizado
        language_detector_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        # Crea y agrega el detector de idioma personalizado a SpaCy
        Language.factory(language_detector_name, func=self._get_lang_detector)
        self.nlp.add_pipe(language_detector_name, last=True)
        # Procesa el texto del PDF y detecta el idioma
        doc = self.nlp(self.pdf)
        return doc._.language["language"]

    def _decode_pdf(self, pdf_base64):
        # Decodifica el archivo PDF en base64
        pdf_bytes = base64.b64decode(pdf_base64)
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_stream)
        text = ""
        # Extrae el texto de cada página del PDF
        for page in pdf_reader.pages:
            text += page.extract_text()
        # Normaliza el texto, reemplazando saltos de línea y espacios múltiples por un solo espacio
        text = re.sub(r'\n+|\s+', ' ', text)
        return text

    def _calculate_word_count(self):
        # Calcula la cantidad de palabras en el PDF
        return len(self.pdf.split())

    def _calculate_lorem_matches(self):
        # Cuenta las coincidencias de palabras clave "lorem ipsum" en el PDF
        matches = [word for word in self.pdf.split() if re.match(r'lorem ipsum|loremipsum|lorem|ipsum|amet|etiam|quis', word, re.IGNORECASE)]
        return len(matches)

    def _calculate_dirty_matches(self):
        # Cuenta las coincidencias de palabras ofensivas en el PDF
        matches = [word for word in self.pdf.split() if re.match("|".join(self._bad_words), unidecode(word), re.IGNORECASE)]
        return len(matches)

    def _calculate_web_links(self):
        # Cuenta los enlaces web en el texto del PDF
        matches = re.findall(r'(http[s]?://|www.)\S+', self.pdf)
        return len(matches)

    def validate_pdf(self, pdf_base64):
        # Decodifica el PDF en base64
        self.pdf = self._decode_pdf(pdf_base64)

        if not self.pdf:
            return False, "El documento está vacío."

        num_words = self._calculate_word_count()
        if num_words < 350:
            return False, "Archivo muy corto."

        num_lorem_matches = self._calculate_lorem_matches()
        if num_lorem_matches > 10:
            return False, "Archivo potencialmente autogenerado."

        num_dirty_matches = self._calculate_dirty_matches()
        if num_dirty_matches > 10:
            return False, "Archivo potencialmente agresivo."

        num_web_links = self._calculate_web_links()
        if num_web_links > 0:
            return False, "Archivo contiene enlaces web."

        language = self._language_detector()
        if language not in ["es", "en"]:
            return False, "El idioma del archivo debe ser Español o Inglés."

        return True, "Válido"

if __name__ == "__main__":
    vl = PDFValidator()