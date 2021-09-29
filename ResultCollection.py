import numpy
from EPExceptions import *
from Message import Message


class ResultCollection:
    def __init__(self, results):
        results.sort()
        self.__results = results
        self.autovalue_matrix = self.generate_autovalue_matrix()
        self.autovector_matrix = self.generate_autovector_matrix()

#  Montamos a matriz de autovalores, calculados anteriormente
    def generate_autovalue_matrix(self):
        n = len(self.__results)
        autovalue_matrix = numpy.zeros((n, n))
        for i in range(n):
            result = self.__results[i]
            autovalue_matrix[i][i] = result.autovalue

        return autovalue_matrix

    # Montamos a matriz de autovetores, calculados anteriormente
    def generate_autovector_matrix(self):
        n = len(self.__results)
        autovector_matrix = []
        for i in range(n):
            result = self.__results[i]
            autovector_matrix.append(result.autovector)

        autovector_matrix = numpy.transpose(autovector_matrix)

        return autovector_matrix

    # Transpõe uma cópia da matriz de autovetores
    def autovector_at_index(self, i):
        copy = self.autovector_matrix.copy()
        transposed_copy = numpy.transpose(copy)
        return transposed_copy[i]

    # Valida que A.vi = λi.vi
    def validate_autovalue_autovector(self, matrix):
        message = Message()
        for i in range(len(matrix)):
            # Faz o produto entre a matriz original A e o autovetor vi
            transformed_autovector = numpy.matmul(matrix, self.autovector_at_index(i))

            # Faz o produto entre o autovalor λi e o autovetor vi
            scaled_autovector = numpy.multiply(self.autovalue_matrix[i][i], self.autovector_at_index(i))

            # Valida que os resultados obtidos anteriormente (A.vi) e (λi.vi) são iguais, assumindo um erro
            if not numpy.allclose(transformed_autovector, scaled_autovector, atol=1e-05):
                errors = []
                for n in range(len(transformed_autovector)):
                    errors.append(abs(transformed_autovector[n] - scaled_autovector[n]))

                max_error = max(errors)

                raise NotAutovalueAutovectorException(self.autovalue_matrix[i][i], self.autovector_at_index(i), matrix, max_error, errors)
            else:
                message.add(f'\n------------------------------------------------------------------------------------\n'
                            f'Para o seguinte autovetor v:\n'
                            
                            f'\n{numpy.matrix.round(self.autovector_matrix[i], 6)}\n'
                            
                            f'\ntemos A*v igual a:\n'
                            
                            f'\n{numpy.matrix.round(transformed_autovector, 6)}\n'
                            
                            f'\nO mesmo resultado que obtemos através do produto do autovalor λ = {numpy.round(self.autovalue_matrix[i][i], 6)} pelo autovetor v:\n'
                            
                            f'\n{numpy.matrix.round(scaled_autovector, 6)}\n'
                            
                            f'\nTemos, portanto, que A.vi = λi.vi!')

        return message

    # Valida que a matriz de autovetores é ortogonal e printa isso na tela
    def pretty_ortogonal(self):
        # Calcula a transposta da matriz de autovetores
        transposed_autovector_matrix = numpy.transpose(self.autovector_matrix)

        # Calcula a inversa da matriz de autovetores
        inversed_autovector_matrix = numpy.linalg.inv(self.autovector_matrix)

        # Se for transposta, mostra na tela
        if numpy.allclose(transposed_autovector_matrix, inversed_autovector_matrix):
            return (f'\nA matriz de autovetores é ortogonal!\n'
                    f'\n---------------------------------------------------------------------------------------------\n'
                    f'A matriz de autovetores transposta é\n'
                    f'\n---------------------------------------------------------------------------------------------\n'
                    f'\n{numpy.matrix.round(transposed_autovector_matrix, 6)}\n'
                    f'\n---------------------------------------------------------------------------------------------\n'
                    f'A matriz de autovetores inversa é\n'
                    f'\n---------------------------------------------------------------------------------------------\n'
                    f'\n{numpy.matrix.round(inversed_autovector_matrix, 6)}'
                    f'\n---------------------------------------------------------------------------------------------\n'
                    f'Observe que ambas são iguais, provando que a matriz de autovetores é, de fato, ortogonal!')

        # Se não for, raise exception
        else:
            raise NotOrtogonalException(transposed_autovector_matrix, inversed_autovector_matrix)

    # Printa a matriz de autovalores e a matriz de autovetores, arredondados para 6 casas decimais
    def pretty(self):
        return (f'\nA matriz de autovalores associada à matriz original A é:\n '
                f'\n-------------------------------------------------------------------------------------------------\n'
                f'\n{numpy.matrix.round(self.autovalue_matrix, 6)}\n'
                f'\n-------------------------------------------------------------------------------------------------\n'
                f'A matriz de autovetores associada à sua matriz original A é:\n '
                f'\n-------------------------------------------------------------------------------------------------\n'
                f'\n{numpy.matrix.round(self.autovector_matrix, 6)}')

