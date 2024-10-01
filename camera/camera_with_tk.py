import json
import tkinter as tk
import argparse
import carla
import random

# Flag globale per il controllo dell'aggiornamento
flag = True
vehicle = None

# Percorso del file JSON (inserisci qui il percorso del tuo file)
json_file_path = 'C:/Users/barim/OneDrive/Desktop/CARLA_0.9.15/WindowsNoEditor/Co-Simulation/Sumo/vehicles_data.json'

def read_vehicle_info_from_json(file_path, vehicle_id):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            vehicle_info = data.get(str(vehicle_id))
            if vehicle_info:
                return vehicle_info
            else:
                print(f"Veicolo con ID {vehicle_id} non trovato nel file JSON.")
                return None
    except Exception as e:
        print(f"Errore durante la lettura del file JSON: {e}")
        return None

def update_ui(file_path, vehicle_id, speed_label, acceleration_label, type_label, lane_id_label, id_label):
    vehicle_info = read_vehicle_info_from_json(file_path, vehicle_id)
    if vehicle_info:
        try:
            speed = vehicle_info.get("speed", "N/A")
            acceleration = vehicle_info.get("acceleration", "N/A")
            vehicle_type = vehicle_info.get("type", "N/A")
            lane_id = vehicle_info.get("lane_id", "N/A")

            # Aggiorna l'interfaccia utente
            id_label.config(text=f"ID: {vehicle_id}")
            type_label.config(text=f"Type: {vehicle_type}")
            speed_label.config(text=f"Speed: {speed:.2f} km/h")
            acceleration_label.config(text=f"Acceleration: {acceleration:.2f} m/s²")
            lane_id_label.config(text=f"Lane ID: {lane_id}")
            
        except Exception as e:
            print(f"Errore durante l'aggiornamento dell'UI: {e}")

def update_camera_and_ui(world, spectator, speed_label, acceleration_label, type_label, lane_id_label, id_label):
    global flag, vehicle
    if flag and vehicle is not None:
        try:
            # Ottieni la trasformazione del veicolo
            transform = vehicle.get_transform()

            # Imposta la posizione e la rotazione della telecamera
            offset = carla.Location(x=-10, z=5)
            location = transform.location + transform.rotation.get_forward_vector() * offset.x + carla.Location(z=offset.z)
            rotation = transform.rotation
            rotation.pitch = -20
            rotation.roll = 0

            spectator.set_transform(carla.Transform(location, rotation))

            # Aggiorna l'interfaccia utente con i nuovi valori
            update_ui(json_file_path, vehicle.id, speed_label, acceleration_label, type_label, lane_id_label, id_label)
        except Exception as e:
            print(f"Errore durante l'aggiornamento della telecamera: {e}")
    
    # Pianifica il prossimo aggiornamento
    root.after(100, update_camera_and_ui, world, spectator, speed_label, acceleration_label, type_label, lane_id_label, id_label)

def follow_vehicle_by_id(world, spectator, vehicle_id, speed_label, acceleration_label, type_label, lane_id_label, id_label):
    global flag, vehicle
    if vehicle_id is not None:
        # Cerca il veicolo con l'ID specificato
        vehicle = world.get_actor(vehicle_id)
        if vehicle is not None:
            flag = True
            print(f"La telecamera sta seguendo il veicolo con id: {vehicle.id}")
            update_camera_and_ui(world, spectator, speed_label, acceleration_label, type_label, lane_id_label, id_label)
        else:
            print(f"Nessun veicolo trovato con l'ID: {vehicle_id}")
    else:
        on_enter_press(None, world, spectator, speed_label, acceleration_label, type_label, lane_id_label, id_label)

def on_enter_press(event, world, spectator, speed_label, acceleration_label, type_label, lane_id_label, id_label): 
    global vehicle, flag
    vehicles = world.get_actors().filter('vehicle.*')
    if vehicles:
        vehicle = random.choice(vehicles)
        print(f"La telecamera sta seguendo il veicolo con id: {vehicle.id}")
        flag = True
        update_camera_and_ui(world, spectator, speed_label, acceleration_label, type_label, lane_id_label, id_label)
    else:
        print("Nessun veicolo trovato nella simulazione.")

def stop_following():
    global flag
    flag = False
    root.destroy()

def main():
    global flag, vehicle

    # Parser per gli argomenti della riga di comando
    parser = argparse.ArgumentParser(description="Script per seguire un veicolo in CARLA e visualizzare le sue informazioni")
    parser.add_argument('--id', type=int, help="ID del veicolo da seguire")
    args = parser.parse_args()

    try:
        # Connettiti al server CARLA
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)  # Timeout di 10 secondi per evitare che il programma si blocchi

        # Ottieni il mondo e i veicoli attualmente nella simulazione
        world = client.get_world()

        # Imposta la modalità sincrona
        settings = world.get_settings()
        settings.synchronous_mode = True
        world.apply_settings(settings)

        # Ottieni l'actor della telecamera
        spectator = world.get_spectator()

        print("Connesso al server CARLA.")
        
        # Crea la finestra Tkinter
        global root
        root = tk.Tk()
        root.title("Vehicle Info")

        id_label = tk.Label(root, text="ID: N/A", font=("Helvetica", 16))
        id_label.pack(pady=5)

        type_label = tk.Label(root, text="Type: N/A", font=("Helvetica", 16))
        type_label.pack(pady=5)

        lane_id_label = tk.Label(root, text="Lane ID: N/A", font=("Helvetica", 16))
        lane_id_label.pack(pady=5)

        speed_label = tk.Label(root, text="Speed: N/A", font=("Helvetica", 16))
        speed_label.pack(pady=5)

        acceleration_label = tk.Label(root, text="Acceleration: N/A", font=("Helvetica", 16))
        acceleration_label.pack(pady=5)


        # Se è stato fornito un ID, inizia automaticamente a seguire il veicolo
        if args.id:
            follow_vehicle_by_id(world, spectator, args.id, speed_label, acceleration_label, type_label, lane_id_label, id_label)
        else:
            # Attendi che l'utente prema ENTER per iniziare a seguire un veicolo
            root.bind('<Return>', lambda event: on_enter_press(event, world, spectator, speed_label, acceleration_label, type_label, lane_id_label, id_label))
        
        root.protocol("WM_DELETE_WINDOW", stop_following)

        # Avvia l'aggiornamento continuo
        root.after(100, update_camera_and_ui, world, spectator, speed_label, acceleration_label, type_label, lane_id_label, id_label)

        # Ciclo di aggiornamento Tkinter
        root.mainloop()

    except Exception as e:
        print(f"Errore durante l'esecuzione del programma: {e}")

if __name__ == '__main__':
    main()
