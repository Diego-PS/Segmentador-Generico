import codecs
import PyPDF2
 
pdf = open('colunamista.pdf','rb')
 
leitor_pdf = PyPDF2.PdfReader(pdf)
 
texto = ''
for page in leitor_pdf.pages:
    texto += page.extract_text()

saida = codecs.open("colunamista.txt", "w", "utf-8")
saida.write(texto)