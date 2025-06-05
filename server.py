import socket
import threading
import struct
import time


class Server:
    def __init__(self, host: str='127.0.0.1', port: int = 62743) -> None:
        self.host: str = host
        self.port: int = port

        self.kill = False
        self.thread_count: int = 0

        self.players: list = []

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
                    if len(self.players) < 2:
                        self.players.append(conn)
                except socket.timeout:
                    continue
                time.sleep(0.01)

        self.thread_count -= 1
    
    def await_kill(self) -> None:
        self.kill = True
        while self.thread_count:
            time.sleep(0.01)
        print("Killed")

    def run(self) -> None:
        threading.Thread(target=self.connection_listen_loop).start()
        try:
            while True:
                time.sleep(0.05)
        except KeyboardInterrupt:
            self.await_kill()

if __name__== '__main__':
    Server().run()