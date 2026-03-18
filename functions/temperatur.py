from unittest import result
import datetime


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
    # Wechselkurse (Basis: EUR = 1)
    exchange_rates = {
        "EUR": 1.0,
        "USD": 1.10,
        "GBP": 0.86,
        "JPY": 130.50
    }
    
    # Umrechnung
    amount_in_eur = amount / exchange_rates[from_currency]
    result = amount_in_eur * exchange_rates[to_currency]
 
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "eingabe": amount,
        "amount_in_eur": amount_in_eur,
        "result": result,
    }

    
    
    