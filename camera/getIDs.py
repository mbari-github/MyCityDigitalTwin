import carla

def main():
    try:
        # Connettiti al server CARLA
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)  # Timeout di 10 secondi
        print("Connessione al server CARLA avvenuta con successo.")

        # Ottieni il mondo e i veicoli attualmente nella simulazione
        world = client.get_world()

        # Ottieni tutti gli attori nella simulazione e filtra solo i veicoli
        vehicles = world.get_actors()
        IDs = []
        i=1
        print(len(vehicles))
        for vehicle in vehicles:
            i=i+1
            IDs.append(vehicle.id) 
        
        if IDs:  
            print("Veicoli trovati:", IDs)
            print(i)
        else:
            print("Nessun veicolo trovato nella simulazione.")
            print(i)

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == '__main__':
    main()
