import math
from VibrationResult import *


class Truss:
    def __init__(self, bars, total_nodes, free_nodes):
        self.bars = bars
        self.nodes = []
        # Adicionando nós livres
        for i in range(free_nodes):
            self.nodes.append(Node(i+1, False))
        # Adicionando nós fixos
        for i in range(free_nodes, total_nodes):
            self.nodes.append(Node(i+1, True))
        self.first_fixed_node_number = free_nodes + 1
        self.__calculate_nodes()
        self.total_stiffness_matrix = self.__calculate_total_stiffness()
        self.bigemu = self.__calculate_mass_bigemu()
        self.sqrt_bigemu = self.__calculate_sqrt_bigemu()
        self.stiffness_til = self.__generate_stiffness_til()

    # Calcula as massas dos nós
    def __calculate_nodes(self):
        for i in range(len(self.bars)):
            bar = self.bars[i]
            first_node = self.nodes[bar.node_numbers[0] - 1]
            second_node = self.nodes[bar.node_numbers[1] - 1]
            first_node.add_mass(bar.mass/2)
            second_node.add_mass(bar.mass/2)

    # Monta a matriz de rigidez total (K)
    def __calculate_total_stiffness(self):
        n = self.first_fixed_node_number - 1
        total_stiffness_matrix = numpy.zeros((n*2, n*2))
        for bar in self.bars:
            for line in range(4):
                for column in range(4):
                    indexes = bar.stiffness_matrix_indexes[line][column]
                    n = indexes[0]
                    m = indexes[1]
                    if n < 2*(self.first_fixed_node_number - 1) and m < 2*(self.first_fixed_node_number - 1):
                        total_stiffness_matrix[n][m] += bar.stiffness_matrix[line][column]
        return total_stiffness_matrix

    # Calcula a matriz de massas (M), com as massas de cada nó
    def __calculate_mass_bigemu(self):
        n = self.first_fixed_node_number - 1
        bigemu = numpy.zeros((n*2, n*2))
        for node in self.nodes:
            if not node.is_fixed:
                bigemu[(2*node.index)-1-1][(2*node.index)-1-1] = node.mass
                bigemu[(2*node.index)-1][(2*node.index)-1] = node.mass
        return bigemu

    # Calcula M^(-1/2)
    def __calculate_sqrt_bigemu(self):
        size = len(self.bigemu)
        sqrt_bigemu = numpy.zeros((size, size))
        for i in range(size):
            sqrt_bigemu[i][i] = 1/math.sqrt(self.bigemu[i][i])

        return sqrt_bigemu

    # Calcula K~ = [M^(-1/2)*K*M^(-1/2)]
    def __generate_stiffness_til(self):
        aux = numpy.matmul(self.sqrt_bigemu, self.total_stiffness_matrix)
        stiffness_til = numpy.matmul(aux, self.sqrt_bigemu)

        return stiffness_til

    # Calcula as 5 menores frequências (ω) e respectivos modos de vibração (z)
    def calculate_sorted_frequencies_and_vibrational_modes(self, results):
        sorted_frequencies_and_vibrational_modes = []
        for i in range(min(5, len(results))):
            result = results[i]
            vib_freq = math.sqrt(result.autovalue)
            vib_modes = numpy.matmul(self.sqrt_bigemu, result.autovector)
            vib = VibrationResult(vib_freq, vib_modes)
            sorted_frequencies_and_vibrational_modes.append(vib)

        return sorted_frequencies_and_vibrational_modes

    def pretty_truss(self, result):
        return f"\n{result}\n"

    @staticmethod
    def ep_truss():
        bars = Bar.generate_ep_bars()
        return Truss(bars, 14, 12)

    @staticmethod
    def triforce_truss():
        bars = Bar.generate_triforce()
        return Truss(bars, 6, 3)


