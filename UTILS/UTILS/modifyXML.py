import xml.etree.ElementTree as ET
import random
import argparse

# Lista dei tipi di veicoli disponibili
vehicle_types = [
    "vehicle.audi.a2", "vehicle.audi.tt", "vehicle.carlamotors.carlacola", "vehicle.dodge.charger_police",
    "vehicle.jeep.wrangler_rubicon", "vehicle.chevrolet.impala", "vehicle.mini.cooper_s", "vehicle.micro.microlino",
    "vehicle.audi.etron", "vehicle.mercedes.coupe", "vehicle.bmw.grandtourer", "vehicle.toyota.prius",
    "vehicle.citroen.c3", "vehicle.ford.mustang", "vehicle.tesla.model3", "vehicle.diamondback.century",
    "vehicle.gazelle.omafiets", "vehicle.harley-davidson.low_rider", "vehicle.bh.crossbike", "vehicle.tesla.cybertruck",
    "vehicle.volkswagen.t2", "vehicle.kawasaki.ninja", "vehicle.lincoln.mkz_2017", "vehicle.seat.leon",
    "vehicle.yamaha.yzf", "vehicle.nissan.patrol", "vehicle.nissan.micra"
]

# Funzione per aggiungere la nuova tag <vehicle_type> con valore casuale e generare un nuovo file XML
def add_vehicle_type(xml_file, output_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for vehicle in root.findall('vehicle'):
        vehicle_type = random.choice(vehicle_types)
        vehicle.set('type', vehicle_type)

    tree.write(output_file)

# Funzione principale
def main():
    parser = argparse.ArgumentParser(description="Modifica il file XML aggiungendo un tipo di veicolo casuale.")
    parser.add_argument('--xml', required=True, help='Percorso del file XML di input')
    args = parser.parse_args()

    input_xml_file = args.xml
    output_xml_file = 'modified_' + input_xml_file  # Crea un file di output modificato

    add_vehicle_type(input_xml_file, output_xml_file)
    print(f"File XML modificato salvato come: {output_xml_file}")

# Esempio di utilizzo
if __name__ == "__main__":
    main()
