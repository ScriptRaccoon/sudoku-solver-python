"""Tests for Sudoku class"""
from sudoku import (
    Sudoku,
    key,
    coords,
    peers,
    all_units,
    row_units,
    col_units,
    box_units,
)

# pylint: disable=line-too-long, missing-function-docstring


def test_key():
    assert key(2, 3) == "23"
    assert key(0, 8) == "08"


def test_coords():
    assert isinstance(coords, set)
    assert len(coords) == 81
    assert "25" in coords
    assert "89" not in coords
    for coord in coords:
        assert isinstance(coord, str)
        assert len(coord) == 2


def test_units():
    assert isinstance(all_units, list)
    assert len(all_units) == 9 + 9 + 9  # 9 rows, 9 columns, 9 boxes
    row_unit = {"00", "01", "02", "03", "04", "05", "06", "07", "08"}
    assert row_unit in row_units
    col_unit = {"01", "11", "21", "31", "41", "51", "61", "71", "81"}
    assert col_unit in col_units
    box_unit = {"00", "01", "02", "10", "11", "12", "20", "21", "22"}
    assert box_unit in box_units
    for unit in all_units:
        assert isinstance(unit, set)
        assert len(unit) == 9


def test_peers():
    assert isinstance(peers, dict)
    for coord, peers_of_coord in peers.items():
        assert isinstance(peers_of_coord, set)
        assert len(peers_of_coord) == 20
        assert coord not in peers_of_coord
        for peer in peers_of_coord:
            assert isinstance(peer, str)
            assert len(peer) == 2
    assert peers["00"] == {
        "22",
        "06",
        "30",
        "40",
        "60",
        "01",
        "12",
        "10",
        "50",
        "02",
        "20",
        "04",
        "08",
        "07",
        "80",
        "70",
        "05",
        "21",
        "03",
        "11",
    }


def test_string_generation():
    string = "48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5...."
    sudoku = Sudoku.generate_from_string(string)
    assert sudoku.values["00"] == 4
    assert sudoku.values["01"] == 8
    assert sudoku.values["88"] == 0


def test_board_generation():
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    sudoku = Sudoku.generate_from_board(board)
    assert sudoku.values["00"] == 5
    assert sudoku.values["88"] == 9


def test_candidates():
    sample = "48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5...."
    sudoku = Sudoku.generate_from_string(sample)
    candidates = sudoku.candidates
    assert isinstance(candidates, dict)
    assert candidates["00"] == {4}
    assert candidates["02"] == {6, 7, 9}
    assert candidates["34"] == {1, 3, 4, 8, 9}


def test_printing():
    sample = "48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5...."
    sudoku = Sudoku.generate_from_string(sample)
    assert (
        str(sudoku)
        == " -----------------------\n"
        + "| 4 8 . | 3 . . | . . . | \n"
        + "| . . . | . . . | . 7 1 | \n"
        + "| . 2 . | . . . | . . . | \n"
        + " -----------------------\n"
        + "| 7 . 5 | . . . | . 6 . | \n"
        + "| . . . | 2 . . | 8 . . | \n"
        + "| . . . | . . . | . . . | \n"
        + " -----------------------\n"
        + "| . . 1 | . 7 6 | . . . | \n"
        + "| 3 . . | . . . | 4 . . | \n"
        + "| . . . | . 5 . | . . . | \n"
        + " -----------------------\n"
    )


def test_solving_algorithm():
    sample = "48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5...."
    soluti = "487312695593684271126597384735849162914265837268731549851476923379128456642953718"
    sudoku = Sudoku.generate_from_string(sample)
    sols = list(sudoku.solutions())
    assert len(sols) == 1
    sol = sols[0]
    assert sol.to_line() == soluti


def test_several_solutions():
    sample = "....5.2......479..1.5.6.8..246......3.7...4.6......753..9.8.5....821......4.7...."
    soluti = "493158267862347915175962834246735198357891426981426753719683542538214679624579381"
    sudoku = Sudoku.generate_from_string(sample)
    sols = list(sudoku.solutions())
    assert len(sols) == 6
    assert any(sol.to_line() == soluti for sol in sols)
