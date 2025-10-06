from pycricbuzz import Cricbuzz
import json

# Create a Cricbuzz object
c = Cricbuzz()

# Get all live matches
matches = c.matches()

# Print live matches
print(json.dumps(matches, indent=4))

# Get match ID
match_id = matches[0]['id']

# Get live score
live_score = c.livescore(match_id)
print(json.dumps(live_score, indent=4))

# Get scorecard
scorecard = c.scorecard(match_id)
print(json.dumps(scorecard, indent=4))

# Get commentary
commentary = c.commentary(match_id)
print(json.dumps(commentary, indent=4))