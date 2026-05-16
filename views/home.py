import streamlit as st
import pandas as pd
from utils.data_manager import DataManager

st.markdown("""
<style>

/* METRIC LABEL (Bezeichnung) */
div[data-testid="stMetric"] * {
    font-size: 30px !important;
    font-weight: 900 !important;
    color: #054033 !important;
}

/* METRIC VALUE (Zahl) */
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 42px !important;
    font-weight: 900 !important;
    color: #1b5e54 !important;
}

/* METRIC BOX */
div[data-testid="stMetric"] {
    background-color: #e8fff5;
    padding: 20px;
    border-radius: 18px;
}

</style>
""", unsafe_allow_html=True)

dm = DataManager()

# Daten laden
subs = dm.load_user_data(
    'subscriptions.csv',
    initial_value=pd.DataFrame()
)

# Falls leer
if subs is None or subs.empty:
    st.info("Noch keine Abonnements vorhanden.")
    st.stop()

# Nur aktive Abos
active_subs = subs[subs['active'] == True]

# Kosten berechnen
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

# Begrüssung
name = st.session_state.get("name", "User")

st.markdown(f"""
<div style="
    background:#e8fff5;
    padding:30px;
    border-radius:20px;
    margin-bottom:30px;
">
    <h2>Hallo {name} 👋</h2>
    <p>Willkommen zurück zu deiner Aboverwaltung.</p>
</div>
""", unsafe_allow_html=True)

# Metriken
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Monatliche Kosten", f"CHF {monthly_cost:.2f}")

with col2:
    st.metric("Jährliche Kosten", f"CHF {yearly_cost:.2f}")

with col3:
    st.metric("Aktive Abos", len(active_subs))




# !! WICHTIG: Eure Emails müssen in der App erscheinen!!



"""
Diese App wurde von folgenden Personen entwickelt:
- Jessica Itulah (itulajes@students.zhaw.ch)
- Medhani Kathirkamanathan (kathimed@students.zhaw.ch)
- Michelle Assadi Rad (assadmic@students.zhaw.ch)

Kaitas wurde entwickelt, um eine übersichtliche Verwaltung aller Abonnemente zu ermöglichen.
"""

