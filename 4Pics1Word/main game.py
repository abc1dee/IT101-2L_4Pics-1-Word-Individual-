from tkinter import *
import subprocess


class Menu(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('500x650')
        self.resizable(False,False)
        self.title("4 Pics 1 Word")
        self.canvas = Canvas(self,width=500,height=650)
        self.canvas.pack(fill=BOTH, expand=True)


        self.bg = PhotoImage(file=r'Made by Clarence ABcdee M. GLorioso.png')
        self.canvas.create_image(250,320,image = self.bg)

        with open("picList.txt", "r") as f:
            x = f.readlines()
            self.picfiles = list()
            for p in x:
                fn = p.strip().split(';')
                self.picfiles.append(fn[1])

        self.levelsync()
        self.pics = PhotoImage(file=self.picfiles[self.picNum] + ".png")
        self.canvas.create_image(250, 335, image=self.pics)
        self.ribbon = PhotoImage(file=r'ribbon.png')
        self.ribbon_ = self.ribbon.subsample(9, 9)
        self.container = self.canvas.create_image(250, 337, image=self.ribbon_)
        self.txtlvl = self.canvas.create_text(250, 335, text=f'{self.level}', font='Times 35 bold', fill='white')
        self.txt_title = self.canvas.create_text(250, 140, text=f'4 Pics 1 Word', font='Times 35 bold', fill='white')

        self.coins = PhotoImage(file=r'coins.png')
        self.coins_ = self.coins.subsample(27, 27)
        self.coinHolder = self.canvas.create_image(50, 600, image=self.coins_)
        self.txtCoins = self.canvas.create_text(130, 600, text=f'{self.amount}', font='Times 35 bold', fill='white')


        # Create a button to start the game
        self.start_button = Button(self,command=self.start_game,text='Play Game',font='Fixedsys 34 italic',bg='#a4cc04',fg='white',highlightcolor='white',highlightbackground='white')
        self.start_button.place(x=85,y=450)

    def levelsync(self):
        try:
            with open('gamestate.txt', 'r') as f:
                lines = f.readlines()
                self.amount,self.picNum,self.level = lines[0].split(',')
                self.level = int(self.level);self.picNum = int(self.picNum);self.amount = int(self.amount)
                self.pics.configure(file=self.picfiles[self.picNum] + ".png")

        except:
            pass

    def start_game(self):
        # Destroy the menu window
        self.destroy()

        # Start the game using subprocess
        subprocess.Popen(["python", "gamecont.py"])



root = Menu()
root.mainloop()
