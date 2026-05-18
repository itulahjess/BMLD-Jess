import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.data_manager import DataManager


st.title("Aboverwaltung")

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


ICON_OPTIONS = {
	'📷': 'Kamera',
	'📱': 'Smartphone',
	'🎵': 'Musik',
	'📺': 'TV',
	'🎮': 'Spiele',
	'📚': 'Bücher',
	'💼': 'Geschäft',
	'🏠': 'Zuhause',
	'🍎': 'Apple',
	'🎥': 'Video',
	'🌐': 'Web',
	'📧': 'E-Mail',
	'📰': 'Nachrichten',
	'🎬': 'Unterhaltung',
	'💳': 'Finanzen'
}


def _load():

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


def _save(df):
	dm.save_user_data(df, 'subscriptions.csv')


def _calculate_next_renewal(start_date, interval):

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


def _render_subscription_cards(df, editable=True):

	if df.empty:
		st.info('Keine Abonnements gefunden')
		return

	for idx, row in df.iterrows():

		next_renewal = _calculate_next_renewal(
			row['start_date'],
			row['interval']
		)

		with st.container():

			col1, col2, col3, col4, col5 = st.columns(
				[0.8, 2, 1.5, 1, 0.5]
			)

			if row.get('link'):

				col1.markdown(
					f"<a href='{row['link']}' target='_blank' "
					f"style='text-decoration:none;font-size:28px;'>"
					f"{row['icon']}</a>",
					unsafe_allow_html=True
				)

			else:
				col1.write(row['icon'])

			col2.write(f"**{row['name']}**")

			interval_text = (
				"Monatlich"
				if row['interval'] == 'Monthly'
				else "Jährlich"
				if row['interval'] == 'Yearly'
				else "Quartalsweise"
			)

			col2.caption(
				f"Nächste Verlängerung: "
				f"{next_renewal.strftime('%d.%m.%Y')}"
			)

			col3.write(f"CHF {row['amount']:.2f}")
			col3.caption(interval_text)

			status = (
				"✅ Aktiv"
				if row['active']
				else "❌ Inaktiv"
			)

			col4.write(status)

			if editable and col5.button(
				'✏️',
				key=f'edit-{idx}',
				help='Bearbeiten'
			):

				st.session_state['edit_idx'] = idx
				_rerun()


subs = _load()


if 'edit_idx' in st.session_state:

	edit_idx = st.session_state['edit_idx']

	if edit_idx < len(subs):

		row = subs.iloc[edit_idx]

		st.header(
			f"Abonnement bearbeiten: "
			f"{row['icon']} {row['name']}"
		)

		with st.form('edit_sub'):

			c1, c2 = st.columns(2)

			ename = c1.text_input(
				'Name',
				value=row['name']
			)

			estart = st.date_input(
				'Startdatum',
				value=row['start_date']
				if not pd.isna(row['start_date'])
				else date.today()
			)

			eamount = st.number_input(
				'Betrag (CHF)',
				min_value=0.0,
				value=float(row['amount']),
				step=0.5
			)

			einterval = st.selectbox(
				'Intervall',
				['Monatlich', 'Jährlich', 'Quartalsweise'],
				index=[
					'Monatlich',
					'Jährlich',
					'Quartalsweise'
				].index(
					'Monatlich'
					if row['interval'] == 'Monthly'
					else 'Jährlich'
					if row['interval'] == 'Yearly'
					else 'Quartalsweise'
				)
			)

			eactive = st.checkbox(
				'Aktiv',
				value=bool(row['active'])
			)

			elink = c2.text_input(
				'Link (URL)',
				value=row.get('link', '')
			)

			eicon = st.selectbox(
				'Icon',
				options=list(ICON_OPTIONS.keys()),
				format_func=lambda x: f"{x} {ICON_OPTIONS[x]}",
				index=list(ICON_OPTIONS.keys()).index(
					row.get('icon', '📱')
				)
				if row.get('icon') in ICON_OPTIONS
				else 0
			)

			col1, col2, col3 = st.columns(3)

			if col1.form_submit_button('Speichern'):

				sd = pd.to_datetime(
					estart,
					errors='coerce'
				)

				sd = sd.date() if not pd.isna(sd) else None

				interval_map = {
					'Monatlich': 'Monthly',
					'Jährlich': 'Yearly',
					'Quartalsweise': 'Quarterly'
				}

				subs.at[edit_idx, 'name'] = ename
				subs.at[edit_idx, 'start_date'] = sd
				subs.at[edit_idx, 'amount'] = float(eamount)
				subs.at[edit_idx, 'interval'] = interval_map.get(
					einterval,
					'Monthly'
				)
				subs.at[edit_idx, 'active'] = bool(eactive)
				subs.at[edit_idx, 'link'] = elink
				subs.at[edit_idx, 'icon'] = eicon

				_save(subs)

				del st.session_state['edit_idx']

				st.success('Änderungen gespeichert')

				_rerun()

			if col2.form_submit_button('Löschen'):

				subs = subs.drop(
					index=edit_idx
				).reset_index(drop=True)

				_save(subs)

				del st.session_state['edit_idx']

				st.success('Abonnement gelöscht')

				_rerun()

			if col3.form_submit_button('Abbrechen'):

				del st.session_state['edit_idx']

				_rerun()

	else:

		st.error('Ungültiges Abo zum Bearbeiten')

		if 'edit_idx' in st.session_state:
			del st.session_state['edit_idx']

