# Sample kenken puzzles, created using http://www.poisonmeatball.com/kenken/
#
# 1. Create a Puzzle at poisonmeatball.com/kenkey/
# 2. Make sure that it can be solved there.
# 3. Use the JSON button to get the puzzle definition
# 4. Paste it here and give it a name.
# 5. Create a new puzzle in the main program
# 6. Give it the puzzle JSON with the set_cells method.
# 7. Solve it!


# From NYT Magazine, 27-Mar-2022
p7_mar2022 = {"width":7,"height":7,"values":[1,2,3,4,5,6,7],"rules":[{"op":"*","value":30,"cells":[{"x":0,"y":0},{"x":0,"y":1}]},{"op":"*","value":84,"cells":[{"x":0,"y":2},{"x":0,"y":3},{"x":0,"y":4}]},{"op":"=","value":1,"cells":[{"x":0,"y":5}]},{"op":"*","value":84,"cells":[{"x":0,"y":6},{"x":1,"y":6},{"x":2,"y":6}]},{"op":"=","value":4,"cells":[{"x":3,"y":6}]},{"op":"*","value":12,"cells":[{"x":4,"y":5},{"x":4,"y":6}]},{"op":"+","value":8,"cells":[{"x":6,"y":5},{"x":5,"y":6},{"x":6,"y":6}]},{"op":"+","value":16,"cells":[{"x":4,"y":4},{"x":5,"y":4},{"x":5,"y":5}]},{"op":"/","value":3,"cells":[{"x":1,"y":4},{"x":1,"y":5}]},{"op":"-","value":4,"cells":[{"x":2,"y":4},{"x":2,"y":5}]},{"op":"+","value":14,"cells":[{"x":3,"y":3},{"x":3,"y":4},{"x":3,"y":5}]},{"op":"-","value":3,"cells":[{"x":1,"y":3},{"x":2,"y":3}]},{"op":"-","value":1,"cells":[{"x":4,"y":3},{"x":5,"y":3}]},{"op":"+","value":8,"cells":[{"x":6,"y":3},{"x":6,"y":4}]},{"op":"-","value":2,"cells":[{"x":6,"y":1},{"x":6,"y":2}]},{"op":"=","value":7,"cells":[{"x":6,"y":0}]},{"op":"/","value":2,"cells":[{"x":4,"y":0},{"x":5,"y":0}]},{"op":"+","value":12,"cells":[{"x":1,"y":0},{"x":2,"y":0},{"x":3,"y":0}]},{"op":"+","value":10,"cells":[{"x":1,"y":1},{"x":2,"y":1}]},{"op":"-","value":4,"cells":[{"x":3,"y":1},{"x":4,"y":1}]},{"op":"-","value":3,"cells":[{"x":5,"y":1},{"x":5,"y":2}]},{"op":"+","value":7,"cells":[{"x":1,"y":2},{"x":2,"y":2}]},{"op":"-","value":6,"cells":[{"x":3,"y":2},{"x":4,"y":2}]}]}

p5_27_mar = {"width":5,"height":5,"values":[1,2,3,4,5],"rules":[{"op":"/","value":2,"cells":[{"x":0,"y":0},{"x":0,"y":1}]},{"op":"+","value":9,"cells":[{"x":0,"y":2},{"x":0,"y":3},{"x":0,"y":4}]},{"op":"*","value":15,"cells":[{"x":1,"y":0},{"x":2,"y":0},{"x":3,"y":0}]},{"op":"*","value":12,"cells":[{"x":4,"y":0},{"x":4,"y":1},{"x":4,"y":2}]},{"op":"+","value":7,"cells":[{"x":4,"y":3},{"x":4,"y":4}]},{"op":"+","value":9,"cells":[{"x":1,"y":4},{"x":2,"y":4}]},{"op":"=","value":3,"cells":[{"x":3,"y":4}]},{"op":"+","value":3,"cells":[{"x":1,"y":3},{"x":2,"y":3}]},{"op":"+","value":12,"cells":[{"x":3,"y":1},{"x":2,"y":2},{"x":3,"y":2},{"x":3,"y":3}]},{"op":"-","value":1,"cells":[{"x":1,"y":1},{"x":2,"y":1}]},{"op":"=","value":4,"cells":[{"x":1,"y":2}]}]}

