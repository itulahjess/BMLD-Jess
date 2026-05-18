import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.data_manager import DataManager


st.markdown("""
<style>
/* ---------- GLOBAL PAGE STYLE ---------- */

.stApp {
	background:
		radial-gradient(circle at top right, rgba(116, 222, 188, 0.22), transparent 34%),
		radial-gradient(circle at bottom left, rgba(203, 245, 229, 0.35), transparent 38%),
		#f5fbf8;
	color: #2f3038;
}

.block-container {
	padding-top: 2.2rem;
	padding-bottom: 3rem;
	max-width: 1050px;
}

/* ---------- TYPOGRAPHY ---------- */

h1 {
	font-size: 58px !important;
	font-weight: 900 !important;
	letter-spacing: -1.8px !important;
	color: #2f3038 !important;
	margin-bottom: 1.2rem !important;
}

h2, h3 {
	color: #2f3038 !important;
	letter-spacing: -0.7px !important;
}

p, label, span {
	color: #2f3038;
}

/* ---------- PAGE INTRO ---------- */

.page-intro {
	background:
		linear-gradient(135deg, rgba(232, 255, 245, 0.96), rgba(255, 255, 255, 0.76));
	padding: 28px 32px;
	border-radius: 28px;
	border: 1px solid rgba(95, 208, 173, 0.18);
	box-shadow: 0 18px 45px rgba(31, 122, 99, 0.08);
	margin-bottom: 28px;
	backdrop-filter: blur(14px);
}

.page-intro-title {
	font-size: 24px;
	font-weight: 900;
	color: #054033;
	margin-bottom: 6px;
}

.page-intro-text {
	font-size: 15px;
	color: #52796f;
	line-height: 1.5;
}

/* ---------- TABS ---------- */

button[data-baseweb="tab"] {
	font-size: 16px;
	font-weight: 700;
	color: #52796f;
	padding: 12px 18px;
	border-radius: 999px;
	margin-right: 8px;
	transition: all 0.2s ease;
}

button[data-baseweb="tab"]:hover {
	background: rgba(95, 208, 173, 0.12);
	color: #054033;
}

button[data-baseweb="tab"][aria-selected="true"] {
	background: #5fd0ad;
	color: white;
}

div[data-baseweb="tab-highlight"] {
	display: none;
}

/* ---------- SUBSCRIPTION CARDS ---------- */

.subscription-card {
	background: rgba(255, 255, 255, 0.82);
	border: 1px solid rgba(95, 208, 173, 0.18);
	border-radius: 26px;
	padding: 20px 22px;
	margin-bottom: 16px;
	box-shadow: 0 14px 34px rgba(31, 122, 99, 0.07);
	backdrop-filter: blur(12px);
	transition: transform 0.24s ease, box-shadow 0.24s ease, border 0.24s ease;
}

.subscription-card:hover {
	transform: translateY(-4px);
	box-shadow: 0 22px 48px rgba(31, 122, 99, 0.13);
	border: 1px solid rgba(95, 208, 173, 0.34);
}

.sub-icon {
	width: 54px;
	height: 54px;
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 18px;
	background: linear-gradient(145deg, rgba(232, 255, 245, 1), rgba(255, 255, 255, 0.75));
	font-size: 28px;
	box-shadow: inset 0 0 0 1px rgba(95, 208, 173, 0.16);
}

.sub-name {
	font-size: 20px;
	font-weight: 900;
	color: #054033;
	margin-bottom: 4px;
	letter-spacing: -0.2px;
}

.sub-detail {
	font-size: 14px;
	color: #6b9080;
	line-height: 1.45;
}

.sub-price {
	font-size: 19px;
	font-weight: 900;
	color: #2f3038;
	margin-bottom: 4px;
}

.sub-interval {
	font-size: 14px;
	color: #7b8790;
}

.status-active {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 8px 13px;
	border-radius: 999px;
	background: rgba(95, 208, 173, 0.16);
	color: #1f7a63;
	font-weight: 800;
	font-size: 14px;
}

.status-inactive {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 8px 13px;
	border-radius: 999px;
	background: rgba(255, 120, 120, 0.13);
	color: #a13a3a;
	font-weight: 800;
	font-size: 14px;
}

/* ---------- STREAMLIT BUTTONS ---------- */

.stButton > button {
	border-radius: 16px !important;
	border: 1px solid rgba(95, 208, 173, 0.26) !important;
	background: rgba(255, 255, 255, 0.78) !important;
	color: #054033 !important;
	font-weight: 800 !important;
	box-shadow: 0 8px 20px rgba(31, 122, 99, 0.08) !important;
	transition: all 0.2s ease !important;
}

.stButton > button:hover {
	transform: translateY(-2px);
	border: 1px solid rgba(95, 208, 173, 0.48) !important;
	box-shadow: 0 14px 28px rgba(31, 122, 99, 0.13) !important;
	background: #e8fff5 !important;
	color: #054033 !important;
}

/* ---------- EXPANDER ---------- */

.streamlit-expanderHeader {
	background: rgba(255, 255, 255, 0.72);
	border-radius: 18px;
	border: 1px solid rgba(95, 208, 173, 0.18);
	font-weight: 800;
	color: #054033;
}

div[data-testid="stExpander"] {
	border: none;
	background: transparent;
}

div[data-testid="stExpander"] details {
	background: rgba(255, 255, 255, 0.5);
	border-radius: 22px;
	border: 1px solid rgba(95, 208, 173, 0.18);
	box-shadow: 0 14px 34px rgba(31, 122, 99, 0.06);
}

/* ---------- INPUTS ---------- */

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox div[data-baseweb="select"],
.stCheckbox {
	border-radius: 14px !important;
}

.stTextInput input,
.stNumberInput input,
.stDateInput input {
	background: rgba(255, 255, 255, 0.85) !important;
	border: 1px solid rgba(95, 208, 173, 0.22) !important;
	color: #2f3038 !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stDateInput input:focus {
	border-color: #5fd0ad !important;
	box-shadow: 0 0 0 3px rgba(95, 208, 173, 0.16) !important;
}

/* ---------- EDIT BOX ---------- */

.edit-box {
	background:
		linear-gradient(135deg, rgba(232, 255, 245, 0.95), rgba(255, 255, 255, 0.78));
	border: 1px solid rgba(95, 208, 173, 0.2);
	border-radius: 28px;
	padding: 24px 28px;
	margin-bottom: 24px;
	box-shadow: 0 18px 45px rgba(31, 122, 99, 0.08);
}

.edit-title {
	font-size: 25px;
	font-weight: 900;
	color: #054033;
	margin-bottom: 6px;
}

.edit-subtitle {
	font-size: 14px;
	color: #52796f;
}

/* ---------- EMPTY STATE ---------- */

.empty-state {
	background: rgba(255, 255, 255, 0.72);
	border: 1px dashed rgba(95, 208, 173, 0.42);
	border-radius: 24px;
	padding: 30px;
	text-align: center;
	color: #52796f;
	margin-top: 12px;
}

.empty-title {
	font-size: 21px;
	font-weight: 900;
	color: #054033;
	margin-bottom: 6px;
}

/* ---------- DIVIDER ---------- */

hr {
	border-color: rgba(95, 208, 173, 0.18) !important;
	margin-top: 2rem !important;
	margin-bottom: 2rem !important;
}

/* ---------- RESPONSIVE ---------- */

@media (max-width: 800px) {
	h1 {
		font-size: 42px !important;
	}

	.page-intro {
		padding: 24px;
	}

	.subscription-card {
		padding: 18px;
	}
}
</style>
""", unsafe_allow_html=True)


