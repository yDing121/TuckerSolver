from Classes import Display
from Classes import Solver
from Classes import TableauGetter

if __name__ == "__main__":
    solver = Solver.Solver(-1, -1)
    solver.create_from_sympy(TableauGetter.main().copy())

    app = Display.MatrixDisplay(solver, cell_size=70)  # Larger cell size to accommodate fraction strings

    app.run()
