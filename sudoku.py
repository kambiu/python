import argparse


class SudokuPuzzle:
    def __init__(self):
        self.rows = []
        self.columns = []
        self.area = []

    def get_classic_area(self):
        x = self.row_idx % 3
        y = self.col_idx % 3

        return str(x) + str(y)


class Squares:
    def __init__(self, row, col, value=0):
        self.row_idx = row
        self.col_idx = col
        self.value = value
        self.area = None


def solve_puzzle():
    return

if __name__ == "__main__":
    solve_puzzle()