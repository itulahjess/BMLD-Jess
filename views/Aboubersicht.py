import streamlit as st
import pandas as pd
from utils.data_manager import DataManager

st.title("Aboübersicht")

dm = DataManager()

if st.session_state.get('username') is None:
	st.error('Kein Benutzer eingeloggt. Bitte zuerst anmelden.')
	st.stop()

# Icons
ICON_OPTIONS = {
	'📷': 'Kamera',
	'📱': 'Smartphone',
	'🎵': 'Musik',
	'📺': 'TV',
	'🎮': 'Spiele',
	'📚': 'Bücher',
	'💼': 'Geschäft',
	'🏠': 'Zuhause',
	'🍎': 'Apple',
	'🎥': 'Video',
	'🌐': 'Web',
	'📧': 'E-Mail',
	'📰': 'Nachrichten',
	'🎬': 'Unterhaltung',
	'💳': 'Finanzen'
}

# Load data
df = dm.load_user_data('subscriptions.csv', initial_value=pd.DataFrame())

if df is None or df.empty:
	st.info('Keine Abonnements vorhanden.')
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

# Edit mode
if "edit_idx" in st.session_state:

	edit_idx = st.session_state["edit_idx"]

	if edit_idx < len(df):

		row = df.iloc[edit_idx]

		st.subheader(f"Abonnement bearbeiten: {row['name']}")

		with st.form("edit_subscription"):

			name = st.text_input("Name", value=row["name"])

			amount = st.number_input(
				"Betrag (CHF)",
				min_value=0.0,
				value=float(row["amount"]),
				step=0.5
			)

			interval = st.selectbox(
				"Intervall",
				["Monthly", "Yearly", "Quarterly"],
				index=["Monthly", "Yearly", "Quarterly"].index(row["interval"])
			)

			active = st.checkbox(
				"Aktiv",
				value=bool(row["active"])
			)

			icon = st.selectbox(
				'Icon',
				options=list(ICON_OPTIONS.keys()),
				format_func=lambda x: f"{x} {ICON_OPTIONS[x]}",
				index=list(ICON_OPTIONS.keys()).index(row.get('icon', '📱'))
				if row.get('icon') in ICON_OPTIONS else 0
			)

			col1, col2 = st.columns(2)

			if col1.form_submit_button("Speichern"):

				df.at[edit_idx, "name"] = name
				df.at[edit_idx, "amount"] = amount
				df.at[edit_idx, "interval"] = interval
				df.at[edit_idx, "active"] = active
				df.at[edit_idx, "icon"] = icon

				dm.save_user_data(df, "subscriptions.csv")

				del st.session_state["edit_idx"]

				st.success("Abonnement aktualisiert")
				st.rerun()

			if col2.form_submit_button("Abbrechen"):

				del st.session_state["edit_idx"]
				st.rerun()

	st.divider()

# Cards
st.subheader("Alle Abonnements")

def render_subscription_cards(df):

	if df.empty:
		st.info("Keine Abonnements gefunden")
		return

	for idx, row in df.iterrows():

		with st.container():

			col1, col2, col3, col4, col5 = st.columns([0.6, 2, 1.5, 1, 0.8])

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

			edit_col, delete_col = col5.columns(2)

			if edit_col.button("✏️", key=f"edit-{idx}"):

				st.session_state["edit_idx"] = idx
				st.rerun()

			if delete_col.button("🗑️", key=f"delete-{idx}"):

				df = df.drop(index=idx).reset_index(drop=True)

				dm.save_user_data(df, "subscriptions.csv")

				st.success("Abonnement gelöscht")
				st.rerun()

render_subscription_cards(df)

st.divider()

# Summary
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
