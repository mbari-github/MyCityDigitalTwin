import carla

def main():
    try:
        # Connettiti al server CARLA
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)  # Timeout di 10 secondi per evitare che il programma si blocchi

        world = client.get_world()
        print("Connessione al server CARLA avvenuta con successo.")

        vehicles = world.get_actors().filter('vehicle.*')
        IDs = []
        
        for vehicle in vehicles:
            IDs.append(vehicle.id) 
        
        if vehicles:  
            print("Veicoli trovati:", IDs)
        else:
            print("Nessun veicolo trovato nella simulazione.")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == '__main__':
    main()
