import streamlit as st
import pandas as pd
from datetime import date
from utils.data_manager import DataManager
from functions.icons import ICON_OPTIONS
from functions.budgetplaner import (
	get_rerun_function,
	load_budget_data,
	load_expenses_data,
	load_monthly_sub_cost,
	calculate_budget_totals
)
from functions.design import (
	apply_global_styles,
	render_page_intro,
	render_section_title,
	render_empty_state,
	render_separator
)


apply_global_styles()

st.title("Budgetplaner")

render_page_intro(
	"Plane dein monatliches Budget",
	"Erstelle Budgetkategorien, verfolge deine Ausgaben und sieh sofort, wie viel Budget noch verfügbar ist."
)


dm = DataManager()

if st.session_state.get('username') is None:
	st.error('Kein Benutzer eingeloggt. Bitte zuerst anmelden.')
	st.stop()


_rerun = get_rerun_function()

budget_data = load_budget_data(dm)
expenses_data = load_expenses_data(dm)
monthly_sub_cost = load_monthly_sub_cost(dm)

total_budget, total_spent, remaining = calculate_budget_totals(
	budget_data,
	expenses_data
)


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


render_section_title(
	"Budgetkategorien",
	"Füge neue Kategorien hinzu, um dein Budget genauer aufzuteilen."
)

with st.expander("Neue Budgetkategorie hinzufügen"):

	with st.form("add_budget"):

		col1, col2 = st.columns(2)

		icon_labels = [f"{icon} {name}" for icon, name in ICON_OPTIONS.items()]
		selected_icon_label = col1.selectbox("Kategorie", icon_labels)

		planned_amount = col2.number_input(
			"Betrag (CHF)",
			min_value=0.0,
			step=1.0
		)

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


if "edit_budget_idx" in st.session_state:

	edit_idx = st.session_state["edit_budget_idx"]

	if edit_idx < len(budget_data):

		row = budget_data.iloc[edit_idx]

		render_section_title("Budget bearbeiten")

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


render_section_title("Neue Ausgabe")

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


if "edit_expense_idx" in st.session_state:

	edit_idx = st.session_state["edit_expense_idx"]

	if edit_idx < len(expenses_data):

		expense = expenses_data.iloc[edit_idx]

		render_section_title("Ausgabe bearbeiten")

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


render_section_title("Aktuelle Budgets")

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


		if not category_expenses.empty:

			for expense_idx, expense in category_expenses.iterrows():

				box1, box2, box3, box4, box5 = st.columns(
					[2.1, 1.4, 1.4, 0.8, 1]
				)

				with box1:
					st.markdown(
						f"""
						<div style="
							margin-top:8px;
							padding:18px;
							background:white;
							border-radius:16px;
							border:1px solid rgba(95,208,173,0.15);
						">
							<strong>{expense['description']}</strong><br>
							CHF {expense['amount']:.2f}
						</div>
						""",
						unsafe_allow_html=True
					)

				with box2:
					st.empty()

				with box3:
					st.empty()

				with box4:
					st.empty()

				with box5:
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

		render_separator("budget-separator")

else:

	render_empty_state(
		"Keine Budgetkategorien vorhanden",
		"Füge oben eine Kategorie hinzu, um dein Budget zu planen."
	)