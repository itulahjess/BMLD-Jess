import streamlit as st
import pandas as pd


def get_rerun_function():
	try:
		return st.rerun
	except AttributeError:
		return st.experimental_rerun


def load_budget_data(dm):
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

	return budget_data


def load_expenses_data(dm):
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

	return expenses_data


def load_monthly_sub_cost(dm):
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

	return monthly_sub_cost


def calculate_budget_totals(budget_data, expenses_data):
	total_budget = budget_data['planned_amount'].sum()
	total_spent = expenses_data['amount'].sum()
	remaining = total_budget - total_spent

	return total_budget, total_spent, remaining