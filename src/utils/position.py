class Position:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def adjust_position(self, rows: int, columns: int):
        if self.row < 0:
            self.row += rows
        if self.column < 0:
            self.column += columns
