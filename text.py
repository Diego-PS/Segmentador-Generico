import codecs
import PyPDF2

def converterPDFtoTXT(file):

    pdf = open(file,'rb')
 
    leitor_pdf = PyPDF2.PdfReader(pdf)
 
    texto = ''
    for page in leitor_pdf.pages:
        texto += page.extract_text()

    saida = codecs.open("./Textos/"+ file[:len(file)-4] + ".txt", "w", "utf-8")
    saida.write(texto)


converterPDFtoTXT("diariobh.pdf")