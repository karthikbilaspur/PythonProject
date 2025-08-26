# Fetcher script

Fetches all links: Retrieves all links from a given webpage.
Classifies links: Categorizes links as internal, external, or invalid.
Validates links: Verifies link format using regular expressions.
Simulates browser request: Adds User-Agent header to request.
Benefits:
Organized link retrieval: Uses a class-based structure for better organization.
Improved link analysis: Provides separate lists for internal, external, and invalid links.
Usage:
Create a LinkFetcher object with a URL.
Call the fetch_links method to retrieve links.
Use getter methods to access links, internal links, external links, and invalid links.
