
from multiprocessing import Process, Queue
import time


def sender(q):
    for i in range(5):
        message = f"Message {i}"
        print("Sending:", message)
        q.put(message)
        time.sleep(1)
    q.put("DONE")


def receiver(q):
    while True:
        msg = q.get()
        if msg == "DONE":
            break
        print("Received:", msg)


if __name__ == "__main__":
    q = Queue()

    p1 = Process(target=sender, args=(q,))
    p2 = Process(target=receiver, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
