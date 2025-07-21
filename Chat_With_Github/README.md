GitHub Repository Details Script

A Python script that retrieves and displays details of a GitHub user's repositories.

## Features

* Retrieves repository names, descriptions, creation dates, programming languages, and fork counts
* Displays additional details such as stars, watchers, and repository URLs
* Handles missing values for description and language
* Error handling for exceptions during API calls

## Requirements

* Python 3.x
* `PyGithub` library (install using `pip3 install PyGithub`)

## Usage

1. Save the script to a file (e.g., `github_repo_details.py`)
2. Make the script executable with `chmod +x github_repo_details.py`
3. Run the script with `./github_repo_details.py <github_username>`

## Example

```bash
./github_repo_details.py octocat