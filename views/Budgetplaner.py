import streamlit as st
import pandas as pd
from datetime import date
from utils.data_manager import DataManager
from functions.icons import ICON_OPTIONS

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
	font-size: 58px !important;
	font-weight: 800 !important;
	letter-spacing: -1.8px !important;
	color: #2f3038 !important;
	margin-bottom: 1.2rem !important;
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

div[data-testid="stMetric"] {
	background:
		linear-gradient(145deg, rgba(232, 255, 245, 0.95), rgba(255, 255, 255, 0.72));
	padding: 24px;
	border-radius: 24px;
	box-shadow: 0 14px 35px rgba(31, 122, 99, 0.08);
	border: 1px solid rgba(95, 208, 173, 0.17);
	min-height: 125px;
}

div[data-testid="stMetric"] label {
	font-size: 15px !important;
	font-weight: 800 !important;
	color: #054033 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
	font-size: 27px !important;
	font-weight: 900 !important;
	color: #1b5e54 !important;
}

.section-title {
	font-size: 32px;
	font-weight: 900;
	color: #2f3038;
	margin-top: 10px;
	margin-bottom: 18px;
}

.section-subtitle {
	font-size: 15px;
	color: #6b9080;
	margin-top: -8px;
	margin-bottom: 18px;
}

.stButton > button {
	border-radius: 16px !important;
	border: 1px solid rgba(95, 208, 173, 0.26) !important;
	background: rgba(255, 255, 255, 0.78) !important;
	color: #054033 !important;
	font-weight: 800 !important;
	box-shadow: 0 8px 20px rgba(31, 122, 99, 0.08) !important;
}