else:

	tab_alle, tab_monatlich, tab_jährlich = st.tabs(
		['Alle', 'Monatlich', 'Jährlich']
	)

	with tab_alle:

		st.header('Alle Abonnements')

		_render_subscription_cards(
			subs,
			editable=True
		)

	with tab_monatlich:

		st.header('Monatliche Abonnements')

		dfm = (
			subs[subs['interval'] == 'Monthly']
			if not subs.empty
			else subs
		)

		_render_subscription_cards(
			dfm,
			editable=False
		)

	with tab_jährlich:

		st.header('Jährliche Abonnements')

		dfy = (
			subs[subs['interval'] == 'Yearly']
			if not subs.empty
			else subs
		)

		_render_subscription_cards(
			dfy,
			editable=False
		)

	st.divider()

	with st.expander('Neues Abo erfassen'):

		with st.form('add_sub'):

			c1, c2 = st.columns(2)

			name = c1.text_input('Name')

			start_date = st.date_input(
				'Startdatum',
				value=date.today()
			)

			amount = st.number_input(
				'Betrag (CHF)',
				min_value=0.0,
				value=0.0,
				step=0.5
			)

			interval = st.selectbox(
				'Intervall',
				['Monatlich', 'Jährlich', 'Quartalsweise']
			)

			active = st.checkbox(
				'Aktiv',
				value=True
			)

			link = c2.text_input(
				'Link (URL)'
			)

			icon = st.selectbox(
				'Icon',
				options=list(ICON_OPTIONS.keys()),
				format_func=lambda x: f"{x} {ICON_OPTIONS[x]}"
			)

			if st.form_submit_button('Hinzufügen'):

				if not name:

					st.error(
						'Bitte geben Sie einen Namen ein'
					)

				else:

					sd = pd.to_datetime(
						start_date,
						errors='coerce'
					)

					sd = (
						sd.date()
						if not pd.isna(sd)
						else None
					)

					interval_map = {
						'Monatlich': 'Monthly',
						'Jährlich': 'Yearly',
						'Quartalsweise': 'Quarterly'
					}

					rec = {
						'name': name,
						'start_date': sd,
						'amount': float(amount),
						'interval': interval_map[interval],
						'active': active,
						'link': link,
						'icon': icon
					}

					subs = pd.concat(
						[
							subs,
							pd.DataFrame([rec])
						],
						ignore_index=True
					)

					_save(subs)

					st.success(
						'Abonnement hinzugefügt'
					)

					_rerun()



