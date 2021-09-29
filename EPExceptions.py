class InvalidLineVectorAException(Exception):
    def __init__(self, line):
        self.message = f'Should not return vector A for line: {line}'
        super().__init__(self.message)


class IntermediateMatrixDoesNotExistException(Exception):
    def __init__(self):
        self.message = f'Intermediate Matrix does not exist. Are you pretty sure you created it?'
        super().__init__(self.message)


class FinalMatrixDoesNotExistException(Exception):
    def __init__(self):
        self.message = f'Final Matrix does not exist. Are you pretty sure you created it?'
        super().__init__(self.message)


class NotSuperiorTriangularException(Exception):
    def __init__(self, matrix):
        self.message = f"Resulting matrix is not superior triangular: {matrix}"
        super().__init__(self.message)


class NotTridiagonalSimmetricException(Exception):
    def __init__(self, matrix):
        self.message = f"Resulting matrix is not tridiagonal simmetric: {matrix}"
        super().__init__(self.message)


class MatrixTooSmallToRotateException(Exception):
    def __init__(self, size, matrix):
        self.message = f"Matrix size {size} is too small to rotate: {matrix}"
        super().__init__(self.message)


class CreateNewIterationException(Exception):
    def __init__(self, current_iteration, constants):
        self.message = f"Current iteration {current_iteration} should be one unit lower than the amount of constants {len(constants)}"
        super().__init__(self.message)


class NotAutovalueAutovectorException(Exception):
    def __init__(self, current_autovalue, current_autovector, matrix, error, errors):
        self.message = f"Biggest differnce =\n {error}\n" \
            f"List of differences: {errors}"
        super().__init__(self.message)


class NotOrtogonalException(Exception):
    def __init__(self, transposed, inversed):
        self.message = f"Your eigenvector matrix is not ortogonal"
        super().__init__(self.message)
