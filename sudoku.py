"""Efficient Sudoku solver"""

from __future__ import annotations
from collections.abc import Iterator
from time import perf_counter


def key(row: int, col: int) -> str:
    """Encodes a coordinate such as (3,1) with the string 31"""
    return str(row) + str(col)


class Sudoku:
    """Sudoku class"""

    coords = [key(row, col) for row in range(9) for col in range(9)]
    """List of all coordinates, encoded as strings"""

    peers: dict[str, set[str]] = {
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
        values: dict[str, int],
        candidates: dict[str, str] | None = None,
    ) -> None:
        """Initialize Sudoku with a value and a candidate dictionary"""
        self.values = values
        self.has_contradiction = False

        if candidates is None:
            self.candidates = self.get_candidate_board()
        else:
            self.candidates = candidates

    @staticmethod
    def generate_from_board(
        board: list[list[int]],
    ) -> Sudoku:
        """Generates a Sudoku object from a given 2-dimensional list of integers"""
        values = {
            key(row, col): board[row][col] for row in range(9) for col in range(9)
        }
        return Sudoku(values)

    @staticmethod
    def generate_from_string(line: str) -> Sudoku:
        """Generates a Sudoku object from a string as in the samples file"""
        line = line.replace("\n", "")
        assert len(line) == 81

        def to_digit(c: str) -> int:
            return int(c) if c.isnumeric() else 0

        values = {
            key(row, col): to_digit(line[row * 9 + col])
            for row in range(9)
            for col in range(9)
        }
        return Sudoku(values)

    def copy(self) -> Sudoku:
        """Generates a copy of the given Sudoku"""
        return Sudoku(self.values.copy(), self.candidates.copy())

    def __str__(self) -> str:
        """Prints the Sudoku in a nice way to the console"""
        output = " " + "-" * 23 + "\n"
        for row in range(9):
            for col in range(9):
                digit = self.values[key(row, col)]
                if col == 0:
                    output += "| "
                output += (str(digit) if digit > 0 else ".") + " "
                if col % 3 == 2:
                    output += "| "
            output += "\n"
            if row % 3 == 2:
                output += " " + "-" * 23 + "\n"
        output += "\n"
        return output

    def get_candidates(self, coord: str) -> str:
        """Generates the list (encoded as a string) of candidates at a position"""
        digit = self.values[coord]
        if digit != 0:
            return str(digit)
        values_of_peers = {self.values[peer] for peer in Sudoku.peers[coord]}
        return "".join([str(n) for n in range(1, 10) if n not in values_of_peers])

    def get_candidate_board(self) -> dict[str, str]:
        """Returns the dictionary of candidates over all coordinates"""
        return {coord: self.get_candidates(coord) for coord in Sudoku.coords}

    def get_next_coord(self) -> str | None:
        """Returns the free coordinate with the least number of candidates"""
        try:
            return min(
                [coord for coord in Sudoku.coords if self.values[coord] == 0],
                key=lambda coord: len(self.candidates[coord]),
            )
        except:
            return None

    def remove_candidate(self, coord: str, digit: int) -> None:
        """Removes a candidate from a coordinate (in case it's there),
        detects if a contradiction happens, and if a single candidate
        is left this one is set."""
        if str(digit) not in self.candidates[coord]:
            return
        self.candidates[coord] = self.candidates[coord].replace(str(digit), "")
        if not self.candidates[coord]:
            self.has_contradiction = True
        elif len(self.candidates[coord]) == 1:
            self.set_digit(coord, int(self.candidates[coord]))

    def set_digit(self, coord: str, digit: int) -> None:
        """Sets a digit at a given coordinate and removes that digit
        from the candidates of the coordinate's peers"""
        self.values[coord] = digit
        self.candidates[coord] = str(digit)
        for peer in Sudoku.peers[coord]:
            self.remove_candidate(peer, digit)
            if self.has_contradiction:
                return

    def solutions(self) -> Iterator[Sudoku]:
        """Generates solutions of the given Sudoku"""
        coord = self.get_next_coord()
        if not coord:
            yield self
            return
        for num in self.candidates[coord]:
            copy = self.copy()
            copy.set_digit(coord, int(num))
            if not copy.has_contradiction:
                yield from copy.solutions()


def measure_time():
    """Solves all sudoku samples and measures the time"""
    sudoku_counter = 0
    total = 0
    with open("performance.txt", "w", encoding="utf8") as output:
        with open("samples.txt", "r", encoding="utf8") as file:
            for line in file:
                if line.startswith("#"):
                    continue
                sudoku_counter += 1
                sudoku = Sudoku.generate_from_string(line)
                print("solving sudoku", sudoku_counter)
                start = perf_counter()
                list(sudoku.solutions())
                end = perf_counter()
                output.write(str(end - start) + "\n")
                total += end - start
        output.write("total: " + str(total))
    print("results written to performance.txt")


def solve_sample():
    """Prints the solutions of a sample Sudoku"""
    sample = "48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5...."
    sudoku = Sudoku.generate_from_string(sample)
    print("Sample:")
    print(sudoku)
    print("Solutions:")
    start = perf_counter()
    for sol in sudoku.solutions():
        print(sol)
    end = perf_counter()
    print("Elapsed time: ", end - start, "\n")


if __name__ == "__main__":
    solve_sample()
    # measure_time()
