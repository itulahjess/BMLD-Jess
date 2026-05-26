import streamlit as st
import pandas as pd
from datetime import date
from utils.data_manager import DataManager
from functions.icons import ICON_OPTIONS
from functions.aboverwaltung import (
	get_rerun_function,
	load_subscriptions_data,
	save_subscriptions_data,
	calculate_next_renewal,
	interval_to_text,
	interval_to_english,
	interval_to_german
)
from functions.design import (
	apply_global_styles,
	render_page_intro,
	render_empty_state
)


apply_global_styles()

st.title("Aboverwaltung")

render_page_intro(
	"Verwalte deine Abonnements",
	"Behalte aktive und inaktive Abos im Blick, aktualisiere Beträge und prüfe die nächste Verlängerung."
)


dm = DataManager()

if st.session_state.get('username') is None:
	st.error('Kein Benutzer eingeloggt. Bitte zuerst anmelden.')
	st.stop()


_rerun = get_rerun_function()


def render_subscription_cards(df, editable=True):

	if df.empty:
		render_empty_state(
			"Noch keine Abonnements vorhanden",
			"Füge unten dein erstes Abo hinzu, um deine Kosten zu verwalten."
		)
		return

	for idx, row in df.iterrows():

		next_renewal = calculate_next_renewal(
			row['start_date'],
			row['interval']
		)

		interval_text = interval_to_text(
			row['interval']
		)

		status_class = (
			"status-active"
			if row['active']
			else "status-inactive"
		)

		status_text = (
			"✅ Aktiv"
			if row['active']
			else "❌ Inaktiv"
		)

		icon = row.get('icon', '📱')
		link = row.get('link', '')

		if link:
			icon_html = (
				f"<a href='{link}' target='_blank' style='text-decoration:none;'>"
				f"<div class='sub-icon'>{icon}</div>"
				f"</a>"
			)
		else:
			icon_html = f"<div class='sub-icon'>{icon}</div>"

		col1, col2, col3, col4, col5 = st.columns(
			[0.75, 2.2, 1.35, 1.1, 0.55]
		)

		with col1:
			st.markdown(
				icon_html,
				unsafe_allow_html=True
			)

		with col2:
			st.markdown(
				f"""
				<div class="sub-name">{row['name']}</div>
				<div class="sub-detail">
					Nächste Verlängerung:<br>
					<strong>{next_renewal.strftime('%d.%m.%Y')}</strong>
				</div>
				""",
				unsafe_allow_html=True
			)

		with col3:
			st.markdown(
				f"""
				<div class="sub-price">CHF {row['amount']:.2f}</div>
				<div class="sub-interval">{interval_text}</div>
				""",
				unsafe_allow_html=True
			)

		with col4:
			st.markdown(
				f'<span class="{status_class}">{status_text}</span>',
				unsafe_allow_html=True
			)

		with col5:
			if editable and st.button(
				'✏️',
				key=f'edit-{idx}',
				help='Bearbeiten'
			):

				st.session_state['edit_idx'] = idx
				_rerun()

		st.markdown(
			'<div class="subscription-separator"></div>',
			unsafe_allow_html=True
		)


subs = load_subscriptions_data(dm)


