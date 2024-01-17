from tkinter import *
import random
from tkinter import messagebox
import subprocess

class FourPicsOneWord(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x650")
        self.title('4 Pics 1 Word')
        self.resizable(False,False)
        self.configure(background='#1c1c24')
        self.picNum = 0
        self.amount = 100
        self.level = 1
        self.word = ""

        self.bind('<Control-s>', lambda event: self.saveGameState())

        #Read file content and store the words in a list named picfiles
        with open("picList.txt", "r") as f:
            x = f.readlines()
            self.picfiles = list()
            for p in x:
                fn = p.strip().split(';')
                self.picfiles.append(fn[1])

        self.hintlist = [[letter.upper() for letter in word] for word in self.picfiles]

        #Create a list of jumbled letters
        self.target_length = 12
        self.words_with_random_letters = []
        for word in self.picfiles:
            current_length = len(word)
            if current_length == self.target_length:
                self.words_with_random_letters.append(word)
                continue
            additional_letters = self.target_length - current_length
            random_letters = ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(additional_letters)])
            modified_word = ((word + random_letters)).upper()
            shuffled = ''.join(random.sample(modified_word, len(modified_word)))
            self.words_with_random_letters.append(shuffled)
        self.letters = [[letter for letter in word] for word in self.words_with_random_letters]

        # Create label boxes
        self.label_frame = Frame(self, name='label_frame', width=500, height=50, bg='#1c1c24')
        self.label_frame.place(x=180,y=410)
        self.label_boxes = []
        for i in range(len(self.picfiles[self.picNum])):
            label_box = Label(self.label_frame, width=2, height=1, bg='white', font='AvenirNext 20 bold', relief='groove')
            label_box.grid(row=0, column=i, padx=5, pady=5)
            self.label_boxes.append(label_box)

    #Keyboard
        self.keyboard_frame = Frame(self, name='keyboard_frame',bg='#1c1c24')
        self.keyboard_frame.place(x=75,y=480)
        self.keyboard_buttons = []
        for row in range(2):
            for col in range(6):
                letter_index = row * 6 + col
                letter = self.letters[0][letter_index]
                button = Button(self.keyboard_frame, text=letter, font='AvenirNext 16 bold',
                                command=lambda x=letter_index: self.updateLabel(x),width=3,height=1)
                button.grid(row=row, column=col, padx=5, pady=5)
                self.keyboard_buttons.append(button)

        # Header
        self.top_Canvas = Canvas(self, name='top_canvas', width=500, height=50, bg='#535d85',highlightthickness=0)
        self.top_Canvas.pack(side=TOP)


        self.ribbon = PhotoImage(file=r'ribbon.png')
        self.ribbon_=self.ribbon.subsample(18,18)
        self.top_Canvas.create_image(250, 25, image=self.ribbon_)
        self.txtlvl = self.top_Canvas.create_text(250, 25, text=f'{self.level}', font='Times 25 bold', fill='white')
        self.img = PhotoImage(file=r'coins.png')
        self.img_resized = self.img.subsample(35, 45)
        self.top_Canvas.create_image(385, 25, image=self.img_resized)
        self.texting = self.top_Canvas.create_text(450, 25, text=self.amount, font='Times 25 bold', fill='white')

        # The pictures
        self.pics = PhotoImage(file=self.picfiles[0] + ".png")
        self.lblpic = Label(self, image=self.pics)
        self.lblpic.place(x=100, y=90)

        #backbutton
        self.back = Button(self, text="BACK", command=self.backtothefuture,font='Fixedsys 15 underline',bg='#535d85',fg='white')
        self.back.place(x=10, y=8)

        #hint button
        self.hint_button = Button(self, text="HINT", command=self.clickHintButton,font='Fixedsys 15 underline',bg='#b40404',fg='white')
        self.hint_button.place(x=434, y=520)

        # check button
        self.check_button = Button(self, text="SUBMIT", command=self.checkWord,font='Fixedsys 15 underline',bg='#64b31c',fg='white')
        self.check_button.place(x=180, y=600)

        #skip button
        self.nextPic = Button(self, text="SKIP", command=self.changeImage,font='Fixedsys 15 underline',bg='#b40404',fg='white')
        self.nextPic.place(x=260, y=600)
        self.window()


    def backtothefuture(self):
        self.destroy()
        subprocess.Popen(["python", "main game.py"])

    def clickHintButton(self):
        if self.picNum >= len(self.hintlist):
            messagebox.showerror("Error", "No more hints available.")
            return
        counter = len(self.picfiles[self.picNum])
        if self.amount >= 2 and len(self.word) < counter:
            self.amount -= 2
            self.top_Canvas.itemconfig(self.texting, text=self.amount)
            counter -= 1
            for letter in self.hintlist[self.picNum]:
                if letter:
                    for i, kb_button in enumerate(self.keyboard_buttons):
                        if kb_button['text'] == letter:
                            kb_button.invoke()
                            self.hintlist[self.picNum][self.hintlist[self.picNum].index(letter)] = ''  # mark as used
                            return

        elif self.amount < 2:
            messagebox.showerror("Error", "Insufficient Coins.")
            # if there are no non-empty characters left, show a message
        messagebox.showerror("Error", "No more hints available.")

    def updateLabel(self, index):
        self.keyboard_buttons[index].config(bg='#1c1c24', fg='#1c1c24')
        letter = self.letters[self.picNum][index]
        self.word += letter
        for i, label_box in enumerate(self.label_boxes):
            if not label_box['text']:
                label_box.config(text=letter,font='AvenirNext 20 bold')
                break

    def origKey(self):
        try:
            for i in range(len(self.letters)):
                self.keyboard_buttons[i].config(bg='SystemButtonFace', fg='#1c1c24')
        except:pass

    def collectWord(self):
        for label_box in self.label_boxes:
            label_box.destroy()
        self.label_boxes = []
        self.labelfixing()
        self.origKey()

    def labelfixing(self):
        # Create new label boxes based on the length of the word
        word_length = len(self.picfiles[self.picNum])
        self.label_frame = Frame(self, name='label_frame', width=500, height=50, bg='black',)
        xcoord = 130
        if word_length == 3:xcoord = 180
        elif word_length == 4:xcoord = 150
        elif word_length == 6:xcoord = 110
        elif word_length == 7:xcoord = 85
        elif word_length == 8:xcoord = 65
        elif word_length == 9:xcoord = 45
        self.label_frame.place(x=xcoord, y=410)
        for i in range(word_length):
            label_box = Label(self.label_frame, width=2, height=1, bg='white', font=('Helvetica', 20),
                              relief='groove')
            label_box.bind("<Button-1>", lambda event: self.collectWord())
            label_box.grid(row=0, column=i, padx=5, pady=5)
            self.label_boxes.append(label_box)
        self.word = ""
        for label_box in self.label_boxes:
            label_box.config(text="")

    def checkWord(self):
        if self.word.lower() == self.picfiles[self.picNum]:
            self.amount += 10
            self.top_Canvas.itemconfig(self.texting, text=self.amount)
            self.levelstock()
            self.origKey()

        else:
            response = messagebox.askretrycancel("Wrong Answer!", "Wrong Answer!\n  Try again?")
            if response == True:
                self.origKey()
                self.word = ""
                for label_box in self.label_boxes:
                    label_box.config(text="")
            else:self.backtothefuture()

    def updateHeader(self):
        self.top_Canvas.itemconfigure(self.txtlvl, text=f'{self.level}')
        self.top_Canvas.itemconfigure(self.texting, text=f'{self.amount}')

    def levelstock(self):
        self.level += 1
        self.top_Canvas.itemconfig(self.txtlvl, text=f'{self.level}')
        self.picNum += 1
        try:
            current_word_letters = self.letters[self.picNum]
            for i, button in enumerate(self.keyboard_buttons):
                button.config(text=current_word_letters[i])
        except:
            # Destroy the menu window
            messagebox.showinfo('Congratulations!',f'Congratulations!\nYou Beat The Game\nCoins Earned: {self.amount}')
            self.destroy()

            # Start the game using subprocess
            self.picNum = 49
            self.level = 50
            self.saveGameState()
            subprocess.Popen(["python", "main game.py"])

        self.pics.config(file=self.picfiles[self.picNum] + ".png")
        self.saveGameState()


        # Delete existing label boxes
        for label_box in self.label_boxes:
            label_box.destroy()
        self.label_boxes = []
        self.labelfixing()

    def changeImage(self):
        if self.amount < 10:
            messagebox.showinfo("Not enough coins", "You need at least 10 coins to skip the level.")
            return
        elif self.amount >= 10:
            self.amount -= 10
            self.top_Canvas.itemconfig(self.texting, text=self.amount)
            self.levelstock()
            self.origKey()

    def resetGameState(self):
        # Set the game state back to its default values
        try:
            self.picNum = 0
            self.amount = 100
            self.level = 1
            self.saveGameState()
            self.destroyer()
        except:
            pass

    def destroyer(self):
        self.updateLoadAndReset()
        self.reset_button.destroy()
        self.load_button.destroy()
        self.black_screen.destroy()
        self.top_Canvas.pack(side=TOP)

    def updateLoadAndReset(self):
        self.word = ""
        for box in self.label_boxes:
            box.configure(text="")
        self.updateKeyboardButtons(self.letters[self.picNum])
        self.pics.configure(file=self.picfiles[self.picNum] + ".png")
        self.updateHeader()
        self.labelfixing()
        self.origKey()

    def loadGameState(self):
        try:
            with open('gamestate.txt', 'r') as f:
                lines = f.readlines()
                self.amount,self.picNum,self.level = lines[0].split(',')
                self.amount = int(self.amount);self.picNum = int(self.picNum);self.level = int(self.level)
                self.destroyer()

        except:
            pass

    def saveGameState(self):
        # Open a file and write the current state of the game
        with open("gamestate.txt", "w") as f:
            f.write(f"{self.amount},{self.picNum},{self.level}\n")

    def updateKeyboardButtons(self, letters):
        for i in range(len(letters)):
            self.keyboard_buttons[i].configure(text=letters[i])

    def window(self):
        self.black_screen = Frame(self, bg='#1c1c24', width=1000, height=1000)
        self.black_screen.pack(fill='both', expand=True)

        self.top_Canvas.pack_forget()

        # create the reset and load buttons and place them on the black screen
        self.reset_button = Button(self.black_screen, text="Start New Game", command=self.resetGameState,width=20,
                                   font='Fixedsys 20 underline',bg='#a4cc04',fg='white',highlightcolor='white',highlightbackground='white')
        self.reset_button.place(x=90,y=280)
        self.load_button = Button(self.black_screen, text="Load Saved Progress", command=self.loadGameState,width=20,
                                  font='Fixedsys 20 underline',bg='#b40404',fg='white',highlightcolor='white',highlightbackground='white')
        self.load_button.place(x=90,y=200)

def main():
    root = FourPicsOneWord()
    root.mainloop()

if __name__ == '__main__':
    main()