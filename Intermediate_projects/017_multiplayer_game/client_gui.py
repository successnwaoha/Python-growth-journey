import customtkinter as ctk
import socket
import threading
import json
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GameOverDialog(ctk.CTkToplevel):
    def __init__(self, parent, message, on_play_again, on_exit):
        super().__init__(parent)
        self.title("Game Over")
        self.geometry("300x200")
        
        # Center it over the main window
        self.transient(parent)
        self.grab_set() # Make it "modal" (must interact with this window)

        self.label = ctk.CTkLabel(self, text=message, font=("Arial", 18, "bold"))
        self.label.pack(pady=30)

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        self.play_again_btn = ctk.CTkButton(self.btn_frame, text="Play Again", width=100,
                                           command=on_play_again)
        self.play_again_btn.grid(row=0, column=0, padx=10)

        self.exit_btn = ctk.CTkButton(self.btn_frame, text="Exit", width=100, 
                                     fg_color="crimson", hover_color="darkred",
                                     command=on_exit)
        self.exit_btn.grid(row=0, column=1, padx=10)

class TicTacToeGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        print("[1] Initializing GUI...")
        self.title("Modern Tic-Tac-Toe")
        self.geometry("400x550")
        
        # Bring window to front (Mac fix)
        self.attributes("-topmost", True)
        self.after(1000, lambda: self.attributes("-topmost", False))

        self.symbol = ""
        self.my_turn = False
        self.buttons = []

        # UI Setup
        self.label = ctk.CTkLabel(self, text="Status: Starting...", font=("Arial", 18))
        self.label.pack(pady=20)

        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(pady=10, padx=10)

        for i in range(9):
            btn = ctk.CTkButton(self.grid_frame, text="", width=100, height=100, 
                                font=("Arial", 30, "bold"),
                                command=lambda i=i: self.send_move(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # FIX: Start connection in a thread so the window isn't blocked
        print("[2] Starting connection thread...")
        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def connect_to_server(self):
        try:
            print("[3] Attempting to connect to 127.0.0.1:5555...")
            self.client.connect(('127.0.0.1', 5555))
            print("[4] Connected successfully!")
            self.receive_messages()
        except Exception as e:
            print(f"[!] Connection failed: {e}")
            self.after(0, lambda: self.label.configure(text="Error: Server not found!"))
            self.after(0, lambda: messagebox.showerror("Error", "Make sure the SERVER is running first!"))

    def send_move(self, index):
        if self.my_turn:
            try:
                self.client.send(json.dumps({"type": "MOVE", "index": index}).encode())
            except:
                print("[!] Failed to send move.")

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
                if not data: break
                msg = json.loads(data)
                
                if msg['type'] == 'SETUP':
                    self.symbol = msg['symbol']
                    self.after(0, lambda: self.label.configure(text=f"You are: {self.symbol}"))
                
                elif msg['type'] == 'UPDATE':
                    self.after(0, self.update_ui, msg)
            except:
                break

    def update_ui(self, msg):
        board = msg['board']
        turn_idx = msg['turn']
        winner = msg['winner']

        for i in range(9):
            self.buttons[i].configure(text=board[i])
            if board[i] != " ":
                self.buttons[i].configure(state="disabled")
            else:
                self.buttons[i].configure(state="normal")
        
        self.update() # Forces the final X or O to draw on the screen

        current_player_symbol = "X" if turn_idx == 0 else "O"
        if winner:
            status_text = f"Winner: {winner}!" if winner != "Tie" else "It's a Tie!"
            self.label.configure(text=status_text)
            
            # FIX: We wait 500ms (half a second) so you can SEE the winning move,
            # then we call our NEW show_end_game function instead of the old messagebox.
            self.after(500, lambda: self.show_end_game(status_text))
        else:
            self.my_turn = (self.symbol == current_player_symbol)
            status = "Your Turn!" if self.my_turn else f"Waiting for {current_player_symbol}..."
            self.label.configure(text=status)
        
    def show_end_game(self, status_text):
        # Instead of messagebox, show our custom dialog
        self.dialog = GameOverDialog(
            self, 
            status_text, 
            on_play_again=self.request_reset, 
            on_exit=self.quit_game
        )

    def request_reset(self):
        self.client.send(json.dumps({"type": "RESET"}).encode())
        if hasattr(self, 'dialog'):
            self.dialog.destroy()

    def quit_game(self):
        self.client.close()
        self.destroy()

if __name__ == "__main__":
    print("--- Client Script Started ---")
    app = TicTacToeGUI()
    app.mainloop()