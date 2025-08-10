# Currency Convertor

This code is a simple currency converter application written in Python. Here's a summary:
Key Features:
Currency Conversion: Converts an amount from one currency to another using the forex_python library.
Currency Symbol Retrieval: Retrieves the symbol for a given currency code.
Currency Name Retrieval: Retrieves the name for a given currency code.
How it Works:
The application initializes a CurrencyConverter object, which uses the forex_python library to access currency rates and codes.
The user is presented with a menu to choose from four options: convert currency, get currency symbol, get currency name, or quit.
Based on the user's choice, the application prompts for additional input (e.g., amount, from currency, to currency) and performs the selected action.
The application displays the result of the user's chosen action.
Code Structure:
The CurrencyConverter class encapsulates the currency conversion and retrieval functionality.
The main function implements the menu-driven interface and handles user input.
This application provides a simple and intuitive way to perform currency-related tasks, making it useful for individuals who need to work with multiple currencies.
