import streamlit as st
import pandas as pd
import json
import os
import time
from filelock import FileLock


# 1. Caricare i dati dal file JSON
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
    # Visualizza velocità e accelerazione
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Velocity", value=f"{round(veicolo_selezionato['speed'].values[0], 2)} m/s")
        st.metric(label="Acceleration", value=f"{round(veicolo_selezionato['acceleration'].values[0], 2)} m/s²")
    
    with col2:
        st.write("**Angle:**", round(veicolo_selezionato['angle'].values[0], 2))
        st.write("**Road ID:**", veicolo_selezionato['lane_id'].values[0])

# Funzione per visualizzare le nuove metriche
def update_additional_metrics(veicolo_selezionato):
    st.write("### Emissions & Consuptions")
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    
    with row1_col1:
        st.write("**CO2 Emission:**", round(veicolo_selezionato['co2_emission'].values[0], 2), "**mg/s**")
    with row1_col2:
        st.write("**CO Emission:**", round(veicolo_selezionato['co_emission'].values[0], 2), "**mg/s**")
    with row1_col3:
        st.write("**PM Emission:**", round(veicolo_selezionato['pm_emission'].values[0], 2), "**mg/s**")
    
    with row2_col1:
        st.write("**Electic Consuption:**", round(veicolo_selezionato['electricity_consumption'].values[0], 2), "**Wh/s**")
    with row2_col2:
        st.write("**Fuel Consuption:**", round(veicolo_selezionato['fuel_consumption'].values[0], 2), "**mg/s**")
    with row2_col3:
        st.write("**Noise:**", round(veicolo_selezionato['noise'].values[0], 2),"**dB**")

# Carica i dati
data = load_data()

st.title('Vehicles Watcher')

# 2. Mantieni l'ultimo ID selezionato
if 'last_selected' not in st.session_state:
    st.session_state.last_selected = data['id'].tolist()[0]

# 3. Creare il menù a tendina con gli ID veicoli
id_veicoli = data['id'].tolist()
selezionato = st.selectbox('Select the vehicle ID:', id_veicoli, index=id_veicoli.index(st.session_state.last_selected))

# Aggiorna la selezione memorizzata
st.session_state.last_selected = selezionato

# Percorso della cartella immagini
image_folder = 'images'

# Aggiorna i dati e le metriche ogni pochi secondi
while True:
    # Ricarica i dati dal file JSON
    data = load_data()
    
    # Aggiorna la lista di ID veicoli nel caso sia cambiata
    id_veicoli = data['id'].tolist()

    # Trova i dati del veicolo selezionato
    veicolo_selezionato = data[data['id'] == selezionato]

    if not veicolo_selezionato.empty:
        st.subheader('Selected vehicle info:')
        
        # Recupera il tipo di veicolo
        vehicle_type = veicolo_selezionato['type'].values[0]
        
        # Costruisce il percorso dell'immagine
        image_path = os.path.join(image_folder, f"{vehicle_type}.jpg")
        
        # Crea due colonne: una per l'immagine e una per le informazioni di velocità e accelerazione
        col_img, col_metrics = st.columns([1, 2])
        
        with col_img:
            if os.path.exists(image_path):
                st.image(image_path, caption=vehicle_type)
            else:
                st.write(f"**Tipo:** {vehicle_type} (Immagine non trovata)")
        
        with col_metrics:
            update_metrics(veicolo_selezionato)
        
        # Nuova riga per le nuove metriche
        st.write("---")  # Linea orizzontale per separare le sezioni
        update_additional_metrics(veicolo_selezionato)
        
    else:
        st.write('Nessun veicolo trovato con questo ID.')

    # Attende qualche secondo prima di ricaricare i dati
    time.sleep(0.1)
    st.experimental_rerun()  # Rerun the app to refresh the data and metrics
