import streamlit as st
import pandas as pd
from datetime import date, timedelta


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


def load_subscriptions_data(dm):
	df = dm.load_user_data(
		'subscriptions.csv',
		initial_value=pd.DataFrame()
	)

	if df is None or df.empty:
		return pd.DataFrame(
			columns=[
				'name',
				'start_date',
				'amount',
				'interval',
				'active',
				'link',
				'icon'
			]
		)

	if 'provider' in df.columns:
		df = df.drop(columns=['provider'])

	if 'timestamp' in df.columns:
		df = df.drop(columns=['timestamp'])

	if 'notes' in df.columns and 'link' not in df.columns:

		df['link'] = df['notes'].astype(str).where(
			df['notes'].astype(str).str.contains(
				r'^https?://',
				na=False
			),
			''
		)

		df = df.drop(columns=['notes'])

	if 'link' not in df.columns:
		df['link'] = ''

	if 'icon' not in df.columns:
		df['icon'] = '📱'

	if 'start_date' in df.columns:
		df['start_date'] = pd.to_datetime(
			df['start_date'],
			errors='coerce'
		).dt.date

	df['amount'] = pd.to_numeric(
		df['amount'],
		errors='coerce'
	).fillna(0.0)

	df['active'] = df.get('active', True)

	df['link'] = df['link'].astype(str).fillna('')

	return df


def save_subscriptions_data(dm, df):
	dm.save_user_data(
		df,
		'subscriptions.csv'
	)


def calculate_next_renewal(start_date, interval):
	if pd.isna(start_date):
		return date.today()

	next_renewal = start_date
	today = date.today()

	max_iterations = 100
	iterations = 0

	if interval == 'Monthly':

		while next_renewal <= today and iterations < max_iterations:

			try:

				if next_renewal.month == 12:

					next_renewal = next_renewal.replace(
						year=next_renewal.year + 1,
						month=1
					)

				else:

					next_renewal = next_renewal.replace(
						month=next_renewal.month + 1
					)

			except ValueError:

				next_renewal = (
					next_renewal.replace(day=1)
					+ timedelta(days=32)
				)

				next_renewal = next_renewal.replace(day=1)

			iterations += 1

	elif interval == 'Yearly':

		while next_renewal <= today and iterations < max_iterations:

			next_renewal = next_renewal.replace(
				year=next_renewal.year + 1
			)

			iterations += 1

	elif interval == 'Quarterly':

		while next_renewal <= today and iterations < max_iterations:

			next_renewal = next_renewal + timedelta(days=91)

			iterations += 1

	return next_renewal


def interval_to_text(interval):
	if interval == 'Monthly':
		return 'Monatlich'

	if interval == 'Yearly':
		return 'Jährlich'

	if interval == 'Quarterly':
		return 'Quartalsweise'

	return interval


def interval_to_english(interval):
	interval_map = {
		'Monatlich': 'Monthly',
		'Jährlich': 'Yearly',
		'Quartalsweise': 'Quarterly'
	}

	return interval_map.get(
		interval,
		'Monthly'
	)


def interval_to_german(interval):
	if interval == 'Monthly':
		return 'Monatlich'

	if interval == 'Yearly':
		return 'Jährlich'

	if interval == 'Quarterly':
		return 'Quartalsweise'

	return 'Monatlich'