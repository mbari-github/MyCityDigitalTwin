import xml.etree.ElementTree as ET

def validate_xml(xml_file):
    try:
        # Prova a parsare il file XML
        tree = ET.parse(xml_file)
        print(f"{xml_file} è ben formato.")
    except ET.ParseError as e:
        print(f"Errore nel file XML: {e}")

# Specifica il percorso del file XML
xml_file = 'Bari_map.xodr'

validate_xml(xml_file)