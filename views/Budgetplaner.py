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

# Initialize or load budget data
budget_data = dm.load_user_data('budget.csv', initial_value=pd.DataFrame())
if budget_data is None or budget_data.empty:
	budget_data = pd.DataFrame(columns=['category', 'planned_amount', 'spent_amount', 'date'])

# Load subscriptions to calculate costs
subs = dm.load_user_data('subscriptions.csv', initial_value=pd.DataFrame())
if subs is not None and not subs.empty:
	subs['amount'] = pd.to_numeric(subs['amount'], errors='coerce').fillna(0.0)
	subs['active'] = subs.get('active', True)
	monthly_sub_cost = subs[subs['active'] == True]['amount'].sum()
else:
	monthly_sub_cost = 0

# Budget overview
col1, col2, col3, col4 = st.columns(4)

col1.metric("Abonnements/Monat", f"CHF {monthly_sub_cost:.2f}")
col2.metric("Gesamtbudget", "CHF 0.00", delta=None)
col3.metric("Ausgegeben", "CHF 0.00")
col4.metric("Verbleibend", "CHF 0.00")

st.divider()

# Budget planning form
st.subheader("Budgetkategorien")

with st.expander("Neue Budgetkategorie hinzufügen"):
	with st.form("add_budget"):
		cat_col, amount_col = st.columns(2)
		category = cat_col.text_input("Kategorie")
		planned_amount = amount_col.number_input("Geplanter Betrag (CHF)", min_value=0.0, step=1.0)
		
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

# Display existing budget categories
if not budget_data.empty:
	st.subheader("Aktuelle Budgets")
	
	for idx, row in budget_data.iterrows():
		col1, col2, col3, col4 = st.columns(4)
		
		col1.write(f"**{row['category']}**")
		col2.write(f"Geplant: CHF {row['planned_amount']:.2f}")
		col3.write(f"Ausgegeben: CHF {row.get('spent_amount', 0):.2f}")
		
		spent = row.get('spent_amount', 0)
		planned = row['planned_amount']
		if planned > 0:
			percentage = (spent / planned) * 100
			col4.write(f"{percentage:.0f}%")
else:
	st.info("Keine Budgetkategorien vorhanden")

st.divider()

# Monthly overview
st.subheader("Monatlicher Überblick")

overview_data = {
	"Abonnements": monthly_sub_cost,
	"Sonstiges Budget": budget_data['planned_amount'].sum() if not budget_data.empty else 0,
	"Gesamtbudget": (monthly_sub_cost + budget_data['planned_amount'].sum()) if not budget_data.empty else monthly_sub_cost
}

overview_df = pd.DataFrame(list(overview_data.items()), columns=['Kategorie', 'Betrag (CHF)'])
st.dataframe(overview_df, use_container_width=True)
