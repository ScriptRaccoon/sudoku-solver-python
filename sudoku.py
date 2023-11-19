"""Efficient Sudoku solver"""

from __future__ import annotations
from collections.abc import Iterator
from time import perf_counter

import samples


def key(row: int, col: int) -> str:
    """Encode coordinates such as (3,1) with the string 31"""
    return f"{row}{col}"


class Sudoku:
    """Sudoku class"""

    peer_dict: dict[str, set[tuple[int, int]]] = {
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
    """Dictionary of peers of a coordinate: those in the same row, column or block"""

    def __init__(
        self,
        value_dict: dict[str, int],
        candidate_dict: dict[str, str] | None = None,
    ) -> None:
        """Initialize Sudoku with a value and a candidate dictionary"""
        self.value_dict = value_dict
        self.coords = value_dict.keys()
        self.has_contradiction = False

        if candidate_dict is None:
            self.candidate_dict = self.get_candidate_board()
        else:
            self.candidate_dict = candidate_dict

    @staticmethod
    def generate_from_board(
        board: list[list[int]],
    ) -> Sudoku:
        """Generates a Sudoku object from a given 2-dimensional list of integers"""
        value_dict = {
            key(row, col): board[row][col] for row in range(9) for col in range(9)
        }
        return Sudoku(value_dict, None)

    def copy(self) -> Sudoku:
        """Generates a copy of the given Sudoku"""
        return Sudoku(self.value_dict.copy(), self.candidate_dict.copy())

    def print(self) -> None:
        """Prints the Sudoku in a nice way to the console"""
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

    def candidates(self, _key: str) -> str:
        """Generates the list (encoded as a string) of candidates at a position"""
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
        """Returns the dictionary of candidates over all coordinates"""
        return {coord: self.candidates(coord) for coord in self.coords}

    def get_next_coord(self) -> str | None:
        """Returns the open coordinate with the least number of candidates"""

        candidate_list = [
            (coord, len(self.candidate_dict[coord]))
            for coord in self.coords
            if self.value_dict[coord] == 0
        ]

        if not candidate_list:
            return None
        return min(candidate_list, key=lambda x: x[1])[0]

    def remove_candidate(self, coord: str, num: int) -> None:
        """Removes a candidate from a coordinate (in case it's there),
        detects if a contradiction happens, and if a single candidate
        is left this one is set."""
        if str(num) not in self.candidate_dict[coord]:
            return
        self.candidate_dict[coord] = self.candidate_dict[coord].replace(str(num), "")
        if len(self.candidate_dict[coord]) == 0:
            self.has_contradiction = True
        elif len(self.candidate_dict[coord]) == 1:
            unique_candidate = int(self.candidate_dict[coord])
            self.set_number(coord, unique_candidate)

    def set_number(self, coord: str, num: int) -> None:
        """Sets a number at a given coordinate (via its key), and removes
        that number from the candidates of the coordinate's peers"""
        self.value_dict[coord] = num
        self.candidate_dict[coord] = str(num)
        for peer in Sudoku.peer_dict[coord]:
            self.remove_candidate(peer, num)
            if self.has_contradiction:
                return

    def solutions(self) -> Iterator[Sudoku]:
        """Generates solutions of the given Sudoku"""
        coord = self.get_next_coord()
        if not coord:
            yield self
            return

        for num in self.candidate_dict[coord]:
            copy = self.copy()
            copy.set_number(coord, int(num))
            if not copy.has_contradiction:
                yield from copy.solutions()


def main():
    """Prints the solutions of a sample Sudoku"""
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
