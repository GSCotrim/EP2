import numpy
from EPExceptions import *


class Matrix:

    def __init__(self, matrix):
        initial = numpy.array(matrix, dtype=float)
        initial.flags.writeable = False
        self.initial = initial
        self.intermediate = self.initial.copy()
        self.n = len(matrix)
        if self.n > 0:
            self.m = len(matrix[0])
        else:
            self.m = 0
        self.__vector_e = self.__calculate_vector_e()
        self.omega = self.__calculate_omega()
        self.final = None

    # Define o vetor que será utilizado para definir nosso ômega
    # e os vetores (coluna) da matriz de entrada que serão alterados
    # pela transformação de Householder aplicada "pela esquerda"
    def calculate_column_vector_a(self, column):
        vector_a = []

        for i in range(1, self.n):
            vector_a.append(self.intermediate[i][column])

        return vector_a

    # Define os vetores (linha) que serão alterados
    # pela transformação de Householder aplicada "pela direita"
    def calculate_line_vector_a(self, line):
        if line == 0:
            raise InvalidLineVectorAException(line)

        if self.intermediate is None:
            raise IntermediateMatrixDoesNotExistException()

        vector_a = []

        for i in range(1, self.m):
            vector_a.append(self.intermediate[line][i])

        return vector_a

    # Calcula o ômega que será utilizado nas contas, seguindo o método definido na apostila
    def __calculate_omega(self):
        vector_a = self.calculate_column_vector_a(0)

        if vector_a[0] >= 0:
            delta = 1
        else:
            delta = -1

        omega = numpy.add(vector_a, numpy.multiply(delta * numpy.linalg.norm(vector_a), self.__vector_e))

        return omega

    # Retorna uma "sub-matriz" (n-1 x n-1) calculada a partir da remoção
    # da primeira linha e primeira coluna da matriz atual
    def sub_matrix(self):
        if self.intermediate is None:
            raise IntermediateMatrixDoesNotExistException()

        second_matrix = []

        for i in range(1, self.n):
            second_matrix.append([])
            for j in range(1, self.n):
                second_matrix[i - 1].append(self.intermediate[i][j])

        return Matrix(second_matrix)

    def yoshi(self):
        if self.intermediate is None:
            raise IntermediateMatrixDoesNotExistException()

        second_matrix = []

        for i in range(0, self.n):
            second_matrix.append([])
            for j in range(1, self.m):
                second_matrix[i].append(self.intermediate[i][j])

        return Matrix(second_matrix)

    # Define o vetor e como (1,0,0...,0), de acordo com o tamanho n da matriz atual
    def __calculate_vector_e(self):
        vector_e = [0]*(self.n - 1)
        vector_e[0] = 1

        return vector_e

    @staticmethod
    def pretty_print(matrix, precision=6):
        with numpy.printoptions(precision=precision):
            print(matrix)