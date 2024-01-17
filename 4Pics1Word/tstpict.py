from tkinter import *
f = open("picList.txt","r")
x = f.readlines()

picfiles = list()
for p in x:
    fn = p.strip().split(';')
    picfiles.append(fn[1])
amount = 100
picNum = 0
level = 1
def changeImage():
    global amount
    amount -= 10
    global picNum
    global level
    level += 1
    picNum+=1
    if picNum==50:
        picNum=0
    pics.config(file=picfiles[picNum]+".png")
    nextPic.config(text="Picture No."+str(picNum+1)+". NEXT?")


    
root = Tk()
root.geometry("500x650")


pics = PhotoImage(file=picfiles[0]+".png")
top_Canvas = Canvas(root, name='top_canvas', width=500, height=50, bg='blue',highlightthickness=0)
top_Canvas.pack(side=TOP)
lblpic = Label(root,image=pics)
lblpic.place(x=100, y=90)
txtlvl = top_Canvas.create_text(75, 25, text=f'Level {level}', font='Times 25 bold', fill='white')
img = PhotoImage(file=r'coins.png')
img_resized = img.subsample(35, 45)
top_Canvas.create_image(385, 25, image=img_resized)
texting = top_Canvas.create_text(450, 25, text=amount, font='Times 25 bold', fill='white')
nextPic = Button(root,text="Picture No."+str(picNum+1)+". NEXT?",command=changeImage)
nextPic.place(x=200, y=450)
root.mainloop()


