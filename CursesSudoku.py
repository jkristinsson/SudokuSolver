import curses
from Sudoku import *

# This is how curses actually work:
#    # Set up curses
#    stdscr = curses.initscr() # Initialize the curses environment
#    curses.noecho() # Turn off echo so that keypresses doesn't show automatically
#    curses.cbreak() # Enable key detection without having to press enter
#    stdscr.keypad(True) # Enable multi-byte-escape codes (e.g. for arrow keys)
#
#    # Do code here
#
#    # End the application
#    curses.nocbreak() # Disable key detection
#    stdscr.keypad(False) # Reverse multi-byte-escape code catching
#    curses.echo() # Turn on the key echo
#    curses.endwin() # Return terminal to original state
#
# However, in order to automatically manage exception handling and setting up/restoring
# the terminal afterwards, we are using the 'wrapper' class. We define our program in
# a main function, then ask wrapper to execute it.



def printGrid(scr : curses.window, sboard : SudokuBoard):
    if curses.LINES < 37 or curses.COLS < 50 :
        scr.addstr(0,0,f"Terminal must be at least {50} x {37} for this to work!")
        scr.addstr(1,0,f"Current size is {curses.COLS} x {curses.LINES}")
        scr.addstr(3,0,"Press 'q' to exit")
        scr.refresh()
        return

    scr.addstr(1,38,"Screen Size")
    scr.addstr(2,39,f"Lines: {curses.LINES}")
    scr.addstr(3,39,f"Cols:  {curses.COLS}")
    scr.addstr(5,38,f"Highlighted row:   {sboard.highlightedRow}   ")
    scr.addstr(6,38,f"Highlighted col:   {sboard.highlightedCol}   ")
    scr.addstr(7,38,f"Highlighted cell:  {sboard.highlightedCell}   ")
    scr.addstr(8,38,f"Highlighted block: {sboard.highlightedBlock}   ")
    scr.addstr(9,38,f"Cursor cell:       {sboard.cursorCell}   ")

    curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_WHITE)

    # Plaster the board with the most common numbers grid borders
    for i in range(37):
        for j in range(10):
            scr.addstr(i,j*4,'|')
        for j in range(4):
            scr.addstr(i,j*12,' ', curses.color_pair(1))


    # Add the vertical cell borders
    for i in range(10):
        for j in range(9):
            scr.addstr(i*4,j*4,'+---')
        for j in range(4):
            scr.addstr(i*4,j*12,' ', curses.color_pair(1))

    # Add the four bold vertical ones
    for i in range(4):
        scr.addstr(12*i,0,str(' '*37), curses.color_pair(1))


    # Add the possible
    # Finalized
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
    # Highlighted
    curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_YELLOW)
    # Cursor
    curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_MAGENTA)
    # CursorFinal
    curses.init_pair(5,curses.COLOR_RED,curses.COLOR_MAGENTA)

    for cellRow in range(1,10):
        for cellCol in range(1,10):
            blockrow = 1+ (cellRow-1) // 3
            blockcol = 1+ (cellCol-1) // 3

            # Define upper left corner
            cellx = 1+(cellCol-1)*4
            celly = 1+(cellRow-1)*4

            highlighted = False
            if sboard.highlightedRow == cellRow : highlighted = True
            if sboard.highlightedCol == cellCol : highlighted = True
            if sboard.highlightedCell == (cellRow,cellCol) : highlighted = True
            if sboard.highlightedBlock == (blockrow,blockcol) : highlighted = True

            color = curses.A_DIM
            if highlighted : 
                color = curses.color_pair(3)

            if sboard.cursorCell == (SudokuCoordinate(cellRow,cellCol)):
                color = curses.color_pair(4)

            finalNumber = sboard.getFinal(SudokuCoordinate(cellRow,cellCol))
            if finalNumber != None : 
                x = cellx + 1
                y = celly + 1
                if sboard.cursorCell == (cellRow,cellCol):
                    # Color the background
                    for i in range(3):
                        scr.addstr(y+i-1,x-1,'   ', curses.color_pair(5))
                    # Color the number
                    scr.addstr(y,x,str(finalNumber), curses.color_pair(5))
                else:
                    for i in range(3):
                        scr.addstr(y+i-1,x-1,'   ', curses.color_pair(2))
                    scr.addstr(y,x,str(finalNumber), curses.color_pair(2))
            else:
                for n in range(1,10):
                    x = cellx + (n-1) % 3
                    y = celly + (n-1) // 3
                    if sboard.isPossible(SudokuCoordinate(cellRow,cellCol),n):
                        scr.addstr(y,x,str(n),color)
                    else:
                        scr.addstr(y,x,' ',color)










### TODO: Delete this

def printCell(scr : curses.window):
    # Create the initial grid
    scr.move(0,0)
    scr.addch(curses.ACS_ULCORNER)
    scr.addstr("---")
    scr.addch(curses.ACS_URCORNER)
    scr.addstr(1,0,"|   |")
    scr.addstr(2,0,"|   |")
    scr.addstr(3,0,"|   |")
    scr.move(4,0)
    scr.addch(curses.ACS_LLCORNER)
    scr.addstr("---")
    scr.addch(curses.ACS_LRCORNER)

    # Add the numbers
    scr.addstr(1,1,'123',curses.A_DIM)
    scr.addstr(2,1,'456',curses.A_DIM)
    scr.addstr(3,1,'789',curses.A_DIM)

