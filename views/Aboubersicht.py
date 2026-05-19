import streamlit as st
import pandas as pd
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


dm = DataManager()

if st.session_state.get('username') is None:
	st.error('Kein Benutzer eingeloggt. Bitte zuerst anmelden.')
	st.stop()

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

from functions.aboübersicht import _interval_to_text

from functions.aboübersicht import _format_start_date

from functions.aboübersicht import render_subscription_cards