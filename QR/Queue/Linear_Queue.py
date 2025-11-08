class LinearQueue:
    def __init__(self, size: int):
        self.queue = [0] * size
        self.front = 0
        self.rear = -1
        self.MaxSize = size

    def enqueue(self, data: int):
        if self.isFull():
            print("\nQueue is full. Cannot enqueue.")
            return
        self.rear += 1
        self.queue[self.rear] = data
        print(f"\n{data} enqueued in Queue at position {self.rear + 1}")

    def dequeue(self):
        if self.isEmpty():
            print("\nQueue is empty. Cannot dequeue.")
            return
        temp = self.queue[self.front]
        self.front += 1
        print(f"\n{temp} dequeued from Queue at position {self.front}")

    def isFull(self):
        return self.rear == self.MaxSize - 1

    def isEmpty(self):
        return self.front > self.rear

    def printQueue(self):
        if self.isEmpty():
            print("\nQueue is empty.")
            return
        print("\nPosition\tData")
        for i in range(self.front, self.rear + 1):
            print(f"{i + 1}\t\t{self.queue[i]}")


def main():
    size = int(input("Enter size of the queue: "))
    queue = LinearQueue(size)

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