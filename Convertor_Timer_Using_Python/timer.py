import time
import datetime

def countdown(t):
    """
    Countdown timer function.

    Args:
        t (int): Time in seconds.
    """
    while t:
        mins, secs = divmod(t, 60)
        hours, mins = divmod(mins, 60)
        timer = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    print("Time's Up!")

def clock():
    """
    Display the current time.
    """
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(current_time, end="\r")
        time.sleep(1)

def main():
    print("1. Countdown Timer")
    print("2. Clock")
    choice = input("Enter your choice: ")

    if choice == "1":
        t = input("Enter the time in seconds: ")
        countdown(int(t))
    elif choice == "2":
        print("Current time will be displayed. Press Ctrl+C to exit.")
        try:
            clock()
        except KeyboardInterrupt:
            print("\nExiting...")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()