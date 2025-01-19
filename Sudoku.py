


class SudokuCell:

    def __init__(self):
        self.validNumbers = set(list(range(1,10))) 
        self.finalNumber = None

    def __str__(self):
        return f"SudokuCell{self.validNumbers}"

    def getValidNumbers(self) -> set[int] :
        return self.validNumbers
    
    def removeNumber(self, number : int) :
        self.validNumbers.discard(number)

    def removeNumbers(self, numbers : list) :
        for number in numbers : self.removeNumber(number)

    def isDone(self) -> bool :
        return len(self.validNumbers) == 1
    
    def setNumber(self, number : int) :
        self.validNumbers = set([number])
        self.finalNumber = number

    def isFinal(self) :
        return not self.finalNumber == None
    
    def getFinalNumber(self) :
        return self.finalNumber
    
    def contains(self, number) :
        return number in self.validNumbers

    
class SudokuCoordinate:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def __str__(self):
        return f"[{self.row},{self.col}]"
    
    # Define __eq__ so that we can compare two coordinates
    def __eq__(self, other):
        if not isinstance(other,SudokuCoordinate) :
            # Don't attempt to compare unrelated types
            return NotImplemented
        return self.row == other.row and self.col == other.col

    def moveUp(self)    : self.row = max(1,self.row-1)
    def moveDown(self)  : self.row = min(9,self.row+1)
    def moveLeft(self)  : self.col = max(1,self.col-1)
    def moveRight(self) : self.col = min(9,self.col+1)

    
class SudokuBoard:
    def __init__(self):
        self.cells : list[list[SudokuCell]] = []
        for _ in range(9): # Row
            row = []
            for _ in range(9): # Col
                c = SudokuCell()
                row.append(c)
            self.cells.append(row)
            row = None
        
        # Keep track of highlights and cursors
        self.highlightedRow = None #5
        self.highlightedCol = None #9
        self.highlightedCell = None #(1,3)
        self.highlightedBlock = SudokuCoordinate(2,2)
        self.cursorCell = SudokuCoordinate(5,5)


    def getCell(self,c : SudokuCoordinate) -> SudokuCell :
        return self.cells[c.row-1][c.col-1]
    
    def getRow(self, coord : SudokuCoordinate) -> list[SudokuCell] :
        return self.cells[coord.row-1]
    
    def getColumn(self, coord : SudokuCoordinate) -> list[SudokuCell] :
        return [row[coord.col-1] for row in self.cells]

    def setCell(self, coord : SudokuCoordinate, number) :
        
        # First, remove all instances in the row
        for c in self.getRow(coord) :
            c.removeNumber(number)

        # Second, remove all instances in the column
        for c in self.getColumn(coord) :
            c.removeNumber(number)

        # Third, remove all instances in the box
        for row in range(3*((coord.row-1)//3),3*(1+(coord.row-1)//3)):
            for col in range(3*((coord.col-1)//3),3*(1+(coord.col-1)//3)):
                self.cells[row][col].removeNumber(number)
        
        # Finally, clear out all other values
        self.getCell(coord).setNumber(number)
        
    def getOtherRowPossibilities(self, coord : SudokuCoordinate) -> set[int] :
        s = set()
        for c in range(coord.row-1) :
            if c == coord.col-1 : continue
            s = s.union(self.cells[coord.row-1][c])
        return s

    def getFinal(self, c : SudokuCoordinate) :
        cell = self.getCell(c)
        return cell.getFinalNumber()
    
    def isPossible(self, c : SudokuCoordinate, number : int) : 
        cell = self.getCell(c)
        return number in cell.getValidNumbers()

        
    