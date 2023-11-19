from __future__ import annotations
from collections.abc import Iterator
from copy import deepcopy
from time import perf_counter

import samples


class Sudoku:
    def __init__(
        self,
        board: list[list[int]],
        candidate_board: list[list[list[int]]] | None = None,
        debug: bool = False,
    ) -> None:
        self.board = board
        self.has_contradiction = False
        self.debug = debug

        if candidate_board is None:
            self.candidate_board = self.get_candidate_board()
        else:
            self.candidate_board = candidate_board

    def copy(self) -> Sudoku:
        return Sudoku(deepcopy(self.board), deepcopy(self.candidate_board), self.debug)

    def print(self) -> None:
        print(" " + "-" * 23)
        for row in range(9):
            for col in range(9):
                num = self.board[row][col]
                if col == 0:
                    print("| ", end="")
                print(num if num > 0 else ".", end="")
                print(" ", end="")
                if col % 3 == 2:
                    print("| ", end="")
            print()
            if row % 3 == 2:
                print(" " + "-" * 23)
        print()

    def candidates(self, row: int, col: int) -> list[int]:
        num = self.board[row][col]
        if num != 0:
            return [num]
        row_values = self.board[row]
        col_values = [self.board[i][col] for i in range(9)]
        row_start = 3 * (row // 3)
        col_start = 3 * (col // 3)
        block_values = [
            self.board[i][j]
            for i in range(row_start, row_start + 3)
            for j in range(col_start, col_start + 3)
        ]
        return [
            n for n in range(1, 10) if n not in row_values + col_values + block_values
        ]

    def get_candidate_board(self) -> list[list[list[int]]]:
        return [[self.candidates(row, col) for col in range(9)] for row in range(9)]

    def get_next_coord(self) -> tuple[int, int] | None:
        candidate_list = [
            (row, col, self.candidate_board[row][col])
            for row in range(9)
            for col in range(9)
            if self.board[row][col] == 0
        ]
        if len(candidate_list) == 0:
            return None
        coord_with_count = min(candidate_list, key=lambda x: len(x[2]))
        coord = coord_with_count[:2]
        if self.debug:
            print(f"try {coord} with the candidates {coord_with_count[2]}")

        return coord

    def remove_candidate(self, row: int, col: int, num: int) -> None:
        if num not in self.candidate_board[row][col]:
            return
        if self.debug:
            print(f"remove candidate {num} from {(row,col)}")
        self.candidate_board[row][col].remove(num)
        if len(self.candidate_board[row][col]) == 0:
            if self.debug:
                print(f"found a contradiction in {(row,col)}, will backtrack")
            self.has_contradiction = True
        elif len(self.candidate_board[row][col]) == 1:
            if self.debug:
                print(f"just one candidate left in {(row,col)}")
            unique_candidate = self.candidate_board[row][col][0]
            self.set_number(row, col, unique_candidate)

    def set_number(self, row: int, col: int, num: int) -> None:
        if self.debug:
            print(f"in {(row,col)} we try to set {num}")
        self.board[row][col] = num
        self.candidate_board[row][col] = [num]
        for i in range(9):
            if i != col:
                self.remove_candidate(row, i, num)
                if self.has_contradiction:
                    return
            if i != row:
                self.remove_candidate(i, col, num)
                if self.has_contradiction:
                    return
        row_start = 3 * (row // 3)
        col_start = 3 * (col // 3)
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                if i != row or j != col:
                    self.remove_candidate(i, j, num)
                    if self.has_contradiction:
                        return

    def solutions(self) -> Iterator[Sudoku]:
        coord = self.get_next_coord()
        if coord is None:
            if self.debug:
                print("found a solution")
            yield self
            return
        row, col = coord
        for num in self.candidate_board[row][col]:
            copy = self.copy()
            copy.set_number(row, col, num)
            if not copy.has_contradiction:
                yield from copy.solutions()


def main():
    sudoku = Sudoku(samples.hard_sudoku, debug=False)
    sudoku.print()

    counter = 0
    start = perf_counter()
    sols = sudoku.solutions()

    for sol in sols:
        sol.print()
        counter += 1

    end = perf_counter()
    print(f"Found {counter} solutions")
    print("Elapsed time: ", end - start)


if __name__ == "__main__":
    main()
