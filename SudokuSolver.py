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


ARROW_KEYS = {curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN}

def main(scr : curses.window):
    # Clear screen
    scr.clear()
    curses.curs_set(False)
    defineColors()

    while True:
        printGrid(scr, b)
        scr.refresh()
        k = scr.getch()

        if k == ord('q') : 
            break # Exit the program

        elif k == curses.KEY_ENTER or k == 10 :
            finalizeCell(scr, b)
            continue
            
        elif k == ord('h') :
            getHighlight(scr, b)
            continue

        elif k == ord('c') : 
            if b.cursorCell == None :
                b.cursorCell = SudokuCoordinate(5,5) 
            else :
                b.cursorCell = None
            continue

        elif b.cursorCell != None and k in ARROW_KEYS :
            if   k == curses.KEY_LEFT  : b.cursorCell.moveLeft()
            elif k == curses.KEY_RIGHT : b.cursorCell.moveRight()
            elif k == curses.KEY_UP    : b.cursorCell.moveUp()
            elif k == curses.KEY_DOWN  : b.cursorCell.moveDown()
            continue

        else :
            setMessage(scr, f"Key {k} not recognized")



curses.wrapper(main)