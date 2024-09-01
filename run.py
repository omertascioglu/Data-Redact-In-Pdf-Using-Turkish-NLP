import fitz  # PyMuPDF
import random
import string
import stanza
import re
import os

class Redactor:

    def __init__(self, path):
        self.path = path
        self.nlp = stanza.Pipeline('tr', processors='tokenize,ner')

    @staticmethod
    def random_string(length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def random_number(length):
        return ''.join(random.choice(string.digits) for _ in range(length))

    def get_sensitive_data(self, text):
        doc = self.nlp(text)
        sensitive_data = []

        for sentence in doc.sentences:
            for ent in sentence.ents:
                sensitive_data.append(ent.text)

        numbers = re.findall(r'\b\d+\b', text)
        sensitive_data.extend(numbers)

        return sensitive_data

    def redaction(self):
        doc = fitz.open(self.path)

        for page in doc:
            page.wrap_contents()
            text = page.get_text("text")

            sensitive_data = self.get_sensitive_data(text)

            for data in sensitive_data:
                areas = page.search_for(data)

                if data.isdigit():
                    replacement_text = self.random_number(len(data))
                else:
                    replacement_text = self.random_string(len(data))

                for area in areas:
                    page.add_redact_annot(area, fill=(1, 1, 1))
                    page.apply_redactions()

                    page.add_redact_annot(area, text=replacement_text, fill=(1, 1, 1), align=fitz.TEXT_ALIGN_JUSTIFY,
                                          fontsize=46)
                    page.apply_redactions()

        return doc

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
