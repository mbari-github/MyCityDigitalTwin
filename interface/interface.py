import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import time
from filelock import FileLock

# Funzione per caricare i dati dal file JSON
def load_data():
    with FileLock('C:/Users/barim/OneDrive/Desktop/CARLA_0.9.15/WindowsNoEditor/Co-Simulation/Sumo/vehicles_data.json.lock'):
        with open('C:/Users/barim/OneDrive/Desktop/CARLA_0.9.15/WindowsNoEditor/Co-Simulation/Sumo/vehicles_data.json') as f:
            data = json.load(f)
    records = []
    for key, value in data.items():
        record = {'id': key}
        record.update(value)
        records.append(record)
    return pd.DataFrame(records)

# Funzione per aggiornare i dati e visualizzare le metriche
def update_metrics(veicolo_selezionato):      
    speed =  veicolo_selezionato['speed'].values[0]
    acceeleration = veicolo_selezionato['acceleration'].values[0]
    angle = veicolo_selezionato['angle'].values[0]
    lane_id = veicolo_selezionato['lane_id'].values[0]
    
    return speed, acceeleration, angle, lane_id


# Funzione per visualizzare le nuove metriche
def update_additional_metrics(veicolo_selezionato):
    co2_emission = veicolo_selezionato['co2_emission'].values[0]
    co_emission = veicolo_selezionato['co_emission'].values[0]
    pm_emission = veicolo_selezionato['pm_emission'].values[0]
    electricity_consumption = veicolo_selezionato['electricity_consumption'].values[0]
    fuel_consuption = veicolo_selezionato['fuel_consumption'].values[0]
    noise = veicolo_selezionato['noise'].values[0]
    
    return co2_emission, co_emission, pm_emission, electricity_consumption, fuel_consuption, noise
    
    
# Funzione per calcolare le metriche aggregate
def aggregate_metrics(data):
    total_co2 = data['co2_emission'].sum()
    total_co = data['co_emission'].sum()
    total_pm = data['pm_emission'].sum()
    total_fuel_consumption = data['fuel_consumption'].sum()
    total_electricity_consumption = data['electricity_consumption'].sum()
    
    return total_co2, total_co, total_pm, total_fuel_consumption, total_electricity_consumption


# Funzione per calcolare la velocità media
def calculate_speed_metrics(data, veicolo_selezionato):
    # Velocità media del veicolo selezionato durante l'intera simulazione
    speed_selected = veicolo_selezionato['speed'].values[0]
    avg_speed_selected = sum(speed_selected) / len(speed_selected)
    
    # Velocità media di tutti i veicoli nell'ultimo istante
    last_speeds = [vehicle['speed'][-1] for _, vehicle in data.iterrows() if vehicle['speed']]
    avg_last_speed_all = sum(last_speeds) / len(last_speeds) if last_speeds else 0
    
    # Velocità media di tutti i veicoli durante l'intera simulazione
    all_speeds = [sum(vehicle['speed']) / len(vehicle['speed']) for _, vehicle in data.iterrows() if vehicle['speed']]
    avg_speed_all = sum(all_speeds) / len(all_speeds) if all_speeds else 0
    
    return avg_speed_selected, avg_last_speed_all, avg_speed_all

#def gather_all_speeds_padded(data):
    # Ottieni il valore di step_count dal primo veicolo (dato che è comune a tutti)
    step_count = data['step_count'].values[0]
    
    # Crea un dizionario per contenere le velocità di ciascun veicolo
    speeds_over_time = {}

    # Itera su ogni veicolo nel dataset
    for _, vehicle in data.iterrows():
        vehicle_id = vehicle['id']
        speeds = vehicle['speed']
        
        # Aggiungi NaN all'inizio dell'array per uniformare la lunghezza a step_count
        if len(speeds) < step_count:
            speeds = np.pad(speeds, (step_count - len(speeds), 0), constant_values=np.nan)
        
        speeds_over_time[vehicle_id] = speeds

    return speeds_over_time

def add_padding_to_speed(speed, data):
    # Calcola la lunghezza attuale del vettore speed
    current_length = len(speed)
    step_count = data['step_count'].values[0]

    
    # Calcola il padding necessario
    padding_needed = step_count - current_length
    
    # Aggiungi NaN come padding se necessario
    if padding_needed > 0:
        # Crea un array di NaN con la dimensione necessaria
        padding = np.full(padding_needed, np.nan)
        # Restituisci l'array di padding seguito dal vettore speed
        return np.concatenate((padding, speed))
    
    # Se non è necessario padding, restituisci il vettore speed così com'è
    return speed


