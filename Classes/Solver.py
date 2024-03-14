import sympy as sy


class Solver:
    def __init__(self, n: int = None, m: int = None) -> None:
        if n and m:
            self.n = n
            self.m = m
            self.arr = sy.zeros(n + 1, m + 1)

    def create_from(self, arr):
        self.arr = sy.Matrix(arr)
        self.n = len(arr) - 1
        self.m = len(arr[0]) - 1
        return self

    def __str__(self) -> str:
        ret = ""
        for i in range(self.n+1):
            ret += str(self.arr.row(i)) + "\n"
        return ret

    def edit(self, i, j, k:str):
        self.arr[i,j] = sy.Rational(k)

    def pivot(self, i, j):
        p = self.arr[i, j]
        if p == 0:
            print("Divide by zero, check input")
            return

        if i == self.n:
            print("Requesting pivot on c, skipping")
            return
        elif j == self.m:
            print("Requesting pivot on b, skipping")
            return

        print(f"Pivoting on 0-indexed position ({i},{j}):\t{p}")
        temp = self.arr.copy()

        # PQRS
        for r in range(self.n+1):
            if r == i:
                for k in range(self.m+1):
                    self.arr[i, k] = temp[i,k]/p
                continue
            for c in range(self.m+1):
                if c == j:
                    for k in range(self.n+1):
                        self.arr[k, j] = temp[k,j]/(-p)
                    continue
                self.arr[r, c] = (temp[r, c] * p - temp[i, c]*temp[r, j])/p
        self.arr[i, j] = 1 / p


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
    solver.pivot(0,1)
    print(solver)
