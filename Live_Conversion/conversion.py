from forex_python.converter import CurrencyRates, CurrencyCodes

class CurrencyConverter:
    def __init__(self):
        self.c = CurrencyRates()
        self.codes = CurrencyCodes()

    def convert_currency(self, amount, from_currency, to_currency):
        """Converts currency from one type to another"""
        try:
            result = self.c.convert(from_currency, to_currency, amount)
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_currency_symbol(self, currency_code):
        """Gets the symbol for a given currency code"""
        try:
            symbol = self.codes.get_symbol(currency_code)
            return symbol
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_currency_name(self, currency_code):
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