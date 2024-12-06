import fitz  # PyMuPDF
import random
import string
import spacy
import re
import os

class Redactor:
    def __init__(self, path):
        self.path = path
        self.nlp = spacy.load("tr_core_news_lg")

    @staticmethod
    def random_string(length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def random_number(length):
        return ''.join(random.choice(string.digits) for _ in range(length))


    def get_text_info(self, page):
        text_info = []
        blocks = page.get_text("dict")["blocks"]

        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        text_info.append({
                            "text": s["text"],
                            "bbox": s["bbox"],
                            "font_size": s["size"]
                        })
        return text_info

    def redaction(self):
        doc = fitz.open(self.path)

        for page in doc:
            page.wrap_contents()
            text_info = self.get_text_info(page)

            for info in text_info:
                text = info["text"]
                if self.is_sensitive_data(text):
                    bbox = info["bbox"]
                    original_font_size = info["font_size"]

                    # Redaksiyon alanını oluştur
                    rect = fitz.Rect(bbox)

                    # Yeni metin oluştur
                    if text.isdigit():
                        replacement_text = self.random_number(len(text))
                    else:
                        replacement_text = self.random_string(len(text))

                    # İlk redaksiyon - temizleme
                    annot = page.add_redact_annot(rect)
                    page.apply_redactions()

                    # İkinci redaksiyon - yeni metin
                    annot = page.add_redact_annot(
                        rect,
                        text=replacement_text,
                        fontname="Helvetica",
                        fontsize=original_font_size,
                        text_color=(0, 0, 0),
                        fill=(1, 1, 1),
                        align=fitz.TEXT_ALIGN_LEFT
                    )
                    page.apply_redactions()

        return doc
    
    def is_sensitive_data(self, text):
        """Hassas veri kontrolü - daha seçici"""
        # Çok kısa metinleri atla
        if len(text.strip()) < 2:
            return False

        doc = self.nlp(text.strip())
        sensitive_data = []

        for ent in doc.ents:
            if ent.label_ in ["GPE", "ORG", "NORP", "TITLE", "PERSON", "EVENT", "PRODUCT"]:
                sensitive_data.append(ent.text)

        numbers = re.findall(r'\b\d+\b', text)
        sensitive_data.extend(numbers)

        return sensitive_data

def process_pdfs(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            input_path = os.path.join(input_folder, filename)
            output_filename = filename.replace('.pdf', '_redacted.pdf')
            output_path = os.path.join(output_folder, output_filename)

            print(f"Processing {input_path}...")

            redactor = Redactor(input_path)
            doc = redactor.redaction()

            doc.save(output_path)
            print(f"Saved redacted PDF to {output_path}")

if __name__ == "__main__":
    input_folder = 'input_pdfs'
    output_folder = 'output_pdfs'
    process_pdfs(input_folder, output_folder)
