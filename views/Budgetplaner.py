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

/* ---------- BUDGET CARDS ---------- */

.budget-card {
	background: rgba(255, 255, 255, 0.82);
	border: 1px solid rgba(95, 208, 173, 0.18);
	border-radius: 26px;
	padding: 22px 24px;
	margin-bottom: 16px;
	box-shadow: 0 14px 34px rgba(31, 122, 99, 0.07);
	backdrop-filter: blur(12px);
	transition: transform 0.24s ease, box-shadow 0.24s ease, border 0.24s ease;
}

.budget-card:hover {
	transform: translateY(-4px);
	box-shadow: 0 22px 48px rgba(31, 122, 99, 0.13);
	border: 1px solid rgba(95, 208, 173, 0.34);
}

.budget-category {
	font-size: 21px;
	font-weight: 900;
	color: #054033;
	letter-spacing: -0.3px;
	margin-bottom: 6px;
}

.budget-label {
	font-size: 13px;
	font-weight: 800;
	color: #6b9080;
	margin-bottom: 4px;
}

.budget-value {
	font-size: 18px;
	font-weight: 900;
	color: #2f3038;
	letter-spacing: -0.2px;
}

.budget-percent {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 8px 13px;
	border-radius: 999px;
	background: rgba(95, 208, 173, 0.16);
	color: #1f7a63;
	font-weight: 900;
	font-size: 14px;
}

.budget-percent-warning {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 8px 13px;
	border-radius: 999px;
	background: rgba(255, 193, 7, 0.18);
	color: #8a6500;
	font-weight: 900;
	font-size: 14px;
}

.budget-percent-danger {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 8px 13px;
	border-radius: 999px;
	background: rgba(255, 120, 120, 0.14);
	color: #a13a3a;
	font-weight: 900;
	font-size: 14px;
}

/* ---------- PROGRESS BAR ---------- */

