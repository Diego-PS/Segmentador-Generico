import argparse
import segmentador

def main():

    parser = argparse.ArgumentParser(description='Segmentação dos Diários Oficiais de Belo Horizonte')
    parser.add_argument("-o", metavar="<diretório>",type=str, help="Caminho do diretório par guardar as saídas no formato .json.", default="MPMG_segmentos/")
    parser.add_argument('--pdf', metavar='<arquivo>', type=str, help='Nome do arquivo do diário oficial em formato PDF.')
    parser.add_argument("--dir", help="Caminho do diretório contendos os arquivos dos diário oficiais em formato PDF.", default="amostra_BH/")

    args = parser.parse_args()
    dir_output = getattr(args, "o")
    if dir_output[-1] != "/":
        dir_output += "/"

    if getattr(args, 'pdf') is not None:
        segmentador.segmentador(getattr(args, 'pdf'), './MPMG_segmentos/')
    else:
        dir_input = getattr(args, "dir")
        if dir_input[-1] != "/":
            dir_input += "/"
        segmentador.segmentadorDir(dir_input, dir_output)

if __name__ == "__main__":
    main()