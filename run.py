import fitz  # PyMuPDF
import random
import string
import stanza
import re


class Redactor:

    def __init__(self, path):
        self.path = path
        self.nlp = stanza.Pipeline('tr', processors='tokenize,ner')

    @staticmethod
    def random_string(length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))

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


        doc.save('redacted.pdf')
        print("Successfully redacted")


if __name__ == "__main__":
    path = 'input_pdfs/Gerekceli-karar-1.pdf'
    redactor = Redactor(path)
    redactor.redaction()
