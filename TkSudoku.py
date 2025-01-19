from tkinter import *
from Sudoku import *

class SudokuCellWidget(Frame) :

    def __init__(self, parent, cell : SudokuCell, default=""):
        Frame.__init__(self, parent, highlightbackground="blue", highlightthickness=1)

        if cell.isDone() :
            Label(self, text=str(cell.getFinalNumber()), fg="red", anchor="center").pack()


        else:
            for row in range(3):
                for col in range(3):
                    i = 1 + row*3+col
                    lbl = str(i) if (i in cell.getValidNumbers()) else " "
                    Label(self, text=lbl, anchor="center").grid(row=row, column=col)



class SudokuBoardWidget(Frame) :

    def __init__(self, parent, board : SudokuBoard, default=""):
        Frame.__init__(self, parent, highlightbackground="red", highlightthickness=1)

        for boxRow in range(3):
            for boxCol in range(3):
                f = Frame(self, highlightbackground="green", highlightthickness=1)
                for fr in range(3) :
                    for fc in range(3) :
                        row = boxRow*3 + fr
                        col = boxCol*3 + fc

                        sc = SudokuCoordinate(row+1, col+1)
                        cell = board.getCell(sc)
                        scw = SudokuCellWidget(f,cell)
                        scw.grid(row=fr, column=fc)
                f.grid(row=boxRow, column=boxCol)




def ShowSodukuBoard(b : SudokuBoard):
    window = Tk()
    window.title("SudokuBoard")
    #window.configure(background="yellow")
    #window.minsize(200,200)
    #window.maxsize(500,500)
    #window.geometry("300x300+100+100")

    #l1 = tk.Label(window, text="Nothing will work unless you do.").pack()
    #l2 = tk.Label(window, text="- Maya Angelou").pack()

    s = SudokuBoardWidget(window, b)
    s.pack()

    button = Button(window, text="Close", command=lambda: window.destroy())
    button.pack()


    window.mainloop()