# 5-Dec-2022: Removing singles and doubles row/col working
puzzle7 = {"width":7,"height":7,"values":[1,2,3,4,5,6,7],"rules":[
    {"op":"+","value":12,"cells":[{"x":0,"y":0},{"x":1,"y":0},{"x":1,"y":1}]},
    {"op":"+","value":11,"cells":[{"x":0,"y":1},{"x":0,"y":2}]},
    {"op":"+","value":7,"cells":[{"x":0,"y":3},{"x":0,"y":4}]},
    {"op":"-","value":3,"cells":[{"x":1,"y":2},{"x":1,"y":3}]},
    {"op":"+","value":12,"cells":[{"x":0,"y":5},{"x":0,"y":6},{"x":1,"y":6}]},
    {"op":"*","value":36,"cells":[{"x":1,"y":4},{"x":2,"y":4},{"x":2,"y":5}]},
    {"op":"=","value":1,"cells":[{"x":1,"y":5}]},
    {"op":"-","value":3,"cells":[{"x":2,"y":6},{"x":3,"y":6}]},
    {"op":"+","value":16,"cells":[{"x":3,"y":4},{"x":4,"y":4},{"x":3,"y":5}]},
    {"op":"=","value":7,"cells":[{"x":4,"y":6}]},
    {"op":"/","value":2,"cells":[{"x":5,"y":6},{"x":6,"y":6}]},
    {"op":"*","value":30,"cells":[{"x":4,"y":5},{"x":5,"y":5},{"x":6,"y":5}]},
    {"op":"*","value":42,"cells":[{"x":5,"y":3},{"x":5,"y":4},{"x":6,"y":4}]},
    {"op":"*","value":35,"cells":[{"x":6,"y":2},{"x":6,"y":3}]},
    {"op":"=","value":4,"cells":[{"x":2,"y":3}]},
    {"op":"*","value":105,"cells":[{"x":2,"y":0},{"x":2,"y":1},{"x":2,"y":2}]},
    {"op":"*","value":108,"cells":[{"x":3,"y":0},{"x":4,"y":0},{"x":5,"y":0},{"x":3,"y":1}]},
    {"op":"+","value":3,"cells":[{"x":3,"y":2},{"x":3,"y":3}]},
    {"op":"+","value":12,"cells":[{"x":4,"y":1},{"x":4,"y":2},{"x":4,"y":3}]},
    {"op":"-","value":3,"cells":[{"x":5,"y":1},{"x":5,"y":2}]},
    {"op":"+","value":5,"cells":[{"x":6,"y":0},{"x":6,"y":1}]}]}

puzzle5 = {"width":5,"height":5,"values":[1,2,3,4,5],"rules":[{"op":"-","value":4,"cells":[{"x":0,"y":0},{"x":1,"y":0}]},{"op":"*","value":12,"cells":[{"x":2,"y":0},{"x":3,"y":0},{"x":3,"y":1}]},{"op":"-","value":1,"cells":[{"x":4,"y":0},{"x":4,"y":1}]},{"op":"/","value":2,"cells":[{"x":0,"y":1},{"x":0,"y":2}]},{"op":"-","value":1,"cells":[{"x":1,"y":1},{"x":1,"y":2}]},{"op":"+","value":9,"cells":[{"x":2,"y":1},{"x":2,"y":2}]},{"op":"=","value":1,"cells":[{"x":3,"y":2}]},{"op":"-","value":4,"cells":[{"x":4,"y":2},{"x":4,"y":3}]},{"op":"+","value":11,"cells":[{"x":3,"y":3},{"x":3,"y":4},{"x":4,"y":4}]},{"op":"=","value":4,"cells":[{"x":0,"y":3}]},{"op":"-","value":2,"cells":[{"x":0,"y":4},{"x":1,"y":4}]},{"op":"-","value":1,"cells":[{"x":1,"y":3},{"x":2,"y":3}]},{"op":"=","value":1,"cells":[{"x":2,"y":4}]}]}

