import codecs
import PyPDF2
 
pdf = open('diariobh.pdf','rb')
 
leitor_pdf = PyPDF2.PdfReader(pdf)
 
texto = ''
for page in leitor_pdf.pages:
    texto += page.extract_text()

saida = codecs.open("texto.txt", "w", "utf-8")
saida.write(texto)