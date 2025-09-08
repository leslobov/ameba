from torch.types import Number


class Position:

    @staticmethod
    def move_according_prediction(neural_network_prediction: Number) -> "Position":
        if neural_network_prediction == 0:
            return Position(0, 1)
        elif neural_network_prediction == 1:
            return Position(1, 0)
        elif neural_network_prediction == 2:
            return Position(0, -1)
        elif neural_network_prediction == 3:
            return Position(-1, 0)
        else:
            raise ValueError("Invalid neural network prediction")

    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def adjust_position(self, rows: int, columns: int):
        if self.row < 0:
            self.row += rows
        elif self.row >= rows:
            self.row -= rows
        if self.column < 0:
            self.column += columns
        elif self.column >= columns:
            self.column -= columns

    def __add__(self, other: "Position") -> "Position":
        if not isinstance(other, Position):
            raise TypeError("Operand must be of type Position")
        return Position(self.row + other.row, self.column + other.column)
