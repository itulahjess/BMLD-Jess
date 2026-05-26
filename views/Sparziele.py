import streamlit as st
import pandas as pd
from datetime import date
from utils.data_manager import DataManager
from functions.sparziele import (
	get_rerun_function,
	load_savings_goals_data,
	calculate_savings_metrics,
	get_goal_progress_data,
	format_deadline
)
from functions.design import (
	apply_global_styles,
	render_page_intro,
	render_section_title,
	render_empty_state
)


apply_global_styles()

st.title("Sparziele")

render_page_intro(
	"Verwalte deine Sparziele",
	"Erstelle Ziele, verfolge deinen Fortschritt und sieh direkt, wie viel du noch sparen musst."
)


dm = DataManager()

if st.session_state.get('username') is None:
	st.error('Kein Benutzer eingeloggt. Bitte zuerst anmelden.')
	st.stop()


_rerun = get_rerun_function()


goals_data = load_savings_goals_data(dm)


total_target, total_current, overall_progress = calculate_savings_metrics(
	goals_data
)


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


render_section_title(
	"Neues Sparziel erstellen",
	"Lege ein neues Ziel fest und erfasse, wie viel du bereits gespart hast."
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


render_section_title("Ihre Sparziele")

if not goals_data.empty:

	for idx, row in goals_data.iterrows():

		target, current, progress, progress_width, remaining, percent_class, progress_class = get_goal_progress_data(
			row
		)

		deadline_text = format_deadline(row)

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

			st.markdown(
				'<div class="goal-row-spacer"></div>',
				unsafe_allow_html=True
			)

else:

	render_empty_state(
		"Keine Sparziele vorhanden",
		"Erstelle oben dein erstes Sparziel, um deinen Fortschritt zu verfolgen."
	)