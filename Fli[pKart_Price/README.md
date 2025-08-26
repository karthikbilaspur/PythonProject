# Flipkart Price Alert Script

This Python script uses the Flipkart Seller API to:
Generate access token: Using Client Credentials Flow
Get current price: Of a product using the Listing Management API
Check price: Periodically (every hour) and compare with a threshold price
Send notification: Via email when the price drops below the threshold
Key Features
Uses Flipkart Seller API for price data
Periodic price checking using schedule library
Email notification using smtplib library
Customizable threshold price and notification settings
Requirements
Flipkart Seller account
App ID and App Secret
requests, schedule, and smtplib libraries installed
