import numpy


class VibrationResult:
    def __init__(self, vib_freq, vib_modes):
        self.vib_freq = vib_freq
        self.vib_modes = vib_modes

    def __str__(self):
        return self.pretty()

    def pretty(self):
        return f"------------------------------------------------------------------------------------------\n" \
            f"Frequência de vibração: {round(self.vib_freq, 6)} \nModo de vibração associado:\n {numpy.matrix.round(self.vib_modes, 6)}" \
            f"\n------------------------------------------------------------------------------------------\n"

