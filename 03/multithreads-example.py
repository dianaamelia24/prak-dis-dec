import threading
import time

def task(name, delay):
    print(f"Task {name} starting...")
    time.sleep(delay)  # Simulates an I/O-bound operation
    print(f"Task {name} finished after {delay}s.")

# 1. Create thread objects
t1 = threading.Thread(target=task, args=("A", 2))
t2 = threading.Thread(target=task, args=("B", 7))
t3 = threading.Thread(target=task, args=("C", 9))
t4 = threading.Thread(target=task, args=("D", 1))
t5 = threading.Thread(target=task, args=("E", 5))

# 2. Start the threads
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

# 3. Wait for threads to finish before continuing
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()

print("All tasks completed.")
