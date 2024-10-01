import streamlit as st
import pandas as pd
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
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Velocità", value=f"{round(veicolo_selezionato['speed'].values[0], 2)} m/s")
        st.metric(label="Accelerazione", value=f"{round(veicolo_selezionato['acceleration'].values[0], 2)} m/s²")
    
    with col2:
        st.write("**Angolo:**", round(veicolo_selezionato['angle'].values[0], 2))
        st.write("**ID corsia:**", veicolo_selezionato['lane_id'].values[0])

# Funzione per visualizzare le nuove metriche
def update_additional_metrics(veicolo_selezionato):
    st.write("### Emissions & Consumptions")
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    
    with row1_col1:
        st.write("**CO2 Emission:**", round(veicolo_selezionato['co2_emission'].values[0], 2), "**mg/s**")
    with row1_col2:
        st.write("**CO Emission:**", round(veicolo_selezionato['co_emission'].values[0], 2), "**mg/s**")
    with row1_col3:
        st.write("**PM Emission:**", round(veicolo_selezionato['pm_emission'].values[0], 2), "**mg/s**")
    
    with row2_col1:
        st.write("**Electric Consumption:**", round(veicolo_selezionato['electricity_consumption'].values[0], 2), "**Wh/s**")
    with row2_col2:
        st.write("**Fuel Consumption:**", round(veicolo_selezionato['fuel_consumption'].values[0], 2), "**mg/s**")
    with row2_col3:
        st.write("**Noise:**", round(veicolo_selezionato['noise'].values[0], 2),"**dB**")

# Funzione per calcolare le metriche aggregate
def aggregate_metrics(data):
    total_co2 = data['co2_emission'].sum()
    total_co = data['co_emission'].sum()
    total_pm = data['pm_emission'].sum()
    avg_speed = data['speed'].mean()
    total_fuel_consumption = data['fuel_consumption'].sum()
    total_electricity_consumption = data['electricity_consumption'].sum()
    
    return total_co2, total_co, total_pm, avg_speed, total_fuel_consumption, total_electricity_consumption

# Carica i dati
data = load_data()

st.title('Vehicles Watcher')

# 2. Mantieni l'ultimo ID selezionato
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
        st.subheader('Dettagli veicolo selezionato:')
        
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

        # Mostra le metriche aggregate
        total_co2, total_co, total_pm, avg_speed, total_fuel_consumption, total_electricity_consumption = aggregate_metrics(data)

        st.write("### Aggregate Metrics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**CO2 Emission:**", round(total_co2, 2), "**mg/s**")
        with col2:
            st.write("**CO Emission:**", round(total_co, 2), "**mg/s**")
        with col3:
            st.write("**PM Emission:**", round(total_pm, 2), "**mg/s**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Fuel Consumption:**", round(total_fuel_consumption, 2), "**mg/s**")
        
        with col2:
            st.write("**Electric Consumption:**", round(total_electricity_consumption, 2), "**mg/s**")

        st.write("---")  # Linea orizzontale per separare le sezioni
        st.write("### Average Speed")
        st.write("**Average Speed:**", round(avg_speed, 2), "**m/s**")
        
    else:
        st.write('Nessun veicolo trovato con questo ID.')

    # Attende qualche secondo prima di ricaricare i dati
    time.sleep(0.1)
    st.experimental_rerun()  # Rerun the app to refresh the data and metrics
