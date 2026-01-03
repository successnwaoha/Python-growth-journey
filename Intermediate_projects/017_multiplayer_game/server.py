import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 5555

class TicTacToeServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.server.listen(2)
        self.clients = [] 
        self.board = [" " for _ in range(9)]
        self.turn = 0 

    def broadcast(self, message):
        for client in self.clients:
            try:
                client[0].send(json.dumps(message).encode('utf-8'))
            except:
                continue

    def check_winner(self):
        win_coords = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in win_coords:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return self.board[a]
        if " " not in self.board: return "Tie"
        return None

    def handle_client(self, conn, player_index):
        symbol = "X" if player_index == 0 else "O"
        conn.send(json.dumps({"type": "SETUP", "symbol": symbol}).encode('utf-8'))
        
        while True:
                try:
                    data = conn.recv(1024).decode('utf-8')
                    if not data: break
                    msg = json.loads(data)
                    
                    # Check for MOVE
                    if msg['type'] == 'MOVE':
                        idx = msg['index']
                        if self.turn == player_index and self.board[idx] == " ":
                            self.board[idx] = symbol
                            self.turn = (self.turn + 1) % 2
                            winner = self.check_winner()
                            self.broadcast({"type": "UPDATE", "board": self.board, "turn": self.turn, "winner": winner})
                    
                    # FIX: This 'elif' must align with 'if msg['type'] == 'MOVE''
                    elif msg['type'] == 'RESET':
                        print(f"Player {player_index} requested a reset.")
                        self.board = [" " for _ in range(9)]
                        self.turn = 0
                        self.broadcast({
                            "type": "UPDATE", 
                            "board": self.board, 
                            "turn": self.turn, 
                            "winner": None
                        })
                except Exception as e:
                    print(f"Error handling client: {e}")
                    break
        conn.close()

    def start(self):
        print(f"Server listening on {HOST}:{PORT}...")
        while len(self.clients) < 2:
            conn, addr = self.server.accept()
            print(f"Player {len(self.clients)} connected.")
            self.clients.append((conn, addr))
            threading.Thread(target=self.handle_client, args=(conn, len(self.clients)-1)).start()
        
        self.broadcast({"type": "UPDATE", "board": self.board, "turn": 0, "winner": None})

if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()