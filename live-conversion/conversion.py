from decimal import Decimal
from typing import Protocol, cast

from forex_python.converter import CurrencyCodes, CurrencyRates  # pyright: ignore[reportMissingTypeStubs]


class CurrencyRatesProtocol(Protocol):
    def convert(self, base_cur: str, dest_cur: str, amount: float) -> Decimal | float:
        ...

    def get_rates(self, base_cur: str) -> dict[str, object] | None:
        ...


class CurrencyCodesProtocol(Protocol):
    def get_symbol(self, currency_code: str) -> str | None:
        ...

    def get_currency_name(self, currency_code: str) -> str | None:
        ...


class CurrencyConverter:
    def __init__(self):
        self.c = cast(CurrencyRatesProtocol, CurrencyRates())
        self.codes = cast(CurrencyCodesProtocol, CurrencyCodes())

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float | None:
        """Converts currency from one type to another"""
        try:
            result = self.c.convert(from_currency, to_currency, amount)
            return float(result)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_currency_symbol(self, currency_code: str) -> str | None:
        """Gets the symbol for a given currency code"""
        try:
            return self.codes.get_symbol(currency_code)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_currency_name(self, currency_code: str) -> str | None:
        """Gets the name for a given currency code"""
        try:
            name = self.codes.get_currency_name(currency_code)
            return name
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

def main():
    converter = CurrencyConverter()

    while True:
        try:
            amount = float(input("Enter the amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    from_currency = input("Enter the from currency (e.g. USD, EUR, JPY): ").upper()
    while not converter.c.get_rates(from_currency):
        print("Invalid currency code. Please check the currency codes.")
        from_currency = input("Enter the from currency (e.g. USD, EUR, JPY): ").upper()

    to_currency = input("Enter the to currency (e.g. USD, EUR, JPY): ").upper()
    while not converter.c.get_rates(to_currency):
        print("Invalid currency code. Please check the currency codes.")
        to_currency = input("Enter the to currency (e.g. USD, EUR, JPY): ").upper()

    result = converter.convert_currency(amount, from_currency, to_currency)
    symbol = converter.get_currency_symbol(to_currency)
    from_symbol = converter.get_currency_symbol(from_currency)
    from_name = converter.get_currency_name(from_currency)
    to_name = converter.get_currency_name(to_currency)

    if result:
        print(f"{amount} {from_currency} ({from_name}) {from_symbol} is equal to {result} {to_currency} ({to_name}) {symbol}")

if __name__ == "__main__":
    main()