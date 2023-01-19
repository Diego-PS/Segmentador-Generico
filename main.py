import argparse
import text

def main():

    parser = argparse.ArgumentParser(description='Segmentação dos Diários Oficiais de Belo Horizonte')
    parser.add_argument('--pdf', metavar='<arquivo>', type=str, help='Nome do arquivo do diário oficial em formato PDF.')


    args = parser.parse_args()

    with pdf_args as getattr(args, 'pdf'):
        if pdf_args is not None:
            text.(pdf_args)