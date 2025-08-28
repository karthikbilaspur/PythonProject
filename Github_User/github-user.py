from github import Github

def get_token():
    return input("Enter your GitHub personal access token: ")

def get_repository():
    return input("Enter the GitHub repository name (Example: Ayush7614/Hello-World-): ")

def get_issue_details():
    title = input("Enter the title for the issues: ")
    body = input("Enter the body for the issues: ")
    labels = input("Enter labels for the issues (comma-separated): ").split(',')
    labels = [label.strip() for label in labels]
    return title, body, labels

def create_issues(repo, number, title, body, labels):
    for x in range(number):
        issue = repo.create_issue(title=title, body=body, labels=labels)
        print(f"Issue {x+1} created successfully! Issue Number: {issue.number}")

def main():
    token = get_token()
    g = Github(token)
    repository = get_repository()
    repo = g.get_repo(repository)
    number = int(input("Enter the number of issues you want to create: "))
    title, body, labels = get_issue_details()
    create_issues(repo, number, title, body, labels)

if __name__ == "__main__":
    main()