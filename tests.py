import unittest
import numpy.testing
from ResultCollection import *
from Result import *
from Matrix import *
from Solver import *
from Truss import *
from Intern import *


class TestEverythingInOneSingleFile(unittest.TestCase):

    # def test_result_collection_generates_correct_matrixes(self):
    #     #GIVEN
    #     result1 = Result(1, [1, 1, 1, 1])
    #     result2 = Result(2, [2, 2, 2, 2])
    #     result3 = Result(3, [3, 3, 3, 3])
    #     result4 = Result(4, [4, 4, 4, 4])
    #     value_matrix = numpy.array([
    #       [1, 0, 0, 0],
    #       [0, 2, 0, 0],
    #       [0, 0, 3, 0],
    #       [0, 0, 0, 4]
    #     ])
    #     vector_matrix = numpy.array([
    #       [1, 2, 3, 4],
    #       [1, 2, 3, 4],
    #       [1, 2, 3, 4],
    #       [1, 2, 3, 4]
    #     ])
    #
    #     # WHEN
    #     collection = ResultCollection([result1, result2, result3, result4])
    #
    #     # THEN
    #     numpy.testing.assert_array_almost_equal(collection.autovalue_matrix, value_matrix)
    #     numpy.testing.assert_array_almost_equal(collection.autovector_matrix, vector_matrix)
    #     print(collection.validate_autovalue_autovector())

    def test_matrix_returns_column_vector_a_correctly(self):
        # GIVEN
        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        # WHEN
        column_vector = matrix.calculate_column_vector_a(0)
        vector_dimension = len(column_vector)
        matrix_dimension = matrix.n

        #THEN
        self.assertEqual(vector_dimension, matrix_dimension - 1)
        self.assertEqual(column_vector, [4, 7])

    def test_matrix_returns_line_vector_a_correctly(self):
        # GIVEN
        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        # WHEN
        line_vector = matrix.calculate_line_vector_a(1)
        vector_dimension = len(line_vector)
        matrix_dimension = matrix.n

        # THEN
        self.assertEqual(vector_dimension, matrix_dimension - 1)
        self.assertEqual(line_vector, [5, 6])

    def test_matrix_explodes_if_trying_to_return_vector_a_for_line_zero(self):
        # GIVEN
        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        #THEN
        with self.assertRaises(InvalidLineVectorAException):
            matrix.calculate_line_vector_a(0)

    def test_matrix_calculates_omega(self):
        # Can´t
        # GIVEN
        matrix = Matrix([
            [2, -1, 1, 3],
            [-1, 1, 4, 2],
            [1, 4, 2, -1],
            [3, 2, -1, 1]
        ])

        # WHEN
        omega = matrix._Matrix__calculate_omega()

        # THEN
        numpy.testing.assert_array_almost_equal([-4.3166247904, 1, 3], omega)

    def test_matrix_returns_submatrix(self):
        # GIVEN
        matrix = Matrix([
            [2, -1, 1, 3],
            [-1, 1, 4, 2],
            [1, 4, 2, -1],
            [3, 2, -1, 1]
        ])

        # WHEN
        sub = matrix.sub_matrix()
        expected_sub = [
            [1, 4, 2],
            [4, 2, -1],
            [2, -1, 1]
        ]

        #THEN
        self.assertEqual(sub.n, matrix.n - 1)
        self.assertTrue(numpy.allclose(sub.intermediate, expected_sub))

    def test_solver_correctly_transforms_matrix_into_tridiagonal_simmetric(self):
        # GIVEN
        matrix = Solver([
            [2, -1, 1, 3],
            [-1, 1, 4, 2],
            [1, 4, 2, -1],
            [3, 2, -1, 1]
        ])

        # WHEN
        transformed_matrix = matrix.transformando()

        # THEN
        for i in range(len(transformed_matrix)):
            for j in range(len(transformed_matrix)):
                if i != j and (i + 1 < j or i > j + 1):
                    self.assertEqual(round(transformed_matrix[i][j], 6), 0)

    def test_add_mass_to_nodes(self):
        # GIVEN
        node = Node(12, 2)

        # WHEN
        k = 0
        while k < 4:
            Node.add_mass(node, 5)
            k += 1

        # THEN
        self.assertEqual(node.mass, 20)

    # Para estes dois testes, vamos trazer os dados dos inputs?
    def test_bar_calculates_properties_correctly(self):
        pass

    def test_checking_bars(self):
        # GIVEN
        bars = Bar.generate_ep_bars()

        # THEN
        for bar in bars:
            print(bar)

    def test_truss_nodes_have_correct_mass(self):
        # GIVEN
        bars = Bar.generate_ep_bars()
        truss = Truss(bars, 14, 12)

        # WHEN
        nodes_masses = []
        for n in range(len(truss.nodes)):
            nodes_masses.append(truss.nodes[n].mass)

        print(nodes_masses)

    def test_eigenvalues_eigenvectors_dont_match(self):
        # GIVEN
        matrix_ruim = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        matrix_bom = [
            [1, 2, 3],
            [2, 3, 4],
            [3, 4, 5]
        ]

        # WHEN
        resolve = Solver(matrix_bom)
        give_matrix_please = resolve.transformando()

        intern = Intern(give_matrix_please.tolist(), resolve.ht.intermediate).use_spectral_shift()
        intern.run_all_iterations()

        collection = ResultCollection(intern.results)

        x = 1

        # THEN
        with self.assertRaises(NotAutovalueAutovectorException):
            collection.validate_autovalue_autovector(matrix_ruim)

    def test_if_symmetric(self):
        # GIVEN
        bars = Bar.generate_ep_bars()
        truss = Truss(bars, 14, 12)
        matrix = truss.stiffness_til

        # THEN
        self.assertTrue(numpy.allclose(matrix, numpy.transpose(matrix)))

    def test_autovalues_teste_b(self):
        # GIVEN
        matrix = self.generate_matrix_teste_b(20)
        expected_autovalue_list = []
        for i in range(1, 21):
            expected_autovalue = (1/2)*(1 - math.cos((2*i - 1)*math.pi/41))**-1
            expected_autovalue_list.append(expected_autovalue)

        # WHEN
        resolve = Solver(matrix)
        give_matrix_please = resolve.transformando()

        intern = Intern(give_matrix_please.tolist(), resolve.ht.intermediate).use_spectral_shift()
        intern.run_all_iterations()
        collection = ResultCollection(intern.results)

        n = len(collection.autovalue_matrix)
        found_autovalue_list = []
        for i in range(n):
            j = n - (i+1)
            found_autovalue_list.append(collection.autovalue_matrix[j][j])

        found_autovalue_list.sort(reverse=True)

        # THEN
        for i in range(20):
            self.assertEqual(numpy.round(found_autovalue_list[i], 7), numpy.round(expected_autovalue_list[i], 7))

    def generate_matrix_teste_b(self, dimensao):
        generated_matrix = numpy.zeros((dimensao, dimensao))
        for i in range(dimensao):

            for j in range(dimensao):
                generated_matrix[i][j] = dimensao - (max(i, j))

        return generated_matrix


if __name__ == '__main__':
    unittest.main(verbosity=2)