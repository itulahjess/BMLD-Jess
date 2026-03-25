import streamlit as st  # type: ignore
import datetime
from utils.data_manager import DataManager
from functions.temperatur import convert_currency, EXCHANGE_RATES
import pandas as pd  # type: ignore

st.title("Währungsrechner")

st.write("Hier kannst du verschiedene Währungen umrechnen. Gib den Betrag und die Währungen ein, um die Umrechnung durchzuführen.")


with st.form("currency_form"):
    amount = st.number_input("Betrag", min_value=0.0, step=0.01, value=1.0)
    from_currency = st.selectbox("Von Währung", EXCHANGE_RATES, index=0)
    to_currency = st.selectbox("Zu Währung", EXCHANGE_RATES, index=1)
    submit_button = st.form_submit_button("Umrechnen") 

if submit_button:
    if amount > 0:
        result = convert_currency(amount, from_currency, to_currency)

        st.session_state['data_df'] = pd.concat([st.session_state['data_df'], pd.DataFrame([result])])
        
        # --- CODE UPDATE: save data to data manager ---
        data_manager = DataManager()
        data_manager.save_user_data(st.session_state['data_df'], 'data.csv')
        # --- END OF CODE UPDATE ---
    else:
        st.warning("Bitte einen positiven Betrag eingeben!")
        
# display the data frame in a table
st.dataframe(st.session_state['data_df'])

# Add a simple chart of the conversion results
if not st.session_state['data_df'].empty:
    st.subheader("Verlauf der Umrechnungen")
    chart_df = st.session_state['data_df'].copy()
    chart_df['timestamp'] = pd.to_datetime(chart_df['timestamp'], format='ISO8601')  # --- CODE UPDATE: specify format for timestamp ---
    st.line_chart(chart_df.set_index('timestamp')['result'])