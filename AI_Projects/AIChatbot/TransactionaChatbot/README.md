Overview
This project integrates various banking APIs to provide a range of services, including user authentication, account management, transaction history, bill payment, fund transfer, and payment gateway integration. The project also includes multi-language support and SBI API integration.
Features
User Authentication: Authenticates users using a username and password
Account Management: Retrieves account information and transaction history
Bill Payment: Pays bills using a bill ID and amount
Fund Transfer: Transfers funds to a recipient's account
Payment Gateway Integration: Integrates with various payment gateways, including PayPal, Stripe, and UPI
Multi-Language Support: Translates text into different languages
SBI API Integration: Integrates with the SBI API to retrieve account information
Requirements
Python 3.x
requests library (for making API calls)
hashlib library (for password hashing)
Installation
Clone the repository
Install the required libraries: pip install requests hashlib
Usage
Run the project: python main.py
Enter your username and password to authenticate
Use the various services provided by the project, such as account management, bill payment, and fund transfer
API Endpoints
User Authentication: /authenticate
Account Management: /accounts
Transaction History: /transactions
Bill Payment: /bills/pay
Fund Transfer: /transfers
Payment Gateway Integration: /payments
SBI API Integration: /sbi/accounts
Multi-Language Support: /translate
Notes