.progress-track {
	width: 100%;
	height: 10px;
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

.progress-fill-danger {
	height: 100%;
	border-radius: 999px;
	background: linear-gradient(90deg, #ff8a8a, #c94c4c);
}

/* ---------- EDIT BOX ---------- */

.edit-box {
	background:
		linear-gradient(135deg, rgba(232, 255, 245, 0.95), rgba(255, 255, 255, 0.78));
	border: 1px solid rgba(95, 208, 173, 0.2);
	border-radius: 28px;
	padding: 24px 28px;
	margin-bottom: 24px;
	box-shadow: 0 18px 45px rgba(31, 122, 99, 0.08);
}

.edit-title {
	font-size: 25px;
	font-weight: 900;
	color: #054033;
	margin-bottom: 6px;
}

.edit-subtitle {
	font-size: 14px;
	color: #52796f;
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

	.budget-card {
		padding: 18px;
	}
}
</style>
""", unsafe_allow_html=True)


st.title("Budgetplaner")

st.markdown("""
<div class="page-intro">
	<div class="page-intro-title">Plane dein monatliches Budget</div>
	<div class="page-intro-text">
		Erstelle Budgetkategorien, verfolge deine Ausgaben und sieh sofort, wie viel Budget noch verfügbar ist.
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


# Budgetdaten laden
budget_data = dm.load_user_data(
	'budget.csv',
	initial_value=pd.DataFrame()
)

if budget_data is None or budget_data.empty:
	budget_data = pd.DataFrame(
		columns=[
			'category',
			'planned_amount',
			'spent_amount',
			'date'
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


# Abos laden
subs = dm.load_user_data(
	'subscriptions.csv',
	initial_value=pd.DataFrame()
)

if subs is not None and not subs.empty:

	subs['amount'] = pd.to_numeric(
		subs['amount'],
		errors='coerce'
	).fillna(0.0)

	subs['active'] = subs.get('active', True)

	monthly_sub_cost = subs[
		subs['active'] == True
	]['amount'].sum()

else:
	monthly_sub_cost = 0


# Übersicht
total_budget = (
	budget_data['planned_amount'].sum()
	if not budget_data.empty else 0
)

total_spent = (
	budget_data['spent_amount'].sum()
	if not budget_data.empty else 0
) + monthly_sub_cost

remaining = total_budget - total_spent


col1, col2, col3, col4 = st.columns(4)

col1.metric(
	"Abos / Monat",
	f"CHF {monthly_sub_cost:.2f}"
)

col2.metric(
	"Gesamtbudget",
	f"CHF {total_budget:.2f}"
)

col3.metric(
	"Ausgegeben",
	f"CHF {total_spent:.2f}"
)

col4.metric(
	"Verbleibend",
	f"CHF {remaining:.2f}"
)


st.divider()


# Neue Kategorie
st.markdown('<div class="section-title">Budgetkategorien</div>', unsafe_allow_html=True)
st.markdown(
	'<div class="section-subtitle">Füge neue Kategorien hinzu, um dein Budget genauer aufzuteilen.</div>',
	unsafe_allow_html=True
)

with st.expander("Neue Budgetkategorie hinzufügen"):

	with st.form("add_budget"):

		cat_col, amount_col = st.columns(2)

		category = cat_col.text_input("Kategorie")

		planned_amount = amount_col.number_input(
			"Geplanter Betrag (CHF)",
			min_value=0.0,
			step=1.0
		)

		if st.form_submit_button("Kategorie hinzufügen"):

			if category:

				new_entry = pd.DataFrame([{
					'category': category,
					'planned_amount': planned_amount,
					'spent_amount': 0.0,
					'date': date.today()
				}])

				budget_data = pd.concat(
					[budget_data, new_entry],
					ignore_index=True
				)

				dm.save_user_data(
					budget_data,
					'budget.csv'
				)

				st.success(
					f"Kategorie '{category}' hinzugefügt"
				)

				_rerun()

			else:
				st.error(
					"Bitte geben Sie eine Kategorie ein"
				)


st.divider()


# Bearbeiten
if "edit_budget_idx" in st.session_state:

	edit_idx = st.session_state["edit_budget_idx"]

	if edit_idx < len(budget_data):

		row = budget_data.iloc[edit_idx]

		st.markdown(
			f"""
			<div class="edit-box">
				<div class="edit-title">Kategorie bearbeiten: {row['category']}</div>
				<div class="edit-subtitle">
					Aktualisiere den geplanten Betrag oder erfasse deine bisherigen Ausgaben.
				</div>
			</div>
			""",
			unsafe_allow_html=True
		)

		with st.form("edit_budget"):

			new_category = st.text_input(
				"Kategorie",
				value=row["category"]
			)

			new_planned_amount = st.number_input(
				"Geplanter Betrag (CHF)",
				min_value=0.0,
				value=float(row["planned_amount"]),
				step=1.0
			)

			new_spent_amount = st.number_input(
				"Ausgaben (CHF)",
				min_value=0.0,
				value=float(
					row.get("spent_amount", 0.0)
				),
				step=1.0
			)

			col1, col2 = st.columns(2)

			if col1.form_submit_button("Speichern"):

				budget_data.at[
					edit_idx,
					"category"
				] = new_category

				budget_data.at[
					edit_idx,
					"planned_amount"
				] = new_planned_amount

				budget_data.at[
					edit_idx,
					"spent_amount"
				] = new_spent_amount

				dm.save_user_data(
					budget_data,
					'budget.csv'
				)

				del st.session_state[
					"edit_budget_idx"
				]

				st.success(
					"Kategorie aktualisiert"
				)

				_rerun()

			if col2.form_submit_button("Abbrechen"):

				del st.session_state[
					"edit_budget_idx"
				]

				_rerun()

	st.divider()


# Aktuelle Budgets
st.markdown('<div class="section-title">Aktuelle Budgets</div>', unsafe_allow_html=True)

if not budget_data.empty:

	for idx, row in budget_data.iterrows():

		planned = float(row['planned_amount'])
		spent = float(row.get('spent_amount', 0)) + float(monthly_sub_cost)

		if planned > 0:
			percentage = (spent / planned) * 100
		else:
			percentage = 0

		progress_width = min(percentage, 100)

		if percentage >= 100:
			percent_class = "budget-percent-danger"
			progress_class = "progress-fill-danger"
		elif percentage >= 75:
			percent_class = "budget-percent-warning"
			progress_class = "progress-fill-warning"
		else:
			percent_class = "budget-percent"
			progress_class = "progress-fill"

		with st.container():

			st.markdown('<div class="budget-card">', unsafe_allow_html=True)

			col1, col2, col3, col4, col5 = st.columns(
				[2.1, 1.4, 1.4, 0.8, 1]
			)

			with col1:
				st.markdown(
					f"""
					<div class="budget-category">{row['category']}</div>
					<div class="progress-track">
						<div class="{progress_class}" style="width: {progress_width}%;"></div>
					</div>
					""",
					unsafe_allow_html=True
				)

			with col2:
				st.markdown(
					f"""
					<div class="budget-label">Geplant</div>
					<div class="budget-value">CHF {planned:.2f}</div>
					""",
					unsafe_allow_html=True
				)

			with col3:
				st.markdown(
					f"""
					<div class="budget-label">Ausgegeben</div>
					<div class="budget-value">CHF {spent:.2f}</div>
					""",
					unsafe_allow_html=True
				)

			with col4:
				st.markdown(
					f'<div class="{percent_class}">{percentage:.0f}%</div>',
					unsafe_allow_html=True
				)

			with col5:

				edit_col, delete_col = st.columns(2)

				if edit_col.button(
					"✏️",
					key=f"edit-budget-{idx}",
					help="Bearbeiten"
				):

					st.session_state[
						"edit_budget_idx"
					] = idx

					_rerun()

				if delete_col.button(
					"🗑️",
					key=f"delete-budget-{idx}",
					help="Löschen"
				):

					budget_data = budget_data.drop(
						index=idx
					).reset_index(drop=True)

					dm.save_user_data(
						budget_data,
						'budget.csv'
					)

					st.success(
						"Kategorie gelöscht"
					)

					_rerun()

			st.markdown('</div>', unsafe_allow_html=True)

else:
	st.markdown("""
	<div class="empty-state">
		<div class="empty-title">Keine Budgetkategorien vorhanden</div>
		<div>Füge oben eine Kategorie hinzu, um dein Budget zu planen.</div>
	</div>
	""", unsafe_allow_html=True)