import math
from datetime import datetime
from decimal import Decimal

from trading_bots.contrib.money import Money

DECIMALS = {
    # Fiat
    'ARS': 2,
    'BRL': 2,
    'CLP': 2,
    'COP': 2,
    'EUR': 2,
    'PEN': 2,
    'USD': 2,
    # Crypto
    'BCH': 8,
    'BTC': 8,
    'ETH': 8,
    'LTC': 8,
}


def get_iso_time_str(timestamp=None):
    """Get the ISO time string from a timestamp or date obj. Returns current time str if no timestamp is passed"""
    if isinstance(timestamp, (int, float)):
        timestamp = datetime.utcfromtimestamp(timestamp)
    if timestamp is None:
        timestamp = datetime.utcnow()
    return timestamp.isoformat(sep=' ', timespec='seconds')


def truncate(value: Decimal, n_digits: int) -> Decimal:
    """Truncates a value to a number of decimals places"""
    return Decimal(math.trunc(value * (10 ** n_digits))) / (10 ** n_digits)


def truncate_to(value: Decimal, currency: str) -> Decimal:
    """Truncates a value to the number of decimals corresponding to the currency"""
    decimal_places = DECIMALS.get(currency.upper(), 2)
    return truncate(value, decimal_places)


def truncate_money(money: Money) -> Money:
    """Truncates money amount to the number of decimals corresponding to the currency"""
    amount = truncate_to(money.amount, money.currency)
    return Money(amount, money.currency)


def spread_value(value: float, spread_p: float):
    """Returns a lower and upper value separated by a spread percentage"""
    upper = value * (1 + spread_p)
    lower = value / (1 + spread_p)
    return lower, upper


def validate(name: str, value, condition: bool):
    """Validates value on condition"""
    assert condition, f'{name} is invalid! ({name}: {value})'


def validate_age(name: str, tolerance, from_timestamp, to_timestamp):
    """Check if age is valid (within tolerance)"""
    age = to_timestamp - from_timestamp
    assert age <= tolerance, f'{name} is too old! (Age: {age} > Tolerance: {tolerance})'
