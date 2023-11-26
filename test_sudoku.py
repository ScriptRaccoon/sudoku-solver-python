"""Tests for Sudoku class"""
from sudoku import Sudoku, coords, peers, all_units

# pylint: disable=line-too-long, missing-function-docstring


def test_coords():
    assert isinstance(coords, set)
    assert len(coords) == 81
    assert "25" in coords
    assert "89" not in coords
    for coord in coords:
        assert isinstance(coord, str)
        assert len(coord) == 2


def test_units():
    assert len(all_units) == 27
    assert isinstance(all_units, list)
    row_unit = {"00", "01", "02", "03", "04", "05", "06", "07", "08"}
    assert row_unit in all_units
    for unit in all_units:
        assert isinstance(unit, set)
        assert len(unit) == 9


def test_peers():
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


def test_sample():
    sample_sudo = "48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5...."
    correct_sol = "487312695593684271126597384735849162914265837268731549851476923379128456642953718"
    sudoku = Sudoku.generate_from_string(sample_sudo)
    sols = list(sudoku.solutions())
    assert len(sols) == 1
    sol = sols[0]
    assert sol.to_line() == correct_sol


def test_several_sols():
    sample_sudok = "....5.2......479..1.5.6.8..246......3.7...4.6......753..9.8.5....821......4.7...."
    one_solution = "493158267862347915175962834246735198357891426981426753719683542538214679624579381"
    sudoku = Sudoku.generate_from_string(sample_sudok)
    sols = list(sudoku.solutions())
    assert len(sols) == 6
    assert any(sol.to_line() == one_solution for sol in sols)
