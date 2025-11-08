class CircularQueue:
    def __init__(self, size: int):
        self.queue = [0] * size
        self.front = 0
        self.rear = -1
        self.count = 0
        self.MaxSize = size

    def enqueue(self, data: int):
        if self.isFull():
            print("\nQueue is full. Cannot enqueue.")
            return
        self.rear = (self.rear + 1) % self.MaxSize
        self.queue[self.rear] = data
        self.count += 1
        print(f"{data} enqueued in Queue")

    def dequeue(self):
        if self.isEmpty():
            print("\nQueue is empty. Cannot dequeue.")
            return
        temp = self.queue[self.front]
        self.front = (self.front + 1) % self.MaxSize
        self.count -= 1
        print(f"{temp} dequeued from Queue")

    def isFull(self):
        return self.count == self.MaxSize

    def isEmpty(self):
        return self.count == 0

    def printQueue(self):
        if self.isEmpty():
            print("\nQueue is empty.")
            return
        print("\nData:")
        i = self.front
        for _ in range(self.count):
            print(self.queue[i], end="-->")
            i = (i + 1) % self.MaxSize
        print()

def main():
    size = int(input("Enter size of the queue: "))
    queue = CircularQueue(size)

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
            break
        else:
            print("\nWrong Input. Please enter the correct choice.")

if __name__ == "__main__":
    main()