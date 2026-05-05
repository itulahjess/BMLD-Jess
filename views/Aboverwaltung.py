import streamlit as st
import pandas as pd
from datetime import date
from utils.data_manager import DataManager


st.title("Aboverwaltung")


dm = DataManager()
if st.session_state.get('username') is None:
	st.error('Kein Benutzer eingeloggt. Bitte zuerst anmelden.')
	st.stop()


# rerun compatibility: some streamlit versions may not expose experimental_rerun
try:
	_rerun = st.experimental_rerun  # type: ignore[attr-defined]
except Exception:
	try:
		# newer runtime location
		from streamlit.runtime.scriptrunner import RerunException

		def _rerun():
			raise RerunException()
	except Exception:
		# last fallback: stop the script (best-effort)
		def _rerun():
			st.stop()


def _load():
	df = dm.load_user_data('subscriptions.csv', initial_value=pd.DataFrame())
	if df is None or df.empty:
		return pd.DataFrame(columns=['name','start_date','amount','interval','active','link'])
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


with st.expander('Neues Abo hinzufügen'):
	with st.form('add_sub'):
		c1, c2 = st.columns(2)
		name = c1.text_input('Name')
		start_date = st.date_input('Startdatum', value=date.today())
		amount = st.number_input('Betrag', min_value=0.0, value=0.0, step=0.5)
		interval = st.selectbox('Intervall', ['Monthly','Yearly','Quarterly'])
		active = st.checkbox('Aktiv', value=True)
		link = c2.text_input('Link (URL)')
		if st.form_submit_button('Hinzufügen'):
			# ensure start_date is stored as a date (no time component)
			sd = pd.to_datetime(start_date, errors='coerce')
			sd = sd.date() if not pd.isna(sd) else None
			rec = {'name':name,'start_date':sd,'amount':float(amount),'interval':interval,'active':active,'link': link}
			subs = pd.concat([subs, pd.DataFrame([rec])], ignore_index=True)
			_save(subs)
			st.success('Abonnement hinzugefügt')


tab_all, tab_monthly, tab_yearly = st.tabs(['Alle','Monatlich','Jährlich'])


def _render_table(df, scope=""):
	if df.empty:
		st.info('Keine Abonnemente gefunden')
		return
	df_display = df.copy()
	df_display['start_date'] = df_display['start_date'].astype(str)
	st.dataframe(df_display)
	# actions
	for local_i, (idx, row) in enumerate(df.iterrows()):
		cols = st.columns([3,1])
		with cols[0]:
			st.write(f"**{row['name']}** ({row['interval']})")
			link = row.get('link','')
			if pd.notna(link) and str(link).strip():
				st.markdown(f"[Link]({link})")
		with cols[1]:
			btn_del_key = f"del-{scope}-{idx}"
			btn_edit_key = f"edit-{scope}-{idx}"
			if st.button('Bearbeiten', key=btn_edit_key):
				st.session_state['edit_idx'] = int(idx)
			if st.button('Löschen', key=btn_del_key):
				_safe_delete(idx)


with tab_all:
	st.header('Alle Abonnemente')
	_render_table(subs, scope='all')

with tab_monthly:
	st.header('Monatliche Abonnemente')
	dfm = subs[subs['interval']=='Monthly'] if not subs.empty else subs
	_render_table(dfm, scope='monthly')

with tab_yearly:
	st.header('Jährliche Abonnemente')
	dfy = subs[subs['interval']=='Yearly'] if not subs.empty else subs
	_render_table(dfy, scope='yearly')

# Edit form (appears when edit_idx is set)
if 'edit_idx' in st.session_state:
	edit_i = st.session_state.pop('edit_idx')
	if edit_i not in subs.index:
		st.error('Ungültiger Eintrag zum Bearbeiten')
	else:
		row = subs.loc[edit_i]
		st.subheader('Abonnement bearbeiten')
		with st.form('edit_sub'):
			c1, c2 = st.columns(2)
			ename = c1.text_input('Name', value=row['name'])
			estart = st.date_input('Startdatum', value=row['start_date'] if not pd.isna(row['start_date']) else date.today())
			eamount = st.number_input('Betrag', min_value=0.0, value=float(row['amount']), step=0.5)
			einterval = st.selectbox('Intervall', ['Monthly','Yearly','Quarterly'], index=['Monthly','Yearly','Quarterly'].index(row['interval']) if row['interval'] in ['Monthly','Yearly','Quarterly'] else 0)
			eactive = st.checkbox('Aktiv', value=bool(row['active']))
			elink = c2.text_input('Link (URL)', value=row.get('link',''))
			if st.form_submit_button('Speichern'):
				sd = pd.to_datetime(estart, errors='coerce')
				sd = sd.date() if not pd.isna(sd) else None
				subs.at[edit_i, 'name'] = ename
				subs.at[edit_i, 'start_date'] = sd
				subs.at[edit_i, 'amount'] = float(eamount)
				subs.at[edit_i, 'interval'] = einterval
				subs.at[edit_i, 'active'] = bool(eactive)
				subs.at[edit_i, 'link'] = elink
				_save(subs)
				st.success('Änderungen gespeichert')
				_rerun()

