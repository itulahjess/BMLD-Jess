import streamlit as st
import pandas as pd
from utils.data_manager import DataManager

st.markdown("""
<style>
/* ---------- GLOBAL PAGE STYLE ---------- */

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
	max-width: 1350px;
}

/* ---------- HEADER ---------- */

.header {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 45px;
	margin-top: 10px;
	margin-bottom: 35px;
}

.logo {
	width: 500px;
	border-radius: 18px;
	filter: drop-shadow(0 12px 25px rgba(0, 0, 0, 0.06));
}

.app-title {
	font-size: 58px;
	font-weight: 800;
	color: #2f3038;
	margin-bottom: 5px;
	letter-spacing: -1.5px;
	line-height: 1.05;
}

.subtitle {
	text-align: center;
	font-size: 58px;
	color: #52796f;
	margin-bottom: 35px;
}

/* ---------- HERO BOX ---------- */

.hero-box {
	position: relative;
	overflow: hidden;
	background:
		linear-gradient(135deg, rgba(232, 255, 245, 0.95), rgba(255, 255, 255, 0.78));
	padding: 42px 35px;
	border-radius: 32px;
	margin-bottom: 34px;
	text-align: center;
	box-shadow: 0 18px 45px rgba(31, 122, 99, 0.09);
	border: 1px solid rgba(95, 208, 173, 0.18);
	backdrop-filter: blur(14px);
	transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.hero-box:hover {
	transform: translateY(-3px);
	box-shadow: 0 24px 55px rgba(31, 122, 99, 0.13);
}

.hero-box::before {
	content: "";
	position: absolute;
	width: 230px;
	height: 230px;
	border-radius: 50%;
	background: rgba(95, 208, 173, 0.17);
	top: -90px;
	right: -70px;
	filter: blur(4px);
}

.hero-box::after {
	content: "";
	position: absolute;
	width: 160px;
	height: 160px;
	border-radius: 50%;
	background: rgba(223, 248, 236, 0.9);
	bottom: -80px;
	left: -50px;
	filter: blur(8px);
}

.hero-title {
	position: relative;
	z-index: 1;
	font-size: 34px;
	font-weight: 900;
	color: #054033;
	letter-spacing: -0.5px;
}

.hero-text {
	position: relative;
	z-index: 1;
	font-size: 17px;
	color: #3b5f58;
	margin-top: 12px;
}

/* ---------- METRIC CARDS ---------- */

div[data-testid="stMetric"] {
	background:
		linear-gradient(145deg, rgba(232, 255, 245, 0.95), rgba(255, 255, 255, 0.72));
	padding: 24px 26px;
	border-radius: 24px;
	box-shadow: 0 14px 35px rgba(31, 122, 99, 0.08);
	border: 1px solid rgba(95, 208, 173, 0.17);
	backdrop-filter: blur(12px);
	transition: transform 0.22s ease, box-shadow 0.22s ease, border 0.22s ease;
	min-height: 120px;
}

div[data-testid="stMetric"]:hover {
	transform: translateY(-4px);
	box-shadow: 0 20px 45px rgba(31, 122, 99, 0.14);
	border: 1px solid rgba(95, 208, 173, 0.32);
}

div[data-testid="stMetric"] label {
	font-size: 16px !important;
	font-weight: 800 !important;
	color: #054033 !important;
	white-space: normal !important;
	line-height: 1.25 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
	font-size: 30px !important;
	font-weight: 900 !important;
	color: #1b5e54 !important;
	letter-spacing: -0.5px;
	white-space: normal !important;
}

div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
	display: none;
}

/* ---------- INFO CARDS ---------- */

.info-card {
	position: relative;
	overflow: hidden;
	background: rgba(255, 255, 255, 0.82);
	border: 1px solid rgba(95, 208, 173, 0.18);
	padding: 28px 20px;
	border-radius: 26px;
	text-align: center;
	box-shadow: 0 14px 34px rgba(31, 122, 99, 0.07);
	height: 190px;
	backdrop-filter: blur(12px);
	transition: transform 0.25s ease, box-shadow 0.25s ease, border 0.25s ease;
}

.info-card:hover {
	transform: translateY(-6px);
	box-shadow: 0 22px 48px rgba(31, 122, 99, 0.13);
	border: 1px solid rgba(95, 208, 173, 0.34);
}

.info-card::before {
	content: "";
	position: absolute;
	top: 0;
	left: -80%;
	width: 60%;
	height: 100%;
	background: linear-gradient(
		90deg,
		transparent,
		rgba(255, 255, 255, 0.55),
		transparent
	);
	transform: skewX(-18deg);
	transition: left 0.65s ease;
}

.info-card:hover::before {
	left: 125%;
}

.info-icon {
	font-size: 36px;
	margin-bottom: 10px;
	filter: drop-shadow(0 8px 12px rgba(31, 122, 99, 0.12));
}

.info-title {
	font-size: 19px;
	font-weight: 900;
	color: #054033;
	letter-spacing: -0.2px;
	line-height: 1.2;
}

.info-text {
	font-size: 13px;
	color: #52796f;
	margin-top: 8px;
	line-height: 1.45;
}

/* ---------- INFO CARD BUTTONS ---------- */

.stButton > button {
	position: relative;
	overflow: hidden;
	background: rgba(255, 255, 255, 0.82) !important;
	border: 1px solid rgba(95, 208, 173, 0.18) !important;
	padding: 28px 20px !important;
	border-radius: 26px !important;
	text-align: center;
	box-shadow: 0 14px 34px rgba(31, 122, 99, 0.07) !important;
	height: 190px !important;
	backdrop-filter: blur(12px);
	transition: transform 0.25s ease, box-shadow 0.25s ease, border 0.25s ease !important;
	width: 100% !important;
	color: #054033 !important;
	white-space: pre-wrap !important;
	word-wrap: break-word !important;
	line-height: 1.35 !important;
}

.stButton > button p {
	font-size: 15px !important;
	font-weight: 400 !important; /* description normal */
	line-height: 1.35 !important;
	color: #054033 !important;
	white-space: pre-line !important;
	margin: 0 !important;
}

/* ONLY first line (emoji + title) */
.stButton > button p::first-line {
	font-size: 26px !important;
	font-weight: 900 !important;
	-webkit-text-stroke: 0.5px #054033 !important;
}
			
.stButton > button:hover {
	transform: translateY(-6px) !important;
	box-shadow: 0 22px 48px rgba(31, 122, 99, 0.13) !important;
	border: 1px solid rgba(95, 208, 173, 0.34) !important;
	background: rgba(255, 255, 255, 0.82) !important;
}

/* ---------- FOOTER ---------- */

.footer {
	margin-top: 52px;
	text-align: center;
	font-size: 12px;
	color: #6b9080;
	line-height: 1.55;
	opacity: 0.9;
}

/* ---------- RESPONSIVE ---------- */

@media (max-width: 1000px) {
	.info-card {
		height: 175px;
		margin-bottom: 14px;
	}

	.info-title {
		font-size: 18px;
	}
}

@media (max-width: 900px) {
	.hero-title {
		font-size: 28px;
	}

	.hero-text {
		font-size: 15px;
	}

	div[data-testid="stMetric"] [data-testid="stMetricValue"] {
		font-size: 26px !important;
	}

	.info-card {
		height: auto;
		margin-bottom: 14px;
	}
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


# Nur echte monatliche Abos
monthly_cost = active_subs[
	active_subs['interval'] == 'Monthly'
]['amount'].sum()

# Nur echte jährliche Abos
yearly_cost = active_subs[
	active_subs['interval'] == 'Yearly'
]['amount'].sum()


name = st.session_state.get("name", "User")

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


c1, c2, c3, c4 = st.columns(4)

with c1:
	if st.button("📋 Aboverwaltung\nFüge neue Abos hinzu und verwalte bestehende Einträge.", key="btn_aboverwaltung", use_container_width=True):
		st.switch_page("views/Aboverwaltung.py")

with c2:
	if st.button("📊 Aboübersicht\nSieh deine monatlichen und jährlichen Kosten auf einen Blick.", key="btn_aboubersicht", use_container_width=True):
		st.switch_page("views/Aboubersicht.py")

with c3:
	if st.button("💰 Budgetplaner\nPlane dein Budget und behalte deine Ausgaben im Griff.", key="btn_budgetplaner", use_container_width=True):
		st.switch_page("views/Budgetplaner.py")

with c4:
	if st.button("🎯 Sparziele\nErstelle Sparziele und verfolge deinen Fortschritt.", key="btn_sparziele", use_container_width=True):
		st.switch_page("views/Sparziele.py")


st.markdown("""
<div class="footer">
	Diese App wurde entwickelt von:<br>
	Jessica Itulah · itulajes@students.zhaw.ch<br>
	Medhani Kathirkamanathan · kathimed@students.zhaw.ch<br>
	Michelle Assadi Rad · assadmic@students.zhaw.ch
</div>
""", unsafe_allow_html=True)