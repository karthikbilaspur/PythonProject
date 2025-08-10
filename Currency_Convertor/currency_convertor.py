from forex_python.converter import CurrencyRates, CurrencyCodes

class CurrencyConverter:
    def __init__(self):
        self.c = CurrencyRates()
        self.cc = CurrencyCodes()

    def convert_currency(self, amount, from_currency, to_currency):
        result = self.c.convert(from_currency, to_currency, amount)
        return result

    def get_currency_symbol(self, currency_code):
        symbol = self.cc.get_symbol(currency_code)
        return symbol

    def get_currency_name(self, currency_code):
        # Add a dictionary to map currency codes to names
        currency_names = {
            'USD': 'United States Dollar',
            'EUR': 'Euro',
            'INR': 'Indian Rupee',
            'GBP': 'British Pound',
            'AUD': 'Australian Dollar',
            'CAD': 'Canadian Dollar',
            'SGD': 'Singapore Dollar',
            # Add more currency codes and names as needed
        }
        return currency_names.get(currency_code, 'Unknown')

def main():
    converter = CurrencyConverter()

    print("Currency Converter")
    print("------------------")

    while True:
        print("1. Convert Currency")
        print("2. Get Currency Symbol")
        print("3. Get Currency Name")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            amount = float(input("Enter the amount: "))
            from_currency = input("Enter the from currency (e.g. USD, EUR, INR): ").upper()
            to_currency = input("Enter the to currency (e.g. USD, EUR, INR): ").upper()

            result = converter.convert_currency(amount, from_currency, to_currency)
            from_symbol = converter.get_currency_symbol(from_currency)
            to_symbol = converter.get_currency_symbol(to_currency)

            print(f"{amount} {from_symbol}{from_currency} = {result} {to_symbol}{to_currency}")
        elif choice == '2':
            currency_code = input("Enter the currency code (e.g. USD, EUR, INR): ").upper()
            symbol = converter.get_currency_symbol(currency_code)
            print(f"The symbol for {currency_code} is {symbol}")
        elif choice == '3':
            currency_code = input("Enter the currency code (e.g. USD, EUR, INR): ").upper()
            name = converter.get_currency_name(currency_code)
            print(f"The name for {currency_code} is {name}")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()