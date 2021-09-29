import numpy
from Matrix import Matrix


class Solver:

    def __init__(self, matrix, ht=None):
        # if not self.__simmetric(matrix): # TODO: Criar nova exception
        #     raise NovaException(matrix)
        self.matrix = Matrix(matrix)
        if ht is None:
            self.ht = Matrix(numpy.identity(self.matrix.n))
        else:
            self.ht = ht

    # Realiza a operação: Hω.x = x - 2.(ω.x/ω.ω).ω
    def __fazendo_contas(self, vector_a, omega):
        omega_x = (numpy.dot(omega, vector_a))
        omega_omega = numpy.linalg.norm(omega)

        transformed = numpy.subtract(vector_a, numpy.multiply(2 * omega_x / omega_omega ** 2, omega))

        return transformed

    # Este método é executado recursivamente para "sub-matrizes" de tamanho (n-1 x n-1), (n-2 x n-2), ... , (2 x 2)
    def transformando(self):
        # Se a matriz for (2 x 2) não são necessárias contas.
        if self.matrix.n <= 2:
            return self.matrix.intermediate

        # Faz a operação definida em "def __fazendo_contas()" para as colunas de tamanho (n-1 x 1) da matriz desta iteração
        for column in range(self.matrix.m):
            transformed = self.__fazendo_contas(self.matrix.calculate_column_vector_a(column), self.matrix.omega)

            # substitui esses termos alterados na matriz intermediária
            for line in range(1, self.matrix.n):
                self.matrix.intermediate[line][column] = transformed[line - 1]

        # Aqui estamos copiando os dados da atual coluna 0 para a atual linha 0
        for i in range(1, self.matrix.n):
            self.matrix.intermediate[0][i] = self.matrix.intermediate[i][0]

        # Faz a operação definida em "def __fazendo_contas()" para as linhas de tamanho (1 x n-1) da matriz desta iteração
        for line in range(1, self.matrix.n):
            transformed = self.__fazendo_contas(self.matrix.calculate_line_vector_a(line), self.matrix.omega)

            # substitui esses termos alterados na matriz intermediária
            for column in range(1, self.matrix.m):
                self.matrix.intermediate[line][column] = transformed[column - 1]

        for line in range(1, self.ht.n):
            transformed = self.__fazendo_contas(self.ht.calculate_line_vector_a(line), self.matrix.omega)

            for column in range(1, self.ht.m):
                self.ht.intermediate[line][column] = transformed[column - 1]

        # Chamamos uma recursividade para re-executar a mesma operação na "sub-matriz" gerada
        # a partir da remoção da primeira linha e coluna da matriz atual
        sub_solver = Solver(self.matrix.sub_matrix().initial.tolist(), self.ht.yoshi())
        solved = sub_solver.transformando()

        self.matrix.final = self.matrix.intermediate.copy()

        # Devolve os termos calculados na recursão, arredondando termos da matriz menores que nosso erro (10^-6) para zero.
        for line in range(1, self.matrix.n):
            for column in range(1, self.matrix.m):
                self.matrix.final[line][column] = self.arredondando(solved[line - 1][column - 1])

        # HT
        for line in range(1, self.ht.n):
            for column in range(1, self.ht.m):
                self.ht.intermediate[line][column] = self.arredondando(sub_solver.ht.intermediate[line][column - 1])

        return self.matrix.final

    # Arredonda termos menores que nosso erro (10^-6) para zero.
    def arredondando(self, num):
        if abs(num) < 10**-6:
            return 0
        return num