if 'edit_idx' in st.session_state:

	edit_idx = st.session_state['edit_idx']

	if edit_idx < len(subs):

		row = subs.iloc[edit_idx]

		st.markdown(
			f"""
			<div class="edit-box">
				<div class="edit-title">Abonnement bearbeiten: {row['icon']} {row['name']}</div>
				<div class="edit-subtitle">
					Passe Details wie Betrag, Intervall, Status oder Link an.
				</div>
			</div>
			""",
			unsafe_allow_html=True
		)

		with st.form('edit_sub'):

			c1, c2 = st.columns(2)

			ename = c1.text_input(
				'Name',
				value=row['name']
			)

			estart = c1.date_input(
				'Startdatum',
				value=row['start_date']
				if not pd.isna(row['start_date'])
				else date.today()
			)

			eamount = c1.number_input(
				'Betrag (CHF)',
				min_value=0.0,
				value=float(row['amount']),
				step=0.5
			)

			einterval = c2.selectbox(
				'Intervall',
				['Monatlich', 'Jährlich', 'Quartalsweise'],
				index=[
					'Monatlich',
					'Jährlich',
					'Quartalsweise'
				].index(
					interval_to_german(
						row['interval']
					)
				)
			)

			elink = c2.text_input(
				'Link (URL)',
				value=row.get('link', '')
			)

			eicon = c2.selectbox(
				'Icon',
				options=list(ICON_OPTIONS.keys()),
				format_func=lambda x: f"{x} {ICON_OPTIONS[x]}",
				index=list(ICON_OPTIONS.keys()).index(
					row.get('icon', '📱')
				)
				if row.get('icon') in ICON_OPTIONS
				else 0
			)

			eactive = st.checkbox(
				'Aktiv',
				value=bool(row['active'])
			)

			col1, col2, col3 = st.columns(3)

			if col1.form_submit_button('Speichern'):

				sd = pd.to_datetime(
					estart,
					errors='coerce'
				)

				sd = sd.date() if not pd.isna(sd) else None

				subs.at[edit_idx, 'name'] = ename
				subs.at[edit_idx, 'start_date'] = sd
				subs.at[edit_idx, 'amount'] = float(eamount)
				subs.at[edit_idx, 'interval'] = interval_to_english(
					einterval
				)
				subs.at[edit_idx, 'active'] = bool(eactive)
				subs.at[edit_idx, 'link'] = elink
				subs.at[edit_idx, 'icon'] = eicon

				save_subscriptions_data(
					dm,
					subs
				)

				del st.session_state['edit_idx']

				st.success('Änderungen gespeichert')

				_rerun()

			if col2.form_submit_button('Löschen'):

				subs = subs.drop(
					index=edit_idx
				).reset_index(drop=True)

				save_subscriptions_data(
					dm,
					subs
				)

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

	tab_alle, tab_monatlich, tab_jährlich, tab_quartalsweise = st.tabs(
		['Alle', 'Monatlich', 'Jährlich', 'Quartalsweise']
	)

	with tab_alle:

		st.header('Alle Abonnements')

		render_subscription_cards(
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

		render_subscription_cards(
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

		render_subscription_cards(
			dfy,
			editable=False
		)

	with tab_quartalsweise:

		st.header('Quartalsweise Abonnements')

		dfq = (
			subs[subs['interval'] == 'Quarterly']
			if not subs.empty
			else subs
		)

		render_subscription_cards(
			dfq,
			editable=False
		)

	st.divider()

	with st.expander('Neues Abo erfassen'):

		with st.form('add_sub'):

			c1, c2 = st.columns(2)

			name = c1.text_input('Name')

			start_date = c1.date_input(
				'Startdatum',
				value=date.today()
			)

			amount = c1.number_input(
				'Betrag (CHF)',
				min_value=0.0,
				value=0.0,
				step=0.5
			)

			interval = c2.selectbox(
				'Intervall',
				['Monatlich', 'Jährlich', 'Quartalsweise']
			)

			link = c2.text_input(
				'Link (URL)'
			)

			icon = c2.selectbox(
				'Icon',
				options=list(ICON_OPTIONS.keys()),
				format_func=lambda x: f"{x} {ICON_OPTIONS[x]}"
			)

			active = st.checkbox(
				'Aktiv',
				value=True
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

					rec = {
						'name': name,
						'start_date': sd,
						'amount': float(amount),
						'interval': interval_to_english(interval),
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

					save_subscriptions_data(
						dm,
						subs
					)

					st.success(
						'Abonnement hinzugefügt'
					)

					_rerun()