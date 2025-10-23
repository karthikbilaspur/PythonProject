
from pagespeed_api import PageSpeedAPI

api_key = "YOUR_API_KEY"  # Replace with your PageSpeed API key
pagespeed = PageSpeedAPI(api_key)

url = "https://example.com"
strategy = "desktop"
category = "performance"

results = pagespeed.get_pagespeed_results(url, strategy, category)
print(results)

pagespeed.save_pagespeed_results(url, strategy, category, "example_pagespeed_results.json")