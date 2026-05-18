import streamlit as st
import pandas as pd
from utils.data_manager import DataManager

st.markdown("""
<style>
.header {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 45px;
	margin-top: 10px;
	margin-bottom: 35px;
}

.logo {
	width: 360px;
}

.app-title {
	font-size: 48px;
	font-weight: 900;
	color: #2f3038;
	margin-bottom: 5px;
}

.subtitle {
	text-align: center;
	font-size: 18px;
	color: #52796f;
	margin-bottom: 35px;
}

.hero-box {
	background: linear-gradient(135deg, #e8fff5, #f6fffb);
	padding: 35px;
	border-radius: 28px;
	margin-bottom: 30px;
	text-align: center;
	box-shadow: 0 8px 20px rgba(0,0,0,0.06);
}

.hero-title {
	font-size: 32px;
	font-weight: 800;
	color: #054033;
}

.hero-text {
	font-size: 17px;
	color: #3b5f58;
	margin-top: 10px;
}

div[data-testid="stMetric"] {
	background-color: #e8fff5;
	padding: 22px;
	border-radius: 20px;
	box-shadow: 0 5px 14px rgba(0,0,0,0.05);
}

div[data-testid="stMetric"] * {
	font-size: 22px !important;
	font-weight: 800 !important;
	color: #054033 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
	font-size: 34px !important;
	font-weight: 900 !important;
	color: #1b5e54 !important;
}

.info-card {
	background: white;
	border: 1px solid #dff5ec;
	padding: 24px;
	border-radius: 22px;
	text-align: center;
	box-shadow: 0 5px 14px rgba(0,0,0,0.04);
	height: 150px;
}

.info-icon {
	font-size: 34px;
	margin-bottom: 8px;
}

.info-title {
	font-size: 20px;
	font-weight: 800;
	color: #054033;
}

.info-text {
	font-size: 14px;
	color: #52796f;
	margin-top: 6px;
}

.footer {
	margin-top: 45px;
	text-align: center;
	font-size: 12px;
	color: #6b9080;
}
</style>
""", unsafe_allow_html=True)

dm = DataManager()

subs = dm.load_user_data(
	'subscriptions.csv',
	initial_value=pd.DataFrame()
)

if subs is None or subs.empty:
	subs = pd.DataFrame(columns=['name', 'amount', 'interval', 'active'])

subs['amount'] = pd.to_numeric(
	subs.get('amount', 0),
	errors='coerce'
).fillna(0.0)

subs['active'] = subs.get('active', True)

active_subs = subs[subs['active'] == True]

monthly_cost = 0
yearly_cost = 0

for _, row in active_subs.iterrows():

	if row['interval'] == 'Monthly':
		monthly_cost += float(row['amount'])
		yearly_cost += float(row['amount']) * 12

	elif row['interval'] == 'Yearly':
		yearly_cost += float(row['amount'])

	elif row['interval'] == 'Quarterly':
		monthly_cost += float(row['amount']) / 3
		yearly_cost += float(row['amount']) * 4

name = st.session_state.get("name", "User")

st.markdown("""
<div class="subtitle">Deine Abos, Kosten und Budgets immer im Blick</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero-box">
	<div class="hero-title">Hallo {name} 👋</div>
	<div class="hero-text">
		Willkommen zurück! Hier siehst du eine schnelle Übersicht über deine laufenden Abonnements.
	</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
	st.metric("Monatliche Kosten", f"CHF {monthly_cost:.2f}")

with col2:
	st.metric("Jährliche Kosten", f"CHF {yearly_cost:.2f}")

with col3:
	st.metric("Aktive Abos", len(active_subs))

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
	st.markdown("""
	<div class="info-card">
		<div class="info-icon">📋</div>
		<div class="info-title">Aboverwaltung</div>
		<div class="info-text">Füge neue Abos hinzu und verwalte bestehende Einträge.</div>
	</div>
	""", unsafe_allow_html=True)

with c2:
	st.markdown("""
	<div class="info-card">
		<div class="info-icon">📊</div>
		<div class="info-title">Aboübersicht</div>
		<div class="info-text">Sieh deine monatlichen und jährlichen Kosten auf einen Blick.</div>
	</div>
	""", unsafe_allow_html=True)

with c3:
	st.markdown("""
	<div class="info-card">
		<div class="info-icon">💰</div>
		<div class="info-title">Budgetplaner</div>
		<div class="info-text">Plane dein Budget und behalte deine Ausgaben im Griff.</div>
	</div>
	""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
	Diese App wurde entwickelt von:<br>
	Jessica Itulah · itulajes@students.zhaw.ch<br>
	Medhani Kathirkamanathan · kathimed@students.zhaw.ch<br>
	Michelle Assadi Rad · assadmic@students.zhaw.ch
</div>
""", unsafe_allow_html=True)