# Data Masking in PDFs using NLP and Regex
# PDF Redaction Automation

## Overview

This project automates the redaction of sensitive information in PDF files. It processes PDFs to obscure sensitive data and saves the redacted versions in a specified output folder. The redaction is achieved through a combination of natural language processing (NLP) and regular expressions to identify and replace sensitive information.

## Project Structure

- **`input_pdfs/`**: Contains the original PDF files that need to be redacted.
  - Example: `input_pdfs/Gerekceli-karar-1.pdf`
  
- **`output_pdfs/`**: Will hold the redacted PDF files. The filenames will include a `_redacted` suffix.
  - Example: `output_pdfs/Gerekceli-karar-1_redacted.pdf`
  
- **`run.py`**: The main script for processing PDFs. It reads from `input_pdfs`, applies redactions, and saves the results to `output_pdfs`.
  
- **`requirements.txt`**: Lists the required Python libraries for the project.

## Main Aim

- **Sensitive Data Redaction**: Automatically redact sensitive information (e.g., personal identifiers and numbers) from PDFs.
  
- **Automation**: Streamline the redaction process for multiple PDFs, ensuring consistency and efficiency.
  
- **Output Management**: Save redacted PDFs with a clear naming convention for easy identification.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
