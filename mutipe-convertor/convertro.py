import requests
import math
import datetime

# Define conversion functions
def currency_converter(amount, from_currency, to_currency):
    api_key = "YOUR_CURRENCY_API_KEY"  # Get your API key from free.currconv.com
    url = f"https://free.currconv.com/api/v7/convert?q={from_currency}_{to_currency}&compact=ultra&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    if f"{from_currency}_{to_currency}" in data:
        return amount * data[f"{from_currency}_{to_currency}"]
    else:
        return "Invalid currency"

def length_converter(value, from_unit, to_unit):
    conversions = {
        "km": {"m": 1000, "cm": 100000, "mm": 1000000, "mi": 0.621371, "in": 39370.1, "ft": 3280.84},
        "m": {"km": 0.001, "cm": 100, "mm": 1000, "mi": 0.000621371, "in": 39.3701, "ft": 3.28084},
        "cm": {"km": 0.00001, "m": 0.01, "mm": 10, "mi": 0.00000621371, "in": 0.393701, "ft": 0.0328084},
        "mm": {"km": 0.000001, "m": 0.001, "cm": 0.1, "mi": 0.000000621371, "in": 0.0393701, "ft": 0.00328084},
        "mi": {"km": 1.60934, "m": 1609.34, "cm": 160934, "mm": 1609340, "in": 63360, "ft": 5280},
        "in": {"km": 0.0000254, "m": 0.0254, "cm": 2.54, "mm": 25.4, "mi": 0.000015783, "ft": 0.0833333},
        "ft": {"km": 0.0003048, "m": 0.3048, "cm": 30.48, "mm": 304.8, "mi": 0.000189394, "in": 12}
    }
    return value * conversions[from_unit][to_unit]

def temperature_converter(value, from_unit, to_unit):
    if from_unit == "C" and to_unit == "F":
        return (value * 9/5) + 32
    elif from_unit == "F" and to_unit == "C":
        return (value - 32) * 5/9
    elif from_unit == "C" and to_unit == "K":
        return value + 273.15
    elif from_unit == "K" and to_unit == "C":
        return value - 273.15
    elif from_unit == "F" and to_unit == "K":
        return (value - 32) * 5/9 + 273.15
    elif from_unit == "K" and to_unit == "F":
        return (value - 273.15) * 9/5 + 32

def area_converter(value, from_unit, to_unit):
    conversions = {
        "sq_km": {"sq_m": 1000000, "sq_mi": 0.386102, "acre": 247.105},
        "sq_m": {"sq_km": 0.000001, "sq_mi": 0.000000386102, "acre": 0.000247105},
        "sq_mi": {"sq_km": 2.58999, "sq_m": 2589990, "acre": 640},
        "acre": {"sq_km": 0.00404686, "sq_m": 4046.86, "sq_mi": 0.0015625}
    }
    return value * conversions[from_unit][to_unit]

def weight_converter(value, from_unit, to_unit):
    conversions = {
        "kg": {"g": 1000, "mg": 1000000, "t": 0.001, "lb": 2.20462, "oz": 35.274},
        "g": {"kg": 0.001, "mg": 1000, "t": 0.000001, "lb": 0.00220462, "oz": 0.035274},
        "mg": {"kg": 0.000001, "g": 0.001, "t": 0.000000001, "lb": 0.00000220462, "oz": 0.000035274},
        "t": {"kg": 1000, "g": 1000000, "mg": 1000000000, "lb": 2204.62, "oz": 35274},
        "lb": {"kg": 0.453592, "g": 453.592, "mg": 453592, "t": 0.000453592, "oz": 16},
        "oz": {"kg": 0.0283495, "g": 28.3495, "mg": 28349.5, "t": 0.0000283495, "lb": 0.0625}
    }
    return value * conversions[from_unit][to_unit]

def time_converter(value, from_unit, to_unit):
    conversions = {
        "s": {"min": 0.0166667, "h": 0.000277778, "d": 0.000011574},
        "min": {"s": 60, "h": 0.0166667, "d": 0.000694444},
        "h": {"s": 3600, "min": 60, "d": 0.0416667},
        "d": {"s": 86400, "min": 1440, "h": 24}
    }
    return value * conversions[from_unit][to_unit]

def speed_converter(value, from_unit, to_unit):
    conversions = {
        "km/h": {"m/s": 0.277778, "mi/h": 0.621371, "ft/s": 0.911344},
        "m/s": {"km/h": 3.6, "mi/h": 2.23694, "ft/s": 3.28084},
        "mi/h": {"km/h": 1.60934, "m/s": 0.44704, "ft/s": 1.46667},
        "ft/s": {"km/h": 1.09728, "m/s": 0.3048, "mi/h": 0.681818}
    }
    return value * conversions[from_unit][to_unit]

