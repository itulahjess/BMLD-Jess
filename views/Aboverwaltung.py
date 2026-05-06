import streamlit as st
import pandas as pd
from datetime import date
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
	'📷': 'Camera',
	'📱': 'Smartphone',
	'🎵': 'Music',
	'📺': 'TV',
	'🎮': 'Gaming',
	'📚': 'Books',
	'💼': 'Business',
	'🏠': 'Home',
	'🍎': 'Apple',
	'🎥': 'Video',
	'🌐': 'Web',
	'📧': 'Email',
	'📰': 'News',
	'🎬': 'Entertainment',
	'💳': 'Finance'
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


subs = _load()


def _safe_delete(index):
	"""Try to delete a subscription by original index without throwing errors to the UI.
	If the index is already gone or deletion fails, quietly refresh the UI and show a friendly notice.
	"""
	try:
		if index in subs.index:
			subs.drop(index=index, inplace=True)
			subs.reset_index(drop=True, inplace=True)
			_save(subs)
			_rerun()
		else:
			# already deleted by another action — refresh silently
			_rerun()
	except Exception:
		# do not show a full traceback to the user; give a short message and refresh
		st.warning('Löschen fehlgeschlagen. Bitte die Seite neu laden oder erneut versuchen.')
		_rerun()


def _render_subscription_cards(df, editable=True):
	if df.empty:
		st.info('Keine Abonnemente gefunden')
		return
	for idx, row in df.iterrows():
		with st.container():
			col1, col2, col3 = st.columns([1, 4, 1])
			col1.write(row['icon'])
			col2.write(f"**{row['name']}** - {row['amount']:.2f}€ ({row['interval']})")
			col2.write(f"Start: {row['start_date']} | Aktiv: {'Ja' if row['active'] else 'Nein'}")
			if editable and col3.button('Bearbeiten', key=f'edit-{idx}'):
				st.session_state['edit_idx'] = idx
				_rerun()


# Edit form as separate "page"
if 'edit_idx' in st.session_state:
	edit_idx = st.session_state['edit_idx']
	if edit_idx in subs.index:
		row = subs.loc[edit_idx]
		st.header(f"Abonnement bearbeiten: {row['icon']} {row['name']}")
		with st.form('edit_sub'):
			c1, c2 = st.columns(2)
			ename = c1.text_input('Name', value=row['name'])
			estart = st.date_input('Startdatum', value=row['start_date'] if not pd.isna(row['start_date']) else date.today())
			eamount = st.number_input('Betrag', min_value=0.0, value=float(row['amount']), step=0.5)
			einterval = st.selectbox('Intervall', ['Monthly','Yearly','Quarterly'], index=['Monthly','Yearly','Quarterly'].index(row['interval']) if row['interval'] in ['Monthly','Yearly','Quarterly'] else 0)
			eactive = st.checkbox('Aktiv', value=bool(row['active']))
			elink = c2.text_input('Link (URL)', value=row.get('link',''))
			eicon = st.selectbox('Icon', options=list(ICON_OPTIONS.keys()), format_func=lambda x: f"{x} {ICON_OPTIONS[x]}", index=list(ICON_OPTIONS.keys()).index(row.get('icon', '📱')) if row.get('icon') in ICON_OPTIONS else 0)
			col1, col2, col3 = st.columns(3)
			if col1.form_submit_button('Speichern'):
				sd = pd.to_datetime(estart, errors='coerce')
				sd = sd.date() if not pd.isna(sd) else None
				subs.at[edit_idx, 'name'] = ename
				subs.at[edit_idx, 'start_date'] = sd
				subs.at[edit_idx, 'amount'] = float(eamount)
				subs.at[edit_idx, 'interval'] = einterval
				subs.at[edit_idx, 'active'] = bool(eactive)
				subs.at[edit_idx, 'link'] = elink
				subs.at[edit_idx, 'icon'] = eicon
				_save(subs)
				del st.session_state['edit_idx']
				st.success('Änderungen gespeichert')
				_rerun()
			if col2.form_submit_button('Löschen'):
				_safe_delete(edit_idx)
				del st.session_state['edit_idx']
				_rerun()
			if col3.form_submit_button('Abbrechen'):
				del st.session_state['edit_idx']
				_rerun()
	else:
		st.error('Ungültiges Abo zum Bearbeiten')
		del st.session_state['edit_idx']
else:
	# Show tabs only when not editing
	tab_all, tab_monthly, tab_yearly = st.tabs(['Alle','Monatlich','Jährlich'])

	with tab_all:
		st.header('Alle Abonnemente')
		_render_subscription_cards(subs, editable=True)

	with tab_monthly:
		st.header('Monatliche Abonnemente')
		dfm = subs[subs['interval']=='Monthly'] if not subs.empty else subs
		_render_subscription_cards(dfm, editable=False)

	with tab_yearly:
		st.header('Jährliche Abonnemente')
		dfy = subs[subs['interval']=='Yearly'] if not subs.empty else subs
		_render_subscription_cards(dfy, editable=False)

	st.divider()

	with st.expander('➕ Neues Abo erfassen'):
		with st.form('add_sub'):
			c1, c2 = st.columns(2)
			name = c1.text_input('Name')
			start_date = st.date_input('Startdatum', value=date.today())
			amount = st.number_input('Betrag', min_value=0.0, value=0.0, step=0.5)
			interval = st.selectbox('Intervall', ['Monthly','Yearly','Quarterly'])
			active = st.checkbox('Aktiv', value=True)
			link = c2.text_input('Link (URL)')
			icon = st.selectbox('Icon', options=list(ICON_OPTIONS.keys()), format_func=lambda x: f"{x} {ICON_OPTIONS[x]}")
			if st.form_submit_button('Hinzufügen'):
				# ensure start_date is stored as a date (no time component)
				sd = pd.to_datetime(start_date, errors='coerce')
				sd = sd.date() if not pd.isna(sd) else None
				rec = {'name':name,'start_date':sd,'amount':float(amount),'interval':interval,'active':active,'link': link, 'icon': icon}
				subs = pd.concat([subs, pd.DataFrame([rec])], ignore_index=True)
				_save(subs)
				st.success('Abonnement hinzugefügt')



