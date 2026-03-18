from unittest import result
import datetime

# Wechselkurse zu EUR (Basiswährung)
EXCHANGE_RATES = {
    "EUR": 1.0,
    "USD": 1.08,
    "GBP": 0.86,
    "JPY": 160.5,
    "CHF": 0.95
}

def convert_currency(amount, from_currency, to_currency):
    """
    Konvertiert einen Betrag von einer Währung in eine andere.
    
    Args:
        amount: Betrag zum Umrechnen
        from_currency: Ausgangs-Währung (z.B. "EUR")
        to_currency: Ziel-Währung (z.B. "USD")
    
    Returns:
        Umgerechneter Betrag
    """
    
    # Umrechnung
    amount_in_eur = amount / EXCHANGE_RATES[from_currency]
    result = amount_in_eur * EXCHANGE_RATES[to_currency]
 
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "eingabe": amount,
        "amount_in_eur": amount_in_eur,
        "result": result,
    }

    
    
    