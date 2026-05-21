import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.data_manager import DataManager


st.markdown("""
<style>
.stApp {
	background:
		radial-gradient(circle at top right, rgba(116, 222, 188, 0.22), transparent 34%),
		radial-gradient(circle at bottom left, rgba(203, 245, 229, 0.35), transparent 38%),
		#f5fbf8;
	color: #2f3038;
}

.block-container {
	padding-top: 2.2rem;
	padding-bottom: 3rem;
	max-width: 1100px;
}

h1 {
	font-size: 52px !important;
	font-weight: 800 !important;
	letter-spacing: -1.8px !important;
	color: #2f3038 !important;
	margin-bottom: 1.2rem !important;
}

h2, h3 {
	color: #2f3038 !important;
	letter-spacing: -0.7px !important;
}

.page-intro {
	position: relative;
	overflow: hidden;
	background:
		linear-gradient(135deg, rgba(232, 255, 245, 0.96), rgba(255, 255, 255, 0.76));
	padding: 28px 32px;
	border-radius: 28px;
	border: 1px solid rgba(95, 208, 173, 0.18);
	box-shadow: 0 18px 45px rgba(31, 122, 99, 0.08);
	margin-bottom: 30px;
	backdrop-filter: blur(14px);
}

.page-intro::before {
	content: "";
	position: absolute;
	width: 190px;
	height: 190px;
	border-radius: 50%;
	background: rgba(95, 208, 173, 0.14);
	top: -80px;
	right: -60px;
}

.page-intro-title {
	position: relative;
	z-index: 1;
	font-size: 24px;
	font-weight: 900;
	color: #054033;
	margin-bottom: 6px;
}

.page-intro-text {
	position: relative;
	z-index: 1;
	font-size: 15px;
	color: #52796f;
	line-height: 1.5;
}

.section-title {
	font-size: 32px;
	font-weight: 900;
	color: #2f3038;
	letter-spacing: -0.9px;
	margin-top: 10px;
	margin-bottom: 18px;
}

.sub-icon {
	width: 54px;
	height: 54px;
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 18px;
	background: linear-gradient(145deg, rgba(232, 255, 245, 1), rgba(255, 255, 255, 0.75));
	font-size: 28px;
	box-shadow:
		inset 0 0 0 1px rgba(95, 208, 173, 0.16),
		0 10px 22px rgba(31, 122, 99, 0.08);
}

.sub-name {
	font-size: 20px;
	font-weight: 900;
	color: #054033;
	margin-bottom: 4px;
	letter-spacing: -0.2px;
}

.sub-detail {
	font-size: 14px;
	color: #6b9080;
	line-height: 1.45;
}

.sub-price {
	font-size: 19px;
	font-weight: 900;
	color: #2f3038;
	margin-bottom: 4px;
}

.sub-interval {
	font-size: 14px;
	color: #7b8790;
}

.status-active {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 8px 13px;
	border-radius: 999px;
	background: rgba(95, 208, 173, 0.16);
	color: #1f7a63;
	font-weight: 800;
	font-size: 14px;
}

.status-inactive {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 8px 13px;
	border-radius: 999px;
	background: rgba(255, 120, 120, 0.13);
	color: #a13a3a;
	font-weight: 800;
	font-size: 14px;
}

.subscription-separator {
	height: 1px;
	background: rgba(95, 208, 173, 0.14);
	margin: 22px 0;
}

.interval-heading {
	font-size: 18px;
	font-weight: 900;
	color: #054033;
	margin-bottom: 12px;
}

.interval-card {
	background: rgba(255, 255, 255, 0.78);
	border: 1px solid rgba(95, 208, 173, 0.18);
	border-radius: 26px;
	padding: 22px;
	margin-bottom: 16px;
	box-shadow: 0 14px 34px rgba(31, 122, 99, 0.07);
	backdrop-filter: blur(12px);
	transition: transform 0.22s ease, box-shadow 0.22s ease, border 0.22s ease;
}

.interval-card:hover {
	transform: translateY(-4px);
	box-shadow: 0 20px 45px rgba(31, 122, 99, 0.13);
	border: 1px solid rgba(95, 208, 173, 0.34);
}

.interval-label {
	font-size: 14px;
	font-weight: 800;
	color: #6b9080;
	margin-bottom: 4px;
}

.interval-value {
	font-size: 25px;
	font-weight: 900;
	color: #1b5e54;
	letter-spacing: -0.5px;
}

.empty-state {
	background: rgba(255, 255, 255, 0.72);
	border: 1px dashed rgba(95, 208, 173, 0.42);
	border-radius: 24px;
	padding: 30px;
	text-align: center;
	color: #52796f;
	margin-top: 12px;
}

.empty-title {
	font-size: 21px;
	font-weight: 900;
	color: #054033;
	margin-bottom: 6px;
}

hr {
	border-color: rgba(95, 208, 173, 0.18) !important;
	margin-top: 2rem !important;
	margin-bottom: 2rem !important;
}

@media (max-width: 800px) {
	h1 {
		font-size: 42px !important;
	}

	.page-intro {
		padding: 24px;
	}
}
</style>
""", unsafe_allow_html=True)


