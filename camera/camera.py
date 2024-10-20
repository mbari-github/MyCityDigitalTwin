import carla
import random
import time
import threading

class VehicleFollower:
    def __init__(self, spectator):
        self.spectator = spectator
        self.following_thread = None
        self.flag = False

    def follow_vehicle(self, vehicle):
        """
        Segui il veicolo specificato e aggiorna la posizione della telecamera.
        """
        self.flag = True
        while self.flag:
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
            self.spectator.set_transform(carla.Transform(location, rotation))

            time.sleep(0.05)  # Aggiorna la posizione della telecamera ogni 50 millisecondi

    def stop_following(self):
        """Ferma l'inseguimento del veicolo corrente."""
        if self.following_thread is not None:
            self.flag = False
            self.following_thread.join()  # Aspetta che il thread finisca

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

    vehicle_follower = VehicleFollower(spectator)

    try:
        while True:
            input()  # Attendi che l'utente prema ENTER
            
            # Ferma l'inseguimento del veicolo corrente se è in corso
            vehicle_follower.stop_following()
            
            # Ottieni tutti i veicoli attualmente nella simulazione
            vehicles = world.get_actors().filter('vehicle.*')
            
            if vehicles:
                # Se ci sono veicoli, seleziona un veicolo casuale
                vehicle = random.choice(vehicles)
                
                print(f"La telecamera sta seguendo il veicolo con ID: {vehicle.id}")

                # Inizia a seguire il veicolo in un nuovo thread
                vehicle_follower.following_thread = threading.Thread(target=vehicle_follower.follow_vehicle, args=(vehicle,))
                vehicle_follower.following_thread.start()

            else:
                print("Nessun veicolo trovato nella simulazione.")

    except KeyboardInterrupt:
        print("Uscita dal programma.")
        vehicle_follower.stop_following()  # Assicurati di fermare l'inseguimento
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        print("Disconnetti dal server CARLA.")
        client.close()  

if __name__ == '__main__':
    main()
