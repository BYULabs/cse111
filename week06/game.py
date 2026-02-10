import tkinter as tk
from tkinter import Frame, Label, Button
import random

def main():
    root = tk.Tk()
    root.option_add("*Font", "Helvetica 14")
    root.title("Rock, Paper, Scissors Game")
    root.geometry("500x450")
    frm_main = Frame(root, bg="#2b2b2b")
    frm_main.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    setup_game(frm_main)
    frm_main.mainloop()

def setup_game(frm):
    # Title
    lbl_title = Label(frm, text="🎮 Rock, Paper, Scissors 🎮", 
                     font=("Helvetica", 20, "bold"), bg="#2b2b2b", fg="#ffffff")
    lbl_title.pack(pady=15)
    
    # Score frame
    frm_score = Frame(frm, bg="#2b2b2b")
    frm_score.pack(pady=10)
    
    lbl_score = Label(frm_score, text="Your Score: 0  |  Computer Score: 0", 
                     font=("Helvetica", 12, "bold"), bg="#2b2b2b", fg="#66ff00")
    lbl_score.pack()
    
    # Game state dictionary
    game_state = {"player_score": 0, "computer_score": 0, "last_result": ""}
    
    # Choice frame
    frm_choices = Frame(frm, bg="#2b2b2b")
    frm_choices.pack(pady=20)
    
    Label(frm_choices, text="Make Your Choice:", font=("Helvetica", 12, "bold"), 
         bg="#2b2b2b", fg="#ffffff").pack()
    
    frm_buttons = Frame(frm_choices, bg="#2b2b2b")
    frm_buttons.pack(pady=10)
    
    choices = ["Rock", "Paper", "Scissors"]
    
    def play_game(player_choice):
        computer_choice = random.choice(choices)
        result = determine_winner(player_choice, computer_choice)
        
        if result == "You win!":
            game_state["player_score"] += 1
            result_color = "#00aa00"
        elif result == "Computer wins!":
            game_state["computer_score"] += 1
            result_color = "#aa0000"
        else:
            result_color = "#ff8800"
        
        game_state["last_result"] = f"You chose {player_choice}\nComputer chose {computer_choice}\n{result}"
        
        lbl_score.config(text=f"Your Score: {game_state['player_score']}  |  Computer Score: {game_state['computer_score']}")
        lbl_result.config(text=game_state["last_result"], fg=result_color)
    
    def determine_winner(player, computer):
        if player == computer:
            return "It's a tie!"
        elif (player == "Rock" and computer == "Scissors") or \
             (player == "Paper" and computer == "Rock") or \
             (player == "Scissors" and computer == "Paper"):
            return "You win!"
        else:
            return "Computer wins!"
    
    # Create choice buttons with colors
    colors = {"Rock": "#FF6B6B", "Paper": "#4ECDC4", "Scissors": "#FFE66D"}
    
    for choice in choices:
        btn = Button(frm_buttons, text=choice, width=12, height=2,
                    command=lambda c=choice: play_game(c),
                    bg=colors[choice], fg="#000000", font=("Helvetica", 12, "bold"),
                    relief=tk.RAISED, bd=3)
        btn.pack(side=tk.LEFT, padx=8)
    
    # Result frame
    lbl_result = Label(frm, text="Make your first move!", font=("Helvetica", 12, "bold"), 
                      justify=tk.CENTER, bg="#3c3c3c", fg="#ffffff",
                      relief=tk.SUNKEN, bd=2, padx=10, pady=10)
    lbl_result.pack(pady=15, fill=tk.BOTH, expand=True)
    
    # Reset button
    def reset_game():
        game_state["player_score"] = 0
        game_state["computer_score"] = 0
        game_state["last_result"] = ""
        lbl_score.config(text=f"Your Score: 0  |  Computer Score: 0")
        lbl_result.config(text="Game reset! Make your first move!", fg="#ffffff")
    
    btn_reset = Button(frm, text="Reset Game", command=reset_game, 
                      bg="#ff7f50", fg="#000000", font=("Helvetica", 12, "bold"),
                      relief=tk.RAISED, bd=2, padx=20, pady=5)
    btn_reset.pack(pady=10)

if __name__ == "__main__":
    main()
