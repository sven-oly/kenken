# kenken
A Python solver for KenKen using rules and patterns

To use this:
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
