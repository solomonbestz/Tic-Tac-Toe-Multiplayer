import socket
import threading
import struct
import time


class Server:
    def __init__(self, host: str='127.0.0.1', port: int = 62743) -> None:
        self.host = host
        self.port = port

        self.kill = False
        self.thread_count = 0

    def connection_listen_loop(self)->None:
        self.thread_count += 1

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            sock.bind((self.host, self.port))

            while not self.kill:
                sock.settimeout(1)
                sock.listen()

                try:
                    conn, addr = sock.accept()
                    print('New Connection: ', conn, addr)
                except socket.timeout:
                    continue
                time.sleep(0.01)

        self.thread_count -= 1

    def run(self) -> None:
        try:
            while True:
                time.sleep(0.05)
                print("Hello")
        except KeyboardInterrupt:
            pass

if __name__== '__main__':
    Server().run()