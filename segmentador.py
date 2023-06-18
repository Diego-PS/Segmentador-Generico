import codecs
import pdfplumber
import re
import json
import conversorParaTxt
import os
import time
import sys

def segmentadorDir (dir_pdf, dir_json):

    if not os.path.exists(dir_pdf):
        print(f"Caminho não existe: '{dir_pdf}'.")
        print(f"Por favor, informar o caminho completo com a entrada dos dados: {sys.argv[0]} --dir <caminho>")
        exit(2)

    arquivos = os.listdir(dir_pdf)
    for arquivo in arquivos:
        if arquivo.endswith('.pdf'):
            segmentador(dir_pdf + arquivo, dir_json)

class Segmento:
    def __init__(self, titulo, conteudo, numero_da_pagina = "", publicador = ""):
        self.titulo = titulo
        self.conteudo = conteudo
        self.numero_da_pagina = numero_da_pagina
        self.publicador = publicador

def converterParaDict (segmentos, numero, data_string, arquivo_pdf):
    
    segmentos_dicts = []
    
    for segmento in segmentos:
        seg_dict = {
            "materia" : segmento.titulo + segmento.conteudo,
            "page" : segmento.numero_da_pagina,
            "publicador" : segmento.publicador,
            "id" : "" 
        }
        segmentos_dicts.append(seg_dict)

    pref_bh_dict = {
        "Matérias" : segmentos_dicts
    }

    document_dict = {
        "origem" : arquivo_pdf,
        "diario": f"Diário Oficial do Município",
        "numero" : numero,
        "data" : data_string,
        "segmentos" : pref_bh_dict
    }

    return document_dict

def segmentador (arquivo_pdf, dir_json):

    start_time = time.time()
    print("Processando arquivo '" + arquivo_pdf + "'")

    if not os.path.exists(dir_json):
        os.makedirs(dir_json)

    arquivo_txt = conversorParaTxt.converterPDFtoTXT(arquivo_pdf)

    texto = open(arquivo_txt, encoding='utf-8').read()

    pdf = pdfplumber.open(arquivo_pdf)
    linhas_em_negrito = dict()
    lista_linhas_em_negrito = [
    'HOMOLOGAÇÃO',
    'RENOVAÇÃO DO REGISTRO',
    'ADJUDICAÇÃO', 
    'REGISTRO CADASTRAL – SUCAF',    
    'EXTRATO',
    'EXTRATOS',
    'EDITAL DE CIÊNCIA DE ELIMINAÇÃO',
    'RETIFICAÇÕES',
    'TORNAR SEM EFEITO',
    'TERMO DE APOSTILA',
    'RENOVAÇÃO DO REGISTRO CADASTRAL',
    'COMUNICADO',
    'EDITAL AUTOS EMITIDOS PELA',
    'JUNTA INTEGRADA DE',
    'PAUTA DE JULGAMENTO',
    'COMUNICADO DE',
    'ATO DO SECRETÁRIO',
    'ABERTURA DE LICITAÇÃO',
    'PROCESSO SELETIVO SIMPLIFICADO',
    'RESULTADO FINAL - HOMOLOGAÇÃO',
    'RECURSOS NÃO JULGADOS',
    'RETIRADOS DE PAUTA',
    'CONVOCAÇÃO PARA POSSE',
    'ATA DA SESSÃO PÚBLICA',
    'DESPACHOS DO SECRETÁRIO',
    'NOTIFICAÇÃO',
    'DISTRATO DE CONTRATO',
    'TERMO DE CONVALIDAÇÃO',
    'EXTRATOS DE CONTRATOS',
    'EXTRATOS DE TERMOS',
    'ADITIVOS DE CONTRATOS',
    'CONVOCAÇÃO PARA',
    'ATOS DO PREFEITO'
    ]

    for page in pdf.pages:
        clean_text = page.filter(lambda obj: obj['object_type'] == 'char' and 'Bold' in obj['fontname'])
        lista_linhas_em_negrito += clean_text.extract_text().split('\n')

    caixa_alta = set()
    caixa_baixa = set()

    for linha in lista_linhas_em_negrito:
        if ''.join(linha.split('º')).isupper():
            caixa_alta.add(linha)
        else:
            caixa_baixa.add(linha)

    linhas = texto.split('\n')
    
    # A última linha vai identificar o final do arquivo, nela um texto sem chance de aparecer no meio do arquivo
    linhas.append('これがファイルの終わりです')
    caixa_alta.add('これがファイルの終わりです')

    segmentos = []

    regex_formula = re.compile(r'.*Diário Oficial do Município[\s]?[\d]+[Poder Executivo]{0,15}')

    PDF_number_formula = re.compile(r'.*DOM Ano [LXVI]{2,6} . N\. [\d]\.[\d]{3}.*')

    page_number_formula = re.compile(r'Page number: [\d]*')

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

    try:
        numero_lista = numeros[:-3]
        dia, mes, ano = numeros[-3:]
        data_string = f'{dia} de {meses[mes]} de {ano}'
        numero = ''.join(numero_lista)
    except:
        numero = 'ERROR'
        data_string = 'ERROR'

    data_flag = False
    number_flag = False
    titulo = ''
    conteudo = ''
    page_number = '1'
    publicador = ''
    linha_anterior = ''

    for linha in linhas:

        if page_number_formula.match(linha) != None:
            page_number = linha[len(linha) - 2 :]
            if int(page_number) < 10:
                page_number = page_number[1]

        if linha in caixa_alta:

            if titulo and conteudo:
                segmentos.append(Segmento(titulo, conteudo, page_number, publicador))
                titulo = ''
                conteudo = ''
                publicador = ''

            titulo += linha + '\n'
        
        elif linha in caixa_baixa:

            publicador += linha_anterior + '\n'

        else:
            if number_flag == False:
                if PDF_number_formula.match(linha) != None:
                    PDF_number_extractor = linha.split()
                    numero = PDF_number_extractor[PDF_number_extractor.index("N.") + 1].translate(str.maketrans('', '','.'))
                    number_flag = True
            if linha[:55] == "Documento assinado digitalmente em consonância com a MP" or linha[:18] == "Poder Executivo" or regex_formula.match(linha) != None or page_number_formula.match(linha) != None:
                if regex_formula.match(linha) != None and data_flag == False:
                    date = linha.split()
                    data_string = ""
                    date[3] = date[3].title()
                    for i in range (1, 6):
                        data_string += date[i]
                        if i < 5:
                            data_string += " "
                    data_flag = True
                if not conteudo and len(segmentos) > 0:
                    ultimo_segmento = segmentos.pop()
                    titulo, conteudo, page_number, publicador = ultimo_segmento.titulo, ultimo_segmento.conteudo, ultimo_segmento.numero_da_pagina, ultimo_segmento.publicador
            else:
                if linha[:19] == "Hash da assinatura:":
                    continue
                else:
                    conteudo += linha + '\n'

        linha_anterior = linha

    if len(segmentos) == 0:
        segmentos.append(Segmento('', '\n'.join(linhas[:-1]), '', ''))
    document_dict = converterParaDict(segmentos, numero, data_string, arquivo_pdf)

    os.remove(arquivo_txt)
    json_file_name = dir_json + arquivo_pdf.split('/')[-1][:-4] + '.json'
    with codecs.open(json_file_name, "w", "utf-8") as outfile: 
        json.dump(document_dict, outfile, indent = 4, ensure_ascii=False)
    print("Processado - %.2f segundos" % (time.time() - start_time))