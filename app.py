import gradio as gr
from pdf2docx import Converter
from docx import Document
from fpdf import FPDF
import os

title_and_description = """
# PDF to Word and Word to PDF converter
Created by [@artificialguybr](https://artificialguy.com)

Upload a PDF file to convert to Word or a Word file to convert to PDF.

## Features
- **Easy to use**: Simple interface to upload PDF or Word files and convert to the desired format.
- **High quality**: Converts while maintaining the best possible quality.
- **Efficient processing**: Uses `pdf2docx`, `fpdf` and `docx` for fast and reliable conversions.
- **Unlimited Use**: No file limit. Use unlimited!

Feel free to use in your own documents!
"""

def pdf_to_word(pdf_file):
    docx_filename = pdf_file.name.replace('.pdf', '.docx')
    
    cv = Converter(pdf_file.name)
    cv.convert(docx_filename, multi_processing=True, start=0, end=None)
    cv.close()
    
    return docx_filename

def word_to_pdf(docx_file):
    pdf_filename = "output.pdf"
    
    doc = Document(docx_file)
    pdf = FPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font('Arial', '', 'Arial.ttf', uni=True)
    pdf.set_font('Arial', size=12)

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:  # Ignorar linhas vazias
            continue
        # Quebrar o texto em várias linhas se necessário
        words = text.split()
        line = ''
        for word in words:
            if pdf.get_string_width(line + word) < (pdf.w - 2 * pdf.l_margin):
                line += word + ' '
            else:
                pdf.cell(0, 10, line, ln=True)
                line = word + ' '
        if line:
            pdf.cell(0, 10, line, ln=True)

    pdf.output(pdf_filename)
    return pdf_filename

with gr.Blocks() as app:
    gr.Markdown(title_and_description)
    
    with gr.Row():
        with gr.Column():
            with gr.Accordion("PDF to Word"):
                pdf_input = gr.File(label="Upload PDF")
                convert_pdf_to_word = gr.Button("Convert to Word")
                word_output = gr.File(label="Download Word file", type="filepath")
                
                convert_pdf_to_word.click(pdf_to_word, inputs=[pdf_input], outputs=[word_output])
                
        with gr.Column():
            with gr.Accordion("Word to PDF"):
                word_input = gr.File(label="Upload Word")
                convert_word_to_pdf = gr.Button("Convert to PDF")
                pdf_output = gr.File(label="Download PDF file", type="filepath")
                
                convert_word_to_pdf.click(word_to_pdf, inputs=[word_input], outputs=[pdf_output])

app.launch()
