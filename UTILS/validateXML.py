import xml.etree.ElementTree as ET
import argparse

# Funzione per validare il file XML
def validate_xml(xodr_file):
    try:
        # Prova a parsare il file XML
        tree = ET.parse(xodr_file)
        print(f"{xodr_file} è ben formato.")
    except ET.ParseError as e:
        print(f"Errore nel file XML: {e}")

# Funzione principale
def main():
    parser = argparse.ArgumentParser(description="Valida un file XODR.")
    parser.add_argument('--xodr', required=True, help='Percorso del file XODR da validare')
    args = parser.parse_args()

    xodr_file = args.xodr
    validate_xml(xodr_file)

# Esempio di utilizzo
if __name__ == "__main__":
    main()
