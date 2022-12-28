# Create with http://www.poisonmeatball.com/kenken/

# 22-Dec-2022: Got this working for 7x7 puzzles, guessing
# from 2-possibles cells as needed.

# TODO:
# 1. Document better
# 2. Remove obsolete code
# 3. Improve it, combining row/column code as possible
# 4. DONE: Add methods to handle things like [235, 235, 23] hidden_triples and
#    hidden quads.q
# 5. Add options to output each reduction.

# cwcornelius@gmail.com

import kk_puzzles

import copy
import functools
import itertools
import math
import operator

# https://stackoverflow.com/questions/798854/all-combinations-of-a-list-of-lists
# https://tutorial.eyehunts.com/python/python-product-of-list-example-code/
# https://docs.python.org/3/library/operator.html

operator_map = {'+': operator.add,
                '*': operator.mul,
                '-': operator.sub,
                '/': operator.truediv,
                '=': operator.is_,
                }


def factor_n(val, max_val, num_cells=2):
    # For multiply cage, return set of all possible factors in num_cells.
    # TODO: Consider number of cells
    factors = set()
    for f in range(1, max_val+1):
        div = val % f
        if div == 0:
            factors.add(f)
    root = math.sqrt(val)
    if num_cells == 2 and root in factors:
        # Special case - it can't be the square root
        factors.remove(root)
    return set(factors)


