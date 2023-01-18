import codecs
import pdfplumber
import re

arquivo = 'texto.txt'
texto = open(arquivo, encoding='utf-8').read()

class Segmento:
    def __init__(self, titulo, conteudo):
        self.titulo = titulo
        self.conteudo = conteudo

pdf = pdfplumber.open('diariobh.pdf')
linhas_em_negrito = dict()
lista_linhas_em_negrito = []

for page in pdf.pages:
    clean_text = page.filter(lambda obj: obj['object_type'] == 'char' and 'Bold' in obj['fontname'])
    lista_linhas_em_negrito += clean_text.extract_text().split('\n')

caixa_alta = dict()
caixa_baixa = dict()
for linha in lista_linhas_em_negrito:
    if linha.isupper():
        if linha not in caixa_alta:
            caixa_alta[linha] = 0
        caixa_alta[linha] += 1
    else:
        if linha not in caixa_baixa:
            caixa_baixa[linha] = 0
        caixa_baixa[linha] += 1

linhas = texto.split('\n')

segmentos = []

titulo = ''
conteudo = ''

saida = codecs.open("saida.txt", "w", "utf-8")

t = re.compile(r'.*Diário Oficial do Município[\d]+$')

primeira_linha, segunda_linha = linhas[:2]
linhas = linhas[2:]

numeros = re.findall(r'[0-9]+', segunda_linha)

meses = {
    '1' : 'Janeiro',
    '2' : 'Fevereiro',
    '3' : 'Março',
    '4' : 'Abril',
    '5' : 'Maio',
    '6' : 'Junho',
    '7' : 'Julho',
    '8' : 'Agosto',
    '9' : 'Setembro',
    '10' : 'Outubro',
    '11' : 'Novembro',
    '12' : 'Dezembro'
}

numero_lista = numeros[:-3]
dia, mes, ano = numeros[-3:]
data_string = f'{dia} de {meses[mes]} de {ano}'
numero = ''.join(numero_lista)

for linha in linhas:
    
    if linha in caixa_alta:

        caixa_alta[linha] -= 1
        if caixa_alta[linha] == 0:
            del caixa_alta[linha]

        if titulo and conteudo:
            segmentos.append(Segmento(titulo, conteudo))
            titulo = ''
            conteudo = ''

        titulo += linha + '\n'
    else:

        if linha[:55] == "Documento assinado digitalmente em consonância com a MP" or linha[:18] == "Poder Executivo" or t.match(linha) != None:
            if not conteudo:    
                ultimo_segmento = segmentos.pop()
                titulo, conteudo = ultimo_segmento.titulo, ultimo_segmento.conteudo
        else:
            if linha[:19] == "Hash da assinatura:":
                continue
            else:
                conteudo += linha + '\n'
                

for segmento in segmentos:
    saida.write('___________________________________________________________\n')
    saida.write(segmento.titulo)
    saida.write('-----------------------------------------------------------\n')
    saida.write(segmento.conteudo)
    saida.write('___________________________________________________________\n')

segmentos_dicts = []
for segmento in segmentos:
    seg_dict = {
        "materia" : segmento.conteudo,
        "page" : "",
        "publicador" : "",
        "id" : "" 
    }
    segmentos_dicts.append(seg_dict)

pref_bh_dict = {
    "PREFEITURA DE BELO HORIZONTE" : segmentos_dicts
}

document_dict = {
    "origem" : "diariobh.pdf",
    "diario": "Diário Oficial de Belo Horizonte",
    "numero" : numero,
    "data" : data_string,
    "segmentos" : pref_bh_dict
}