.budget-category {
	font-size: 21px;
	font-weight: 900;
	color: #054033;
	margin-bottom: 8px;
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

.budget-separator {
	height: 1px;
	background: rgba(95, 208, 173, 0.14);
	margin: 22px 0;
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
	_rerun = st.experimental_rerun


budget_data = dm.load_user_data(
	'budget.csv',
	initial_value=pd.DataFrame()
)

if budget_data is None or budget_data.empty:
	budget_data = pd.DataFrame(
		columns=[
			'icon',
			'planned_amount',
			'date'
		]
	)

budget_data['planned_amount'] = pd.to_numeric(
	budget_data.get('planned_amount', 0),
	errors='coerce'
).fillna(0.0)


expenses_data = dm.load_user_data(
	'expenses.csv',
	initial_value=pd.DataFrame()
)

if expenses_data is None or expenses_data.empty:
	expenses_data = pd.DataFrame(
		columns=[
			'category',
			'description',
			'amount',
			'date'
		]
	)

expenses_data['amount'] = pd.to_numeric(
	expenses_data.get('amount', 0),
	errors='coerce'
).fillna(0.0)

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


total_budget = budget_data['planned_amount'].sum()
total_spent = expenses_data['amount'].sum()
remaining = total_budget - total_spent


col1, col2, col3 = st.columns(3)

col1.metric(
	"Gesamtbudget",
	f"CHF {total_budget:.2f}"
)

col2.metric(
	"Ausgegeben",
	f"CHF {total_spent:.2f}"
)

col3.metric(
	"Verbleibend",
	f"CHF {remaining:.2f}"
)


st.divider()


st.markdown(
	'<div class="section-title">Budgetkategorien</div>',
	unsafe_allow_html=True
)

st.markdown(
	'<div class="section-subtitle">Füge neue Kategorien hinzu, um dein Budget genauer aufzuteilen.</div>',
	unsafe_allow_html=True
)

with st.expander("Neue Budgetkategorie hinzufügen"):

	with st.form("add_budget"):

		col1, col2 = st.columns(2)


		icon_labels = [f"{icon} {name}" for icon, name in ICON_OPTIONS.items()]
		selected_icon_label = col1.selectbox("Kategorie", icon_labels)
	

		planned_amount = col2.number_input("Betrag (CHF)", min_value=0.0, step=1.0)

		if st.form_submit_button("Kategorie hinzufügen"):

			if selected_icon_label:

				new_entry = pd.DataFrame([{
					'icon': selected_icon_label,
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
					f"Kategorie '{selected_icon_label}' hinzugefügt"
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
			'<div class="section-title">Budget bearbeiten</div>',
			unsafe_allow_html=True
		)

		with st.form("edit_budget_form"):

			col1, col2 = st.columns(2)

			icon_labels = [
				f"{icon} {name}"
				for icon, name in ICON_OPTIONS.items()
			]

			selected_icon_label = col1.selectbox(
				"Kategorie",
				icon_labels,
				index=icon_labels.index(row["icon"])
				if row["icon"] in icon_labels
				else 0
			)

			planned_amount = col2.number_input(
				"Betrag (CHF)",
				min_value=0.0,
				value=float(row["planned_amount"]),
				step=1.0
			)

			save_col, cancel_col = st.columns(2)

			if save_col.form_submit_button("Speichern"):

				budget_data.at[edit_idx, "icon"] = selected_icon_label
				budget_data.at[edit_idx, "planned_amount"] = planned_amount

				dm.save_user_data(
					budget_data,
					'budget.csv'
				)

				del st.session_state["edit_budget_idx"]

				st.success("Budget aktualisiert")

				_rerun()

			if cancel_col.form_submit_button("Abbrechen"):

				del st.session_state["edit_budget_idx"]

				_rerun()



# AUSGABE HINZUFÜGEN
st.markdown(
	'<div class="section-title">Neue Ausgabe</div>',
	unsafe_allow_html=True
)

with st.expander("Ausgabe hinzufügen"):

	with st.form("add_expense"):

		col1, col2 = st.columns(2)

		icon_labels = [
			f"{icon} {name}"
			for icon, name in ICON_OPTIONS.items()
		]

		selected_category = col1.selectbox(
			"Kategorie",
			icon_labels
		)

		description = col2.text_input("Beschreibung")

		amount = st.number_input(
			"Betrag (CHF)",
			min_value=0.0,
			step=1.0
		)

		expense_date = st.date_input("Datum")

		if st.form_submit_button("Ausgabe speichern"):

			new_expense = pd.DataFrame([{
				'category': selected_category,
				'description': description,
				'amount': amount,
				'date': expense_date
			}])

			expenses_data = pd.concat(
				[expenses_data, new_expense],
				ignore_index=True
			)

			dm.save_user_data(
				expenses_data,
				'expenses.csv'
			)

			st.success("Ausgabe hinzugefügt")

			_rerun()


# AUSGABE BEARBEITEN
if "edit_expense_idx" in st.session_state:

	edit_idx = st.session_state["edit_expense_idx"]

	if edit_idx < len(expenses_data):

		expense = expenses_data.iloc[edit_idx]

		st.markdown(
			'<div class="section-title">Ausgabe bearbeiten</div>',
			unsafe_allow_html=True
		)

		with st.form("edit_expense_form"):

			col1, col2 = st.columns(2)

			icon_labels = [
				f"{icon} {name}"
				for icon, name in ICON_OPTIONS.items()
			]

			selected_category = col1.selectbox(
				"Kategorie",
				icon_labels,
				index=icon_labels.index(expense["category"])
				if expense["category"] in icon_labels
				else 0
			)

			description = col2.text_input(
				"Beschreibung",
				value=expense["description"]
			)

			amount = st.number_input(
				"Betrag (CHF)",
				min_value=0.0,
				value=float(expense["amount"]),
				step=1.0
			)

			save_col, cancel_col = st.columns(2)

			if save_col.form_submit_button("Speichern"):

				expenses_data.at[edit_idx, "category"] = selected_category
				expenses_data.at[edit_idx, "description"] = description
				expenses_data.at[edit_idx, "amount"] = amount

				dm.save_user_data(
					expenses_data,
					'expenses.csv'
				)

				del st.session_state["edit_expense_idx"]

				st.success("Ausgabe aktualisiert")

				_rerun()

			if cancel_col.form_submit_button("Abbrechen"):

				del st.session_state["edit_expense_idx"]

				_rerun()


# AKTUELLE BUDGETS
st.markdown(
	'<div class="section-title">Aktuelle Budgets</div>',
	unsafe_allow_html=True
)

if not budget_data.empty:

	for idx, row in budget_data.iterrows():

		planned = float(row['planned_amount'])

		category_expenses = expenses_data[
			expenses_data['category'] == row['icon']
		]

		spent = category_expenses['amount'].sum()

		if planned > 0:
			percentage = (spent / planned) * 100
		else:
			percentage = 0

		progress_width = min(percentage, 100)

		category_name = row['icon']

		col1, col2, col3, col4, col5 = st.columns(
			[2.1, 1.4, 1.4, 0.8, 1]
		)

		with col1:
			st.markdown(
				f"""
				<div class="budget-category">{category_name}</div>
				<div class="progress-track">
					<div class="progress-fill" style="width:{progress_width}%"></div>
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
				f'<div class="budget-percent">{percentage:.0f}%</div>',
				unsafe_allow_html=True
			)

		with col5:

			edit_col, delete_col = st.columns(2)

			if edit_col.button(
				"✏️",
				key=f"edit-budget-{idx}"
			):
				st.session_state["edit_budget_idx"] = idx
				_rerun()

			if delete_col.button(
				"🗑️",
				key=f"delete-budget-{idx}"
			):

				budget_data = budget_data.drop(
					index=idx
				).reset_index(drop=True)

				dm.save_user_data(
					budget_data,
					'budget.csv'
				)

				st.success("Kategorie gelöscht")

				_rerun()


		# AUSGABEN DER KATEGORIE
		if not category_expenses.empty:

			for expense_idx, expense in category_expenses.iterrows():

				box1, box2 = st.columns([5, 1])

				with box1:

					st.markdown(
						f"""
						<div style="
							margin-left:20px;
							margin-top:8px;
							padding:12px;
							background:white;
							border-radius:12px;
							border:1px solid rgba(95,208,173,0.15);
						">
							<strong>{expense['description']}</strong><br>
							CHF {expense['amount']:.2f}
						</div>
						""",
						unsafe_allow_html=True
					)

				with box2:

					edit_btn, delete_btn = st.columns(2)

					if edit_btn.button(
						"✏️",
						key=f"edit-expense-{expense_idx}"
					):
						st.session_state["edit_expense_idx"] = expense_idx
						_rerun()

					if delete_btn.button(
						"🗑️",
						key=f"delete-expense-{expense_idx}"
					):

						expenses_data = expenses_data.drop(
							index=expense_idx
						).reset_index(drop=True)

						dm.save_user_data(
							expenses_data,
							'expenses.csv'
						)

						st.success("Ausgabe gelöscht")

						_rerun()

		st.markdown(
			'<div class="budget-separator"></div>',
			unsafe_allow_html=True
		)

else:

	st.markdown("""
	<div class="empty-state">
		<div class="empty-title">Keine Budgetkategorien vorhanden</div>
		<div>Füge oben eine Kategorie hinzu, um dein Budget zu planen.</div>
	</div>
	""", unsafe_allow_html=True)