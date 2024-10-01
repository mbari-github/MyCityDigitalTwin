import carla

def get_vehicle_ids():
    # Connessione al server CARLA
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    # Ottenere il mondo attuale
    world = client.get_world()

    # Ottenere tutti gli attori nella simulazione
    actors = world.get_actors()
    
    print(f"Numero totale di attori: {len(actors)}")  # Debug: Stampare il numero totale di attori

    # Filtrare solo i veicoli
    vehicles = world.get_actors().filter('vehicle.*')

    if len(vehicles) == 0:
        print("Nessun veicolo trovato nella simulazione.")
    else:
        # Stampare gli ID dei veicoli
        for vehicle in vehicles:
            print(f"Vehicle ID: {vehicle.id} - Type: {vehicle.type_id}")

if __name__ == "__main__":
    get_vehicle_ids()
