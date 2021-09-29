import numpy
from Constants import Constants
from Result import Result
from EPExceptions import *


class Intern:

    def __init__(self, matrix, v_matrix=None):
        self.starting_matrix = numpy.array(matrix, dtype=float)
        self.starting_matrix.flags.writeable = False
        self.current_iteration = 0
        if v_matrix is None:
            v_matrix = numpy.identity(len(matrix))
        starting_constants = Constants(self.starting_matrix, v_matrix)
        starting_constants.force_mu(0)
        self.constants = [
            starting_constants
        ]
        self.autovalues = []
        self.autovectors = []
        self.results = []

        self.using_unsafe_sin_cos_calculation = False
        self.using_spectral_shift = False
        self.reduce_next_matrix = False
        self.using_rounding_to_check_identity = False

    def use_unsafe_sin_cos_calculation(self):
        self.using_unsafe_sin_cos_calculation = True
        self.current_constants().use_unsafe_sin_cos_calculation()
        return self

    def use_spectral_shift(self):
        self.using_spectral_shift = True
        self.current_constants().use_spectral_shift()
        return self

    def use_rounding_to_check_identity(self):
        self.using_rounding_to_check_identity = True
        return self

    def current_constants(self):
        return self.constants[self.current_iteration]

    def reduce_matrix(self, matrix):
        matrix = matrix.tolist()
        # matrix.pop(0)
        matrix.pop()
        for i in range(len(matrix)):
            # matrix[i].pop(0)
            matrix[i].pop()
        matrix = numpy.array(matrix, dtype=float)
        matrix.flags.writeable = False
        return matrix

    def extract_last_column(self, matrix):
        autovector = []
        # for i in range(len(matrix)):
        #   autovector.append(matrix[i].pop())
        for line in matrix:
            autovector.append(line.pop())
        return autovector

    def extract_and_save_one_result(self, a_matrix, v_matrix):
        a_matrix, v_matrix = a_matrix.tolist(), v_matrix.tolist()
        lenlen = len(a_matrix)
        autovalue = a_matrix[lenlen - 1][lenlen - 1]
        autovector = self.extract_last_column(v_matrix)
        self.results.append(Result(autovalue, autovector))
        a_matrix.pop()
        for line in a_matrix:
            line.pop()
        return numpy.array(a_matrix), numpy.array(v_matrix)

    def start_new_iteration(self):
        old_a_matrix = self.current_constants().post_finish_a
        old_v_matrix = self.current_constants().post_finish_v
        self.current_iteration += 1
        new_constants = Constants(old_a_matrix, old_v_matrix)
        if self.using_unsafe_sin_cos_calculation:
            new_constants.use_unsafe_sin_cos_calculation()
        if self.using_spectral_shift:
            new_constants.use_spectral_shift()
        self.constants.append(new_constants)
        if self.current_iteration != (len(self.constants) - 1):
            raise CreateNewIterationException(self.current_iteration, self.constants)

    def finish_iteration(self):
        a_matrix = self.current_constants().a().copy()
        v_matrix = self.current_constants().v().copy()
        while len(a_matrix) > 1 and self.last_beta_equals_zero(a_matrix):
            a_matrix, v_matrix = self.extract_and_save_one_result(a_matrix, v_matrix)
        if len(a_matrix) == 1:
            a_matrix, v_matrix = self.extract_and_save_one_result(a_matrix, v_matrix)
        self.current_constants().post_finish_a = a_matrix
        self.current_constants().post_finish_v = v_matrix

    def is_superior_triangular(self, matrix):
        for i in range(1, len(matrix)):
            for j in range(0, i):
                if round(matrix[i][j], 10) != 0:
                    return False
        return True

    def is_tridiagonal_simmetric(self, matrix):
        for i in range(len(matrix)-1):
            t1 = matrix[i][i+1]
            t2 = matrix[i+1][i]
            if round(t1, 12) != round(t2, 12):
                return False
        return True

    def last_beta_equals_zero(self, matrix):
        n = len(matrix) - 1
        if n == 0:
            return True
        # last_beta = matrix[0][1]
        last_beta = matrix[n][n - 1]
        return abs(last_beta) < 10 ** -20

    def tends_to_identity(self, matrix):
        if self.using_rounding_to_check_identity:
            return self.tends_to_identity_by_rounding(matrix)
        else:
            return self.tends_to_identity_by_iterating(matrix)

    def tends_to_identity_by_rounding(self, matrix):
        return numpy.all(numpy.matrix.round(numpy.array(matrix, dtype=float), 6) == numpy.identity(len(matrix)))

    def tends_to_identity_by_iterating(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if i == j and round(matrix[i][j], 7) != 1:
                    return False
                if i != j and abs(matrix[i][j]) >= 10 ** -8:
                    return False
        return True

    def old_qr_multiply(self, i):
        q_matrix = self.current_constants().q(i)
        q_transp = numpy.matrix.transpose(q_matrix)

        # transpondo e de-transpondo because gambeta
        r_matrix = self.current_constants().matrix_for_qr_step(i)
        v_matrix = self.current_constants().matrix_for_qv_step(i)
        r_transp = numpy.matrix.transpose(r_matrix)
        v_transp = numpy.matrix.transpose(v_matrix)
        np_r_matrix = numpy.matrix.transpose(numpy.array([
            r_transp[i],
            r_transp[i + 1]
        ], dtype=float))
        np_v_matrix = numpy.matrix.transpose(numpy.array([
            v_transp[i],
            v_transp[i + 1]
        ], dtype=float))

        # multiplicando
        qr_matrix = numpy.dot(np_r_matrix, q_transp)
        qv_matrix = numpy.dot(np_v_matrix, q_transp)

        # pondo de volta
        resulting_matrix = r_matrix.copy()
        vesulting_matrix = v_matrix.copy()
        for n in range(len(qr_matrix)):
            resulting_matrix[n][i] = qr_matrix[n][0]
            resulting_matrix[n][i + 1] = qr_matrix[n][1]
        for n in range(len(qv_matrix)):
            vesulting_matrix[n][i] = qv_matrix[n][0]
            vesulting_matrix[n][i + 1] = qv_matrix[n][1]

        return resulting_matrix, vesulting_matrix

    def qr_multiply(self, i):

        q_matrix = self.current_constants().q(i)
        q_transp = numpy.matrix.transpose(q_matrix)

        # transpondo e de-transpondo because gambeta
        r_matrix = self.current_constants().matrix_for_qr_step(i)
        r_transp = numpy.matrix.transpose(r_matrix)
        np_r_matrix = numpy.matrix.transpose(numpy.array([
            r_transp[i],
            r_transp[i + 1]
        ], dtype=float))

        # multiplicando
        qr_matrix = numpy.matmul(np_r_matrix, q_transp)

        # pondo de volta
        resulting_matrix = r_matrix.copy()
        for n in range(len(qr_matrix)):
            resulting_matrix[n][i] = qr_matrix[n][0]
            resulting_matrix[n][i + 1] = qr_matrix[n][1]

        return resulting_matrix

    def qv_multiply(self, i):

        q_matrix = self.current_constants().q(i)
        q_transp = numpy.matrix.transpose(q_matrix)

        # transpondo e de-transpondo because gambeta
        v_matrix = self.current_constants().matrix_for_qv_step(i)
        v_transp = numpy.matrix.transpose(v_matrix)
        np_v_matrix = numpy.matrix.transpose(numpy.array([
            v_transp[i],
            v_transp[i + 1]
        ], dtype=float))

        # multiplicando
        qv_matrix = numpy.matmul(np_v_matrix, q_transp)

        # pondo de volta
        vesulting_matrix = v_matrix.copy()
        for n in range(len(qv_matrix)):
            vesulting_matrix[n][i] = qv_matrix[n][0]
            vesulting_matrix[n][i + 1] = qv_matrix[n][1]

        return vesulting_matrix

    def rotacao_givens_step(self, i):

        matrix = self.current_constants().matrix_for_givens_rotation_step(i).copy()
        self.current_constants().calculate_constants(i)

        sin, cos = self.current_constants().sin_cos(i)

        j = i + 1
        for k in range(len(matrix)):
            ik_value = matrix[i][k]
            jk_value = matrix[j][k]
            matrix[i][k] = cos * ik_value - sin * jk_value
            matrix[j][k] = sin * ik_value + cos * jk_value

        if not self.is_superior_triangular:
            raise NotSuperiorTriangularException(matrix)

        return matrix

    def rotacao_givens(self):

        matrix_size = self.current_constants().matrix_size

        if matrix_size < 2:
            raise MatrixTooSmallToRotateException(matrix_size, self.current_constants().starting_matrix)

        for step_number in range(matrix_size - 1):
            matrix = self.rotacao_givens_step(step_number)
            self.current_constants().set_givens_rotation_step(step_number, matrix)

        return matrix

    def work(self):

        r_matrix = self.rotacao_givens()
        self.current_constants().set_r_matrix(r_matrix)

        for i in range(len(r_matrix) - 1):
            qr_i_matrix, qv_i_matrix = self.old_qr_multiply(i)
            self.current_constants().set_qr_multiplication_step(i, qr_i_matrix)
            self.current_constants().set_qv_multiplication_step(i, qv_i_matrix)

        a_matrix, v_matrix = qr_i_matrix.copy(), qv_i_matrix.copy()

        return a_matrix, v_matrix

    def run_all_iterations(self):
        a_matrix, v_matrix = self.work()
        self.current_constants().set_generated_a_matrix(a_matrix)
        self.current_constants().set_generated_v_matrix(v_matrix)
        self.finish_iteration()

        while len(self.results) < len(self.starting_matrix):
            self.start_new_iteration()
            a_matrix, v_matrix = self.work()
            self.current_constants().set_generated_a_matrix(a_matrix)
            self.current_constants().set_generated_v_matrix(v_matrix)
            self.finish_iteration()

        return a_matrix