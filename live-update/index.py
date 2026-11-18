import requests
import json
from typing import TypedDict


class LiveMatch(TypedDict):
    id: str | None
    name: str | None
    status: str
    teams: list[str]
    score: list[str]

# 【entity-ESPN¦canonical_name=ESPN】's public scoreboard - no key needed
SCOREBOARD_URL = "https://site.web.api.espn.com/apis/site/v2/sports/cricket/scoreboard"
# Cricinfo's match details API - no key needed
MATCH_DETAILS_URL = "https://hs-consumer-api.espncricinfo.com/v1/pages/match/details"

class CricketScore:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        })

    def get_live_matches(self) -> list[LiveMatch]:
        """Gets all live / in-progress matches"""
        try:
            resp = self.session.get(SCOREBOARD_URL, timeout=10)
            resp.raise_for_status()
            events = resp.json().get("events", [])

            live: list[LiveMatch] = []
            for e in events:
                comp = e.get("competitions", [{}])[0]
                status = comp.get("status", {}).get("type", {}).get("state", "")
                # only keep live games
                if status == "in":
                    live.append({
                        "id": e.get("id"),
                        "name": e.get("name"),
                        "status": comp.get("status", {}).get("type", {}).get("detail", ""),
                        "teams": [c.get("team", {}).get("displayName", "") for c in comp.get("competitors", [])],
                        "score": [c.get("score", "") for c in comp.get("competitors", [])],
                    })
            return live
        except Exception as e:
            print(f"Error fetching matches: {e}")
            return []

    def get_match_details(self, match_id: str):
        """Gets scorecard + commentary for one match"""
        try:
            # ESPN needs seriesId too, so we use the Cricinfo details endpoint
            # It works with just matchId in the query
            params = {"matchId": match_id}
            resp = self.session.get(MATCH_DETAILS_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            # Also try ESPN summary endpoint for live score
            summary_url = f"https://site.web.api.espn.com/apis/site/v2/sports/cricket/summary?event={match_id}"
            summary = self.session.get(summary_url, timeout=10).json()

            return {
                "live_score": summary.get("header", {}),
                "scorecard": data.get("match", {}),
                "commentary": data.get("commentary", {}),
            }
        except Exception as e:
            print(f"Error fetching match {match_id}: {e}")
            return None

    def print_match_details(self, details: dict[str, object] | None) -> None:
        if not details:
            print("No details available.")
            return
        print("\nLive Score:")
        print(json.dumps(details["live_score"], indent=2))
        print("\nScorecard / Match Info:")
        print(json.dumps(details["scorecard"], indent=2))
        print("\nCommentary:")
        print(json.dumps(details["commentary"], indent=2)[:4000])  # trimmed

def main():
    cs = CricketScore()
    matches = cs.get_live_matches()

    if not matches:
        print("No live matches right now.")
        return

    print("Live Matches:")
    for i, m in enumerate(matches, start=1):
        teams = " vs ".join(m["teams"])
        score = " | ".join([s for s in m["score"] if s])
        print(f"{i}. {teams} - {m['status']} - {score}")

    try:
        choice = int(input("\nEnter match number: ")) - 1
        if not 0 <= choice < len(matches):
            print("Invalid choice.")
            return
    except ValueError:
        print("Enter a number.")
        return

    match_id = matches[choice]["id"]
    if match_id is None:
        print("Match ID is unavailable.")
        return

    details = cs.get_match_details(match_id)
    cs.print_match_details(details)

if __name__ == "__main__":
    main()