import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.data_manager import DataManager


st.title("Aboverwaltung")


dm = DataManager()
if st.session_state.get('username') is None:
	st.error('Kein Benutzer eingeloggt. Bitte zuerst anmelden.')
	st.stop()


# rerun compatibility: use st.rerun() for newer versions
try:
	_rerun = st.rerun
except AttributeError:
	# fallback for older versions
	try:
		_rerun = st.experimental_rerun
	except AttributeError:
		def _rerun():
			st.stop()


# Icon options
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
	df = dm.load_user_data('subscriptions.csv', initial_value=pd.DataFrame())
	if df is None or df.empty:
		return pd.DataFrame(columns=['name','start_date','amount','interval','active','link','icon'])
	# coerce types
	# if older data includes a 'provider' column, drop it to remove the field
	if 'provider' in df.columns:
		df = df.drop(columns=['provider'])
	# if older data includes a 'timestamp' column, drop it as well
	if 'timestamp' in df.columns:
		df = df.drop(columns=['timestamp'])
	# migrate URL-like values that were stored in 'notes' into 'link'
	if 'notes' in df.columns and 'link' not in df.columns:
		# keep only entries that look like a URL (http/https), else leave blank
		df['link'] = df['notes'].astype(str).where(df['notes'].astype(str).str.contains(r'^https?://', na=False), '')
		# drop legacy notes column
		df = df.drop(columns=['notes'])
	if 'start_date' in df.columns:
		df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce').dt.date
	df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0.0)
	df['active'] = df.get('active', True)
	# ensure link is string
	df['link'] = df['link'].astype(str).fillna('')
	# add icon column if not present
	if 'icon' not in df.columns:
		df['icon'] = '📱'
	return df


def _save(df):
	dm.save_user_data(df, 'subscriptions.csv')


def _calculate_metrics(df):
	"""Berechnet Metriken für die Übersicht"""
	active_subs = df[df['active'] == True] if not df.empty else df
	
	monthly_cost = 0
	yearly_cost = 0
	
	for _, row in active_subs.iterrows():
		if row['interval'] == 'Monthly':
			monthly_cost += float(row['amount'])
			yearly_cost += float(row['amount']) * 12
		elif row['interval'] == 'Yearly':
			yearly_cost += float(row['amount'])
		elif row['interval'] == 'Quarterly':
			monthly_cost += float(row['amount']) / 3
			yearly_cost += float(row['amount']) * 4
	
	return {
		'monthly': monthly_cost,
		'yearly': yearly_cost,
		'active_count': len(active_subs)
	}


def _calculate_next_renewal(start_date, interval):
	"""Berechnet das nächste Verlängerungsdatum"""
	if pd.isna(start_date):
		return date.today()
	
	next_renewal = start_date
	today = date.today()
	
	# Limit iterations to prevent infinite loops
	max_iterations = 100
	iterations = 0
	
	if interval == 'Monthly':
		while next_renewal <= today and iterations < max_iterations:
			try:
				# Add one month
				if next_renewal.month == 12:
					next_renewal = next_renewal.replace(year=next_renewal.year + 1, month=1)
				else:
					next_renewal = next_renewal.replace(month=next_renewal.month + 1)
			except ValueError:
				# Handle day overflow (e.g., Jan 31 -> Feb 31 doesn't exist)
				next_renewal = next_renewal.replace(day=1) + timedelta(days=32)
				next_renewal = next_renewal.replace(day=1)
			iterations += 1
	elif interval == 'Yearly':
		while next_renewal <= today and iterations < max_iterations:
			next_renewal = next_renewal.replace(year=next_renewal.year + 1)
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
		next_renewal = _calculate_next_renewal(row['start_date'], row['interval'])
		
		with st.container():
			col1, col2, col3, col4, col5 = st.columns([0.8, 2, 1.5, 1, 0.5])
			col1.write(row['icon'])
			
			col2.write(f"**{row['name']}**")
			interval_text = "Monatlich" if row['interval'] == 'Monthly' else "Jährlich" if row['interval'] == 'Yearly' else "Quartalsweise"
			col2.caption(f"Nächste Verlängerung: {next_renewal.strftime('%d.%m.%Y')}")
			
			col3.write(f"{row['amount']:.2f}€")
			col3.caption(interval_text)
			
			status = "✅ Aktiv" if row['active'] else "❌ Inaktiv"
			col4.write(status)
			
			if editable and col5.button('✏️', key=f'edit-{idx}', help='Bearbeiten'):
				st.session_state['edit_idx'] = idx
				_rerun()


# Load data
subs = _load()

