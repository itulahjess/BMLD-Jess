import streamlit as st

st.title("Währungsrechner")

st.write("Hier kannst du verschiedene Währungen umrechnen. Gib den Betrag und die Währungen ein, um die Umrechnung durchzuführen.")

with st.form("currency_form"):
    amount = st.number_input("Betrag", min_value=0.0, step=0.01)
    from_currency = st.selectbox("Von Währung", ["USD", "EUR", "
GBP", "JPY"])
    to_currency = st.selectbox("Zu Währung", ["USD", "EUR", "GBP", "JPY"])
    submit_button = st.form_submit_button("Umrechnen") 
if submit_button:
    # Hier könntest du die Umrechnungslogik implementieren, z.B. mit einem API-Aufruf
    st.write(f"{amount} {from_currency} entsprechen X {to_currency}. (Umrechnungslogik hier implementieren)")
    