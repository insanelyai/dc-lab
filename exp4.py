import socket
import struct
import threading
import time

MULTICAST_GROUP = '224.1.1.1'
PORT = 5007
MEMBER_COUNT = 3

print("Hasan Sayyed 232P003 32\n")

# ✅ Create ONE shared socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))

group = socket.inet_aton(MULTICAST_GROUP)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


def group_member(member_id):
    print(f"[Member {member_id}] Joined group\n")
    time.sleep(1)

    message = f"Hello world from Member {member_id}"
    sock.sendto(message.encode('utf-8'), (MULTICAST_GROUP, PORT))
    print(f"[Member {member_id}] Sent message\n")

    sock.settimeout(5)

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            print(
                f"[Member {member_id}] Received: {data.decode()} from {addr}\n")
    except socket.timeout:
        pass

    print(f"[Member {member_id}] Left group\n")


def main():
    threads = []
    for i in range(1, MEMBER_COUNT + 1):
        t = threading.Thread(target=group_member, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # cleanup once
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
    sock.close()
    print("Channel closed\n")


if __name__ == "__main__":
    main()
