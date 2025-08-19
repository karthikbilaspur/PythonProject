# Import required libraries
import requests
from decouple import config
import xml.etree.ElementTree as ET

# Function to check domain availability
def check_domain_availability(domain_name):
    """
    Checks if a domain is available using Dynadot's API.

    Args:
        domain_name (str): The domain name to check.

    Returns:
        str: A message indicating whether the domain is available or not.
    """

    # Load API key from .env file
    api_key = config('DYNADOT_API_KEY')

    # Construct API request URL
    url = f"https://api.dynadot.com/api3.xml?key={api_key}&command=search&domain0={domain_name}"

    try:
        # Send GET request to API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Parse XML response
        root = ET.fromstring(response.text)

        # Find the 'available' element in the XML response
        available_element = root.find('.//available')

        if available_element is not None:
            # Check the value of the 'available' element
            if available_element.text == '1':
                return f"{domain_name} is available."
            elif available_element.text == '0':
                return f"{domain_name} is not available."
            else:
                return f"Failed to determine availability for {domain_name}."
        else:
            return f"Invalid response from API for {domain_name}."

    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions
        return f"An error occurred while checking {domain_name}: {e}"
    except ET.ParseError as e:
        # Handle XML parsing exceptions
        return f"Failed to parse API response for {domain_name}: {e}"

# Function to suggest alternative domain names
def suggest_alternative_domains(domain_name):
    """
    Suggests alternative domain names based on the input domain.

    Args:
        domain_name (str): The original domain name.

    Returns:
        list: A list of suggested alternative domain names.
    """

    # Split the domain name into parts (name and extension)
    parts = domain_name.split('.')
    name = '.'.join(parts[:-1])
    extension = parts[-1]

    # Suggest alternative domain names with different extensions
    alternatives = [
        f"{name}.net",
        f"{name}.io",
        f"{name}.org",
        f"{name}.biz",
        f"{name}.info"
    ]

    return alternatives

# Main function
def main():
    domain_name = input("Enter the domain name (without http/https): ")

    # Check domain availability
    availability = check_domain_availability(domain_name)
    print(availability)

    # If the domain is not available, suggest alternative domain names
    if "not available" in availability.lower():
        alternatives = suggest_alternative_domains(domain_name)
        print("Alternative domain names:")
        for alternative in alternatives:
            print(alternative)
            # Check availability of alternative domain names
            availability = check_domain_availability(alternative)
            print(f"  - {availability}")

if __name__ == "__main__":
    main()