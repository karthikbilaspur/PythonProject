import argparse
import json
import sys

import requests

# {username} is filled in later with .format() / .replace() — NOT at import time.
SITES = {
    "instagram": "https://www.instagram.com/{username}/",
    "facebook": "https://www.facebook.com/{username}",
    "twitter": "https://twitter.com/{username}",
    "youtube": "https://www.youtube.com/@{username}",
    "reddit": "https://www.reddit.com/user/{username}/",
    "blogger": "https://{username}.blogspot.com",
    "github": "https://github.com/{username}",
    "steam": "https://steamcommunity.com/id/{username}",
    "soundcloud": "https://soundcloud.com/{username}",
    "medium": "https://medium.com/@{username}",
    "spotify": "https://open.spotify.com/user/{username}",
    "patreon": "https://www.patreon.com/{username}",
    "bitbucket": "https://bitbucket.org/{username}/",
    "goodreads": "https://www.goodreads.com/{username}",
    "wikipedia": "https://en.wikipedia.org/wiki/User:{username}",
    "slack": "https://{username}.slack.com",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (UsernameSearch demo/1.0)"}


def search_one(username: str, target: str) -> dict[str, str]:
    url = SITES[target].format(username=username)
    try:
        r = requests.get(url, headers=HEADERS, timeout=8, allow_redirects=True)
        if r.status_code == 200:
            return {"site": target, "url": url, "status": "POSSIBLY FOUND (200 — verify manually)"}
        if r.status_code == 404:
            return {"site": target, "url": url, "status": "NOT FOUND (404)"}
        if r.status_code in (403, 429):
            return {"site": target, "url": url, "status": f"INCONCLUSIVE ({r.status_code} blocked/rate-limited)"}
        return {"site": target, "url": url, "status": f"UNKNOWN ({r.status_code})"}
    except requests.RequestException as e:
        return {"site": target, "url": url, "status": f"ERROR: {e}"}


def main():
    parser = argparse.ArgumentParser(description="Username Search Tool")
    parser.add_argument("-u", "--username", required=True, help="Username to search (one at a time)")
    parser.add_argument("-t", "--targets", required=True, nargs="+",
                        help=f"Site(s), lowercase. Supported: {', '.join(sorted(SITES))}")
    parser.add_argument("-o", "--output", help="Optional JSON output file")
    if len(sys.argv) == 1:
        parser.print_help(); sys.exit()
    args = parser.parse_args()

    results: list[dict[str, str]] = []
    for target in args.targets:
        target = target.lower()
        if target not in SITES:
            print(f"Target '{target}' not supported.")
            continue
        result = search_one(args.username, target)
        results.append(result)
        print(f"{target}: {result['status']}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
        print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
