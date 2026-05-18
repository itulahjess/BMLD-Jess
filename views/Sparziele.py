import streamlit as st
import pandas as pd
from datetime import date
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
	max-width: 1100px;
}

/* ---------- TYPOGRAPHY ---------- */

h1 {
	font-size: 58px !important;
	font-weight: 900 !important;
	letter-spacing: -1.8px !important;
	color: #2f3038 !important;
	margin-bottom: 1.2rem !important;
}

h2, h3 {
	color: #2f3038 !important;
	letter-spacing: -0.7px !important;
}

p, label, span {
	color: #2f3038;
}

/* ---------- PAGE INTRO ---------- */

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

/* ---------- METRIC CARDS ---------- */

div[data-testid="stMetric"] {
	background:
		linear-gradient(145deg, rgba(232, 255, 245, 0.95), rgba(255, 255, 255, 0.72));
	padding: 24px 24px;
	border-radius: 24px;
	box-shadow: 0 14px 35px rgba(31, 122, 99, 0.08);
	border: 1px solid rgba(95, 208, 173, 0.17);
	backdrop-filter: blur(12px);
	transition: transform 0.22s ease, box-shadow 0.22s ease, border 0.22s ease;
	min-height: 125px;
}

div[data-testid="stMetric"]:hover {
	transform: translateY(-4px);
	box-shadow: 0 20px 45px rgba(31, 122, 99, 0.14);
	border: 1px solid rgba(95, 208, 173, 0.32);
}

div[data-testid="stMetric"] label {
	font-size: 15px !important;
	font-weight: 800 !important;
	color: #054033 !important;
	line-height: 1.25 !important;
	white-space: normal !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
	font-size: 27px !important;
	font-weight: 900 !important;
	color: #1b5e54 !important;
	letter-spacing: -0.5px;
	white-space: normal !important;
}

div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
	display: none;
}

/* ---------- SECTION TITLES ---------- */

.section-title {
	font-size: 32px;
	font-weight: 900;
	color: #2f3038;
	letter-spacing: -0.9px;
	margin-top: 10px;
	margin-bottom: 18px;
}

.section-subtitle {
	font-size: 15px;
	color: #6b9080;
	margin-top: -8px;
	margin-bottom: 18px;
}

/* ---------- EXPANDER ---------- */

.streamlit-expanderHeader {
	background: rgba(255, 255, 255, 0.72);
	border-radius: 18px;
	border: 1px solid rgba(95, 208, 173, 0.18);
	font-weight: 800;
	color: #054033;
}

div[data-testid="stExpander"] {
	border: none;
	background: transparent;
}

div[data-testid="stExpander"] details {
	background: rgba(255, 255, 255, 0.5);
	border-radius: 22px;
	border: 1px solid rgba(95, 208, 173, 0.18);
	box-shadow: 0 14px 34px rgba(31, 122, 99, 0.06);
}

/* ---------- INPUTS ---------- */

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox div[data-baseweb="select"],
.stCheckbox {
	border-radius: 14px !important;
}

.stTextInput input,
.stNumberInput input,
.stDateInput input {
	background: rgba(255, 255, 255, 0.85) !important;
	border: 1px solid rgba(95, 208, 173, 0.22) !important;
	color: #2f3038 !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stDateInput input:focus {
	border-color: #5fd0ad !important;
	box-shadow: 0 0 0 3px rgba(95, 208, 173, 0.16) !important;
}

/* ---------- STREAMLIT BUTTONS ---------- */

.stButton > button {
	border-radius: 16px !important;
	border: 1px solid rgba(95, 208, 173, 0.26) !important;
	background: rgba(255, 255, 255, 0.78) !important;
	color: #054033 !important;
	font-weight: 800 !important;
	box-shadow: 0 8px 20px rgba(31, 122, 99, 0.08) !important;
	transition: all 0.2s ease !important;
}

.stButton > button:hover {
	transform: translateY(-2px);
	border: 1px solid rgba(95, 208, 173, 0.48) !important;
	box-shadow: 0 14px 28px rgba(31, 122, 99, 0.13) !important;
	background: #e8fff5 !important;
	color: #054033 !important;
}

/* ---------- GOAL ROWS ---------- */

.goal-row-spacer {
	height: 18px;
}

.goal-title {
	font-size: 25px;
	font-weight: 900;
	color: #054033;
	letter-spacing: -0.4px;
	margin-bottom: 12px;
}

.goal-label {
	font-size: 13px;
	font-weight: 800;
	color: #6b9080;
	margin-bottom: 4px;
}

.goal-value {
	font-size: 17px;
	font-weight: 900;
	color: #2f3038;
	letter-spacing: -0.2px;
}

.goal-money {
	font-size: 15px;
	color: #52796f;
	margin-top: 10px;
}

.goal-percent {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 10px 16px;
	border-radius: 999px;
	background: rgba(95, 208, 173, 0.16);
	color: #1f7a63;
	font-weight: 900;
	font-size: 15px;
}

