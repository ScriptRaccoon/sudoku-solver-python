from __future__ import annotations
from collections.abc import Iterator
from time import perf_counter

import samples


def key(row: int, col: int) -> str:
    return f"{row}{col}"


class Sudoku:
    peer_dict = {
        key(row, col): set.union(
            {key(i, col) for i in range(9) if i != row},
            {key(row, j) for j in range(9) if j != col},
            {
                key(3 * (row // 3) + i, 3 * (col // 3) + j)
                for i in range(3)
                for j in range(3)
                if 3 * (row // 3) + i != row or 3 * (col // 3) + j != col
            },
        )
        for row in range(9)
        for col in range(9)
    }

    def __init__(
        self,
        value_dict: dict[str, int],
        candidate_dict: dict[str, str] | None = None,
    ) -> None:
        self.value_dict = value_dict
        self.has_contradiction = False

        if candidate_dict is None:
            self.candidate_dict = self.get_candidate_board()
        else:
            self.candidate_dict = candidate_dict

    @staticmethod
    def generate_from_board(
        board: list[list[int]],
    ) -> Sudoku:
        value_dict = {
            key(row, col): board[row][col] for row in range(9) for col in range(9)
        }
        return Sudoku(value_dict, None)

    def copy(self) -> Sudoku:
        return Sudoku(self.value_dict.copy(), self.candidate_dict.copy())

    def print(self) -> None:
        print(" " + "-" * 23)
        for row in range(9):
            for col in range(9):
                num = self.value_dict[key(row, col)]
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

    def candidates(self, row: int, col: int) -> str:
        _key = key(row, col)
        num = self.value_dict[_key]
        if num != 0:
            return str(num)
        values_of_peers = {self.value_dict[peer] for peer in Sudoku.peer_dict[_key]}
        result = ""
        for n in range(1, 10):
            if n not in values_of_peers:
                result += str(n)
        return result

    def get_candidate_board(self) -> dict[str, str]:
        return {
            key(row, col): self.candidates(row, col)
            for row in range(9)
            for col in range(9)
        }

    def get_next_coord(self) -> tuple[int, int] | None:
        candidate_list = [
            (row, col, self.candidate_dict[key(row, col)])
            for row in range(9)
            for col in range(9)
            if self.value_dict[key(row, col)] == 0
        ]
        if len(candidate_list) == 0:
            return None
        coord_with_count = min(candidate_list, key=lambda x: len(x[2]))
        return coord_with_count[:2]

    def remove_candidate(self, row: int, col: int, num: int) -> None:
        _key = key(row, col)
        if str(num) not in self.candidate_dict[_key]:
            return
        self.candidate_dict[_key] = self.candidate_dict[_key].replace(str(num), "")
        if len(self.candidate_dict[_key]) == 0:
            self.has_contradiction = True
        elif len(self.candidate_dict[_key]) == 1:
            unique_candidate = int(self.candidate_dict[_key])
            self.set_number(row, col, unique_candidate)

    def set_number(self, row: int, col: int, num: int) -> None:
        _key = key(row, col)
        self.value_dict[_key] = num
        self.candidate_dict[_key] = str(num)
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
            yield self
            return
        row, col = coord
        for num in self.candidate_dict[key(row, col)]:
            copy = self.copy()
            copy.set_number(row, col, int(num))
            if not copy.has_contradiction:
                yield from copy.solutions()


def main():
    sudoku = Sudoku.generate_from_board(samples.hard_sudoku)
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
