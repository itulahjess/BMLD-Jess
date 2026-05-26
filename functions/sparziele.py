import streamlit as st
import pandas as pd


def get_rerun_function():
	try:
		return st.rerun
	except AttributeError:
		try:
			return st.experimental_rerun
		except AttributeError:
			def _rerun():
				st.stop()

			return _rerun


def load_savings_goals_data(dm):
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

	return goals_data


def calculate_savings_metrics(goals_data):
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

	return total_target, total_current, overall_progress


def get_goal_progress_data(row):
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

	return target, current, progress, progress_width, remaining, percent_class, progress_class


def format_deadline(row):
	deadline_value = row.get('deadline', None)

	if pd.isna(deadline_value):
		deadline_text = "Kein Zieldatum"
	else:
		try:
			deadline_text = deadline_value.strftime('%d.%m.%Y')
		except AttributeError:
			deadline_text = str(deadline_value)

	return deadline_text