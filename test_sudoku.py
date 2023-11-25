"""Tests for Sudoku class"""
from sudoku import Sudoku

# pylint: disable=line-too-long, missing-function-docstring


def test_sample():
    sample_sudo = "48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5...."
    correct_sol = "487312695593684271126597384735849162914265837268731549851476923379128456642953718"
    sudoku = Sudoku.generate_from_string(sample_sudo)
    sols = list(sudoku.solutions())
    assert len(sols) == 1
    sol = sols[0]
    assert sol.to_line() == correct_sol