def calculate_cumulative_avg_speed(veicolo_selezionato):
    # Ottieni il vettore delle velocità del veicolo selezionato
    speed = veicolo_selezionato['speed'].values[0]
    
    # Ottieni il numero totale di step di simulazione (step_count)
    step_count = len(speed)
    
    # Inizializza un array per le velocità medie cumulative
    cumulative_avg_speed = np.zeros(step_count)
    
    # Calcola la media cumulativa per ogni step
    for i in range(1, step_count + 1):
        cumulative_avg_speed[i - 1] = np.mean(speed[:i])
    
    return cumulative_avg_speed


def calculate_all_vehicles_avg_speed_per_instant(data):
    # Crea una lista per memorizzare le velocità di tutti i veicoli
    all_speeds = []
    
    # Itera su ogni veicolo nel DataFrame
    for _, vehicle in data.iterrows():
        all_speeds.append(vehicle['speed'])
    
    # Calcolo della lunghezza massima degli array di velocità
    max_length = data['step_count'].values[0]
    
    # Applico padding per uniformare la lunghezza degli array di velocità
    padded_speeds = [np.pad(vehicle_speed, (0, max_length - len(vehicle_speed)), 'constant', constant_values=np.nan)
                     for vehicle_speed in all_speeds]
    
    # Converto in array numpy
    speeds_array = np.array(padded_speeds)
    
    # Calcolo della velocità media per ogni istante, ignorando i NaN
    avg_speed_all_vehicles_per_instant = np.nanmean(speeds_array, axis=0)
    
    return avg_speed_all_vehicles_per_instant


# Carica i dati
data = load_data()


st.title('Vehicles Watcher')

# Mantieni l'ultimo ID selezionato
if 'last_selected' not in st.session_state:
    st.session_state.last_selected = data['id'].tolist()[0]
    
st.write("### Vehicles' IDs: ")
# Mostra gli ID veicoli con uno sfondo colorato
id_veicoli = data['id'].tolist()

# Sezione scrollante per gli ID
with st.container():
    st.markdown(
        """
        <div style="background-color: #262730; padding: 8px; border-radius: 7px; padding-bottom: 0px; padding-top: 5px">
            <marquee scrollamount="6" direction="left" behavior="scroll">
                <span style="color: #149e3b;">{}</span>
            </marquee>
        </div>
        """.format(" &nbsp&nbsp | &nbsp&nbsp ".join(id_veicoli)),
        unsafe_allow_html=True
    )

# Casella di testo per l'ID veicolo
input_id = st.text_input("ID del veicolo", placeholder="Enter vehicle's ID", label_visibility='hidden')

# Aggiorna la selezione memorizzata
if input_id in id_veicoli:
    st.session_state.last_selected = input_id
else:
    st.session_state.last_selected = data['id'].tolist()[0]

# Percorso della cartella immagini
image_folder = 'images'

