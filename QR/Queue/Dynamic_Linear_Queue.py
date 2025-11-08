class Node:
    def __init__(self, data: int):
        self.data = data
        self.next = None

class DynamicQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, data: int):
        node = Node(data)
        if self.isEmpty():
            self.front = self.rear = node
        else:
            self.rear.next = node
            self.rear = node
        self.size += 1
        print(f"\nElement {data} enqueued in Queue")

    def dequeue(self):
        if self.isEmpty():
            print("\nQueue is empty. Cannot dequeue.")
            return
        temp = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        print(f"\nElement {temp.data} dequeued from Queue")

    def isEmpty(self):
        return self.front is None

    def printQueue(self):
        if self.isEmpty():
            print("\nQueue is empty.")
            return
        temp = self.front
        print("\nQueue elements:")
        while temp:
            print(temp.data, end=" --> ")
            temp = temp.next
        print()

def main():
    queue = DynamicQueue()

    while True:
        print("\n-----------")
        print("1. Enqueue")
        print("2. Dequeue")
        print("3. Print")
        print("0. Exit")
        print("-----------")

        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("\nInvalid input. Please enter a number.")
            continue

        if choice == 1:
            try:
                data = int(input("\nEnter value to enqueue in Queue: "))
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