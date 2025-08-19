# Domain Availability Checker Script

This Python script checks if a domain name is available using Dynadot's API. It also suggests alternative domain names with different extensions if the original domain is not available.
Key Features:
Domain Availability Check: Uses Dynadot's API to check if a domain name is available.
Alternative Domain Suggestions: Suggests alternative domain names with different extensions (e.g., .net, .io, .org) if the original domain is not available.
Error Handling: Handles request-related exceptions and XML parsing exceptions.
Configurable API Key: Uses python-decouple to load the API key from a .env file.
Usage:
Install required libraries: certifi, chardet, idna, python-decouple, requests, and urllib3.
Create a .env file with your Dynadot API key.
Run the script and enter the domain name to check.
