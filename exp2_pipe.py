from multiprocessing import Process, Pipe


def send(conn):
    conn.send("Hello sender here... Hasan Sayyed 32 232P003")
    conn.close()


def receive(conn):
    msg = conn.recv()
    print("Received:", msg)
    conn.close()


if __name__ == "__main__":
    parent_conn, child_conn = Pipe()

    p1 = Process(target=send, args=(child_conn,))
    p2 = Process(target=receive, args=(parent_conn,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
