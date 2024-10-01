import carla
import random
import time
import sys
import keyboard

flag=True

def main():
    # Connettiti al server CARLA
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)  # Timeout di 10 secondi per evitare che il programma si blocchi

    # Ottieni il mondo e i veicoli attualmente nella simulazione
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    
    # Ottieni l'actor della telecamera
    spectator = world.get_spectator()

    print("Connesso al server CARLA. Premi ENTER per seguire un veicolo casuale.")

    try:
        while True:
            input()  # Attendi che l'utente prema ENTER
            
            # Ottieni tutti i veicoli attualmente nella simulazione
            vehicles = world.get_actors().filter('vehicle.*')
            
            if vehicles:
                # Se ci sono veicoli, seleziona un veicolo casuale
                vehicle = random.choice(vehicles)
                
                print(f"La telecamera sta seguendo il veicolo con id: {vehicle.id}")
                flag=True
                
                # Aggiorna la posizione della telecamera per seguire il veicolo selezionato
                while flag:
                    transform = vehicle.get_transform()
                    
                    # Offset per la telecamera (dietro e sopra il veicolo)
                    offset = carla.Location(x=-10, z=5)
                    
                    # Calcola la nuova posizione della telecamera
                    location = transform.location + transform.rotation.get_forward_vector() * offset.x + carla.Location(z=offset.z)
                    
                    # Orienta la telecamera verso il veicolo
                    rotation = transform.rotation
                    rotation.pitch = -20
                    rotation.roll = 0
                    
                    # Imposta la trasformazione della telecamera
                    spectator.set_transform(carla.Transform(location, rotation))
                    
                    
                    if keyboard.is_pressed('enter'):
                        flag=False;

                    time.sleep(0.05)  # Aggiorna la posizione della telecamera ogni 50 millisecondi

            else:
                print("Nessun veicolo trovato nella simulazione.")

    except KeyboardInterrupt:
        print("Uscita dal programma.")

if __name__ == '__main__':
    main()
