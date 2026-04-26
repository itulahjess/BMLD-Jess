import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from datetime import datetime

# Initialisiere DataManager (Singleton)
data_manager = DataManager()

st.title("Abo-Verwaltung")

st.write("Hier kannst du alle deine Abos verwalten. Du kannst neue Abos hinzufügen, bestehende bearbeiten oder löschen.")

# Lade Daten aus session_state (falls vorhanden)
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = pd.DataFrame(columns=['abo_name', 'kosten', 'timestamp'])

data_df = st.session_state['data_df']

# Filtere nur Abo-bezogene Daten (angenommen, es gibt eine Spalte 'type' oder so; ansonsten alle Daten)
# Für Einfachheit: Nehmen wir an, data_df enthält Abos mit Spalten 'abo_name', 'kosten', 'timestamp'
abo_df = data_df.copy() if not data_df.empty else pd.DataFrame(columns=['abo_name', 'kosten', 'timestamp'])

# Anzeige der vorhandenen Abos
st.subheader("Deine Abos")
if not abo_df.empty:
    # Verwende st.data_editor für editierbare Tabelle
    edited_df = st.data_editor(
        abo_df,
        column_config={
            "abo_name": st.column_config.TextColumn("Abo-Name", help="Name des Abonnements"),
            "kosten": st.column_config.NumberColumn("Kosten (CHF)", help="Monatliche Kosten", min_value=0.0, step=0.01),
            "timestamp": st.column_config.DatetimeColumn("Erstellt am", help="Erstellungsdatum"),
        },
        hide_index=True,
        num_rows="dynamic",  # Erlaubt Hinzufügen/Löschen von Zeilen
        key="abo_editor"
    )

    # Speichere Änderungen
    if edited_df is not None and not edited_df.equals(abo_df):
        st.session_state['data_df'] = edited_df
        data_manager.save_user_data(edited_df, 'data.csv')
        st.success("Änderungen gespeichert!")
        st.rerun()  # Seite neu laden, um Änderungen anzuzeigen
else:
    st.info("Noch keine Abos vorhanden. Füge eines hinzu!")

# Formular zum Hinzufügen neuer Abos
st.subheader("Neues Abo hinzufügen")
with st.form("add_abo_form"):
    abo_name = st.text_input("Abo-Name", placeholder="z.B. Netflix")
    kosten = st.number_input("Kosten (CHF)", min_value=0.0, step=0.01, placeholder="z.B. 15.99")
    submit = st.form_submit_button("Hinzufügen")

    if submit:
        if abo_name and kosten > 0:
            new_row = pd.DataFrame({
                'abo_name': [abo_name],
                'kosten': [kosten],
                'timestamp': [datetime.now()]
            })
            updated_df = pd.concat([st.session_state['data_df'], new_row], ignore_index=True)
            st.session_state['data_df'] = updated_df
            data_manager.save_user_data(updated_df, 'data.csv')
            st.success(f"Abo '{abo_name}' hinzugefügt!")
            st.rerun()
        else:
            st.error("Bitte gib einen gültigen Namen und Kosten ein.")

# Zusammenfassung
if not abo_df.empty:
    total_kosten = abo_df['kosten'].sum()
    st.subheader(f"Gesamtkosten pro Monat: {total_kosten:.2f} CHF")
