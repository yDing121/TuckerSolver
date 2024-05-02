import Solver

solver = Solver.Solver()
solver.create_from([[1, 2, -2, 10], [3, 1, -1, 15], [1, 3, -3, 0]])
print(solver)
solver.pivot(0, 1)
print(solver)
solver.delete_col(0)
print(solver)
print(solver.row_vars)
