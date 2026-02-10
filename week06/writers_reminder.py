import tkinter as tk
from tkinter import Frame, Label, Button
from datetime import datetime
import random

def main():
    root = tk.Tk()
    root.title("✍️ The Writer's Compass ✍️")
    root.geometry("800x900")
    root.config(bg="#1a1a1a")
    
    frm_main = Frame(root, bg="#1a1a1a")
    frm_main.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
    setup_reminder(frm_main)
    frm_main.mainloop()

def setup_reminder(frm):
    # Get current date and time
    now = datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    time_str = now.strftime("%I:%M %p")
    
    # Title
    lbl_title = Label(frm, text="✍️ The Writer's Compass", 
                     font=("Helvetica", 28, "bold"), bg="#1a1a1a", fg="#E0B86B")
    lbl_title.pack(pady=10)
    
    # Date and time
    lbl_datetime = Label(frm, text=f"{date_str} • {time_str}", 
                        font=("Helvetica", 18), bg="#1a1a1a", fg="#888888")
    lbl_datetime.pack()
    
    # Core message frame
    frm_core = Frame(frm, bg="#2d2d2d", relief=tk.SUNKEN, bd=2)
    frm_core.pack(pady=20, fill=tk.BOTH, expand=True, padx=5)
    
    lbl_reminder = Label(frm_core, text="Remember Your Why", 
                        font=("Helvetica", 21, "bold"), bg="#2d2d2d", fg="#E0B86B", pady=5)
    lbl_reminder.pack()
    
    # Main motivational text
    lbl_main = Label(frm_core, 
                    text="Everything you code.\nEvery line you write.\nEvery problem you solve.\n\nbrings you closer to your true passion:\n\nWRITING",
                    font=("Helvetica", 19), bg="#2d2d2d", fg="#D0D0D0", 
                    justify=tk.CENTER, pady=20)
    lbl_main.pack(fill=tk.BOTH, expand=True)
    
    # Motivational quotes for writers
    quotes = [
        "\"The secret to getting ahead is getting started.\" - Mark Twain",
        "\"There is no greater agony than bearing an untold story.\" - Maya Angelou",
        "\"A writer who waits for ideal conditions to work will die without writing.\" - E.B. White",
        "\"You fail only if you stop writing.\" - Ray Bradbury",
        "\"The scariest moment is just before you start.\" - Stephen King",
        "\"Writing is the painting of the voice.\" - Voltaire",
        "\"I write to taste life twice.\" - Anaïs Nin",
        "\"All you have to do is write one true sentence. Write the truest sentence you know.\" - Ernest Hemingway",
        "\"There's no such thing as writer's block. There's only writer's fear.\" - Unknown",
        "\"You can make anything by writing.\" - C.S. Lewis",
        "\"A writer who waits for ideal conditions under which to work will die without writing a word.\" - E.B. White",
        "\"Start writing, no matter what. The water does not flow until the faucet is turned on.\" - Louis L'Amour",
        "\"There is no greater agony than bearing an untold story inside you.\" - Maya Angelou",
        "\"Writers are made, not born, not created out of dreams of childhood trauma.\" - Octavia Butler",
        "\"The only way to do daily work well with moments of excellence is by the repetition of simple and obvious practices.\" - Anne Rice",
        "\"The scariest moment is just before you start. After that, things can only get better.\" - Stephen King",
        "\"You must make a commitment to excellence every single day.\" - Vince Lombardi",
        "\"Almost all good writing begins with terrible first efforts. You need to start somewhere.\" - Anne Lamott",
        "\"A professional writer is an amateur who didn't quit.\" - Richard Bach",
        "\"Write. Rewrite. When not writing or rewriting, read.\" - William Faulkner",
        "\"The thing about writing is you have to do your emotional labor voluntarily.\" - Lauren Groff",
        "\"If you don't have time to read, you don't have the time or the tools to write.\" - Stephen King",
        "\"I hate writing, I love having written.\" - Dorothy Parker",
        "\"Every writer has the potential to change the world.\" - Paulo Coelho"
    ]
    
    current_quote = {"index": random.randint(0, len(quotes)-1)}
    
    # Quote display
    lbl_quote = Label(frm, text=quotes[current_quote["index"]], 
                     font=("Helvetica", 21, "italic"), bg="#1a1a1a", fg="#A0D8FF",
                     wraplength=550, justify=tk.CENTER)
    lbl_quote.pack(pady=15)
    
    # Timer section
    frm_timer = Frame(frm, bg="#3a4a4a", relief=tk.RAISED, bd=2)
    frm_timer.pack(pady=15, fill=tk.X, padx=5)
    
    lbl_timer_title = Label(frm_timer, text="Coding Focus Timer", 
                           font=("Helvetica", 17, "bold"), bg="#3a4a4a", fg="#A8D8A8")
    lbl_timer_title.pack(pady=5)
    
    timer_state = {"time_left": 3600, "is_running": False, "after_id": None}
    
    lbl_timer_display = Label(frm_timer, text="60:00", 
                             font=("Helvetica", 40, "bold"), bg="#3a4a4a", fg="#FFD700")
    lbl_timer_display.pack(pady=10)
    
    def update_timer():
        if timer_state["is_running"] and timer_state["time_left"] > 0:
            timer_state["time_left"] -= 1
            minutes = timer_state["time_left"] // 60
            seconds = timer_state["time_left"] % 60
            lbl_timer_display.config(text=f"{minutes}:{seconds:02d}")
            
            if timer_state["time_left"] == 0:
                lbl_timer_display.config(fg="#FF6B6B")
                lbl_timer_title.config(text="✓ 1 Hour Complete! Time for a break!")
                timer_state["is_running"] = False
                btn_start.config(text="Start Timer")
            else:
                timer_state["after_id"] = frm_timer.after(1000, update_timer)
        elif timer_state["is_running"]:
            timer_state["after_id"] = frm_timer.after(1000, update_timer)
    
    def start_stop_timer():
        if timer_state["is_running"]:
            timer_state["is_running"] = False
            btn_start.config(text="Resume Timer")
            if timer_state["after_id"]:
                frm_timer.after_cancel(timer_state["after_id"])
        else:
            timer_state["is_running"] = True
            btn_start.config(text="Pause Timer")
            lbl_timer_title.config(text="Coding Focus Timer")
            lbl_timer_display.config(fg="#FFD700")
            update_timer()
    
    def reset_timer():
        timer_state["time_left"] = 3600
        timer_state["is_running"] = False
        lbl_timer_display.config(text="60:00", fg="#FFD700")
        lbl_timer_title.config(text="Coding Focus Timer")
        btn_start.config(text="Start Timer")
        if timer_state["after_id"]:
            frm_timer.after_cancel(timer_state["after_id"])
    
    frm_timer_buttons = Frame(frm_timer, bg="#3a4a4a")
    frm_timer_buttons.pack(pady=10)
    
    btn_start = Button(frm_timer_buttons, text="Start Timer", command=start_stop_timer,
                      bg="#A0D8FF", fg="#000000", font=("Helvetica", 13, "bold"),
                      padx=20, pady=10, relief=tk.RAISED, bd=2)
    btn_start.pack(side=tk.LEFT, padx=5)
    
    btn_reset_timer = Button(frm_timer_buttons, text="Reset Timer", command=reset_timer,
                            bg="#E88BA8", fg="#000000", font=("Helvetica", 13, "bold"),
                            padx=20, pady=10, relief=tk.RAISED, bd=2)
    btn_reset_timer.pack(side=tk.LEFT, padx=5)
    
    # Daily checklist message
    frm_daily = Frame(frm, bg="#3a3a3a", relief=tk.RAISED, bd=1)
    frm_daily.pack(pady=15, fill=tk.X, padx=5)
    
    lbl_daily_title = Label(frm_daily, text="Today's Focus", 
                           font=("Helvetica", 18, "bold"), bg="#3a3a3a", fg="#A8D8A8")
    lbl_daily_title.pack(pady=5)
    
    lbl_daily_msg = Label(frm_daily, 
                         text="✓ Code with purpose\n✓ Remember: This is for writing\n✓ Take breaks and breathe\n✓ You're investing in your dream",
                         font=("Helvetica", 17), bg="#3a3a3a", fg="#D0D0D0", justify=tk.LEFT)
    lbl_daily_msg.pack(pady=10, padx=10)
    
    # Buttons frame
    frm_buttons = Frame(frm, bg="#1a1a1a")
    frm_buttons.pack(pady=10, fill=tk.X)
    
    def next_quote():
        current_quote["index"] = (current_quote["index"] + 1) % len(quotes)
        lbl_quote.config(text=quotes[current_quote["index"]])
    
    def random_quote():
        current_quote["index"] = random.randint(0, len(quotes)-1)
        lbl_quote.config(text=quotes[current_quote["index"]])
    
    btn_next = Button(frm_buttons, text="Next Quote", command=next_quote,
                     bg="#4ECDC4", fg="#000000", font=("Helvetica", 15, "bold"),
                     padx=25, pady=14, relief=tk.RAISED, bd=2)
    btn_next.pack(side=tk.LEFT, padx=5)
    
    btn_random = Button(frm_buttons, text="Random Quote", command=random_quote,
                       bg="#FFE66D", fg="#000000", font=("Helvetica", 15, "bold"),
                       padx=25, pady=14, relief=tk.RAISED, bd=2)
    btn_random.pack(side=tk.LEFT, padx=5)
    
    # Motivational footer
    lbl_footer = Label(frm, text="\"The world needs your stories. Start writing today.\"",
                      font=("Helvetica", 17, "italic"), bg="#1a1a1a", fg="#E88BA8")
    lbl_footer.pack(pady=5)

if __name__ == "__main__":
    main()
