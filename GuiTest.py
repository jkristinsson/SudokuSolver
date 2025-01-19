import tkinter as tk
from TkSudoku import *



def ShowSodukuBoard(c : SudokuCell):
    window = tk.Tk()
    window.title("Hello World")
    #window.configure(background="yellow")
    #window.minsize(200,200)
    #window.maxsize(500,500)
    window.geometry("300x300+100+100")

    #l1 = tk.Label(window, text="Nothing will work unless you do.").pack()
    #l2 = tk.Label(window, text="- Maya Angelou").pack()


    s = SudokuCellWidget(window,c)
    s.pack()

    button = tk.Button(window, text="Close", command=lambda: window.quit())
    button.pack()

    window.mainloop()

sb = SudokuBoard()

c = SudokuCell()
c.removeNumber(3)
c.removeNumber(7)

ShowSodukuBoard(c)
c.removeNumbers({5,1})
ShowSodukuBoard(c)