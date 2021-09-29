from math import sqrt


class Result:

    def __init__(self, autovalue, autovector):
        self.autovalue = autovalue
        self.autovector = autovector

    def pretty(self):
        return f"Autovalor: {round(self.autovalue, 12)} // Autovetor associado: {self.rounded_autovector(7)}"

    def __str__(self):
        return self.pretty()

    def rounded_autovector(self, n):
        rounded_autovector = [None] * len(self.autovector)
        for i in range(len(self.autovector)):
            rounded_autovector[i] = round(self.autovector[i], n)
        return rounded_autovector

    def rounded_autovalue(self, n):
        return round(self.autovalue, n)

    def __eq__(self, result):
        if not isinstance(result, Result):
            return False
        if round(self.autovalue, 6) != round(result.autovalue, 6):
            return False
        for i in range(len(self.autovector)):
            if abs(round(self.autovector[i], 6)) != abs(round(result.autovector[i], 6)):
                return False
        return True

    def __lt__(self, result):
        if result.autovalue < 0 or self.autovalue < 0:
            return self.autovalue < result.autovalue

        return sqrt(self.autovalue) < sqrt(result.autovalue)