def showcase_sensex():
    # You would need an API key for this. For simplicity, let's just return a static value.
    return "Sensex: 55000"

def showcase_nifty():
    # You would need an API key for this. For simplicity, let's just return a static value.
    return "Nifty: 16000"

def calculator():
    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exponentiation")
        print("6. Back")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            print(f"{num1} + {num2} = {num1 + num2}")
        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            print(f"{num1} - {num2} = {num1 - num2}")
        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            print(f"{num1} * {num2} = {num1 * num2}")
        elif choice == "4":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            if num2 != 0:
                print(f"{num1} / {num2} = {num1 / num2}")
            else:
                print("Error: Division by zero")
        elif choice == "5":
            num1 = float(input("Enter base number: "))
            num2 = float(input("Enter exponent: "))
            print(f"{num1} ^ {num2} = {math.pow(num1, num2)}")
        elif choice == "6":
            break
        else:
            print("Invalid choice")

def main():
    while True:
        print("\nMain Menu:")
        print("1. Unit Converter")
        print("2. Calculator")
        print("3. Showcase Sensex")
        print("4. Showcase Nifty")
        print("5. Current Date and Time")
        print("6. Quit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                print("\nUnit Converter Menu:")
                print("1. Currency Converter")
                print("2. Length Converter")
                print("3. Temperature Converter")
                print("4. Area Converter")
                print("5. Weight Converter")
                print("6. Time Converter")
                print("7. Speed Converter")
                print("8. Back")
                
                unit_choice = input("Enter your choice: ")

                if unit_choice == "1":
                    amount = float(input("Enter amount: "))
                    from_currency = input("Enter from currency (e.g., USD): ").upper()
                    to_currency = input("Enter to currency (e.g., EUR): ").upper()
                    print(f"{amount} {from_currency} = {currency_converter(amount, from_currency, to_currency)} {to_currency}")
                elif unit_choice == "2":
                    value = float(input("Enter value: "))
                    from_unit = input("Enter from unit (km, m, cm, mm, mi, in, ft): ")
                    to_unit = input("Enter to unit (km, m, cm, mm, mi, in, ft): ")
                    print(f"{value} {from_unit} = {length_converter(value, from_unit, to_unit)} {to_unit}")
                elif unit_choice == "3":
                    value = float(input("Enter value: "))
                    from_unit = input("Enter from unit (C, F, K): ")
                    to_unit = input("Enter to unit (C, F, K): ")
                    print(f"{value} {from_unit} = {temperature_converter(value, from_unit, to_unit)} {to_unit}")
                elif unit_choice == "4":
                    value = float(input("Enter value: "))
                    from_unit = input("Enter from unit (sq_km, sq_m, sq_mi, acre): ")
                    to_unit = input("Enter to unit (sq_km, sq_m, sq_mi, acre): ")
                    print(f"{value} {from_unit} = {area_converter(value, from_unit, to_unit)} {to_unit}")
                elif unit_choice == "5":
                    value = float(input("Enter value: "))
                    from_unit = input("Enter from unit (kg, g, mg, t, lb, oz): ")
                    to_unit = input("Enter to unit (kg, g, mg, t, lb, oz): ")
                    print(f"{value} {from_unit} = {weight_converter(value, from_unit, to_unit)} {to_unit}")
                elif unit_choice == "6":
                    value = float(input("Enter value: "))
                    from_unit = input("Enter from unit (s, min, h, d): ")
                    to_unit = input("Enter to unit (s, min, h, d): ")
                    print(f"{value} {from_unit} = {time_converter(value, from_unit, to_unit)} {to_unit}")
                elif unit_choice == "7":
                    value = float(input("Enter value: "))
                    from_unit = input("Enter from unit (km/h, m/s, mi/h, ft/s): ")
                    to_unit = input("Enter to unit (km/h, m/s, mi/h, ft/s): ")
                    print(f"{value} {from_unit} = {speed_converter(value, from_unit, to_unit)} {to_unit}")
                elif unit_choice == "8":
                    break
                else:
                    print("Invalid choice")
        elif choice == "2":
            calculator()
        elif choice == "3":
            print(showcase_sensex())
        elif choice == "4":
            print(showcase_nifty())
        elif choice == "5":
            print(f"Current Date and Time: {datetime.datetime.now()}")
        elif choice == "6":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
