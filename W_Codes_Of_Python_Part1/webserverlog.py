import re
from collections import Counter

# Regular expressions for parsing the Apache Combined Log Format
log_pattern = r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+)\s?(\S+)?\s?(\S+)?" (\d{3}) (\d+|-)'

def parse_log(log_file_path: str):
    """Yield parsed log entries from the given log file."""
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            match = re.match(log_pattern, line)
            if match:
                yield match.groups()

def analyze_logs(log_file_path: str):
    """Analyze the given log file and return statistics."""
    # Initialize counters and sets to store information
    total_requests = 0
    unique_visitors = set()
    page_visits = Counter()
    status_codes = Counter()
    potential_threats = set()

    for ip, _, _, _, method, url, _, status_code, _ in parse_log(log_file_path):
        total_requests += 1
        unique_visitors.add(ip)
        page_visits[url] += 1
        status_codes[status_code] += 1

        # Detect potential security threats (e.g., 4xx errors from the same IP)
        if status_code.startswith('4'):
            potential_threats.add((ip, url))

    return {
        'total_requests'[assert]: total_requests,
        'unique_visitors': len(unique_visitors),
        'page_visits': page_visits,
        'status_codes': status_codes,
        'potential_threats': potential_threats,
    }

if __name__ == "__main__":
    log_file_path = "path/to/your/log/file.log"

    stats = analyze_logs(log_file_path)

    print(f"Total Requests: {stats['total_requests']}")
    print(f"Unique Visitors: {stats['unique_visitors']}")
    print("\nPopular Pages:")
    for page: str, count: int in stats['page_visits'].most_common(10):
        print(f"{page}: {count} visits")

    print("\nStatus Codes:")
    for code: str, count: int in stats['status_codes'].items():
        print(f"Status Code {code}: {count} occurrences")

    print("\nPotential Security Threats:")
    for ip: str, url: str in stats['potential_threats']:
        print(f"IP: {ip}, URL: {url}")