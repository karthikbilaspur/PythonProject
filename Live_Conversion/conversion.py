from forex_python.converter import CurrencyRates, CurrencyCodes

def convert_currency(amount, from_currency, to_currency):
    c = CurrencyRates()
    result = c.convert(from_currency, to_currency, amount)
    return result

def get_currency_symbol(currency_code):
    codes = CurrencyCodes()
    symbol = codes.get_symbol(currency_code)
    return symbol

def main():
    amount = float(input("Enter the amount: "))
    from_currency = input("Enter the from currency (e.g. USD, EUR, JPY): ").upper()
    to_currency = input("Enter the to currency (e.g. USD, EUR, JPY): ").upper()

    result = convert_currency(amount, from_currency, to_currency)
    symbol = get_currency_symbol(to_currency)

    print(f"{amount} {from_currency} is equal to {result} {to_currency} {symbol}")

if __name__ == "__main__":
    main()
    