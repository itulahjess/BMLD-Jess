import streamlit as st
import pandas as pd
from datetime import date
from utils.data_manager import DataManager


st.title("Sparziele")

dm = DataManager()
if st.session_state.get('username') is None:
	st.error('Kein Benutzer eingeloggt. Bitte zuerst anmelden.')
	st.stop()

st.subheader("Verwalten Sie Ihre Sparziele")

# Initialize or load savings goals
goals_data = dm.load_user_data('savings_goals.csv', initial_value=pd.DataFrame())
if goals_data is None or goals_data.empty:
	goals_data = pd.DataFrame(columns=['goal_name', 'target_amount', 'current_amount', 'deadline', 'created_date'])

# Convert date columns
if not goals_data.empty:
	if 'deadline' in goals_data.columns:
		goals_data['deadline'] = pd.to_datetime(goals_data['deadline'], errors='coerce').dt.date
	if 'created_date' in goals_data.columns:
		goals_data['created_date'] = pd.to_datetime(goals_data['created_date'], errors='coerce').dt.date
	goals_data['target_amount'] = pd.to_numeric(goals_data['target_amount'], errors='coerce').fillna(0.0)
	goals_data['current_amount'] = pd.to_numeric(goals_data['current_amount'], errors='coerce').fillna(0.0)

# Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Anzahl Sparziele", len(goals_data))
col2.metric("Gesamtbetrag geplant", f"CHF {goals_data['target_amount'].sum() if not goals_data.empty else 0:.2f}")
col3.metric("Bereits gespart", f"CHF {goals_data['current_amount'].sum() if not goals_data.empty else 0:.2f}")

if not goals_data.empty:
	progress = (goals_data['current_amount'].sum() / goals_data['target_amount'].sum()) * 100 if goals_data['target_amount'].sum() > 0 else 0
	col4.metric("Fortschritt", f"{progress:.0f}%")
else:
	col4.metric("Fortschritt", "0%")

st.divider()

# Add new goal form
st.subheader("Neues Sparziel erstellen")

with st.expander("Sparziel hinzufügen", expanded=True):
	with st.form("add_goal"):
		col1, col2 = st.columns(2)
		goal_name = col1.text_input("Zielname (z.B. 'Urlaub', 'Neuer Computer')")
		target_amount = col1.number_input("Zielbetraag (CHF)", min_value=0.0, step=100.0)
		
		current_amount = col2.number_input("Bereits gespart (CHF)", min_value=0.0, step=10.0)
		deadline = col2.date_input("Zieldatum")
		
		if st.form_submit_button("Sparziel erstellen"):
			if goal_name and target_amount > 0:
				new_goal = pd.DataFrame([{
					'goal_name': goal_name,
					'target_amount': target_amount,
					'current_amount': current_amount,
					'deadline': deadline,
					'created_date': date.today()
				}])
				goals_data = pd.concat([goals_data, new_goal], ignore_index=True)
				dm.save_user_data(goals_data, 'savings_goals.csv')
				st.success(f"Sparziel '{goal_name}' erstellt!")
				st.rerun()
			else:
				st.error("Bitte füllen Sie alle erforderlichen Felder aus")

st.divider()

# Display goals
st.subheader("Ihre Sparziele")

if not goals_data.empty:
	for idx, row in goals_data.iterrows():
		with st.container():
			col1, col2, col3 = st.columns([2, 1, 1])
			
			# Goal name and progress bar
			with col1:
				st.write(f"### {row['goal_name']}")
				progress = (row['current_amount'] / row['target_amount'] * 100) if row['target_amount'] > 0 else 0
				st.progress(progress / 100)
				st.write(f"CHF {row['current_amount']:.2f} von CHF {row['target_amount']:.2f}")
			
			# Deadline and remaining amount
			with col2:
				st.write(f"**Zieldatum:** {row['deadline'].strftime('%d.%m.%Y')}")
				remaining = row['target_amount'] - row['current_amount']
				st.write(f"**Noch zu sparen:** CHF {remaining:.2f}")
			
			# Progress percentage
			with col3:
				st.metric("Fortschritt", f"{progress:.0f}%")
			
			# Edit and delete buttons
			edit_col, delete_col = st.columns(2)
			if edit_col.button("✏️ Bearbeiten", key=f"edit_goal_{idx}"):
				st.session_state[f"edit_goal_{idx}"] = True
			if delete_col.button("🗑️ Löschen", key=f"delete_goal_{idx}"):
				goals_data = goals_data.drop(index=idx).reset_index(drop=True)
				dm.save_user_data(goals_data, 'savings_goals.csv')
				st.success("Sparziel gelöscht!")
				st.rerun()
			
			# Edit form
			if st.session_state.get(f"edit_goal_{idx}", False):
				with st.form(f"edit_goal_form_{idx}"):
					new_current = st.number_input("Aktuell gespart (CHF)", value=float(row['current_amount']), min_value=0.0, step=10.0, key=f"edit_amount_{idx}")
					if st.form_submit_button("Aktualisieren", key=f"update_goal_{idx}"):
						goals_data.at[idx, 'current_amount'] = new_current
						dm.save_user_data(goals_data, 'savings_goals.csv')
						st.success("Sparziel aktualisiert!")
						del st.session_state[f"edit_goal_{idx}"]
						st.rerun()
			
			st.divider()
else:
	st.info("Keine Sparziele vorhanden. Erstellen Sie ein neues Sparziel oben!")
