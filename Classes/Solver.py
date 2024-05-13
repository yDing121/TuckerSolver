import sympy as sy


class Solver:
    # Letting the constraints coefficients matrix (no b and c vectors) be mxn
    def __init__(self, m: int = None, n: int = None) -> None:
        if n and m:
            self.n = n
            self.m = m
            self.arr = sy.zeros(m + 1, n + 1)

            """
            Row and column variable names
            
            Row var keys correspond to primal basis, while values correspond to dual slacks
            Col var keys correspond to dual basis, while values correspond to primal slacks
            
            During pivoting, these relationships are maintained, so it is ok to group them together as such
            """
            self.row_vars = {f"x{i}": f"s{i}" for i in range(self.n)}
            self.col_vars = {f"y{i}": f"t{i}" for i in range(self.m)}

            # self.primal_slacks = [f"t{i}" for i in range(self.m)]
            # self.dual_slacks = [f"s{i}" for i in range(self.n)]

    def create_from(self, arr):
        self.__init__(m=len(arr) - 1, n=len(arr[0]) - 1)
        self.arr = sy.Matrix(arr)
        # self.m = len(arr) - 1
        # self.n = len(arr[0]) - 1
        # return self

    def create_from_sympy(self, symmatrix):
        self.__init__(symmatrix.shape[0]-1, symmatrix.shape[1]-1)
        self.arr = symmatrix.copy()

    def __str__(self) -> str:
        ret = ""
        for i in range(self.m+1):
            ret += str(self.arr.row(i)) + "\n"
        return ret

    def edit(self, i, j, k:str):
        self.arr[i,j] = sy.Rational(k)

    def pivot(self, i, j):
        if i is None or j is None or i < 0 or j < 0:
            print("Missing or negative input, check")
            return

        # TODO: modify pivot() and row/col deletion to account for the variables
        p = self.arr[i, j]
        if p == 0:
            print("Divide by zero, check input")
            return

        if i == self.m and j == self.n:
            print("Requesting pivot on d, skipping")
            return
        elif i == self.m:
            print("Requesting pivot on c, skipping")
            return
        elif j == self.n:
            print("Requesting pivot on b, skipping")
            return

        print(f"Pivoting on 0-indexed position ({i},{j}):\t{p}")
        temp = self.arr.copy()

        # PQRS
        for r in range(self.m+1):
            if r == i:
                for k in range(self.n+1):
                    self.arr[i, k] = temp[i,k]/p
                continue
            for c in range(self.n+1):
                if c == j:
                    for k in range(self.m+1):
                        self.arr[k, j] = temp[k,j]/(-p)
                    continue
                self.arr[r, c] = (temp[r, c] * p - temp[i, c]*temp[r, j])/p
        self.arr[i, j] = 1 / p
        print("wtf")
        return self.arr

    def otherpivot(self, mat, i, j):
        if i is None or j is None or i < 0 or j < 0:
            print("Missing or negative input, check")
            return

        p = mat[i, j]
        if p == 0:
            print("Divide by zero, check input")
            return

        tm = mat.shape[0]-1
        tn = mat.shape[1]-1

        if i == tm:
            print("Requesting pivot on c, skipping")
            return
        elif j == tn:
            print("Requesting pivot on b, skipping")
            return

        print(f"Pivoting on 0-indexed position ({i},{j}):\t{p}")
        temp = mat.copy()

        # PQRS
        for r in range(tm+1):
            if r == i:
                for k in range(tn+1):
                    mat[i, k] = temp[i,k]/p
                continue
            for c in range(tn+1):
                if c == j:
                    for k in range(tm+1):
                        mat[k, j] = temp[k,j]/(-p)
                    continue
                mat[r, c] = (temp[r, c] * p - temp[i, c]*temp[r, j])/p
        mat[i, j] = 1 / p
        print("wtf")
        return self.arr

    def pivot2(self, i, j):
        if i is None or j is None or i < 0 or j < 0:
            print("Missing or negative input, check")
            return

        p = self.arr[i, j]
        if p == 0:
            print("Divide by zero, check input")
            return

        if i == self.m:
            print("Requesting pivot on c, skipping")
            return
        elif j == self.n:
            print("Requesting pivot on b, skipping")
            return

        print(f"Pivoting on 0-indexed position ({i},{j}):\t{p}")
        temp = self.arr.copy()
        ansarr = self.arr.copy()

        # PQRS
        for r in range(self.m + 1):
            if r == i:
                for k in range(self.n + 1):
                    ansarr[i, k] = temp[i, k] / p
                continue
            for c in range(self.n + 1):
                if c == j:
                    for k in range(self.m + 1):
                        ansarr[k, j] = temp[k, j] / (-p)
                    continue
                ansarr[r, c] = (temp[r, c] * p - temp[i, c] * temp[r, j]) / p
        ansarr[i, j] = 1 / p
        print("wtf")
        self.arr = ansarr
        return ansarr

    def check_optimal(self):
        # Check if b column is valid
        for r in range(self.m):
            if self.arr[r, self.n] < 0:
                return False

        # Check if c row is valid
        for c in range(self.n):
            if self.arr[self.m, c] > 0:
                return False

        return True

    def delete_col(self, c):
        if c < 0 or self.n <= c:
            print("Invalid request, ignoring")
            return

        self.arr.col_del(c)

    def delete_row(self, r):
        if r < 0 or self.m <= r:
            print("Invalid request, ignoring")
            return

        self.arr.row_del(r)


if __name__ == "__main__":
    # solver = Solver(3, 2)
    # solver.edit(0, 0, 2)
    # solver.edit(0, 2, 2)
    # solver.edit(3, 0, 3)
    # solver.edit(3, 2, 4)
    # # print(solver.get_A())
    # # print(solver.get_b())
    # # print(solver.get_c())
    # # print(solver.get_d())
    # print(solver)
    # solver.pivot(0, 0)
    # print(solver)
    solver = Solver()
    solver.create_from([[1,2,-2,10], [3,1,-1,15], [1,3,-3,0]])
    print(solver)
    solver.pivot(0,1)
    print(solver)
    solver.delete_col(0)
    print(solver)
    print(solver.row_vars)