class Bar:
    def __init__(self, length, angle, node_numbers):
        self.elasticity_module = 200
        self.mass_density = 7.8 * 10**3
        self.section_area = 10**-1
        self.length = length
        self.angle = angle
        self.node_numbers = node_numbers
        self.mass = self.mass_density*self.length*self.section_area
        self.sin = math.sin(math.radians(self.angle))
        self.cos = math.cos(math.radians(self.angle))
        self.stiffness_matrix = self.__stiffness_matrix()
        self.stiffness_matrix_indexes = self.__stiffness_matrix_indexes()

    def __str__(self):
        return self.pretty()

    def pretty(self):
        return f"Hello. I'm a {numpy.round(self.length, 3)}m bar at a {numpy.round(self.angle, 3)}º angle connecting nodes {self.node_numbers[0]} and {self.node_numbers[1]}"

    # Dados
    @staticmethod
    def generate_ep_bars():
        bars = [
            Bar(node_numbers=[1, 2], angle=0, length=10),
            Bar(node_numbers=[1, 4], angle=90, length=10),
            Bar(node_numbers=[1, 5], angle=45, length=14.14213562373095),
            Bar(node_numbers=[2, 5], angle=90, length=10),
            Bar(node_numbers=[2, 4], angle=135, length=14.14213562373095),
            Bar(node_numbers=[3, 4], angle=0, length=10),
            Bar(node_numbers=[3, 7], angle=90, length=10),
            Bar(node_numbers=[3, 8], angle=45, length=14.14213562373095),
            Bar(node_numbers=[4, 5], angle=0, length=10),
            Bar(node_numbers=[4, 8], angle=90, length=10),
            Bar(node_numbers=[4, 9], angle=45, length=14.14213562373095),
            Bar(node_numbers=[5, 6], angle=0, length=10),
            Bar(node_numbers=[5, 9], angle=90, length=10),
            Bar(node_numbers=[5, 8], angle=135, length=14.14213562373095),
            Bar(node_numbers=[6, 9], angle=135, length=14.14213562373095),
            Bar(node_numbers=[6, 10], angle=90, length=10),
            Bar(node_numbers=[7, 8], angle=0, length=10),
            Bar(node_numbers=[8, 9], angle=0, length=10),
            Bar(node_numbers=[8, 11], angle=90, length=10),
            Bar(node_numbers=[8, 12], angle=45, length=14.14213562373095),
            Bar(node_numbers=[9, 10], angle=0, length=10),
            Bar(node_numbers=[9, 11], angle=135, length=14.14213562373095),
            Bar(node_numbers=[9, 12], angle=90, length=10),
            Bar(node_numbers=[11, 12], angle=0, length=10),
            Bar(node_numbers=[11, 13], angle=116.5650511770780, length=11.18033988749895),
            Bar(node_numbers=[11, 14], angle=33.69006752597979, length=18.02775637731995),
            Bar(node_numbers=[12, 13], angle=146.3099324740202, length=18.02775637731995),
            Bar(node_numbers=[12, 14], angle=63.43494882292201, length=11.18033988749895)
        ]

        return bars

    # Dados
    @staticmethod
    def generate_triforce():
        bars = [
            Bar(node_numbers=[1, 2], angle=120, length=10),
            Bar(node_numbers=[1, 3], angle=60, length=10),
            Bar(node_numbers=[2, 3], angle=0, length=10),
            Bar(node_numbers=[2, 4], angle=120, length=10),
            Bar(node_numbers=[2, 5], angle=60, length=10),
            Bar(node_numbers=[3, 5], angle=120, length=10),
            Bar(node_numbers=[3, 6], angle=60, length=10),
            Bar(node_numbers=[4, 5], angle=0, length=10),
            Bar(node_numbers=[5, 6], angle=0, length=10)
        ]

        return bars

    # Calcula a matriz de rigidez de cada barra (K{i, j})
    def __stiffness_matrix(self):
        c2 = self.cos**2
        s2 = self.sin**2
        cs = self.cos*self.sin
        sincos_matrix = numpy.array([
            [c2, cs, -c2, -cs],
            [cs, s2, -cs, -s2],
            [-c2, -cs, c2, cs],
            [-cs, -s2, cs, s2]
        ], dtype=float)
        return (self.section_area*self.elasticity_module/self.length) * sincos_matrix

    # Define as posições da matriz de rigidez total (K)
    # onde os termos da matriz de rigidez de cada barra {i, j} (K{i, j}) entrarão
    def __stiffness_matrix_indexes(self):
        i = self.node_numbers[0]
        j = self.node_numbers[1]

        return numpy.array([
            [[2*i-1-1, 2*i-1-1], [2*i-1-1, 2*i-1], [2*i-1-1, 2*j-1-1], [2*i-1-1, 2*j-1]],
            [  [2*i-1, 2*i-1-1],   [2*i-1, 2*i-1],   [2*i-1, 2*j-1-1],   [2*i-1, 2*j-1]],
            [[2*j-1-1, 2*i-1-1], [2*j-1-1, 2*i-1], [2*j-1-1, 2*j-1-1], [2*j-1-1, 2*j-1]],
            [  [2*j-1, 2*i-1-1],   [2*j-1, 2*i-1],   [2*j-1, 2*j-1-1],   [2*j-1, 2*j-1]]
        ])


class Node:
    def __init__(self, index, is_fixed):
        self.index = index
        self.is_fixed = is_fixed
        self.mass = 0

    def add_mass(self, mass):
        self.mass += mass
