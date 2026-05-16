import streamlit as st
import pandas as pd
from utils.data_manager import DataManager

st.title("Aboübersicht")

dm = DataManager()

if st.session_state.get('username') is None:
	st.error('Kein Benutzer eingeloggt. Bitte zuerst anmelden.')
	st.stop()

df = dm.load_user_data('subscriptions.csv', initial_value=pd.DataFrame())

if df is None or df.empty:
	st.info('Keine Abonnements vorhanden.')
	st.stop()

if 'start_date' in df.columns:
	df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce').dt.date

df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0.0)
df['active'] = df.get('active', True)

col1, col2, col3, col4 = st.columns(4)

active_df = df[df['active'] == True]

active_count = len(active_df)
inactive_count = len(df[df['active'] == False])

monthly_cost = active_df[active_df['interval'] == 'Monthly']['amount'].sum()
yearly_cost = active_df[active_df['interval'] == 'Yearly']['amount'].sum()
quarterly_cost = active_df[active_df['interval'] == 'Quarterly']['amount'].sum()

total_monthly_cost = monthly_cost + (yearly_cost / 12) + (quarterly_cost / 3)

col1.metric("Aktive Abos", active_count)
col2.metric("Inaktive Abos", inactive_count)
col3.metric("Monatliche Kosten", f"CHF {total_monthly_cost:.2f}")
col4.metric("Gesamtanzahl", len(df))

st.divider()

st.subheader("Alle Abonnements")

def render_subscription_cards(df):

	if df.empty:
		st.info("Keine Abonnements gefunden")
		return

	for idx, row in df.iterrows():

		with st.container():

			col1, col2, col3, col4 = st.columns([0.6, 2, 1.5, 1])

			icon = row.get("icon", "📱")
			col1.write(icon)

			col2.write(f"**{row['name']}**")
			col2.caption(f"Startdatum: {row['start_date']}")

			interval_text = (
				"Monatlich"
				if row["interval"] == "Monthly"
				else "Jährlich"
				if row["interval"] == "Yearly"
				else "Quartalsweise"
			)

			col3.write(f"CHF {row['amount']:.2f}")
			col3.caption(interval_text)

			status = "✅ Aktiv" if row["active"] else "❌ Inaktiv"
			col4.write(status)

render_subscription_cards(df)

st.divider()

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