def add_possibles(val, max_val, num_cells):
    # What values can add the total in N cells
    # TODO: Consider number of cells
    top = min(val - 1, max_val)  # Need to consider # cells
    possibles = set([n for n in range(1, top + 1)])
    if num_cells == 2 and val % 2 == 0:
        # Special case
        possibles.remove(val // 2)
    return possibles


def sub_possibles(val, max_val):
    result = set()
    for n in range(max_val + 1):
        if (n - val) > 0:
            result.add(n)
            result.add(n - val)
    return result


def div_possibles(val, max_val):
    result = set()
    for n in range(1, max_val + 1):
        if n % val == 0:
            result.add(n)
            result.add(n // val)
    return result


def start_cell_values(num_cells, op, val, max_val):
    if op == "*":
        nums = factor_n(val, max_val, num_cells)
    elif op == "+":
        nums = add_possibles(val, max_val, num_cells)
    elif op == "-":
        nums = sub_possibles(val, max_val)
    elif op == "/":
        nums = div_possibles(val, max_val)
    else:
        nums = set([val])
    return nums


class LastRemovedError(BaseException):
    pass
    

class Cell:
    # Stores information about a single cell of the grid
    def __init__(self, position, cell_cage):
        self.position = position
        self.cage = cell_cage
        self.possibles = set()


class Cage:
    # A container for a set of cells with an operator and a value
    # from that operator on the values
    def __init__(self, op, value, cell_data, grid_size, cage_num=-1):
        self.op = op
        self.index = cage_num
        self.value = value
        self.cells = cell_data
        self.cell_list = []
        self.max = grid_size
        self.linear = False
        self.set_up_cell_list(cell_data)
        self.debug = 1
        self.operator = operator_map[op]
        self.is_linear()

    def is_combo_linear(self, cell_list):
        # Check if the cells in this set are in a line.
        return self.is_linear(cells_to_check=cell_list)

    def combos_of_possibles(self, cell_list):
        # Compute the combinations of the possible values in these cells
        list_of_possibles = []
        combos_raw = []
        for cell in cell_list:
            list_of_possibles.append(cell.possibles)
            combos_raw = list(itertools.product(*list_of_possibles))
        combos = []

        if self.is_combo_linear(cell_list):
            # Check each combo for duplicates
            for c in combos_raw:
                reduced = set(c)
                if len(reduced) == len(c):
                    combos.append(c)
        else:
            combos = combos_raw
        return combos

    def apply_operator_to_combos(self, combos, op):
        # Gets the set of operators on these combinations
        return set([functools.reduce(op, combo) for combo in combos])

    def check_combos_for_value(self, combos, cell_options, value):
        # Creates a set of values from the cell_options that combine
        # with the operator to produce the value
        results = self.apply_operator_to_combos(combos, self.operator)
        reduced_set = set()
        for i in cell_options:
            for j in results:
                test_val = self.operator(i, j)
                if self.operator == operator.sub and abs(test_val) == value:
                    reduced_set.add(i)
                elif self.operator == operator.truediv and (
                        round(test_val) == value or
                        round(1.0 / test_val) == value):
                    reduced_set.add(i)
                    # print('   TRUEDIV %s to set' % (i))
                elif test_val == value:  # Add or multiply
                    reduced_set.add(i)
        return reduced_set

    def reduce_cage_with_operator(self):
        # Apply the numeric constraint
        value = self.value
        full_cell_list = self.cell_list.copy()
        index = 0
        changed = False
        num_changed = 0
        for c in self.cell_list:
            # Make list of all cells other than this one
            old_possibles = c.possibles.copy()
            reduced_cell_list = full_cell_list.copy()
            reduced_cell_list.remove(c)
            combos = self.combos_of_possibles(reduced_cell_list)

            new_possibles = self.check_combos_for_value(
                combos, c.possibles, value)

            if len(new_possibles) == 0:
                print(' REMOVING LAST ONE from %s %s' % (index, old_possibles))
                raise LastRemovedError

            if new_possibles != old_possibles:
                changed = True
                num_changed += len(old_possibles) - len(new_possibles)
                c.possibles = new_possibles.copy()
            index += 1
        return changed, num_changed
        
    def set_up_cell_list(self, cell_data):
        start_values = start_cell_values(
            len(cell_data), self.op, self.value, self.max)
        for pos in cell_data:
            # Create a new cell object
            new_cell = Cell(pos, self)
            new_cell.possibles = start_values.copy()
            self.cell_list.append(new_cell)
            
    def is_linear(self, cells_to_check=None):
        x_vals = set()
        y_vals = set()
        if cells_to_check is None:
            cells_to_check = self.cell_list
        for cell in cells_to_check:
            x_vals.add(cell.position['x'])
            y_vals.add(cell.position['y'])
        self.linear = (len(x_vals) == 1 or len(y_vals) == 1)

    def print_possibles(self):
        print('ALL CELLS = %s' % self.cells)
        for cell in self.cell_list:
            print('CELL = %s' % cell)
            print(' %s: %s' % (cell.position, cell.possibles))

    def reduce_with_operator(self):
        if len(self.cell_list) > 1:
            return self.reduce_cage_with_operator()
        else:
            return False, 0

            
class Puzzle:
    def __init__(self, puzzle_json):
        self.rules = None
        self.size = 0
        self.cells = {}  # Keys are (M,N), value is set of possible values.
        self.cages = []
        self.debug = 1
        if puzzle_json:
            self.set_cells(puzzle_json)

        # For statistics
        self.singles_removed = 0
        self.doubles_removed = 0
        self.num_guesses_made = 0

        
    def set_cells(self, puzzle_json):
        self.size = puzzle_json['width']
        rules = puzzle_json['rules']
        cage_num = 0
        for rule in rules:
            new_cage = Cage(
                rule['op'], rule['value'], rule['cells'], self.size, cage_num)
            
            if self.debug > 1:
                print('New cage %s = %s, %s ' %
                      (cage_num, rule['op'], rule['value']))

            self.cages.append(new_cage)

            # TODO: Check if the cells are linear
            # Get the cells from this cage
            cage_cells = new_cage.cell_list
            for cage_cell in cage_cells:
                position = (cage_cell.position['x'],
                            cage_cell.position['y'])
                if self.debug > 1:
                    print('  %s: Cage Cell %s, %s' % (
                        cage_num, position, cage_cell))
                self.cells[position] = cage_cell
            cage_num += 1

    def row_col_for_cell(self, cell):
        # Generates other cells in the row and column of this cell
        row = cell[0]
        col = cell[1]
        new_cells = []
        for f in range(self.size):
            if f != row:
                new_cells.append((f, col))
        for f in range(self.size):
            if f != col:
                new_cells.append((row, f))
        return new_cells

    def row_for_cell(self, cell):
        # Generates other cells in the row of this one
        row = cell[0]
        col = cell[1]
        new_cells = []
        for f in range(self.size):
            if f != col:
                new_cells.append((row, f))
        return new_cells

    def col_for_cell(self, cell):
        # Generates other cells in the column of this one
        row = cell[0]
        col = cell[1]
        new_cells = []
        for f in range(self.size):
            if f != row:
                new_cells.append((f, col))
        return new_cells
    
    def apply_rules(self):
        changed = False
        num_changed = 0
        for cage in self.cages:
            changed_this, num_in_last = cage.reduce_with_operator()
    
            if changed_this:
                num_changed += num_in_last
                changed = True
        return changed, num_changed

    def update_groups(self, groups, row, col):
        # Each of the N groups is a dictionary. Keys are the string form
        # of the possible values. Values are the cells with that key.
        location = (col, row)
        cell = self.cells[location]
        rank = len(cell.possibles)
        key = str(cell.possibles).replace(', ', '').replace('{', '').replace('}', '')
        if key in groups[rank]:
            groups[rank][key].append(cell)
        else:
            # Add it in
            groups[rank][key] = [cell]
        # print('  ADDED %s %s %s' % (rank, key, cell))
        
    def reduce_col(self, col, groups):
        rank = 0
        num_removed = 0
        for group in groups:
            # look for value == rank
            for key, val in group.items():
                if len(val) == rank:
                    # if len(val) > 2:
                    #     print('@@@@ REDUCING %d items in column %s' %
                    #           (len(val), col))
                    num_removed += self.reduce_col_cells(col, val)
            rank += 1
        return num_removed

    def reduce_row(self, row, groups):
        rank = 0
        num_removed = 0
        for group in groups:
            # look for value == rank
            for key, val in group.items():
                if len(val) == rank:
                    # Value is the cells that have the values to be removed
                    num_removed += self.reduce_row_cells(row, val)
            rank += 1
        return num_removed

    def reduce_row_cells(self, row, val):
        # All cells in this row:
        num_removed = 0
        to_reduce = val[0].possibles
        #print('  $$$ REMOVE {%s} from row %s' % (val[0].possibles, row))
        for col in range(self.size):
            label = (col, row)
            test_cell = self.cells[label]
            if test_cell not in val:
                new_possibles = test_cell.possibles.difference(to_reduce)
                if new_possibles != test_cell.possibles:
                    #print('!!! TRY  ROW REMOVING %s from cell %s (%s)' % (
                    #    to_reduce, test_cell.position, test_cell))
                    #print('     OLD = %s, new = %s' % (test_cell.possibles,
                    #                                new_possibles))
                    num_removed += len(test_cell.possibles) - len(new_possibles)
                    self.cells[label].possibles = new_possibles
        return num_removed
                
    def reduce_col_cells(self, col, val):
        # All cells in this row:
        to_reduce = val[0].possibles
        num_removed = 0 
        #return num_removed  ## TEMPORARY!!!
        for row in range(self.size):
            label = (col, row)
            test_cell = self.cells[label]
            if test_cell not in val:
                new_possibles = test_cell.possibles.difference(to_reduce)
                if new_possibles != test_cell.possibles:
                    #print('  COL REMOVING %s from cell %s (%s)' % (
                    #    to_reduce, test_cell.position, test_cell))
                    #print('     OLD = %s, new = %s' % (test_cell.possibles,
                    #                                new_possibles))
                    num_removed += len(test_cell.possibles) - len(new_possibles)
                    self.cells[label].possibles = new_possibles
        return num_removed
                
    def find_n_groups(self):
        # For each column and each row, find groups of cells that have
        # N possibles
        num_removed = 0
        for col in range(self.size):
            # Each group contains a dictionary of possibles, with
            # its value containing the list of cells
            groups = []
            for index in range(self.size + 1):
                groups.append(dict())
            for row in range(self.size):
                self.update_groups(groups, row, col)
            self.detect_hidden_triples(groups, 'COL', col)
            self.detect_hidden_quads(groups, 'col', col)
            num_removed += self.reduce_col(col, groups)
                
        for row in range(self.size):
            groups = []
            for index in range(self.size + 1):
                groups.append(dict())

            for col in range(self.size):
                self.update_groups(groups, row, col)
            self.detect_hidden_triples(groups, 'ROW', row)
            self.detect_hidden_quads(groups, 'ROW', row)
            num_removed += self.reduce_row(row, groups)
        return num_removed

    def detect_hidden_triples(self, groups, row_col, index):
        # Find patterns of 235, 235, 35 and promote to a triple
        rank = 3
        if not groups[rank]:
            return
        for key, cells3 in groups[rank].items():
            if len(cells3) == 2:
                triple = cells3[0].possibles
                for k2, g2 in groups[rank-1].items():
                    g2_cell = g2[0]
                    if len(g2) == 1 and g2_cell.possibles.issubset(triple):
                        groups[rank][key].append(g2_cell)

    def detect_hidden_quads(self, groups, row_col, index):
        # For sets of 1234, 1234, 1234, 123 promote to a quad constraint
        rank = 4
        if not groups[rank]:
            return
        for key, cells3 in groups[rank].items():
            if len(cells3) == rank - 1:
                triple = cells3[0].possibles
                cell3_positions = [cell.position for cell in cells3]
                for k2, g2 in groups[2].items():
                    g2_cell = g2[0]
                    if len(g2) == 1 and g2_cell.possibles.issubset(triple):
                        print('DETECT RANK %d GROUP in %s[%d] for %s: %s' %
                              (
                                  rank, row_col, index, triple, cell3_positions))
                        print('  FOUND A DOUBLE or TRIPLE that fits: %s at %s' % (
                            g2_cell.possibles, g2_cell.position))
                        groups[rank][key].append(g2_cell)

    def print_row_possibles(self, msg=''):
        if msg:
            print('%s' % (msg))
        index = 0
        fmt_pattern = '%' + '%d' % self.size + 's'
        for row in range(self.size):
            row_str = []
            for col in range(self.size):
                label = (col, row)
                cell = self.cells[label]
                poss = cell.possibles
                key = str(poss).replace(', ', '').replace('{', '').replace('}', '')
                row_str.append(fmt_pattern % key)
                index += 1
            print('  %s: %s' % (row, ' '.join(row_str)))

    def print_cell_possibles(self):
        cells = sorted(self.cells.keys())
        for cell in cells:
            poss = self.cells[cell].possibles
            print('%s: %s' % (cell, list(poss)))
            
    def check_done(self):
        number_left = 0
        num_resolved = 0
        for pos, cell in self.cells.items():
            if len(cell.possibles) > 1:
                number_left += 1
            else:
                num_resolved += 1
        done = (number_left == 0)
        print('$$ Done = %s. %d cells resolved, %d unresolved' % (
            done, num_resolved, number_left))
        return done

    def apply_methods(self):
        # Apply the methods until either no change takes place.
        cycle = 0
        changed = True
        try:
            while changed:
                print('---- Cycle %s --------' % cycle) 
                num_removed = self.find_n_groups()
                rule_changed, rules_num_removed = self.apply_rules()
                if num_removed == 0 and rules_num_removed == 0:
                    changed = False
                else:
                    print('--- REMOVED N_GROUPS %d, RULES %d' % (
                        num_removed, rules_num_removed))
                    self.print_row_possibles()
                cycle += 1
            return True
        except LastRemovedError:
            print('FOUND LAST REMOVED ERROR!!!')
            return False

    def find_2cells(self):
        # Return all sells with only two possible values
        list2 = []
        for pos, cell in self.cells.items():
            if len(cell.possibles) == 2:
                list2.append(cell)
        return list2

    def guess2(self):
        # Try solving by cloning the puzzle and picking values for
        # cells with two possible values.
        cells2 = self.find_2cells()
        if not cells2:
            print('!!!!!!! There are no doubles for guessing')
            print('    NEED A BETTER SOLVER FOR THIS ONE!')
            return
        else:
            print('$$$ There are %d items with only 2 values' % (len(cells2)))
        
        solved = False
        guess_index = 0
        while not solved and guess_index < len(cells2):
            # Guess based on this 2-value cell
            guess1 = cells2[guess_index]
            guess_position = (guess1.position['x'],
                              guess1.position['y'])
            twolist = list(guess1.possibles)
            print('GUESS from cell2[%d] %s: %s possible' % (
                guess_index, guess_position, twolist))
            # Remove the first and try
            message = "\n !!!!!! Clone solving with index %s !!!!!!" % guess_index
            for item in twolist:
                # Try cloning
                p2 = copy.deepcopy(self)
                guess_cell = p2.cells[guess_position]
                guess_cell.possibles = set([item])
                p2.print_row_possibles(message)
                result = p2.apply_methods()
                if not result:
                    print('!!!! ERROR: Cannot solve this one')
                solved = p2.check_done()
                # p2.print_row_possibles('As much as can be done...')
                print('DONE = %s' % (solved))
                if solved:
                    print('ALL FINISHED. This guess worked!')
                    return
                else:
                    print('Whoops! Need to make a different guess')
                    
            guess_index += 1
        return solved

    def solve_puzzle(self):
        # Try a solution without guesses
        message = "Start configuration"
        self.print_row_possibles(message)

        result = self.apply_methods()
        self.print_row_possibles('All methods applied')

        # How to know if done?
        solved = self.check_done()
        print('DONE = %s' % (solved))

        return solved


class Testing():
    def __init__(self):
        return
    
    def test_cage_ops(self):
        c1 = {"op":"+","value":12,
              "cells":[{"x": 0,"y": 0},
                       {"x": 1,"y": 0},
                       {"x": 1,"y": 1}]}
        c2 = {"op":"-","value": 3,"cells":[{"x": 1,"y": 2},
                                           {"x": 1,"y": 3}]}
        c3 = {"op":"*","value": 105,"cells":[{"x": 2,"y": 0},
                                             {"x": 2,"y": 1},
                                             {"x":2,"y": 2}]}

        cage1 = cage(c1['op'], c1['value'], c1['cells'], 7, -2)

        print('cage1 before')
        cage1.print_possibles()
        print('After')
        cage1.print_possibles()
        
        cage2 = cage(c2['op'], c2['value'], c2['cells'], 7, -2)
        cage2.print_possibles()
        cage3 = cage(c3['op'], c3['value'], c3['cells'], 7, -3)
        cage3.print_possibles()


def test_reduce_cage(self, index, cage):
    print('REDUCE_CAGE %s' % (index))
    cage.print_possibles()
    cage.reduce_with_operator()
    

def main():
    # This one needs lots of than guesses with the 2-possible cells
    #p = Puzzle(kk_puzzles.p7_mar2022)
    p= Puzzle(kk_puzzles.puzzle9)
    #p = Puzzle(kk_puzzles.puzzle7)  # This one works with a 2-guess
    #p = Puzzle(kk_puzzles.puzzle5)
    #p = Puzzle(kk_puzzles.p5_27_mar)

    solved = p.solve_puzzle()
    if not solved:
        p.guess2()


if __name__ == '__main__':
    main()
