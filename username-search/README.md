# Username Search Tool

Check whether a username appears to exist on supported sites.

 Requirements

```bash
pip install requests
```

Run

```bash
python username_search.py -u octocat -t github reddit youtube
python username_search.py -u octocat -t github -o results.json
```

Supported sites
instagram, facebook, twitter, youtube, reddit, blogger, github, steam, soundcloud, medium, spotify, patreon, bitbucket, goodreads, wikipedia, slack

Critical fix vs original version
Original built the `websites` dict at import time using `{username}` / f-strings before `username` existed → `NameError` on import, script never ran. Sites are now URL *templates* (`https://github.com/{username}`) formatted only when searching.

Other fixes

- Added User-Agent header (many sites block default `python-requests`).
- 403/429 now reported as INCONCLUSIVE (blocked/rate-limited), not FOUND.
- Per-site timeout + proper error handling.

⚠️ Accuracy warning
A HTTP 200 does NOT prove a user exists — many sites return 200 for a 'not found' page. Results here are a signal, not proof. For reliable checks, use each site's official API. Don't use this to stalk/harass anyone.
