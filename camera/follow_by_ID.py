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

        # Estrai i valori dal veicolo
        speed = vehicle.get_velocity()
        speed_kmh = (speed.x**2 + speed.y**2 + speed.z**2)**0.5 * 3.6  # Converti in km/h
        acceleration = vehicle.get_acceleration()
        acceleration_m_s2 = (acceleration.x**2 + acceleration.y**2 + acceleration.z**2)**0.5  # in m/s²

        # Stampa le informazioni sul veicolo
        print(f"ID: {vehicle.id}, Speed: {speed_kmh:.2f} km/h, Acceleration: {acceleration_m_s2:.2f} m/s²")
        
        # Aspetta un attimo prima di aggiornare
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
