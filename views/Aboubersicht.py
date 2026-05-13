import streamlit as st
import pandas as pd
from datetime import date
from utils.data_manager import DataManager


st.title("Aboübersicht")

dm = DataManager()
if st.session_state.get('username') is None:
	st.error('Kein Benutzer eingeloggt. Bitte zuerst anmelden.')
	st.stop()

# Load subscriptions
df = dm.load_user_data('subscriptions.csv', initial_value=pd.DataFrame())
if df is None or df.empty:
	st.info('Keine Abonnements vorhanden. Bitte gehen Sie zur Abo-Verwaltung, um Abos hinzuzufügen.')
	st.stop()

# Prepare data
if 'start_date' in df.columns:
	df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce').dt.date
df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0.0)
df['active'] = df.get('active', True)

# Metrics
col1, col2, col3, col4 = st.columns(4)

active_count = len(df[df['active'] == True])
inactive_count = len(df[df['active'] == False])
total_cost = df[df['active'] == True]['amount'].sum()

col1.metric("Aktive Abos", active_count)
col2.metric("Inaktive Abos", inactive_count)
col3.metric("Monatliche Kosten", f"CHF {total_cost:.2f}")
col4.metric("Gesamtanzahl", len(df))

st.divider()

# Display all subscriptions as table
st.subheader("Alle Abonnements")

display_df = df[['name', 'amount', 'interval', 'active', 'start_date']].copy()
display_df.columns = ['Name', 'Betrag (CHF)', 'Intervall', 'Status', 'Startdatum']
display_df['Status'] = display_df['Status'].apply(lambda x: '✅ Aktiv' if x else '❌ Inaktiv')
display_df['Intervall'] = display_df['Intervall'].apply(lambda x: 'Monatlich' if x == 'Monthly' else 'Jährlich' if x == 'Yearly' else 'Quartalsweise')

st.dataframe(display_df, use_container_width=True)

st.divider()

# Summary by interval
st.subheader("Zusammenfassung nach Intervall")

col1, col2, col3 = st.columns(3)

monthly = df[df['interval'] == 'Monthly']
yearly = df[df['interval'] == 'Yearly']
quarterly = df[df['interval'] == 'Quarterly']

with col1:
	st.write("**Monatliche Abos**")
	st.metric("Anzahl", len(monthly))
	st.metric("Kosten/Monat", f"CHF {monthly['amount'].sum():.2f}")

with col2:
	st.write("**Jährliche Abos**")
	st.metric("Anzahl", len(yearly))
	st.metric("Kosten/Jahr", f"CHF {yearly['amount'].sum():.2f}")

with col3:
	st.write("**Quartalsweise Abos**")
	st.metric("Anzahl", len(quarterly))
	st.metric("Kosten/Quartal", f"CHF {quarterly['amount'].sum():.2f}")
