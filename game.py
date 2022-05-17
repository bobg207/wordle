import tkinter as tk
import utils

class Wordle:
    def __init__(self, frame, label, window):
        self.frame = frame
        self.label = label
        self.window1 = window
        self.window2 = None
        self.new_game()

    def new_game(self):
        if self.window2:
            self.window2.destroy()
        self.game_tiles = []
        self.keys = []
        self.chosen_keys = []
        self.tile = 0
        self.row = 0
        self.sub_btn = None
        self.word = utils.get_word()
        print(self.word)
        self.create_layout()
        
    def create_layout(self):
        self.create_lbl_rows()
        self.create_keyboard()

    def create_lbl_rows(self):
        # 6 rows of 5 labels added to game_tiles list
        for row in range(6):
            for col in range(5):
                lbl = tk.Label(self.frame, relief=tk.SUNKEN, font=("", 32, 'bold'))
                lbl.place(relx = .15+col*.15, rely = .01+row*.12, relwidth=.1, relheight=.1)
                self.game_tiles.append(lbl)

    def create_keyboard(self):
        top='QWERTYUIOP'
        middle = 'ASDFGHJKL'
        bottom = 'ZXCVBNM'
        for i, letter in enumerate(top):
            btn = tk.Button(self.frame, 
                            text=letter,
                            font=("", 18, 'bold'),
                            command= lambda t=letter: self.choose_letter(t))
            btn.place(relx = .12+i*.08, rely = .75, relwidth=.05, relheight=.05)
            self.keys.append(btn)
        for i, letter in enumerate(middle):
            btn = tk.Button(self.frame, 
                            text=letter, 
                            font=("", 18, 'bold'),
                            command=lambda t=letter: self.choose_letter(t))
            btn.place(relx = .16+i*.08, rely = .82, relwidth=.05, relheight=.05)
            self.keys.append(btn)
        for i, letter in enumerate(bottom):
            btn = tk.Button(self.frame, 
                            text=letter, 
                            font=("", 18, 'bold'),
                            command=lambda t=letter: self.choose_letter(t))
            btn.place(relx = .24+i*.08, rely = .89, relwidth=.05, relheight=.05)
            self.keys.append(btn)
        self.sub_btn = tk.Button(self.frame, 
                                text="Submit", 
                                font=("", 14, 'bold'),
                                command = self.submit)
        self.sub_btn.place(relx = .10, rely = .89, relwidth=.1, relheight=.05)
        self.sub_btn.config(state=tk.DISABLED)
        del_btn = tk.Button(self.frame, 
                            text="Delete", 
                            font=("", 14, 'bold'),
                            command=self.delete_letter)
        del_btn.place(relx = .81, rely = .89, relwidth=.1, relheight=.05)

    def choose_letter(self, key):
        # only fill labels in the curent row
        if self.tile // 5 == self.row:
            # update label with chosen letter, "key"
            self.game_tiles[self.tile].configure(text=key)

            # update tile count
            self.tile += 1
            
            # find the chosen key in keys list, change font to chosen, 
            # and add button to chosen_keys lits
            for k in self.keys:
                if k.cget('text') == key:
                    k.configure(fg='grey', font=("", 14))
                    self.chosen_keys.append(k)
        
        # make the submit button available when the 5th letter, in a row, is chosen
        if self.tile % 5 == 0:
            self.sub_btn.config(state=tk.ACTIVE)

    def delete_letter(self):

        # only delete choices in the current row
        if self.row == (self.tile-1) // 5:
            # update tile count
            self.tile -= 1

            try: 
                # delete the letter
                self.game_tiles[self.tile].configure(text="")
                
                # remove the button/letter from the chosen_keys list
                key = self.chosen_keys.pop()

                # locate that key in the keys list and reset the font to original state
                for k in self.keys:
                    key.configure(fg='black', font=("", 18, 'bold'))
            except:
                pass

        # don't allow the tile count to be negative
        if self.tile < 0:
            self.tile = 0

        # keep the submit button disabled while tile count is less than 5
        if self.tile % 5 != 0:
            self.sub_btn.config(state=tk.DISABLED)
    
    def check_solution(self):
        # need slice of chosen keys to correspond with indices of the row of labels
        start = self.tile - 5
        stop = self.tile

        # check if all five letters are in correct order
        total = 0

        word = ''
        # loop through the chosen keys and compare with letters in the word 
        # change colors of labels 
        for index, key in enumerate(self.chosen_keys[start:stop]):
            word_index = index % 6
            current_tile = index+self.row*5
            letter = key.cget('text').lower()
            if letter == self.word[word_index]:
                self.game_tiles[current_tile].configure(bg="green", fg='white')
                total += 1
            elif letter in self.word and letter not in word:
                self.game_tiles[current_tile].configure(bg="#badb12", fg='white')
            else:
                self.game_tiles[current_tile].configure(bg="grey", fg='white')

            word += letter

        # if all letters are correct or run out of guesses
        if total == 5:
            attempts = self.tile // 5
            msg = f"You got the word in {attempts} attempts"
            self.popup_msg(msg)
        elif self.row == 5 and total < 5:
            msg = f"You did not get the word correct.\nIt was {''.join(self.word)}"
            self.popup_msg(msg)

        # disable submit button after a guess
        self.sub_btn.config(state=tk.DISABLED)

    def submit(self):
        start = self.tile - 5
        stop = self.tile
        word = ''

        for key in self.chosen_keys[start:stop]:
            word += key.cget('text').lower()
        
        # if it's a valid word, check the solution and update the row
        if utils.is_valid_word(word):
            print(word)
            self.check_solution()

            if self.row < 6:
                self.row += 1
        else:
            msg = f"{word} is not valid"
            self.popup_msg(msg, False)
        
    def popup_msg(self, msg, end=True):
        # create a new window for the game over message => "msg", if end
        # or invalid word message
        self.window2 = tk.Tk()
        
        if end:
            self.window2.title("Game Over")
            label = tk.Label(self.window2, text=msg)
            label.pack(side="top", fill="x", pady=10)

            b1 = tk.Button(self.window2, text="Quit", command = lambda: self.quit(2))
            b1.pack()

            b2 = tk.Button(self.window2, text="Play Again", command = self.new_game)
            b2.pack()
        else:
            self.window2.title("Invalid Word")
            label = tk.Label(self.window2, text=msg)
            label.pack(side="top", fill="x", pady=10)
            
            b1 = tk.Button(self.window2, text="Close", command = lambda: self.quit(1))
            b1.pack()

        self.window2.mainloop()

    def quit(self, option):
        # destroy the windows
        if option == 1:
            self.window2.destroy()
        else:
            self.window1.destroy()
            self.window2.destroy()
