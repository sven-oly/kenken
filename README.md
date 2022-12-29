# kenken
This is a Python solver for KenKen using rules and patterns. It starts with a set of possible values for each cell, then applies the constraints for each cage of cells and also uses the Kenken rule of no duplicates any row and column.

Using this approach, even large puzzles can be be processed quickly without trying every possible value in every cell.

##  To use this solve:
1. Pick a puzzle to solve. Note that http://www.kenkenpuzzle.com/game is a good source of
   new puzzles.

2. Go to http://www.poisonmeatball.com/kenken/ to create a visual version of this puzzle.

3. After the puzzle is entered with all the cages and operators and values, touch "JSON"
   to show the JSON code for the puzzle. Copy that data into the clipboard.
   
   * Note: you may use the poisonmeatball solver with the puzzle to be sure that it does have
     a solution. However, that solver does not give any details about its process.

4. Edit the file kk_puzzles.py and create a new variable name. Paste the clipboard contents to
   set the variable to the JSON data.

5. Edit the main function in kenken.py to create a new Puzzle object with that JSON data.

6. Run the main program with "python3 kenken.py"

7. Watch the steps of solving the puzzle.

Note that this solver may not find a solution to all puzzles. If this is the case, please
add an Issue with the JSON data.

Also feel free to comment or make suggestions on improving the solver and its operation.

Have fun!

## How does this solver work?

This python kenken solver uses four basic ideas to reduce the possible values for each cell in the puzzle.

A. First, a set of possible values are created for each cage of cells as they are added to the puzzle. The size of the puzzle matrix determines the maximumum possible value.

* For multiplication, the possible factors for the cage's value are computed. For example, if the cell values produce 12, the possible values are the factors of 12 including 1, 2, 3, 4, and 6 (for a puzzle of size 6 or more.)

* For addition, possible values that could possibly add to the sum are allowed. For a sum of 5, initial values are 1, 2, 3, and 4.

* For subtraction and division, the program computes pairs of values that could give the difference of the quotient indicated in two cells.

* When a single cell is given a value, that number is used as the only possible.

B. Collect the cells in each row that have the same set of possible values. If the same N values are found in N cells in that row, then those values can be removed from all other cells in that row.

* For example, if two cells in a row each have the possible values {1, 2}, then 1 and 2 are removed from the other cells in that row.

* The simplest case is when one item in a row has just one possible value, which is then removed from all other cells in that row.

* Similarly, when three cells contain the same triple such as {1, 4, 6}, then 1, 4, and 6 can be removed from the other rows.

* Note that the same can be done for 4 cells with the same 4 values, 5 cells with 5 values, etc., but these situations do not occur often.

* Perform the same operation with all the columns of the matrix.

C. For each cage of cells, apply its math rule, considering the number of cells and the needed result.

* For each cell in the cage, first compute all possible combinations of the values in other cells in the cage.

* Then each possible value I in the cell is combined with the possibles. If the expected value can be computed with I and the other values, then I is kept as a possible value. If value I can't be used to get the expected value, then value I is removed from the set of possibles.

D. Apply steps B. and C. until no more changes are made to any cell. A this point, the matrix may be solved.

However, for many larger puzzles, this process with not completely solve the puzzle. In that case, one more method is applied.

### Picking one possible value for a cell with 2 possibilities
When the process described above doesn't reduce all cells to just one value, the program applies a guessing method.

* For each cell that has only two possible values, pick one of those values V.

* Copy the entire existing solution, but set that 2-value cell to this value V.

* Then apply steps B. and C. above until one of the following occurs:
  * The puzzle is solved, with only one value in every cell.
  * The puzzle doesn't reduce more and it is not solved, with 1 or more possible values for each cell.
  * Applying either B. or C. removes the last value in a cell. This shows that the guess was incorrect.
  
* If the puzzle is not solved, try the next possible value for that 2-cell and repeat the process.

* If this 2-cell's possibles don't solve the puzzle, try again with the values in a different 2-cell.

* Repeat with all the 2-cells until solved or no more progress can be made.

  * Note: a similar guessing method could be tried for each of the 3 values in triple-value cells. This is not yet implemented, however.
  
# Regression testing
The file kk_puzzles.py contains a list of puzzles from several sources of size 5, 7, and 9. These are all known to be solvable with this method, and may be used as tests to detect if changes to kenken.py break the solver.

To use the testing:
* On the command line, type
```` python3 kenkey_test.py````

* Verify that all the tests pass.
