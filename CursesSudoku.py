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

cBORDER = 1
cFINALIZED = 2
cHIGHLIGHTED = 3
cCURSOR = 4
cCURSORFINAL = 5
cMESSAGE = 6

def defineColors() :
    # Border
    curses.init_pair(cBORDER,      curses.COLOR_BLUE,curses.COLOR_BLUE)
    # Finalized
    curses.init_pair(cFINALIZED,   curses.COLOR_RED,   curses.COLOR_WHITE)
    # Highlighted
    curses.init_pair(cHIGHLIGHTED, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    # Cursor
    curses.init_pair(cCURSOR,      curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    # CursorFinal
    curses.init_pair(cCURSORFINAL, curses.COLOR_RED,   curses.COLOR_MAGENTA)
    # GUI Message
    curses.init_pair(cMESSAGE,     curses.COLOR_RED,    curses.COLOR_BLACK)

def setMessage(scr : curses.window, message : str) :
    maxLength = curses.COLS - 39
    # Clear the current message
    scr.addstr(20,39,str(' '*maxLength), curses.color_pair(cMESSAGE))
    trunkatedMessage = message
    if len(trunkatedMessage) > maxLength :
        trunkatedMessage = trunkatedMessage[:maxLength]
    scr.addstr(20,39,trunkatedMessage, curses.color_pair(cMESSAGE))


def getHighlight(scr : curses.window, sboard : SudokuBoard) :
    setMessage(scr, "Select number to highlight or space to remove")
    while True :                  
        k = scr.getch()
        if k in range(ord('0'),ord('9')+1):
            x = k - ord('0')
            sboard.highlightedNumber = x
            setMessage(scr,"")
            printGrid(scr, sboard)
            break
        elif k == ord(' ') : 
            setMessage(scr,"")
            sboard.highlightedNumber = None
            printGrid(scr, sboard)
            break
    
    
def finalizeCell(scr : curses.window, sboard : SudokuBoard) :
    if sboard.cursorCell == None :
        setMessage(scr, "Need to select cell with cursor first")
        return
    
    setMessage(scr,"Select number to finalize (<enter> or <space> to abort)")
    while True :
        k = scr.getch()
        if k in range(ord('0'),ord('9')+1):
            x = k - ord('0')
            sboard.setCell(sboard.cursorCell, x)
            setMessage(scr,"")
            printGrid(scr, sboard)
            break
        elif k == curses.KEY_ENTER or k == 10 or k == ord(' ') : 
            setMessage(scr,"")
            break
        

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
    scr.addstr(11,38,f"Press 'c' to toggle cursor")
    scr.addstr(12,38,f"Press 'h' to highlight a specific number")
    scr.addstr(13,38,f"Press <space> to toggle highlighting on current cell")
    scr.addstr(14,38,f"Press 'e' to enter edit mode.")
    scr.addstr(15,38,f"Press <enter> to finalize a cell")
    scr.addstr(16,38,f"Press 'u' to undo finalization of a cell")
    scr.addstr(17,38,f"Press 'p' to toggle possible values")


    # Plaster the board with the most common numbers grid borders
    for i in range(37):
        for j in range(10):
            scr.addstr(i,j*4,'|')
        for j in range(4):
            scr.addstr(i,j*12,' ', curses.color_pair(cBORDER))


    # Add the vertical cell borders
    for i in range(10):
        for j in range(9):
            scr.addstr(i*4,j*4,'+---')
        for j in range(4):
            scr.addstr(i*4,j*12,' ', curses.color_pair(cBORDER))

    # Add the four bold vertical ones
    for i in range(4):
        scr.addstr(12*i,0,str(' '*37), curses.color_pair(cBORDER))


    # Add the possible


    for cellRow in range(1,10):
        for cellCol in range(1,10):
            blockrow = 1+ (cellRow-1) // 3
            blockcol = 1+ (cellCol-1) // 3

            # Define upper left corner
            cellx = 1+(cellCol-1)*4
            celly = 1+(cellRow-1)*4

            highlighted = False
            if sboard.highlightedRow   == cellRow : highlighted = True
            if sboard.highlightedCol   == cellCol : highlighted = True
            if sboard.highlightedCell  == SudokuCoordinate(cellRow,cellCol)   : highlighted = True
            if sboard.highlightedBlock == SudokuCoordinate(blockrow,blockcol) : highlighted = True

            color = curses.A_DIM
            if highlighted : 
                color = curses.color_pair(cHIGHLIGHTED)


            if sboard.cursorCell == (SudokuCoordinate(cellRow,cellCol)):
                color = curses.color_pair(cCURSOR)

            finalNumber = sboard.getFinal(SudokuCoordinate(cellRow,cellCol))
            if finalNumber != None : # This cell is a finalized cell
                x = cellx + 1
                y = celly + 1
                # The cursor is on this cell
                if sboard.cursorCell == SudokuCoordinate(cellRow,cellCol):
                    # Color the background
                    for i in range(3):
                        scr.addstr(y+i-1,x-1,'   ', curses.color_pair(cCURSORFINAL))
                    # Color the number
                    scr.addstr(y,x,str(finalNumber), curses.color_pair(cCURSORFINAL))
                # The cursor is NOT on this cell
                else:
                    finalizedColor = cFINALIZED
                    if finalNumber == sboard.highlightedNumber : finalizedColor = cHIGHLIGHTED

                    for i in range(3):
                        scr.addstr(y+i-1,x-1,'   ', curses.color_pair(finalizedColor))
                    scr.addstr(y,x,str(finalNumber), curses.color_pair(finalizedColor))
            else: # Not finalized - show individual numbers
                cellCoord = SudokuCoordinate(cellRow,cellCol)
                for n in range(1,10):
                    x = cellx + (n-1) % 3
                    y = celly + (n-1) // 3
                    if sboard.isPossible(cellCoord,n):
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