# http://www.kenkenpuzzle.com/game, puzzle 201886
puzzle9 = {"width":9,"height":9,"values":[1,2,3,4,5,6,7,8,9],"rules":[{"op":"/","value":3,"cells":[{"x":0,"y":0},{"x":0,"y":1}]},{"op":"-","value":4,"cells":[{"x":1,"y":0},{"x":2,"y":0}]},{"op":"-","value":5,"cells":[{"x":1,"y":1},{"x":2,"y":1}]},{"op":"*","value":336,"cells":[{"x":3,"y":0},{"x":4,"y":0},{"x":5,"y":0}]},{"op":"+","value":3,"cells":[{"x":6,"y":0},{"x":7,"y":0}]},{"op":"+","value":15,"cells":[{"x":8,"y":0},{"x":7,"y":1},{"x":8,"y":1},{"x":8,"y":2}]},{"op":"-","value":1,"cells":[{"x":5,"y":1},{"x":6,"y":1}]},{"op":"-","value":3,"cells":[{"x":3,"y":1},{"x":4,"y":1}]},{"op":"-","value":2,"cells":[{"x":0,"y":2},{"x":1,"y":2}]},{"op":"-","value":2,"cells":[{"x":2,"y":2},{"x":3,"y":2}]},{"op":"+","value":17,"cells":[{"x":4,"y":2},{"x":4,"y":3}]},{"op":"*","value":6,"cells":[{"x":5,"y":2},{"x":5,"y":3}]},{"op":"-","value":8,"cells":[{"x":6,"y":2},{"x":6,"y":3}]},{"op":"-","value":2,"cells":[{"x":7,"y":2},{"x":7,"y":3}]},{"op":"+","value":15,"cells":[{"x":8,"y":3},{"x":8,"y":4},{"x":8,"y":5}]},{"op":"*","value":405,"cells":[{"x":8,"y":6},{"x":7,"y":7},{"x":8,"y":7},{"x":8,"y":8}]},{"op":"*","value":56,"cells":[{"x":5,"y":7},{"x":6,"y":7}]},{"op":"-","value":2,"cells":[{"x":6,"y":8},{"x":7,"y":8}]},{"op":"+","value":14,"cells":[{"x":3,"y":8},{"x":4,"y":8},{"x":5,"y":8}]},{"op":"/","value":3,"cells":[{"x":1,"y":8},{"x":2,"y":8}]},{"op":"-","value":4,"cells":[{"x":0,"y":7},{"x":0,"y":8}]},{"op":"-","value":1,"cells":[{"x":0,"y":6},{"x":1,"y":6}]},{"op":"-","value":8,"cells":[{"x":1,"y":7},{"x":2,"y":7}]},{"op":"/","value":3,"cells":[{"x":3,"y":7},{"x":4,"y":7}]},{"op":"/","value":2,"cells":[{"x":2,"y":6},{"x":3,"y":6}]},{"op":"/","value":2,"cells":[{"x":4,"y":5},{"x":4,"y":6}]},{"op":"/","value":4,"cells":[{"x":5,"y":5},{"x":5,"y":6}]},{"op":"-","value":5,"cells":[{"x":6,"y":5},{"x":6,"y":6}]},{"op":"-","value":3,"cells":[{"x":7,"y":5},{"x":7,"y":6}]},{"op":"-","value":5,"cells":[{"x":6,"y":4},{"x":7,"y":4}]},{"op":"+","value":12,"cells":[{"x":4,"y":4},{"x":5,"y":4}]},{"op":"+","value":13,"cells":[{"x":3,"y":3},{"x":3,"y":4},{"x":3,"y":5}]},{"op":"*","value":72,"cells":[{"x":2,"y":3},{"x":2,"y":4},{"x":2,"y":5}]},{"op":"*","value":80,"cells":[{"x":1,"y":3},{"x":1,"y":4},{"x":1,"y":5}]},{"op":"+","value":13,"cells":[{"x":0,"y":3},{"x":0,"y":4},{"x":0,"y":5}]}]}