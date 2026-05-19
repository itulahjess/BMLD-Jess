import streamlit as st
import pandas as pd
from utils.data_manager import DataManager

dm = DataManager()
df = dm.load_user_data('subscriptions.csv', initial_value=pd.DataFrame())

def _interval_to_text(interval):

	if interval == "Monthly":
		return "Monatlich"

	if interval == "Yearly":
		return "Jährlich"

	if interval == "Quarterly":
		return "Quartalsweise"

	return interval


def _format_start_date(value):

	if pd.isna(value):
		return "Kein Startdatum"

	try:
		return value.strftime("%d.%m.%Y")
	except AttributeError:
		return str(value)
	

def render_subscription_cards(df, editable=True):

	if df.empty:
		st.markdown("""
		<div class="empty-state">
			<div class="empty-title">Keine Abonnements gefunden</div>
			<div>Für diese Ansicht gibt es aktuell keine Einträge.</div>
		</div>
		""", unsafe_allow_html=True)
		return

	for idx, row in df.iterrows():

		icon = row.get("icon", "📱")
		interval_text = _interval_to_text(row["interval"])
		start_date_text = _format_start_date(row.get("start_date", None))

		status_class = (
			"status-active"
			if row["active"]
			else "status-inactive"
		)

		status_text = (
			"✅ Aktiv"
			if row["active"]
			else "❌ Inaktiv"
		)

		col1, col2, col3, col4 = st.columns(
			[0.75, 2.2, 1.35, 1.1]
		)

		with col1:
			st.markdown(
				f"<div class='sub-icon'>{icon}</div>",
				unsafe_allow_html=True
			)

		with col2:
			st.markdown(
				f"""
				<div class="sub-name">{row['name']}</div>
				<div class="sub-detail">
					Startdatum:<br>
					<strong>{start_date_text}</strong>
				</div>
				""",
				unsafe_allow_html=True
			)

		with col3:
			st.markdown(
				f"""
				<div class="sub-price">CHF {row['amount']:.2f}</div>
				<div class="sub-interval">{interval_text}</div>
				""",
				unsafe_allow_html=True
			)

		with col4:
			st.markdown(
				f'<span class="{status_class}">{status_text}</span>',
				unsafe_allow_html=True
			)

		st.markdown('<div class="subscription-separator"></div>', unsafe_allow_html=True)


st.markdown('<div class="section-title">Alle Abonnements</div>', unsafe_allow_html=True)

render_subscription_cards(df)


st.divider()

st.markdown('<div class="section-title">Zusammenfassung nach Intervall</div>', unsafe_allow_html=True)


monthly = df[df['interval'] == 'Monthly']
yearly = df[df['interval'] == 'Yearly']
quarterly = df[df['interval'] == 'Quarterly']

col1, col2, col3 = st.columns(3)

with col1:
	st.markdown('<div class="interval-heading">Monatliche Abos</div>', unsafe_allow_html=True)
	st.markdown(
		f"""
		<div class="interval-card">
			<div class="interval-label">Anzahl</div>
			<div class="interval-value">{len(monthly)}</div>
		</div>
		<div class="interval-card">
			<div class="interval-label">Kosten / Monat</div>
			<div class="interval-value">CHF {monthly['amount'].sum():.2f}</div>
		</div>
		""",
		unsafe_allow_html=True
	)

with col2:
	st.markdown('<div class="interval-heading">Jährliche Abos</div>', unsafe_allow_html=True)
	st.markdown(
		f"""
		<div class="interval-card">
			<div class="interval-label">Anzahl</div>
			<div class="interval-value">{len(yearly)}</div>
		</div>
		<div class="interval-card">
			<div class="interval-label">Kosten / Jahr</div>
			<div class="interval-value">CHF {yearly['amount'].sum():.2f}</div>
		</div>
		""",
		unsafe_allow_html=True
	)

with col3:
	st.markdown('<div class="interval-heading">Quartalsweise Abos</div>', unsafe_allow_html=True)
	st.markdown(
		f"""
		<div class="interval-card">
			<div class="interval-label">Anzahl</div>
			<div class="interval-value">{len(quarterly)}</div>
		</div>
		<div class="interval-card">
			<div class="interval-label">Kosten / Quartal</div>
			<div class="interval-value">CHF {quarterly['amount'].sum():.2f}</div>
		</div>
		""",
		unsafe_allow_html=True
	)