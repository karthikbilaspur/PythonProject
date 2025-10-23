class PriorityQueue:
    def __init__(self, size):
        self.queue = []
        self.MaxSize = size

    def enqueue(self, data):
        if len(self.queue) < self.MaxSize:
            self.queue.append(data)
            self.queue.sort(reverse=True)
            print(f"\n{data} enqueued in Queue")
        else:
            print("\nQueue is full. Cannot enqueue.")

    def dequeue(self):
        if self.isEmpty():
            print("\nQueue is empty. Cannot dequeue.")
            return
        temp = self.queue.pop(0)
        print(f"\n{temp} dequeued from Queue")

    def isFull(self):
        return len(self.queue) == self.MaxSize

    def isEmpty(self):
        return len(self.queue) == 0

    def printQueue(self):
        if self.isEmpty():
            print("\nQueue is empty.")
            return
        print("\nQueue elements:")
        for i, element in enumerate(self.queue):
            print(f"Position {i + 1}: {element}")


def main():
    size = int(input("Enter size of the queue: "))
    queue = PriorityQueue(size)

    while True:
        print("\n------------")
        print("1. Enqueue")
        print("2. Dequeue")
        print("3. Print")
        print("0. Exit")
        print("------------")

        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("\nInvalid input. Please enter a number.")
            continue

        if choice == 1:
            try:
                data = int(input("\nEnter data to be enqueued: "))
                queue.enqueue(data)
            except ValueError:
                print("\nInvalid input. Please enter a number.")
        elif choice == 2:
            queue.dequeue()
        elif choice == 3:
            queue.printQueue()
        elif choice == 0:
            print("\nYou are out of the program.")
            break
        else:
            print("\nWrong Input. Please enter the correct choice.")


if __name__ == "__main__":
    main()