import argparse
import segmentador

def main():

    parser = argparse.ArgumentParser(description='Segmentação dos Diários Oficiais de Belo Horizonte')
    parser.add_argument('--pdf', metavar='<arquivo>', type=str, help='Nome do arquivo do diário oficial em formato PDF.')


    args = parser.parse_args()

    if getattr(args, 'pdf') is not None:
        segmentador.segmentador(getattr(args, 'pdf'), './JSON/')

if __name__ == "__main__":
    main()