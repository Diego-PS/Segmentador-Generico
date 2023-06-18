import codecs
import PyPDF2

def converterPDFtoTXT(file):

    pdf = open(file,'rb')
 
    leitor_pdf = PyPDF2.PdfReader(pdf)
 
    texto = ''
    numero_da_pagina = 1

    #Adicionamos em cada página o número da página, para ser inserido no campo correto durante a segmentação
    #e passamos o conteúdo extraído do PDF para uma variável
    for page in leitor_pdf.pages:
        texto += "\nPage number: " + str(numero_da_pagina) + '\n'
        texto += page.extract_text()
        numero_da_pagina += 1
    
    txt_file_name = file[:len(file)-4] + ".txt"

    #Lista dos Iniciadores em caixa cinza que aparecem incorretamente em alguns DOs
    iniciadoresNegrito = [
'GABINETE DO PREFEITO',
'SECRETARIA MUNICIPAL \nDE GOVERNO',
'SECRETARIA MUNICIPAL\nDE GOVERNO',
'SECRETARIA MUNICIPAL DE\nPLANEJAMENTO, ORÇAMENTO E\nINFORMAÇÃO',
'PROCURADORIA-GERAL \nDO MUNICÍPIO',
'PROCURADORIA-GERAL\nDO MUNICÍPIO',
'CONTROLADORIA-GERAL \nDO MUNICÍPIO',
'CONTROLADORIA-GERAL\nDO MUNICÍPIO',
'SECRETARIA MUNICIPAL \nDE FINANÇAS',
'SECRETARIA MUNICIPAL\nDE FINANÇAS',
'SECRETARIA MUNICIPAL \nDE POLÍTICAS SOCIAIS',
'SECRETARIA MUNICIPAL\nDE POLÍTICAS SOCIAIS',
'SECRETARIA MUNICIPAL \nDE EDUCAÇÃO',
'SECRETARIA MUNICIPAL\nDE EDUCAÇÃO',
'SECRETARIA MUNICIPAL \nDE SAÚDE',
'SECRETARIA MUNICIPAL\nDE SAÚDE',
'SECRETARIA MUNICIPAL \nDE POLÍTICAS URBANAS',
'SECRETARIA MUNICIPAL\nDE POLÍTICAS URBANAS',
'SECRETARIA MUNICIPAL DE \nPOLÍTICA URBANA',
'SECRETARIA MUNICIPAL DE\nPOLÍTICA URBANA',
'SECRETARIA MUNICIPAL \nDO MEIO AMBIENTE',
'SECRETARIA MUNICIPAL\nDO MEIO AMBIENTE',
'SECRETARIA MUNICIPAL \nDE MEIO AMBIENTE',
'SECRETARIA MUNICIPAL\nDE MEIO AMBIENTE',
'SECRETARIA MUNICIPAL \nDE SEGURANÇA URBANA \nE PATRIMONIAL',
'SECRETARIA MUNICIPAL\nDE SEGURANÇA URBANA \nE PATRIMONIAL',
'SECRETARIA MUNICIPAL \nDE SEGURANÇA URBANA\nE PATRIMONIAL',
'SECRETARIA MUNICIPAL\nDE SEGURANÇA URBANA\nE PATRIMONIAL',
'SECRETARIA MUNICIPAL DE \nPLANEJAMENTO, ORÇAMENTO \nE GESTÃO',
'SECRETARIA MUNICIPAL DE\nPLANEJAMENTO, ORÇAMENTO \nE GESTÃO',
'SECRETARIA MUNICIPAL DE \nPLANEJAMENTO, ORÇAMENTO\nE GESTÃO',
'SECRETARIA MUNICIPAL DE\nPLANEJAMENTO, ORÇAMENTO\nE GESTÃO',
'SECRETARIA MUNICIPAL \nDE FAZENDA',
'SECRETARIA MUNICIPAL\nDE FAZENDA',
'SECRETARIA MUNICIPAL DE \nDESENVOLVIMENTO \nECONÔMICO',
'SECRETARIA MUNICIPAL DE\nDESENVOLVIMENTO \nECONÔMICO',
'SECRETARIA MUNICIPAL DE \nDESENVOLVIMENTO\nECONÔMICO',
'SECRETARIA MUNICIPAL DE\nDESENVOLVIMENTO\nECONÔMICO',
'SECRETARIA MUNICIPAL \nDE DESENVOLVIMENTO',
'SECRETARIA MUNICIPAL\nDE DESENVOLVIMENTO',
'SECRETARIA MUNICIPAL \nDE OBRAS E INFRAESTRUTURA',
'SECRETARIA MUNICIPAL\nDE OBRAS E INFRAESTRUTURA',
'SECRETARIA MUNICIPAL DE \nOBRAS E INFRAESTRUTURA',
'SECRETARIA MUNICIPAL DE\nOBRAS E INFRAESTRUTURA',
'SECRETARIA MUNICIPAL DE \nPOLÍTICA URBANA',
'SECRETARIA MUNICIPAL DE\nPOLÍTICA URBANA',
'SECRETARIA MUNICIPAL \nDE POLÍTICAS URBANAS',
'SECRETARIA MUNICIPAL\nDE POLÍTICAS URBANAS',
'SECRETARIA MUNICIPAL DE \nSERVIÇOS URBANOS',
'SECRETARIA MUNICIPAL DE\nSERVIÇOS URBANOS',
'SECRETARIA MUNICIPAL DE \nSEGURANÇA E PREVENÇÃO',
'SECRETARIA MUNICIPAL DE\nSEGURANÇA E PREVENÇÃO',
'SECRETARIA MUNICIPAL DE \nASSISTÊNCIA SOCIAL, SEGURANÇA \nALIMENTAR E CIDADANIA',
'SECRETARIA MUNICIPAL DE\nASSISTÊNCIA SOCIAL, SEGURANÇA \nALIMENTAR E CIDADANIA',
'SECRETARIA MUNICIPAL DE \nASSISTÊNCIA SOCIAL, SEGURANÇA\nALIMENTAR E CIDADANIA',
'SECRETARIA MUNICIPAL DE\nASSISTÊNCIA SOCIAL, SEGURANÇA\nALIMENTAR E CIDADANIA',
'SECRETARIA MUNICIPAL DE \nASSUNTOS INSTITUCIONAIS E \nCOMUNICAÇÃO SOCIAL',
'SECRETARIA MUNICIPAL \nDE CULTURA',
'SECRETARIA MUNICIPAL\nDE CULTURA',
'SECRETARIA MUNICIPAL \nDE ESPORTES E LAZER',
'SECRETARIA MUNICIPAL\nDE ESPORTES E LAZER',
'SECRETARIA MUNICIPAL DE \nESPORTES E LAZER',
'SECRETARIA MUNICIPAL DE\nESPORTES E LAZER',
'CONTROLADORIA-GERAL \nDO MUNICÍPIO',
'CONTROLADORIA-GERAL\nDO MUNICÍPIO',
'SECRETARIA DE ADMINISTRAÇÃO \nREGIONAL MUNICIPAL \nCENTRO-SUL',
'SECRETARIA DE ADMINISTRAÇÃO \nREGIONAL MUNICIPAL \nBARREIRO',
'SECRETARIA DE ADMINISTRAÇÃO \nREGIONAL MUNICIPAL \nLESTE',
'SECRETARIA DE ADMINISTRAÇÃO \nREGIONAL MUNICIPAL \nNORDESTE',
'SECRETARIA DE ADMINISTRAÇÃO \nREGIONAL MUNICIPAL \nNOROESTE',
'SECRETARIA DE ADMINISTRAÇÃO \nREGIONAL MUNICIPAL \nPAMPULHA',
'BELOTUR',
'CDPCM',
'BEPREM',
'BHTRANS',
'SLU',
'COMAM',
'PRODABEL',
'SUDECAP',
'COMPUR',
'COMUSA',
'URBEL',
'BELO HORIZONTE\n'
]
    
    #Imprimimos o conteúdo do buffer no arquivo .txt, retirando os títulos em caixa cinza que aparecem
    #incorretamente durante o texto
    saida = open(txt_file_name, "w", encoding="utf-8")
    for iniciadorNegrito in iniciadoresNegrito:
        if iniciadorNegrito in texto:
            texto = texto.replace(iniciadorNegrito, "")
    for linha in texto.split('\n'):
        if linha != "":
            saida.write(linha + '\n')

    return txt_file_name