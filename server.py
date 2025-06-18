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

        self.null_char: str = 'n'
        self.board: list = [self.null_char] * 9

        self.turn: int = 0

        self.winner = None
        self.teams = ['x', 'o']

        self.players: list = []

    def serialize(self):
        return struct.pack('BB9s', self.turn, ord(self.winner), ''.join(self.board).encode('utf-8'))

    def place(self, conn, space_index: int) -> None:
        if self.winner == self.null_char:
            player_id = self.players.index(conn)
            if 0 <= space_index < len(self.board) and (player_id == (self.turn % 2)):
                if self.board[space_index] == self.null_char:
                    self.board[space_index] = self.teams[self.turn % 2]
                    self.turn += 1

    def get_space(self, pos: tuple) -> str:
        space_index = pos[0] + pos[1] * 3
        if (0 <= pos[0] < 3) and (0 <= pos[1] < 3):
            return self.board[space_index]

    def check_win(self) -> str:
        for i, letter in enumerate(self.board):
            if letter != self.null_char:
                space_id = (i % 3, i // 3)
                for angle in [(1, 0), (1, 1), (0, 1), (-1, 1)]:
                    for j in range(3):
                        if self.get_space((space_id[0] + angle[0] * j, space_id[1] + angle[1] * j)) != letter:
                            break
                        if j == 2:
                            return letter
        return self.null_char

    def run_listener(self, conn) -> None:
        self.thread_count += 1
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        conn.settimeout(1)
        with conn:
            while not self.kill:
                try:
                    data = conn.recv(4096)
                    if len(data):
                        target_space = struct.unpack_from('B', data, 0)[0]
                        self.place(conn, target_space)
                except socket.timeout:
                    pass
        
        self.thread_count -= 1


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
                        threading.Thread(target=self.run_listener, args=(conn,)).start()
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
                self.winner = self.check_win()
                for player_conn in self.players:
                    try:
                        player_conn.send(self.serialize())
                    except OSError:
                        pass

                time.sleep(0.05)
        except KeyboardInterrupt:
            self.await_kill()

if __name__== '__main__':
    Server().run()