import tkinter as tk
import utils
import game

root = tk.Tk()
root.title("Wordle")
root.geometry("600x700")

top_frame = tk.Frame(
    root,
    bg='#787059'
)
top_frame.place(relx=0, rely=0, relwidth=1.0, relheight=.07)

wordle_lbl = tk.Label(top_frame, 
                      bg='#787059', 
                      fg='white', 
                      text="WORDLE", 
                      font=("Ariel", 36, "bold italic"))
wordle_lbl.place(relx=.5, rely=.5, anchor=tk.CENTER)

bottom_frame = tk.Frame(
    root,
    bg='#787059'
)
bottom_frame.place(relx=0, rely=.07, relwidth=1.0, relheight=.9)

game_play = game.Wordle(bottom_frame, wordle_lbl, root)

root.mainloop()