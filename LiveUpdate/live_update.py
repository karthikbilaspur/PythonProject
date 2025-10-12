from pycricbuzz import Cricbuzz
import json

class CricketScore:
    def __init__(self):
        self.c = Cricbuzz()

    def get_live_matches(self):
        """Gets all live matches"""
        try:
            return self.c.matches()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_match_details(self, match_id):
        """Gets match details"""
        try:
            return {
                "live_score": self.c.livescore(match_id),
                "scorecard": self.c.scorecard(match_id),
                "commentary": self.c.commentary(match_id)
            }
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def print_match_details(self, match_details):
        """Prints match details"""
        if match_details:
            print("Live Score:")
            print(json.dumps(match_details["live_score"], indent=4))
            print("\nScorecard:")
            print(json.dumps(match_details["scorecard"], indent=4))
            print("\nCommentary:")
            print(json.dumps(match_details["commentary"], indent=4))

def main():
    cricket_score = CricketScore()
    live_matches = cricket_score.get_live_matches()

    if live_matches:
        print("Live Matches:")
        for i, match in enumerate(live_matches):
            print(f"{i+1}. {match['team1']['name']} vs {match['team2']['name']} - {match['status']}")

        match_choice = int(input("Enter the match number: ")) - 1
        match_id = live_matches[match_choice]['id']

        match_details = cricket_score.get_match_details(match_id)
        cricket_score.print_match_details(match_details)

if __name__ == "__main__":
    main()