import wikipedia

def get_historical_event(event_name):
    try:
        # Search for the event
        search_results = wikipedia.search(event_name)

        # Get the page object
        page = wikipedia.page(search_results[0])

        # Return the page content
        return page.content

    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation errors
        return f"Multiple events found: {e}"

    except wikipedia.exceptions.PageError:
        # Handle page not found errors
        return "Event not found."

def get_historical_events():
    historical_events = {
        "The Battle of Hastings": "A turning point in English history.",
        "The American Revolution": "A war for independence.",
        "The French Revolution": "A time of radical change.",
        "World War I": "A global conflict.",
        "World War II": "A devastating war.",
        "The Moon Landing": "A historic achievement.",
        "The Fall of the Berlin Wall": "A symbol of freedom.",
    }

    for event, description in historical_events.items():
        print(f"**{event}**")
        print(description)
        print()

def main():
    print("Historical Events")
    print("-----------------")

    while True:
        print("1. Get information on a specific event")
        print("2. View list of historical events")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            event_name = input("Enter the name of the event: ")
            print(get_historical_event(event_name))
        elif choice == "2":
            get_historical_events()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()