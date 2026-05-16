import streamlit as st
import pandas as pd
from datetime import date
from utils.data_manager import DataManager


st.title("Budgetplaner")

dm = DataManager()

if st.session_state.get('username') is None:
	st.error('Kein Benutzer eingeloggt. Bitte zuerst anmelden.')
	st.stop()

st.subheader("Planen Sie Ihr monatliches Budget")

budget_data = dm.load_user_data('budget.csv', initial_value=pd.DataFrame())

if budget_data is None or budget_data.empty:
	budget_data = pd.DataFrame(columns=['category', 'planned_amount', 'spent_amount', 'date'])

subs = dm.load_user_data('subscriptions.csv', initial_value=pd.DataFrame())

if subs is not None and not subs.empty:
	subs['amount'] = pd.to_numeric(subs['amount'], errors='coerce').fillna(0.0)
	subs['active'] = subs.get('active', True)
	monthly_sub_cost = subs[subs['active'] == True]['amount'].sum()
else:
	monthly_sub_cost = 0

total_budget = budget_data['planned_amount'].sum() if not budget_data.empty else 0
total_spent = budget_data['spent_amount'].sum() if not budget_data.empty else 0
remaining = total_budget - total_spent

col1, col2, col3, col4 = st.columns(4)

col1.metric("Abonnements/Monat", f"CHF {monthly_sub_cost:.2f}")
col2.metric("Gesamtbudget", f"CHF {total_budget:.2f}")
col3.metric("Ausgegeben", f"CHF {total_spent:.2f}")
col4.metric("Verbleibend", f"CHF {remaining:.2f}")

st.divider()

st.subheader("Budgetkategorien")

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

				budget_data = pd.concat([budget_data, new_entry], ignore_index=True)
				dm.save_user_data(budget_data, 'budget.csv')

				st.success(f"Kategorie '{category}' hinzugefügt")
				st.rerun()
			else:
				st.error("Bitte geben Sie eine Kategorie ein")

st.divider()

if "edit_budget_idx" in st.session_state:

	edit_idx = st.session_state["edit_budget_idx"]

	if edit_idx < len(budget_data):

		row = budget_data.iloc[edit_idx]

		st.subheader(f"Kategorie bearbeiten: {row['category']}")

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
				"Ausgegeben (CHF)",
				min_value=0.0,
				value=float(row.get("spent_amount", 0.0)),
				step=1.0
			)

			col1, col2 = st.columns(2)

			if col1.form_submit_button("Speichern"):

				budget_data.at[edit_idx, "category"] = new_category
				budget_data.at[edit_idx, "planned_amount"] = new_planned_amount
				budget_data.at[edit_idx, "spent_amount"] = new_spent_amount

				dm.save_user_data(budget_data, 'budget.csv')

				del st.session_state["edit_budget_idx"]

				st.success("Kategorie aktualisiert")
				st.rerun()

			if col2.form_submit_button("Abbrechen"):

				del st.session_state["edit_budget_idx"]
				st.rerun()

	st.divider()

if not budget_data.empty:

	st.subheader("Aktuelle Budgets")

	for idx, row in budget_data.iterrows():

		col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1, 1])

		col1.write(f"**{row['category']}**")
		col2.write(f"Geplant: CHF {row['planned_amount']:.2f}")
		col3.write(f"Ausgegeben: CHF {row.get('spent_amount', 0):.2f}")

		spent = row.get('spent_amount', 0)
		planned = row['planned_amount']

		if planned > 0:
			percentage = (spent / planned) * 100
			col4.write(f"{percentage:.0f}%")
		else:
			col4.write("0%")

		edit_col, delete_col = col5.columns(2)

		if edit_col.button("✏️", key=f"edit-budget-{idx}"):

			st.session_state["edit_budget_idx"] = idx
			st.rerun()

		if delete_col.button("🗑️", key=f"delete-budget-{idx}"):

			budget_data = budget_data.drop(index=idx).reset_index(drop=True)
			dm.save_user_data(budget_data, 'budget.csv')

			st.success("Kategorie gelöscht")
			st.rerun()

else:
	st.info("Keine Budgetkategorien vorhanden")

st.divider()

st.subheader("Monatlicher Überblick")

overview_data = {
	"Abonnements": monthly_sub_cost,
	"Sonstiges Budget": budget_data['planned_amount'].sum() if not budget_data.empty else 0,
	"Gesamtbudget": (monthly_sub_cost + budget_data['planned_amount'].sum()) if not budget_data.empty else monthly_sub_cost
}

overview_df = pd.DataFrame(
	list(overview_data.items()),
	columns=['Kategorie', 'Betrag (CHF)']
)

st.dataframe(overview_df, use_container_width=True)