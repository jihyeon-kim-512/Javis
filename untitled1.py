
import tkinter
from PIL import ImageTk, Image

root = tkinter.Tk() 
root.title("Wallpaper") 
root.geometry("1000x525") 
wall = ImageTk.PhotoImage(file = "eco.gif") 
wall_label = tkinter.Label(image = wall) 
wall_label.place(x = -2,y = -2) 

lb1 = tkinter.Label(root, text="Test1", bg="white", font=("맑은 고딕", 15))
lb1.pack()
lb1.place(x=181, y=175)

lb2 = tkinter.Label(root, text="Test2", bg="white", font=("맑은 고딕", 15))
lb2.pack()
lb2.place(x=442, y=175)

lb3 = tkinter.Label(root, text="Test3", bg="white", font=("맑은 고딕", 15))
lb3.pack()
lb3.place(x=703, y=175)



cont1 = tkinter.Label(root, text="I am writing a GUI in Tkinter and all it needs to do is have a search box, and then output the results as a hyperlink. I am having lots of trouble. What is the best way to do this?", 
                      font=("맑은 고딕", 12), width=23, height=10, anchor='n', justify='left', wraplength=190)
cont1.pack()
cont1.place(x=181, y=250)

cont2 = tkinter.Label(root, text="두번째 뉴스 입니다 지난 밤,,,"
                      , bg="white", font=("맑은 고딕", 12), width=23, height=10, anchor='n', justify='left', wraplength=190)
cont2.pack()
cont2.place(x=442, y=250)

cont3 = tkinter.Label(root, text="마지막 뉴스 입니다 다음주,,,"
                      , bg="white", font=("맑은 고딕", 12), width=23, height=10, anchor='n', justify='left', wraplength=190)
cont3.pack()
cont3.place(x=703, y=250)



root.mainloop()
