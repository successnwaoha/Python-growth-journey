# client.py
import socket
import threading
import json
import os

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

class TicTacToeClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.symbol = None
        self.board = [" " for _ in range(9)]
        self.my_turn = False

    def display_board(self):
        clear()
        b = self.board
        print(f"You are: {self.symbol}")
        print(f" {b[0]} | {b[1]} | {b[2]} ")
        print("-----------")
        print(f" {b[3]} | {b[4]} | {b[5]} ")
        print("-----------")
        print(f" {b[6]} | {b[7]} | {b[8]} ")
        if self.my_turn:
            print("\nYOUR TURN! Enter 0-8:")
        else:
            print("\nWaiting for opponent...")

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024).decode('utf-8')
                if not data: break
                msg = json.loads(data)
                
                if msg['type'] == 'SETUP':
                    self.symbol = msg['symbol']
                    # Set initial turn logic for Player X
                    if self.symbol == "X":
                        self.my_turn = True
                    print(f"Connected! You are {self.symbol}")
                    
                elif msg['type'] == 'UPDATE':
                    self.board = msg['board']
                    # If it's Player 0's turn and I am X, OR Player 1's turn and I am O
                    self.my_turn = (msg['turn'] == (0 if self.symbol == "X" else 1))
                    self.display_board()
                    if msg['winner']:
                        print(f"GAME OVER! Winner: {msg['winner']}")
                        break
            except Exception as e:
                print(f"Error: {e}")
                break

    def start(self):
        self.client.connect(('127.0.0.1', 5555))
        
        # Start background thread to listen for server updates
        thread = threading.Thread(target=self.receive_messages)
        thread.start()

        while True:
            if self.my_turn:
                try:
                    move = input("> ")
                    self.client.send(json.dumps({"type": "MOVE", "index": int(move)}).encode('utf-8'))
                except ValueError:
                    print("Invalid input.")

if __name__ == "__main__":
    client = TicTacToeClient()
    client.start()