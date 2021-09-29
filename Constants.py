import numpy
from math import sqrt


class Constants:

    def __init__(self, matrix, v_matrix):
        self.matrix_size = len(matrix)
        self.starting_matrix = matrix
        self.starting_v_matrix = v_matrix
        self.__mu = None
        self.list_sin = [None] * self.matrix_size
        self.list_cos = [None] * self.matrix_size
        self.q_matrixes = [None] * (self.matrix_size - 1)
        self.givens_rotation_steps = [None] * (self.matrix_size - 1)
        self.qr_multiplication_steps = [None] * (self.matrix_size - 1)
        self.qv_multiplication_steps = [None] * (self.matrix_size - 1)
        self.r_matrix = None
        self.generated_a_matrix = None
        self.generated_v_matrix = None
        self.product_transposed_qs = None
        self.post_finish_a = None
        self.post_finish_v = None

        self.using_unsafe_sin_cos_calculation = False
        self.using_spectral_shift = False

    def use_unsafe_sin_cos_calculation(self):
        self.using_unsafe_sin_cos_calculation = True
        return self

    def use_spectral_shift(self):
        self.using_spectral_shift = True
        return self

    def givens_rotation_starting_matrix(self):
        if self.using_spectral_shift:
            return numpy.subtract(self.starting_matrix, self.mu() * numpy.identity(self.matrix_size))
        return self.starting_matrix

    def matrix_for_givens_rotation_step(self, step):
        if step == 0:
            return self.givens_rotation_starting_matrix()
        else:
            return self.givens_rotation_steps[step - 1]

    def matrix_for_qr_step(self, step):
        if step == 0:
            return self.r_matrix
        else:
            return self.qr_multiplication_steps[step - 1]

    def matrix_for_qv_step(self, step):
        if step == 0:
            return self.starting_v_matrix
        else:
            return self.qv_multiplication_steps[step - 1]

    def calculate_constants(self, i):
        # SIN_COS
        if not self.using_unsafe_sin_cos_calculation:
            sin, cos = self.safe_sin_cos_calculation(i)
        else:
            matrix = self.matrix_for_givens_rotation_step(i)
            sin = -(matrix[i + 1][i]) / ((matrix[i][i]) ** 2 + (matrix[i + 1][i]) ** 2) ** 0.5
            cos = (matrix[i][i]) / ((matrix[i][i]) ** 2 + (matrix[i + 1][i]) ** 2) ** 0.5
        self.set_sin_cos(i, sin, cos)
        # Q_MATRIX
        q_matrix = numpy.array([
            [cos, -sin],
            [sin, cos]
        ], dtype=float)
        q_matrix.flags.writeable = False
        self.set_q(i, q_matrix)

    def safe_sin_cos_calculation(self, i):
        matrix = self.matrix_for_givens_rotation_step(i)
        alpha = matrix[i][i]
        beta = matrix[i + 1][i]
        tau = 0
        if abs(alpha) > abs(beta):
            tau = - beta / alpha
            cos = 1 / sqrt(1 + tau * tau)
            sin = cos * tau
        else:
            tau = - alpha / beta
            sin = 1 / sqrt(1 + tau * tau)
            cos = sin * tau
        return sin, cos

    def calculate_product_for_transposed_qs(self):
        if self.product_transposed_qs is None:
            resulting_matrix = numpy.matrix.transpose(self.q(0))
            for i in range(1, len(self.q_matrixes)):
                resulting_matrix = numpy.matmul(resulting_matrix, numpy.matrix.transpose(self.q(i)))
            resulting_matrix.flags.writeable = False
            self.product_transposed_qs = resulting_matrix
        return self.product_transposed_qs

    def calculate_product_for_qs(self):
        resulting_matrix = self.q(0)
        for i in range(1, len(self.q_matrixes)):
            resulting_matrix = numpy.matmul(resulting_matrix, self.q(i))
        resulting_matrix.flags.writeable = False
        return resulting_matrix

    def calculate_mu(self):
        matrix = self.starting_matrix

        n = len(matrix) - 1
        dk = ((matrix[n - 1][n - 1]) - (matrix[n][n])) / 2
        if dk >= 0:
            sgn_dk = 1
        else:
            sgn_dk = -1
        mu = (matrix[n][n]) + dk - sgn_dk * sqrt((dk ** 2) + ((matrix[n][n - 1]) ** 2))
        self.__mu = mu

        return mu

    def force_mu(self, forced_value):
        self.__mu = forced_value

    def mu(self):
        if self.__mu is None:
            self.calculate_mu()
        return self.__mu

    def sin_cos(self, index):
        return self.list_sin[index], self.list_cos[index]

    def has_sin(self, index):
        return not self.list_sin[index] is None

    def has_cos(self, index):
        return not self.list_cos[index] is None

    def has_sin_cos(self, index):
        return self.has_sin(index) and self.has_cos(index)

    def set_sin_cos(self, index, sin, cos):
        self.list_sin[index] = sin
        self.list_cos[index] = cos

    def q(self, index):
        return self.q_matrixes[index].copy()

    def set_q(self, index, q):
        self.q_matrixes[index] = q

    def set_givens_rotation_step(self, index, matrix):
        copy = matrix.copy()
        copy.flags.writeable = False
        self.givens_rotation_steps[index] = copy

    def r(self):
        return self.r_matrix

    def set_r_matrix(self, matrix):
        copy = matrix.copy()
        copy.flags.writeable = False
        self.r_matrix = copy

    def set_qr_multiplication_step(self, index, matrix):
        copy = matrix.copy()
        copy.flags.writeable = False
        self.qr_multiplication_steps[index] = copy

    def set_qv_multiplication_step(self, index, matrix):
        copy = matrix.copy()
        copy.flags.writeable = False
        self.qv_multiplication_steps[index] = copy

    def a(self):
        return self.generated_a_matrix

    def set_generated_a_matrix(self, matrix):
        copy = matrix.copy()
        if self.using_spectral_shift:
            copy = numpy.add(copy, self.mu() * numpy.identity(self.matrix_size))
        copy.flags.writeable = False
        self.generated_a_matrix = copy

    def v(self):
        return self.generated_v_matrix

    def set_generated_v_matrix(self, matrix):
        copy = matrix.copy()
        copy.flags.writeable = False
        self.generated_v_matrix = copy

    def big_q(self):
        return self.calculate_product_for_transposed_qs()