st.title("Aboverwaltung")

st.markdown("""
<div class="page-intro">
	<div class="page-intro-title">Verwalte deine Abonnements</div>
	<div class="page-intro-text">
		Behalte aktive und inaktive Abos im Blick, aktualisiere Beträge und prüfe die nächste Verlängerung.
	</div>
</div>
""", unsafe_allow_html=True)


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


def _interval_to_text(interval):

	if interval == 'Monthly':
		return 'Monatlich'

	if interval == 'Yearly':
		return 'Jährlich'

	if interval == 'Quarterly':
		return 'Quartalsweise'

	return interval


def _render_subscription_cards(df, editable=True):

	if df.empty:
		st.markdown("""
		<div class="empty-state">
			<div class="empty-title">Noch keine Abonnements vorhanden</div>
			<div>Füge unten dein erstes Abo hinzu, um deine Kosten zu verwalten.</div>
		</div>
		""", unsafe_allow_html=True)
		return

	for idx, row in df.iterrows():

		next_renewal = _calculate_next_renewal(
			row['start_date'],
			row['interval']
		)

		interval_text = _interval_to_text(row['interval'])

		status_html = (
			'<span class="status-active">✅ Aktiv</span>'
			if row['active']
			else '<span class="status-inactive">❌ Inaktiv</span>'
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

		with st.container():

			st.markdown('<div class="subscription-card">', unsafe_allow_html=True)

			col1, col2, col3, col4, col5 = st.columns(
				[0.75, 2.2, 1.35, 1.1, 0.55]
			)

			with col1:
				st.markdown(icon_html, unsafe_allow_html=True)

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
				st.markdown(status_html, unsafe_allow_html=True)

			with col5:
				if editable and st.button(
					'✏️',
					key=f'edit-{idx}',
					help='Bearbeiten'
				):

					st.session_state['edit_idx'] = idx
					_rerun()

			st.markdown('</div>', unsafe_allow_html=True)


subs = _load()


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
					'Monatlich'
					if row['interval'] == 'Monthly'
					else 'Jährlich'
					if row['interval'] == 'Yearly'
					else 'Quartalsweise'
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



