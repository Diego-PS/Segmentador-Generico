import codecs
import PyPDF2

def converterPDFtoTXT(file):

    pdf = open(file,'rb')
 
    leitor_pdf = PyPDF2.PdfReader(pdf)
 
    texto = ''
    for page in leitor_pdf.pages:
        texto += page.extract_text()
    
    txt_file_name = file[:len(file)-4] + ".txt"
    saida = codecs.open(txt_file_name, "w", "utf-8")
    saida.write(texto)

    return txt_file_name