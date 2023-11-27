# Solving Sudokus using constraint programming

This is an efficient Sudoku solving algorithm using constraint programming. It is very much inspired by (but different from) Peter Norvig's [Solving Every Sudoku Puzzle](https://norvig.com/sudoku.html). It generates quickly all solutions to a given Sudoku (usually in less than 100ms).

The basic idea is to keep track of all the candidates (possible digits) which can go into a square which is not filled yet. When only one candidate is left, place it (this is called a _naked single_). Otherwise, find a square which has the least number of candidates (in practice, that number is usually 1 or 2) and try them one after another. Every time a digit is set, it is removed as a candidate from all of its peers - these are the squares that are in the same unit (row, column or box). Recursively apply this procedure until all squares are filled.

<video alt="Visualization of the algorithm" src="assets/algo.mp4" controls></video>

The solver produces a _generator_ containing all solutions. When a contradiction has been found (that is, 0 candidates were left in a square), we do not require backtracking explicitly: it just means that the current search branch did not yield any new solution, and we just continue with the next one.

To make the algorithm even faster, the _hidden single_ strategy has been implemented. A hidden single is a digit which can only go in one square of a unit. In this case, the square is filled with that digit and we continue. Other solving strategies, which are commonly used in manual Sudoku solving, will probably speed up the algorithm even more, but given that the algorithm is already so fast, it doesn't seem to be necessary to implement them.

In the code, we have used type hints and docstrings to clarify the purpose of each function.

-   `sudoku.py` has the Sudoku class with several methods, including the `solutions` generator
-   `test_sudoku.py` is the corresponding test file which can be executed with `pytest`
-   `samples.txt` is a list of 95 hard Sudokus (the same ones Peter Norvig used)
-   `solutions.txt` is the list of their solutions (generated by the solver)
-   `performance.txt` records information how long it took (on my machine) to solve the samples