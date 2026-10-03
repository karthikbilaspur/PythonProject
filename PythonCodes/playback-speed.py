def audiobook_time_saver_calculator():
    print("Audiobook Time Saver Calculator")
    print("--------------------------------")

    # Get audiobook duration
    hours = int(input("Enter audiobook duration hours: "))
    minutes = int(input("Enter audiobook duration minutes: "))
    seconds = int(input("Enter audiobook duration seconds: "))

    # Get playback speed
    while True:
        try:
            speed = float(input("Enter playback speed (e.g., 1.5 for 1.5x speed): "))
            if speed <= 0:
                print("Playback speed must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Convert time to seconds
    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    
    # Calculate adjusted duration
    adjusted_seconds = total_seconds / speed
    
    # Convert adjusted duration back to hours, minutes, and seconds
    adjusted_hours = int(adjusted_seconds // 3600)
    adjusted_minutes = int((adjusted_seconds % 3600) // 60)
    adjusted_seconds = int(adjusted_seconds % 60)
    
    # Calculate time saved
    time_saved_seconds = (hours * 3600 + minutes * 60 + seconds) - adjusted_seconds
    
    # Convert time saved to hours, minutes, and seconds
    time_saved_hours = int(time_saved_seconds // 3600)
    time_saved_minutes = int((time_saved_seconds % 3600) // 60)
    time_saved_seconds = int(time_saved_seconds % 60)

    # Calculate percentage of time saved
    percentage_saved = ((time_saved_seconds + (time_saved_minutes * 60) + (time_saved_hours * 3600)) / (hours * 3600 + minutes * 60 + seconds)) * 100

    # Display results
    print(f"\nOriginal Duration: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print(f"Adjusted Duration (at {speed}x speed): {adjusted_hours:02d}:{adjusted_minutes:02d}:{adjusted_seconds:02d}")
    print(f"Time Saved: {time_saved_hours:02d}:{time_saved_minutes:02d}:{time_saved_seconds:02d}")
    print(f"Percentage of Time Saved: {percentage_saved:.2f}%")

    # Ask user if they want to calculate again
    while True:
        response = input("\nDo you want to calculate again? (yes/no): ")
        if response.lower() == "yes":
            audiobook_time_saver_calculator()
            break
        elif response.lower() == "no":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    audiobook_time_saver_calculator()