# Edit form as separate "page"
if 'edit_idx' in st.session_state:
	edit_idx = st.session_state['edit_idx']
	if edit_idx < len(subs):
		row = subs.iloc[edit_idx]
		st.header(f"Abonnement bearbeiten: {row['icon']} {row['name']}")
		with st.form('edit_sub'):
			c1, c2 = st.columns(2)
			ename = c1.text_input('Name', value=row['name'])
			estart = st.date_input('Startdatum', value=row['start_date'] if not pd.isna(row['start_date']) else date.today())
			eamount = st.number_input('Betrag (CHF)', min_value=0.0, value=float(row['amount']), step=0.5)
			einterval = st.selectbox('Intervall', ['Monatlich','Jährlich','Quartalsweise'], index=['Monatlich','Jährlich','Quartalsweise'].index('Monatlich' if row['interval'] == 'Monthly' else 'Jährlich' if row['interval'] == 'Yearly' else 'Quartalsweise'))
			eactive = st.checkbox('Aktiv', value=bool(row['active']))
			elink = c2.text_input('Link (URL)', value=row.get('link',''))
			eicon = st.selectbox('Icon', options=list(ICON_OPTIONS.keys()), format_func=lambda x: f"{x} {ICON_OPTIONS[x]}", index=list(ICON_OPTIONS.keys()).index(row.get('icon', '📱')) if row.get('icon') in ICON_OPTIONS else 0)
			col1, col2, col3 = st.columns(3)
			if col1.form_submit_button('Speichern'):
				sd = pd.to_datetime(estart, errors='coerce')
				sd = sd.date() if not pd.isna(sd) else None
				interval_map = {'Monatlich': 'Monthly', 'Jährlich': 'Yearly', 'Quartalsweise': 'Quarterly'}
				subs.at[edit_idx, 'name'] = ename
				subs.at[edit_idx, 'start_date'] = sd
				subs.at[edit_idx, 'amount'] = float(eamount)
				subs.at[edit_idx, 'interval'] = interval_map.get(einterval, 'Monthly')
				subs.at[edit_idx, 'active'] = bool(eactive)
				subs.at[edit_idx, 'link'] = elink
				subs.at[edit_idx, 'icon'] = eicon
				_save(subs)
				del st.session_state['edit_idx']
				st.success('Änderungen gespeichert')
				_rerun()
			if col2.form_submit_button('Löschen'):
				subs = subs.drop(index=edit_idx).reset_index(drop=True)
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
	# Metriken oben anzeigen
	metrics = _calculate_metrics(subs)
	col1, col2, col3 = st.columns(3)
	with col1.container():
		st.metric("Monatliche Kosten", f"CHF {metrics['monthly']:.2f}")
	with col2.container():
		st.metric("Jährliche Kosten", f"CHF {metrics['yearly']:.2f}")
	with col3.container():
		st.metric("Aktive Abos", metrics['active_count'])
	
	st.divider()
	
	# Show tabs only when not editing
	tab_alle, tab_monatlich, tab_jährlich = st.tabs(['Alle', 'Monatlich', 'Jährlich'])

	with tab_alle:
		st.header('Alle Abonnements')
		_render_subscription_cards(subs, editable=True)

	with tab_monatlich:
		st.header('Monatliche Abonnements')
		dfm = subs[subs['interval']=='Monthly'] if not subs.empty else subs
		_render_subscription_cards(dfm, editable=False)

	with tab_jährlich:
		st.header('Jährliche Abonnements')
		dfy = subs[subs['interval']=='Yearly'] if not subs.empty else subs
		_render_subscription_cards(dfy, editable=False)

	st.divider()

	with st.expander('Neues Abo erfassen'):
		with st.form('add_sub'):
			c1, c2 = st.columns(2)
			name = c1.text_input('Name')
			start_date = st.date_input('Startdatum', value=date.today())
			amount = st.number_input('Betrag (CHF)', min_value=0.0, value=0.0, step=0.5)
			interval = st.selectbox('Intervall', ['Monatlich','Jährlich','Quartalsweise'])
			active = st.checkbox('Aktiv', value=True)
			link = c2.text_input('Link (URL)')
			icon = st.selectbox('Icon', options=list(ICON_OPTIONS.keys()), format_func=lambda x: f"{x} {ICON_OPTIONS[x]}")
			if st.form_submit_button('Hinzufügen'):
				if not name:
					st.error('Bitte geben Sie einen Namen ein')
				else:
					sd = pd.to_datetime(start_date, errors='coerce')
					sd = sd.date() if not pd.isna(sd) else None
					interval_map = {'Monatlich': 'Monthly', 'Jährlich': 'Yearly', 'Quartalsweise': 'Quarterly'}
					rec = {'name':name,'start_date':sd,'amount':float(amount),'interval':interval_map[interval],'active':active,'link': link, 'icon': icon}
					subs = pd.concat([subs, pd.DataFrame([rec])], ignore_index=True)
					_save(subs)
					st.success('Abonnement hinzugefügt')
					_rerun()
				_rerun()



