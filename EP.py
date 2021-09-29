from Solver import *
from Intern import *
from ResultCollection import ResultCollection
from Message import Message
from Truss import *


class EP:
    def __init__(self, matrix=None, truss=None):
        if truss is not None:
            self.truss = truss
            self.matrix = self.truss.stiffness_til
        elif matrix is not None:
            self.matrix = matrix
        else:
            print("This should not happen. Please throw exception :)")
        self.solver = Solver(self.matrix)
        self.intern = Intern(self.solver.transformando().tolist(), self.solver.ht.intermediate).use_spectral_shift()
        self.intern.run_all_iterations()
        self.intern.results.sort()
        self.collection = ResultCollection(self.intern.results)

    @staticmethod
    def answer_a():
        ep = EP(matrix=EP.__ex_a_matrix())
        answer = Message()
        answer.add_soft_texts([f"A matriz original A é:", f"{ep.matrix}"])
        answer.add(ep.collection.pretty())
        answer.add_hard_break()
        answer.add(ep.collection.validate_autovalue_autovector(ep.matrix).full_text())
        answer.add_hard_break()
        answer.add(ep.collection.pretty_ortogonal())

        return answer

    @staticmethod
    def answer_b():
        ep = EP(matrix=EP.__ex_b_matrix())
        answer = Message()
        answer.add_soft_texts([f"A matriz original A é:", f"{ep.matrix}"])
        answer.add(ep.collection.pretty())
        answer.add_hard_break()
        answer.add(ep.collection.validate_autovalue_autovector(ep.matrix).full_text())
        answer.add_hard_break()
        answer.add(ep.collection.pretty_ortogonal())

        return answer

    @staticmethod
    def answer_c():
        bars = Bar.generate_ep_bars()
        truss = Truss(bars, 14, 12)
        ep = EP(truss=truss)
        ep.collection.pretty_ortogonal()
        ep.collection.validate_autovalue_autovector(ep.matrix)
        ep.collection.pretty()

        lowest = ep.truss.calculate_sorted_frequencies_and_vibrational_modes(ep.intern.results)
        answer = Message()
        answer.add('\nAs cinco menores frequências, e modos de vibração associados, são:\n')
        for result in lowest:
            answer.add(truss.pretty_truss(result))

        return answer

    @staticmethod
    def __ex_a_matrix():
        return [
            [2, 4, 1, 1],
            [4, 2, 1, 1],
            [1, 1, 1, 2],
            [1, 1, 2, 1]
        ]

    @staticmethod
    def __ex_b_matrix():
        dimensao = 20
        generated_matrix = numpy.zeros((dimensao, dimensao))
        for i in range(dimensao):

            for j in range(dimensao):
                generated_matrix[i][j] = dimensao - (max(i, j))

        return generated_matrix
