import curses
from CursesSudoku import *


# Parse input file
with open("Puzzles/NYT20250117Easy.txt", "r") as f:
    lines = f.read().strip().split('\n')
    f.close()

b = SudokuBoard()
for (r,row) in enumerate(lines):
    for (c,char) in enumerate(row):
        if char != '.' : 
            x = int(char)
            sc = SudokuCoordinate(r+1, c+1)
            b.setCell(sc, x)




def main(scr : curses.window):
    # Clear screen
    scr.clear()
    curses.curs_set(False)

    #cBorder = 1
    #cPossible = 2
    #cFinal = 3
    #curses.init_pair(cBorder, fg=curses.COLOR_BLACK, bg=curses.COLOR_WHITE)
    #curses.init_pair(cPossible, fg=curses.co)

    #b = SudokuBoard()

    while True:
        printGrid(scr, b)
        scr.refresh()
        k = scr.getch()

        if k == ord('q') : 
            break # Exit the program
        
        elif k == ord(' ') : 
            if b.cursorCell == None :
                b.cursorCell = (5,5) 
            else :
                b.cursorCell = None

        elif b.cursorCell != None :
            if   k == curses.KEY_LEFT  : b.cursorCell.moveLeft()
            elif k == curses.KEY_RIGHT : b.cursorCell.moveRight()
            elif k == curses.KEY_UP    : b.cursorCell.moveUp()
            elif k == curses.KEY_DOWN  : b.cursorCell.moveDown()


curses.wrapper(main)