from babel.numbers import format_currency
import decimal
from django.db import models


class PaymentMethodEnum(models.TextChoices):
    tasa = "tasa 0", "T0"
    card = "card", "Card"
    cash = "cash", "Cash"
    na = "na", "N/A"


def factor_tasa_0():
    return 0.81


def factor_card():
    return 0.9268


def price_formatted(price):
    return f'{price:,}₡'


def commission_price(price, factor):
    return round(price / decimal.Decimal(factor), 2)


def formatted_number(number):
    return str(format_currency(number, 'CRC', locale='es_CR'))


def choices_payment(method, price):
    payment = {
        "Credit Card/Debit Card": {
            "method": PaymentMethodEnum.card,
            "price": commission_price(price, factor_card())
        },
        "Sinpe": {
            "method": PaymentMethodEnum.cash,
            "price": price
        },
        "Cash": {
            "method": PaymentMethodEnum.cash,
            "price": price
        },
        "Transfer": {
            "method": PaymentMethodEnum.cash,
            "price": price
        },
        "Tasa 0": {
            "method": PaymentMethodEnum.tasa,
            "price": commission_price(price, factor_tasa_0())
        },
    }

    return payment[method]
