import carla
import argparse
import time

def follow_vehicle_by_id(world, vehicle_id):
    vehicle = world.get_actor(vehicle_id)
    if vehicle is None:
        print(f"Nessun veicolo trovato con l'ID: {vehicle_id}")
        return

    spectator = world.get_spectator()

    print(f"Inseguendo il veicolo con ID: {vehicle.id}")
    
    while True:
        # Ottieni la trasformazione del veicolo
        transform = vehicle.get_transform()

        # Imposta la posizione e la rotazione della telecamera
        offset = carla.Location(x=-10, z=5)
        location = transform.location + transform.rotation.get_forward_vector() * offset.x + carla.Location(z=offset.z)
        rotation = transform.rotation
        rotation.pitch = -20
        rotation.roll = 0

        spectator.set_transform(carla.Transform(location, rotation))

        time.sleep(0.1)

def main():
    # Parser per gli argomenti della riga di comando
    parser = argparse.ArgumentParser(description="Script per seguire un veicolo in CARLA")
    parser.add_argument('--id', type=int, required=True, help="ID del veicolo da seguire")
    args = parser.parse_args()

    try:
        # Connettiti al server CARLA
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)  # Timeout di 10 secondi

        # Ottieni il mondo e i veicoli attualmente nella simulazione
        world = client.get_world()

        follow_vehicle_by_id(world, args.id)

    except Exception as e:
        print(f"Errore durante l'esecuzione del programma: {e}")

if __name__ == '__main__':
    main()
