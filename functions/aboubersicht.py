import streamlit as st
import pandas as pd
from datetime import date, timedelta


def load_abo_uebersicht_data(dm):
	df = dm.load_user_data(
		'subscriptions.csv',
		initial_value=pd.DataFrame()
	)

	if df is None or df.empty:
		return pd.DataFrame()

	if 'start_date' in df.columns:
		df['start_date'] = pd.to_datetime(
			df['start_date'],
			errors='coerce'
		).dt.date

	df['amount'] = pd.to_numeric(
		df['amount'],
		errors='coerce'
	).fillna(0.0)

	df['active'] = df.get('active', True)

	if 'icon' not in df.columns:
		df['icon'] = '📱'

	return df


def interval_to_text(interval):

	if interval == "Monthly":
		return "Monatlich"

	if interval == "Yearly":
		return "Jährlich"

	if interval == "Quarterly":
		return "Quartalsweise"

	return interval


def format_start_date(value):

	if pd.isna(value):
		return "Kein Startdatum"

	try:
		return value.strftime("%d.%m.%Y")
	except AttributeError:
		return str(value)


def calculate_next_due_date(start_date, interval):

	if pd.isna(start_date) or start_date is None:
		return None

	next_due = start_date
	today = date.today()
	iterations = 0
	max_iterations = 100

	if interval == "Monthly":

		while next_due <= today and iterations < max_iterations:

			try:
				if next_due.month == 12:
					next_due = next_due.replace(
						year=next_due.year + 1,
						month=1
					)

				else:
					next_due = next_due.replace(
						month=next_due.month + 1
					)

			except ValueError:
				next_due = next_due.replace(day=1) + timedelta(days=32)
				next_due = next_due.replace(day=1)

			iterations += 1

	elif interval == "Yearly":

		while next_due <= today and iterations < max_iterations:
			next_due = next_due.replace(
				year=next_due.year + 1
			)

			iterations += 1

	elif interval == "Quarterly":

		while next_due <= today and iterations < max_iterations:
			next_due = next_due + timedelta(days=91)

			iterations += 1

	return next_due


def render_subscription_cards(df):

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

		interval_text = interval_to_text(
			row["interval"]
		)

		start_date_text = format_start_date(
			row.get("start_date", None)
		)

		next_due = calculate_next_due_date(
			row.get("start_date", None),
			row.get("interval", None)
		)

		next_due_text = (
			next_due.strftime("%d.%m.%Y")
			if next_due is not None
			else "Keine Verlängerung berechenbar"
		)

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
				<div class="sub-detail">
					Nächste Verlängerung:<br>
					<strong>{next_due_text}</strong>
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

		st.markdown(
			'<div class="subscription-separator"></div>',
			unsafe_allow_html=True
		)


def render_total_subscription_sum(df):
	st.markdown(
		f"""
		<div class="interval-card">
			<div class="interval-label">Gesamtkosten</div>
			<div class="interval-value">CHF {df['amount'].sum():.2f}</div>
		</div>
		""",
		unsafe_allow_html=True
	)


def render_interval_summary(df):
	monthly = df[df['interval'] == 'Monthly']
	yearly = df[df['interval'] == 'Yearly']
	quarterly = df[df['interval'] == 'Quarterly']

	col1, col2, col3 = st.columns(3)

	with col1:
		st.markdown(
			'<div class="interval-heading">Monatliche Abos</div>',
			unsafe_allow_html=True
		)

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
		st.markdown(
			'<div class="interval-heading">Jährliche Abos</div>',
			unsafe_allow_html=True
		)

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
		st.markdown(
			'<div class="interval-heading">Quartalsweise Abos</div>',
			unsafe_allow_html=True
		)

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