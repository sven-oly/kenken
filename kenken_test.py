# Run tests on the kenken, including regression test on those that
# used to pass

import kenken
import kenken_args
import kk_puzzles

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

def regression_test():
  all_passed = True
  for puzz in kk_puzzles.regression_puzzles:
    print('\n+++++++++ TESTING %s !++++++++++' % (puzz['name']))
    p = kenken.Puzzle(puzz)
    p.test_only = True
    solved = p.solve_puzzle()
    if solved:
      print('    ++++ Puzzle %s solved without guesses' % (puzz['name']))
      p.show_statistics('    Statistics without guesses')
    else:
      p.show_statistics('  Before guessing')
      solved, p2 = p.guess2()
      if solved:
          print('  ++++ SOLVED with %d guesses' % (p.num_guesses_made))
          p2.show_statistics('  ++++ Last guess')
    if not solved:
      all_passed = False
      print('    $$$$$$$$$$$$ Cannot solve %s' % (puzz['name']))

  if all_passed:
    print('YAY! All regression tests pass!')
  else:
    print('Uh-oh! Some regression tests fail.')

  return all_passed



def test_reduce_cage(self, index, cage):
  print('REDUCE_CAGE %s' % (index))
  cage.print_possibles()
  cage.reduce_with_operator()

def main():
  result = regression_test()

if __name__ == '__main__':
  main()