st.title("Aboübersicht")

st.markdown("""
<div class="page-intro">
	<div class="page-intro-title">Deine Abos auf einen Blick</div>
	<div class="page-intro-text">
		Hier siehst du deine Abonnements und darunter eine klare Zusammenfassung nach Intervall.
	</div>
</div>
""", unsafe_allow_html=True)


dm = DataManager(
	fs_protocol='webdav',
	fs_root_folder="bmldjm"
)

if not st.session_state.get("authentication_status"):
    st.warning("Bitte zuerst anmelden")
    st.switch_page("app.py")

df = dm.load_user_data('subscriptions.csv', initial_value=pd.DataFrame())

if df is None or df.empty:
	st.markdown("""
	<div class="empty-state">
		<div class="empty-title">Keine Abonnements vorhanden</div>
		<div>Füge zuerst ein Abo hinzu, damit hier deine Übersicht angezeigt wird.</div>
	</div>
	""", unsafe_allow_html=True)
	st.stop()


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

budget_data = dm.load_user_data(
	'budget.csv',
	initial_value=pd.DataFrame()
)

if budget_data is None or budget_data.empty:
	budget_data = pd.DataFrame(
		columns=[
			'planned_amount',
			'spent_amount'
		]
	)

budget_data['planned_amount'] = pd.to_numeric(
	budget_data.get('planned_amount', 0),
	errors='coerce'
).fillna(0.0)

budget_data['spent_amount'] = pd.to_numeric(
	budget_data.get('spent_amount', 0),
	errors='coerce'
).fillna(0.0)

budget_total = budget_data['planned_amount'].sum()

goals_data = dm.load_user_data(
	'savings_goals.csv',
	initial_value=pd.DataFrame()
)

if goals_data is None or goals_data.empty:
	goals_data = pd.DataFrame(
		columns=[
			'goal_name',
			'target_amount',
			'current_amount'
		]
	)

if 'target_amount' in goals_data.columns:
	goals_data['target_amount'] = pd.to_numeric(
		goals_data['target_amount'],
		errors='coerce'
	).fillna(0.0)

if 'current_amount' in goals_data.columns:
	goals_data['current_amount'] = pd.to_numeric(
		goals_data['current_amount'],
		errors='coerce'
	).fillna(0.0)

savings_needed = max(
	goals_data['target_amount'].sum() - goals_data['current_amount'].sum(),
	0.0
)

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


def _calculate_next_due_date(start_date, interval):

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
					next_due = next_due.replace(year=next_due.year + 1, month=1)
				else:
					next_due = next_due.replace(month=next_due.month + 1)
			except ValueError:
				next_due = next_due.replace(day=1) + timedelta(days=32)
				next_due = next_due.replace(day=1)
			iterations += 1

	elif interval == "Yearly":
		while next_due <= today and iterations < max_iterations:
			next_due = next_due.replace(year=next_due.year + 1)
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
		interval_text = _interval_to_text(row["interval"])
		start_date_text = _format_start_date(row.get("start_date", None))
		next_due = _calculate_next_due_date(row.get("start_date", None), row.get("interval", None))
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

		st.markdown('<div class="subscription-separator"></div>', unsafe_allow_html=True)


st.markdown('<div class="section-title">Alle Abonnements</div>', unsafe_allow_html=True)

render_subscription_cards(df)

budget_spent = budget_data['spent_amount'].sum() + df[df['active'] == True]['amount'].sum()
remaining_budget = budget_total - budget_spent
if remaining_budget < 0:
	remaining_budget = 0.0


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