.goal-percent-warning {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 10px 16px;
	border-radius: 999px;
	background: rgba(255, 193, 7, 0.18);
	color: #8a6500;
	font-weight: 900;
	font-size: 15px;
}

.goal-percent-complete {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 10px 16px;
	border-radius: 999px;
	background: rgba(95, 208, 173, 0.25);
	color: #0b5f4d;
	font-weight: 900;
	font-size: 15px;
}

/* ---------- PROGRESS BAR ---------- */

.progress-track {
	width: 100%;
	height: 11px;
	background: rgba(95, 208, 173, 0.12);
	border-radius: 999px;
	overflow: hidden;
	margin-top: 12px;
}

.progress-fill {
	height: 100%;
	border-radius: 999px;
	background: linear-gradient(90deg, #5fd0ad, #1f7a63);
}

.progress-fill-warning {
	height: 100%;
	border-radius: 999px;
	background: linear-gradient(90deg, #ffc857, #d99200);
}

.progress-fill-complete {
	height: 100%;
	border-radius: 999px;
	background: linear-gradient(90deg, #1f7a63, #054033);
}

/* ---------- EDIT BOX ---------- */

.inline-edit-box {
	background:
		linear-gradient(135deg, rgba(232, 255, 245, 0.85), rgba(255, 255, 255, 0.72));
	border: 1px solid rgba(95, 208, 173, 0.2);
	border-radius: 22px;
	padding: 20px;
	margin-top: 18px;
	box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.42);
}

.inline-edit-title {
	font-size: 18px;
	font-weight: 900;
	color: #054033;
	margin-bottom: 10px;
}

/* ---------- EMPTY STATE ---------- */

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

/* ---------- DIVIDER ---------- */

hr {
	border-color: rgba(95, 208, 173, 0.18) !important;
	margin-top: 2rem !important;
	margin-bottom: 2rem !important;
}

/* ---------- RESPONSIVE ---------- */

@media (max-width: 800px) {
	h1 {
		font-size: 42px !important;
	}

	.page-intro {
		padding: 24px;
	}

	div[data-testid="stMetric"] [data-testid="stMetricValue"] {
		font-size: 23px !important;
	}
}
</style>
""", unsafe_allow_html=True)


st.title("Sparziele")

st.markdown("""
<div class="page-intro">
	<div class="page-intro-title">Verwalte deine Sparziele</div>
	<div class="page-intro-text">
		Erstelle Ziele, verfolge deinen Fortschritt und sieh direkt, wie viel du noch sparen musst.
	</div>
</div>
""", unsafe_allow_html=True)


dm = DataManager()

if st.session_state.get('username') is None:
	st.error('Kein Benutzer eingeloggt. Bitte zuerst anmelden.')
	st.stop()


try:
	_rerun = st.rerun
except AttributeError:
	try:
		_rerun = st.experimental_rerun
	except AttributeError:
		def _rerun():
			st.stop()


# Initialize or load savings goals
goals_data = dm.load_user_data(
	'savings_goals.csv',
	initial_value=pd.DataFrame()
)

if goals_data is None or goals_data.empty:
	goals_data = pd.DataFrame(
		columns=[
			'goal_name',
			'target_amount',
			'current_amount',
			'deadline',
			'created_date'
		]
	)


# Convert date columns
if not goals_data.empty:

	if 'deadline' in goals_data.columns:
		goals_data['deadline'] = pd.to_datetime(
			goals_data['deadline'],
			errors='coerce'
		).dt.date

	if 'created_date' in goals_data.columns:
		goals_data['created_date'] = pd.to_datetime(
			goals_data['created_date'],
			errors='coerce'
		).dt.date

	goals_data['target_amount'] = pd.to_numeric(
		goals_data['target_amount'],
		errors='coerce'
	).fillna(0.0)

	goals_data['current_amount'] = pd.to_numeric(
		goals_data['current_amount'],
		errors='coerce'
	).fillna(0.0)


# Metrics
total_target = (
	goals_data['target_amount'].sum()
	if not goals_data.empty else 0
)

total_current = (
	goals_data['current_amount'].sum()
	if not goals_data.empty else 0
)

if total_target > 0:
	overall_progress = (total_current / total_target) * 100
else:
	overall_progress = 0


col1, col2, col3, col4 = st.columns(4)

col1.metric(
	"Anzahl Ziele",
	len(goals_data)
)

col2.metric(
	"Geplant",
	f"CHF {total_target:.2f}"
)

col3.metric(
	"Gespart",
	f"CHF {total_current:.2f}"
)

col4.metric(
	"Fortschritt",
	f"{overall_progress:.0f}%"
)


st.divider()


# Add new goal form
st.markdown('<div class="section-title">Neues Sparziel erstellen</div>', unsafe_allow_html=True)
st.markdown(
	'<div class="section-subtitle">Lege ein neues Ziel fest und erfasse, wie viel du bereits gespart hast.</div>',
	unsafe_allow_html=True
)

with st.expander("Sparziel hinzufügen", expanded=True):

	with st.form("add_goal"):

		col1, col2 = st.columns(2)

		goal_name = col1.text_input(
			"Zielname",
			placeholder="z.B. Urlaub, neuer Laptop, Hochzeit"
		)

		target_amount = col1.number_input(
			"Zielbetrag (CHF)",
			min_value=0.0,
			step=100.0
		)

		current_amount = col2.number_input(
			"Bereits gespart (CHF)",
			min_value=0.0,
			step=10.0
		)

		deadline = col2.date_input(
			"Zieldatum"
		)

		if st.form_submit_button("Sparziel erstellen"):

			if goal_name and target_amount > 0:

				new_goal = pd.DataFrame([{
					'goal_name': goal_name,
					'target_amount': target_amount,
					'current_amount': current_amount,
					'deadline': deadline,
					'created_date': date.today()
				}])

				goals_data = pd.concat(
					[goals_data, new_goal],
					ignore_index=True
				)

				dm.save_user_data(
					goals_data,
					'savings_goals.csv'
				)

				st.success(
					f"Sparziel '{goal_name}' erstellt!"
				)

				_rerun()

			else:
				st.error(
					"Bitte füllen Sie alle erforderlichen Felder aus"
				)


st.divider()


# Display goals
st.markdown('<div class="section-title">Ihre Sparziele</div>', unsafe_allow_html=True)

if not goals_data.empty:

	for idx, row in goals_data.iterrows():

		target = float(row['target_amount'])
		current = float(row['current_amount'])

		if target > 0:
			progress = (current / target) * 100
		else:
			progress = 0

		progress_width = min(progress, 100)
		remaining = target - current

		if progress >= 100:
			percent_class = "goal-percent-complete"
			progress_class = "progress-fill-complete"
		elif progress >= 75:
			percent_class = "goal-percent-warning"
			progress_class = "progress-fill-warning"
		else:
			percent_class = "goal-percent"
			progress_class = "progress-fill"

		deadline_value = row.get('deadline', None)

		if pd.isna(deadline_value):
			deadline_text = "Kein Zieldatum"
		else:
			try:
				deadline_text = deadline_value.strftime('%d.%m.%Y')
			except AttributeError:
				deadline_text = str(deadline_value)

		with st.container():

			col1, col2, col3 = st.columns([2.2, 1.2, 0.8])

			with col1:
				st.markdown(
					f"""
					<div class="goal-title">{row['goal_name']}</div>
					<div class="progress-track">
						<div class="{progress_class}" style="width: {progress_width}%;"></div>
					</div>
					<div class="goal-money">
						CHF {current:.2f} von CHF {target:.2f}
					</div>
					""",
					unsafe_allow_html=True
				)

			with col2:
				st.markdown(
					f"""
					<div class="goal-label">Zieldatum</div>
					<div class="goal-value">{deadline_text}</div>
					<br>
					<div class="goal-label">Noch zu sparen</div>
					<div class="goal-value">CHF {remaining:.2f}</div>
					""",
					unsafe_allow_html=True
				)

			with col3:
				st.markdown(
					f'<div class="{percent_class}">{progress:.0f}%</div>',
					unsafe_allow_html=True
				)

			edit_col, delete_col = st.columns(2)

			if edit_col.button(
				"✏️ Bearbeiten",
				key=f"edit_goal_{idx}"
			):
				st.session_state[f"edit_goal_{idx}"] = True
				_rerun()

			if delete_col.button(
				"🗑️ Löschen",
				key=f"delete_goal_{idx}"
			):
				goals_data = goals_data.drop(
					index=idx
				).reset_index(drop=True)

				dm.save_user_data(
					goals_data,
					'savings_goals.csv'
				)

				st.success("Sparziel gelöscht!")

				_rerun()


			# Edit form
			if st.session_state.get(f"edit_goal_{idx}", False):

				st.markdown(
					"""
					<div class="inline-edit-box">
						<div class="inline-edit-title">Fortschritt aktualisieren</div>
					</div>
					""",
					unsafe_allow_html=True
				)

				with st.form(f"edit_goal_form_{idx}"):

					new_current = st.number_input(
						"Aktuell gespart (CHF)",
						value=float(row['current_amount']),
						min_value=0.0,
						step=10.0,
						key=f"edit_amount_{idx}"
					)

					col_save, col_cancel = st.columns(2)

					if col_save.form_submit_button(
						"Aktualisieren",
						key=f"update_goal_{idx}"
					):
						goals_data.at[
							idx,
							'current_amount'
						] = new_current

						dm.save_user_data(
							goals_data,
							'savings_goals.csv'
						)

						st.success("Sparziel aktualisiert!")

						del st.session_state[f"edit_goal_{idx}"]

						_rerun()

					if col_cancel.form_submit_button("Abbrechen"):
						del st.session_state[f"edit_goal_{idx}"]
						_rerun()

			st.markdown('<div class="goal-row-spacer"></div>', unsafe_allow_html=True)

else:
	st.markdown("""
	<div class="empty-state">
		<div class="empty-title">Keine Sparziele vorhanden</div>
		<div>Erstelle oben dein erstes Sparziel, um deinen Fortschritt zu verfolgen.</div>
	</div>
	""", unsafe_allow_html=True)