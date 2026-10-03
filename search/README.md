# Google Custom Search API Script
================================

A Python script that uses the Google Custom Search API to perform searches and extract relevant information.

## Features
------------

*   **Google Custom Search API integration**: Uses the Google Custom Search API to perform searches.
*   **Search result extraction**: Extracts relevant information like title, link, and snippet from search results.
*   **Search result saving**: Saves search results to a JSON file.
*   **Search result loading**: Loads search results from a JSON file.
*   **Date timestamp**: Adds a date timestamp to each search result.

## Requirements
---------------

*   Python 3.6 or later
*   `google-api-python-client` library
*   Google Custom Search API key
*   Google Custom Search Engine ID

## Setup
--------

1.  Install the required libraries using `pip`.
2.  Set up a Google Custom Search Engine and obtain the API key and search engine ID.
3.  Update the `API_KEY` and `SEARCH_ENGINE_ID` variables in the script.

## Usage
-----

1.  Run the script using `python`.
2.  Enter your search term when prompted.
3.  The script will display the search results and save them to a JSON file.

## Customization
--------------

*   Use the `num` parameter to specify the number of search results.
*   Use the `start` parameter to specify the starting index of search results.
*   Use the `lr` parameter to specify the language of search results.
*   Use the `safe` parameter to specify the safe search filter.

## Contributing
------------

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License
-------

This project is licensed under the MIT License. See the `LICENSE` file for details.