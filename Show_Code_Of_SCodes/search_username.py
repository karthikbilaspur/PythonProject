# IMPORTS
import requests
import argparse
import sys
import json

# Define a dictionary of supported websites
websites = {
    "instagram": f'https://www.instagram.com/{username}',
    "facebook": f'https://www.facebook.com/{username}',
    "twitter": f'https://twitter.com/{username}',
    "youtube": f'https://www.youtube.com/{username}',
    "reddit": f'https://www.reddit.com/user/{username}',
    "blogger": f'https://{username}.blogspot.com',
    "github": f'https://www.github.com/{username}',
    "steam": f'https://steamcommunity.com/id/{username}',
    "soundcloud": f'https://soundcloud.com/{username}',
    "medium": f'https://medium.com/@{username}',
    "spotify": f'https://open.spotify.com/user/{username}',
    "patreon": f'https://www.patreon.com/{username}',
    "bitbucket": f'https://bitbucket.org/{username}',
    "goodreads": f'https://www.goodreads.com/{username}',
    "wikipedia": f'https://www.wikipedia.org/wiki/User:{username}',
    "slack": f'https://{username}.slack.com'
}

def parser_input():
    """
    Function for Parsing the CLI input
    :return: parser.parse_args()  Parsed Arguments
    """
    parser = argparse.ArgumentParser(description="Username Search Tool")
    parser.add_argument("-u",
                        "--username",
                        help="Enter the username.",
                        type=str,
                        required=True)
    parser.add_argument("-t",
                        "--targets",
                        help="Enter the website(s). Use Lowercase only",
                        type=str,
                        required=True,
                        nargs='+')
    parser.add_argument("-o",
                        "--output",
                        help="Output file name (JSON format)",
                        type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    return parser.parse_args()

def search_web(username: str, target_website: str) -> dict[str, str]:
    """
    The search web function
    :param username: Username to be searched across the platforms
    :param target_website: The targeted website
    :return: A dictionary with the result
    """
    try:
        r = requests.get(target_website, timeout=5)
        if r.status_code == 200:
            return {"website": target_website, "status": "FOUND"}
        elif r.status_code == 400:
            return {"website": target_website, "status": "BAD REQUEST"}
        elif r.status_code == 404:
            return {"website": target_website, "status": "NOT FOUND"}
        else:
            return {"website": target_website, "status": "UNKNOWN ERROR"}
    except requests.exceptions.RequestException as e:
        return {"website": target_website, "status": str(e)}

def main():
    print(
        "Hello User, Using this script, you can search for usernames across social media networks.\n"
        "Important, enter only one username at once.\n"
        "Enter as many as required supported platforms (SEE README).\n"
        "Enter the platform in lower case only.\n")
    arg = parser_input()
    username = arg.username
    targets = arg.targets
    output_file = arg.output

    results = []
    for target in targets:
        if target in websites:
            website = websites[target].replace("{username}", username)
            result = search_web(username, website)
            results.append(result)
            print(f"{target}: {result['status']}")
        else:
            print(f"Target '{target}' not supported.")

    if output_file:
        with open(output_file, "w") as f:
            json.dump(results, f, indent=4)
        print(f"Results saved to {output_file}")

if __name__ == '__main__':
    main()