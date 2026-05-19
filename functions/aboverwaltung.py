import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.data_manager import DataManager


dm = DataManager()


try:
	_rerun = st.rerun
except AttributeError:
	try:
		_rerun = st.experimental_rerun
	except AttributeError:
		def _rerun():
			st.stop()
			


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

from functions.aboübersicht import _interval_to_text

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
			
            col1,col2, col3, col4, col5 = st.columns(
                [0.75, 2.2, 1.35, 1.1, 0.55]
            )
			
            with col1:
                st.markdown(icon_html, unsafe_allow_html=True)

            with col2:
                st.markdown(
				    f"""
			        <div class="sub-name">{row['name']}</div>
			        <div class="sub-detail">
                        Nächtste Verlängerung:<br>
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
                    key=f'edit_{idx}',
				    help='Bearbeiten',  
                ):
                
                    st.session_state['edit_idx'] = idx
                    _rerun()
				

subs = _load()





