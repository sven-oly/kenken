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

def factor_n(val, max, num_cells=2):
    # Return set of all possible factors in num_cells.
    # TODO: Consider number of cells
    rem = val
    factors = set()
    for f in range(1, max+1):
        div = val % f
        if div == 0:
            factors.add(f)
    return set(factors)

def add_possibles(val, max, num_cells):
    # What values can add the total in N cells
    # TODO: Consider number of cells
    top = min(val - 1, max)  # Need to consider # cells
    return set([n for n in range(1, top + 1)])

def sub_possibles(val, max):
    result = set()
    for n in range(max + 1):
        if (n - val) > 0:
            result.add(n)
            result.add(n - val)
    return result

def div_possibles(val, max):
    result = set()
    for n in range(1, max + 1):
        if n % val == 0:
            result.add(n)
            result.add(n // val )
    return result

def start_cell_from_rule(rule, max):
    cells = rule['cells']
    return start_cell_values(len(cells), rule['op'], rule['value'], max)

#def start_cell_values(num_cells, op, val, max): 
def start_cell_values(num_cells, op, val, max): 
    if op == "*":
        nums = factor_n(val, max, num_cells)
    elif op == "+":
        nums = add_possibles(val, max, num_cells)
    elif op == "-":
        nums = sub_possibles(val, max)
    elif op == "/":
        nums = div_possibles(val, max)
    else:
        nums = set([val])
    return nums

class LastRemovedError(BaseException):
    pass
    
class cell():
    # Stores information about a single cell of the grid
    def __init__(self, position, cage):
        self.position = position
        self.cage = cage
        self.possibles = set()

def subtract(a, b):
    return a - b

def divide(a, b):
    return a / b

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

class cage():

    def __init__(self, op, value, cell_data, grid_size, cage_num=-1):
        self.op = op
        self.index = cage_num
        self.value = value
        self.cells = cell_data
        self.cell_list = []
        self.max = grid_size
        self.set_up_cell_list(cell_data)
        self.debug = 1
        self.operator = operator_map[op]
        self.linear = self.is_linear()

    def combos_of_possibles(self, cell_list):
        # Compute the combinations of the possible values in these cells
        list_of_possibles = []
        for cell in cell_list:
            list_of_possibles.append(cell.possibles)
            combos_raw = list(itertools.product(*list_of_possibles))
        combos = []
        if self.linear:
            # Check each combo for duplicates
            for c in combos_raw:
                reduced = set(c)
                if len(reduced) == len(c):
                    combos.append(c)
        else:
            combos = combos_raw
        return combos

    def apply_operator_to_combos(self, combos, operator):
        # Gets the set of operators on these combinations
        results = set([functools.reduce(operator, combo) for combo in combos])
        #print(  'OPERATOR_TO_COMBOS %s on %s --> %s' % (
        #    operator, combos, results))
        return set(results)

    def check_combos_for_value(self, combos, cell_options, value):
        # Creates a set of values from the cell_options that combine
        # with the operator to produce the value
        results = self.apply_operator_to_combos(combos, self.operator)
        #print('  COMBO RESULTS: %s' % (results))
        #print('  cell_options: %s' % (cell_options))
        reduced_set = set()
        for i in cell_options:
            for j in results:
                test_val = self.operator(i,j)
                #print('  %s %s %s --> %s (%s)' % (i, op, j, test_val, value))
                if self.operator == operator.sub and abs(test_val) == value:
                    reduced_set.add(i)
                elif self.operator == operator.truediv and (
                        round(test_val) == value or
                        round(1.0 / test_val) == value):
                    reduced_set.add(i)
                    # print('   TRUEDIV %s to set' % (i))
                elif test_val == value:  # Add or multiply
                    reduced_set.add(i)
        #if self.operator == operator.sub or self.operator == operator.truediv:
        #    print('--- REDUCED SET = %s' % (reduced_set))
        return reduced_set

    def reduce_cage_with_operator(self):
        # Apply the numeric constraint
        value = self.value
        full_cell_list = self.cell_list.copy()
        #print('  FULL_CELL_LIST: %s' % ([c.position for c in full_cell_list]))
        index = 0
        changed = False
        num_changed = 0
        for c in self.cell_list:
            # Make list of all cells other than this one
            old_possibles = c.possibles.copy()
            reduced_cell_list = full_cell_list.copy()
            reduced_cell_list.remove(c)
            combos = self.combos_of_possibles(reduced_cell_list)

            # print('  combos: %s' % (combos))
            new_possibles = self.check_combos_for_value(
                combos, c.possibles, value)

            if len(new_possibles) == 0:
                print(' REMOVING LAST ONE from %s %s' % (index, old_possibles))
                raise LastRemovedError

            if new_possibles != old_possibles:
                changed = True
                num_changed += len(old_possibles) - len(new_possibles)
                c.possibles = new_possibles.copy()
                # print('  OPERATOR: %d cells with %s %s' %
                #       (len(self.cell_list), self.operator, value))
                #print('     REDUCED %s %s --> %s' % (
                #    c.position, old_possibles, new_possibles))
            index += 1
        return changed, num_changed
        
    def set_up_cell_list(self, cell_data):
        for pos in cell_data:
            # Create a new cell object
            new_cell = cell(pos, self)
            start_vals = start_cell_values(
                len(cell_data), self.op, self.value, self.max)
            new_cell.possibles = start_vals.copy()
            self.cell_list.append(new_cell)
            
    def is_linear(self):
        x_vals = set()
        y_vals = set()
        for cell in self.cell_list:
            x_vals.add(cell.position['x'])
            y_vals.add(cell.position['y'])
        self.linear = False
        if len(x_vals) == 1 or len(y_vals) == 1:
               self.linear = True
        #print('%s LINEAR RESULT %s' % (self.index, self.linear))

    def print(self):
        print('Cage %s: %s%s linear=%s, %s cells' % (
            self.index, self.op, self.value, self.linear, len(self.cell_list)))

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

            
class puzzle():
    def __init__(self):
        self.rules = None
        self.size = 0
        self.cells = {}  # Keys are (M,N), value is set of possible values.
        self.cages = []
        self.debug = 1
        
    def set_cells(self, puzz):
        self.size = puzz['width']
        rules = puzz['rules']
        # print(self.size)

        cage_num = 0
        for rule in rules:
            new_cage = cage(
                rule['op'], rule['value'], rule['cells'], self.size, cage_num)
            
            start_vals = list(start_cell_from_rule(rule, self.size))
            if self.debug > 1:
                print('New cage %s = %s, %s ' %
                      (cage_num, rule['op'], rule['value']))

            self.cages.append(new_cage)

            # print(rule)
            cells = rule['cells']
            op = rule['op']
            val = rule['value']
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

    def set_constraints(self):
        # Set all possible values for each cell
        # For each column
        # For each row
        # For each cage
        return

    def constraints_cage(self, cage):
        op = cage['op']


    def row_col_for_cell(self, cell):
        # Generates other cells in the row and column of this one
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
            #print("Applying rule for cage [%s]" % cage_num)
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
        key = str(cell.possibles).replace(', ', '').replace('{','').replace('}','')
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
            for key,val in group.items():
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
            for key,val in group.items():
                if len(val) == rank:
                    # if len(val) > 2:
                    #     print('@@@@ REDUCING %d items in row %s' %
                    #           (len(val), row))
                    #print('ROW REDUCABLE: row %s, {%s}, %s' % (row, key, val))
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
        num_removed =0
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
            triple = cells3[0].possibles
            if len(cells3) == 2:
                triple = cells3[0].possibles
                cell3_positions = [cell.position for cell in cells3]
                for k2, g2 in groups[rank-1].items():
                    g2_cell = g2[0]
                    if len(g2) == 1 and g2_cell.possibles.issubset(triple):
                        # print('DETECT RANK %d GROUP in %s[%d] for %s: %s' %
                        #       (
                        #           rank, row_col, index, triple, cell3_positions))
                        # print('  FOUND A DOUBLE that fits: %s at %s' % (
                        #    g2_cell.possibles, g2_cell.position))
                        groups[rank][key].append(g2_cell)

    def detect_hidden_quads(self, groups, row_col, index):
        # For sets of 1234, 1234, 1234, 123 promote to a quad constraint
        rank = 4
        if not groups[rank]:
            return
        for key, cells3 in groups[rank].items():
            triple = cells3[0].possibles
            if len(cells3) == rank - 1:
                triple = cells3[0].possibles
                cell3_positions = [cell.position for cell in cells3]
                for k2, g2 in groups[ 2].items():
                    g2_cell = g2[0]
                    if len(g2) == 1 and g2_cell.possibles.issubset(triple):
                        print('DETECT RANK %d GROUP in %s[%d] for %s: %s' %
                              (
                                  rank, row_col, index, triple, cell3_positions))
                        print('  FOUND A DOUBLE or TRIPLE that fits: %s at %s' % (
                            g2_cell.possibles, g2_cell.position))
                        groups[rank][key].append(g2_cell)

    def apply_singles(self):
        # for each cell, look for single values and remove it in row/columns
        changed = False
        num_removed = 0
        for c in self.cells:
            cell = self.cells[c]
            if len(cell.possibles) == 1:
                #print('%s in %s' % (cell.possibles, cell.position))
                row_col = self.row_col_for_cell(c)
                single_val = list(cell.possibles)[0]
                for pos in row_col:
                    try:
                        previous = list(self.cells[pos].possibles)
                        self.cells[pos].possibles.remove(single_val)
                        #print('Removed %s from cell %s (%s) --> %s' % (
                        #    single_val, pos, previous,
                        #    self.cells[pos].possibles))
                        changed = True
                        num_removed += 1
                    except :
                        continue
                        #print('  %s not in  cell %s' % (single_val, pos))
        return changed, num_removed
                        
    def apply_doubles(self):
        # for each cell with two items, check all others in row / column
        # for same set of possible values.
        # If there are two such cells, then remove those possibles from
        # other in that row or column.
        changed = False
        num_removed = 0
        not_removed = 0
        for c in self.cells:
            cell = self.cells[c]
            if len(cell.possibles) == 2:
                #print('DOUBLE %s in %s' % (cell.possibles, cell.position))
                row_col = self.row_col_for_cell(c)
                double_val = cell.possibles
                double_list = list(double_val)
                row_items = self.row_for_cell(c)
                matched = False
                for pos in row_items:
                    if self.cells[pos].possibles == double_val:
                        # print('  MATCHED DOUBLE ROW %s in %s' % (
                        #cell.possibles, pos))
                        matched = True
                if matched:
                    for pos in row_items:
                        if self.cells[pos].possibles != double_val: 
                            for single_val in double_list:
                                try:
                                    self.cells[pos].possibles.remove(single_val)
                                    # print('  --- Removed %s from cell %s --> %s' % (single_val, pos, self.cells[pos].possibles))
                                    changed = True
                                    num_removed += 1
                                except :
                                    not_removed += 1
                                    #print('  %s not in  cell %s: %s' % (single_val, pos, self.cells[pos].possibles))                         
                        
                matched = None
                col_items = self.col_for_cell(c)
                for pos in col_items:
                    if self.cells[pos].possibles == double_val:
                        # print('  MATCHED DOUBLE COL %s in %s' % (cell.possibles, pos))
                        matched = self.cells[pos]
                if matched:
                    for pos in col_items:
                        if self.cells[pos].possibles != double_val: 
                            for single_val in double_list:
                                try:
                                    self.cells[pos].possibles.remove(single_val)
                                    # print('  --- Removed %s from cell %s --> %s' % (single_val, pos, self.cells[pos].possibles))
                                    changed = True
                                    num_removed += 1
                                except :
                                    not_removed += 1
                                    # print('  %s not in  cell %s: %s' % (single_val, pos, self.cells[pos].possibles))                         

        # print('  Doubles %s removed, %s not_removed' % (num_removed, not_removed))
        return changed, num_removed

    def print_row_possibles(self, msg=''):
        if msg:
            print('%s' % (msg))
        cells = sorted(self.cells.keys())
        index = 0
        for row in range(self.size):
            row_str = []
            for col in range(self.size):
                label = (col, row)
                cell = self.cells[label]
                poss = cell.possibles
                key = str(poss).replace(', ', '').replace('{','').replace('}','')
                row_str.append('%7s ' % key)
                index += 1
            print('  %s: %s' % (row, row_str))

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

    def old_methods(self):
        # Subsumed by find_n_groups
        changed, num_removed  = self.apply_singles()
        if changed:
            print('1111: %d removed' % num_removed)
            self.print_row_possibles()
        else:
            print('Nothing from apply_singles')
        print('------ 22222 ----')
        changed, num_removed = self.apply_doubles()
        if changed:
            print('2222: %d removed' % num_removed)
            self.print_row_possibles()
        else:
            print('Nothing from apply_doubles')


class testing():
    def __init__(self):
        return
    
    def test_cage_ops(self):
        c1 = {"op":"+","value":12,
              "cells":[{"x":0,"y":0},{"x":1,"y":0},{"x":1,"y":1}]}
        c2 = {"op":"-","value":3,"cells":[{"x":1,"y":2},{"x":1,"y":3}]}
        c3 = {"op":"*","value":105,"cells":[{"x":2,"y":0},{"x":2,"y":1},{"x":2,"y":2}]}

        cage1 = cage(c1['op'], c1['value'], c1['cells'], 7, -2)

        print('cage1 before')
        cage1.print_possibles()
        print('After')
        cage1.print_possibles()
        
        cage2 = cage(c2['op'], c2['value'], c2['cells'], 7, -2)
        cage3 = cage(c3['op'], c3['value'], c3['cells'], 7, -3)


    def test_reduce_cage(self, index, cage):
        print('REDUCE_CAGE %s' % (index))
        cage.print_possibles()
        cage.reduce_with_operator()
    
def main():
    test_obj = testing()
    #test_obj.test_cage_ops()
    #return

    p = puzzle()
    #p.set_cells(kk_puzzles.puzzle7)
    #p.set_cells(kk_puzzles.puzzle5)
    #p.set_cells(kk_puzzles.p5_27_mar)
    p.set_cells(kk_puzzles.p7_mar2022)

    message = "Start configuration"
    p.print_row_possibles(message)

    result = p.apply_methods()
    p.print_row_possibles('All methods applied:')

    # How to know if done?
    solved = p.check_done()
    print('DONE = %s' % (solved))

    if not solved:
        print()
        # A cell with only two possibles.
        cells2 = p.find_2cells()
        if not cells2:
            print('!!!!!!! There are no doubles for guessing')
            print('    NEED A BETTER SOLVER FOR THIS ONE!')
            return
        else:
            print('$$$ There are %d items with 2 possible values for guessing' % (len(cells2)))
        
        # !!We may need to try guessing with other cells
        solved = False
        guess_index = 0
        while not solved and guess_index < len(cells2):
            #print('!!! INDEX: %d, CELLS2: %s' % (guess_index, cells2))
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
                p2 = copy.deepcopy(p)
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

if __name__ == '__main__':
    main()
