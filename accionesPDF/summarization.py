import base64
import io
import re
import textwrap
from deep_translator import GoogleTranslator
from transformers import pipeline
import PyPDF2
import spacy
from spacy_langdetect import LanguageDetector
import random
from spacy.language import Language
import string

class SummarizePDF:
    def __init__(self, max_summary_length=500, min_summary_length=250):
        self.summarizer = pipeline('summarization')
        self.max_summary_length = max_summary_length
        self.min_summary_length = min_summary_length
        #self.target_language = "en"
        #self.translate_to_spanish = GoogleTranslator(source="auto",target="es")
        #self.translate_to_englsih = GoogleTranslator(source="auto",target="es")
        self.nlp = spacy.load("en_core_web_sm")

    def _get_lang_detector(self, nlp, name):
        return LanguageDetector()

    def _language_detector(self,text):
        language_detector_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        Language.factory(language_detector_name, func=self._get_lang_detector)
        self.nlp.add_pipe(language_detector_name, last=True)
        text = self.nlp(text)
        return text._.language["language"]

    def decode_pdf(self, pdf_base64):
        pdf_bytes = base64.b64decode(pdf_base64)
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_stream)
        text = " ".join(page.extract_text() for page in pdf_reader.pages)
        text = re.sub(r'\n+|\s+', ' ', text)
        return text

    def detect_language(self, text):
        doc = self.nlp(text)
        return doc._.language["language"]

    def translate(self, text, source_language, target_language):
        translator = GoogleTranslator(source=source_language, target=target_language)
        translated_text=translator.translate(text)
        return translated_text

    def translate_and_summarize(self, pdf_base64):

        text = self.decode_pdf(pdf_base64)

        detected_language = self._language_detector(text)

        if detected_language != "en":
            translated_text = self.translate(text, detected_language, "en")
        else:
            translated_text = text

        wrapped_text = textwrap.fill(translated_text, replace_whitespace=False, fix_sentence_endings=True)
        summarized_text = self.summarizer(wrapped_text, max_length=self.max_summary_length, min_length=self.min_summary_length, do_sample=False)[0]["summary_text"]

        if detected_language != "en":

            summarized_text = self.translate(summarized_text, "en", detected_language)

        return summarized_text

# Ejemplo de uso
if __name__ == "__main__":
    sm = SummarizePDF(max_summary_length=500, min_summary_length=250)