# Aggiorna i dati e le metriche ogni pochi secondi
while True:
    # Ricarica i dati dal file JSON
    data = load_data()
    
    # Aggiorna la lista di ID veicoli nel caso sia cambiata
    id_veicoli = data['id'].tolist()

    # Trova i dati del veicolo selezionato
    veicolo_selezionato = data[data['id'] == st.session_state.last_selected]

    if not veicolo_selezionato.empty:
        st.subheader('Selected vehicle\'s data:')
        
        # Recupera il tipo di veicolo
        vehicle_type = veicolo_selezionato['type'].values[0]
        
        
        #Aggiorna le info
        speed, acceleration, angle, lane_id = update_metrics(veicolo_selezionato)
        
        # Aggiorna le metriche aggiuntive
        co2_emission, co_emission, pm_emission, electricity_consumption, fuel_consuption, noise = update_additional_metrics(veicolo_selezionato)
        
        # Aggiorna le metriche aggregate
        total_co2, total_co, total_pm, total_fuel_consumption, total_electricity_consumption = aggregate_metrics(data)
        
        #Aggiorna le info su velocità medie
        avg_speed_selected, avg_last_speed_all, avg_speed_all = calculate_speed_metrics(data, veicolo_selezionato)
        
        # Calcola l'array della velocità media cumulativa per il veicolo selezionato
        cumulative_avg_speed_array = calculate_cumulative_avg_speed(veicolo_selezionato)
        
        # Calcola la velocità media di tutti i veicoli all'ultimo istante (per ogni step)
        #avg_speed_all_vehicles_last_instant_array = calculate_all_vehicles_avg_speed_last_instant(data)
        avg_speed_all_vehicles_per_instant = calculate_all_vehicles_avg_speed_per_instant(data)

        

        
        
        # Costruisce il percorso dell'immagine
        image_path = os.path.join(image_folder, f"{vehicle_type}.jpg")
        
        # Crea due colonne: una per l'immagine e una per le informazioni di velocità e accelerazione
        col_img, col_metrics = st.columns([1, 2])
        
        with col_img:
            if os.path.exists(image_path):
                st.image(image_path, caption=vehicle_type, use_column_width ="auto" )
            else:
                st.write(f"**Model:** {vehicle_type} (Image not found)")
        
        with col_metrics:
            col1, col2 = st.columns(2)
    
            with col1:
                st.metric(label="Velocity", value=f"{round(speed[-1], 2)} m/s")
                st.metric(label="Acceleration", value=f"{round(acceleration , 2)} m/s²")
            
            with col2:
                st.write("**Angle:**", round(angle, 2))
                st.write("**Road ID:**", lane_id)
        
        
        # Creare un DataFrame con la velocità effettiva e quella media cumulativa
        speed_data = pd.DataFrame({
            'Selected Vehicle Speed': add_padding_to_speed(speed, data),  # Array della velocità effettiva
            #'Selected Vehicle Average Speed': cumulative_avg_speed_array,  # Array della velocità media cumulativa
            'All Vehicles Average Speed': avg_speed_all_vehicles_per_instant
        })

        # Visualizzare entrambe le serie sullo stesso grafico
        st.write("### Vehicle Speed and Average Speed")
        st.line_chart(speed_data)
        
        
        # Nuova riga per le nuove metriche
        st.write("---")  # Linea orizzontale per separare le sezioni
        st.write("### Emissions & Consumptions")
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        row3_col1, row3_col2 = st.columns(2)
        
        with row1_col1:
            st.write("**CO2 Emission:**", round(co2_emission, 2), "**mg/s**")
        with row1_col2:
            st.write("**CO Emission:**", round(co_emission, 2), "**mg/s**")
        with row2_col1:
            st.write("**PM Emission:**", round(pm_emission, 2), "**mg/s**")
        with row2_col2:
            st.write("**Noise:**", round(noise, 2),"**dB**")
        with row3_col1:
            st.write("**Electric Consumption:**", round(electricity_consumption, 2), "**Wh/s**")
        with row3_col2:
            st.write("**Fuel Consumption:**", round(fuel_consuption, 2), "**mg/s**")
    
        
        st.write("---")
        st.write("### Aggregate Metrics")
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        row3_col1, row3_col2 = st.columns(2)
        
        with row1_col1:
            st.write("**CO2 Emission:**", round(total_co2, 2), "**mg/s**")
        with row1_col2:
            st.write("**CO Emission:**", round(total_co, 2), "**mg/s**")
        with row2_col1:
            st.write("**PM Emission:**", round(total_pm, 2), "**mg/s**") 
        with row3_col1:
            st.write("**Fuel Consumption:**", round(total_fuel_consumption, 2), "**mg/s**")
        with row3_col2:
            st.write("**Electric Consumption:**", round(total_electricity_consumption, 2), "**Wh/s**")

        # Visualizza le velocità medie
        st.write("---")
        st.write("### Average Speed")
        st.write("**Selected Vehicle Speed (Last Instant):** ", round(speed[-1], 2), "**m/s**")
        st.write("**Selected Vehicle Average Speed:** ", round(avg_speed_selected, 2), "**m/s**")
        st.write("**All Vehicles Average Speed (Last Instant):** ", round(avg_last_speed_all, 2), "**m/s**")
        st.write("**All Vehicles Average Speed (Overall):** ", round(avg_speed_all, 2),  "**m/s**")

        
        #st.write("### All Vehicles' Speed Plot")
        # Recupera tutte le velocità dei veicoli
        #speeds_over_time = gather_all_speeds_padded(data)

        # Creare un DataFrame con le velocità
        #df_speeds = pd.DataFrame(speeds_over_time)

        # Visualizzare il grafico con tutte le velocità dei veicoli
        #st.line_chart(df_speeds)
        
        

        
    else:
        st.write('Nessun veicolo trovato con questo ID.')

    # Attende qualche secondo prima di ricaricare i dati
    time.sleep(0.1)
    st.experimental_rerun()  # Rerun the app to refresh the data and metrics
