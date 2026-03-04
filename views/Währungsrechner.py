import streamlit as st

# Wechselkurse zu EUR (Basiswährung)
EXCHANGE_RATES = {
    "EUR": 1.0,
    "USD": 1.08,
    "GBP": 0.86,
    "JPY": 160.5,
    "CHF": 0.95
}

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Konvertiert einen Betrag von einer Währung zu einer anderen."""
    if from_currency == to_currency:
        return amount
    
    # Umrechnung über EUR als Basiswährung
    amount_in_eur = amount / EXCHANGE_RATES[from_currency]
    result = amount_in_eur * EXCHANGE_RATES[to_currency]
    return result

st.title("Währungsrechner")

st.write("Hier kannst du verschiedene Währungen umrechnen. Gib den Betrag und die Währungen ein, um die Umrechnung durchzuführen.")

currencies = list(EXCHANGE_RATES.keys())

with st.form("currency_form"):
    amount = st.number_input("Betrag", min_value=0.0, step=0.01, value=1.0)
    from_currency = st.selectbox("Von Währung", currencies, index=0)
    to_currency = st.selectbox("Zu Währung", currencies, index=1)
    submit_button = st.form_submit_button("Umrechnen") 

if submit_button:
    if amount > 0:
        result = convert_currency(amount, from_currency, to_currency)
        st.success(f"💱 **{amount:.2f} {from_currency} = {result:.2f} {to_currency}**")
        st.info(f"Wechselkurs: 1 {from_currency} = {result/amount:.4f} {to_currency}")
    else:
        st.warning("Bitte einen positiven Betrag eingeben!")


    