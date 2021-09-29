# CABEÇALHO
# Exercício Programa 2
# Autovalores e Autovetores de Matrizes Reais Simétricas - O Algoritmo QR
# Nomes: Giovanni Simoes Cotrim e Julia Melnic Correa
# Respectivos Números USP: 11302543 e 10823640
# Prof.: Henrique Von Dreifus


from EP import EP
import re
from Animation import Animation
from Truss import *
from matplotlib import pyplot as plt


def main():
    print('\nVocê deseja rodar qual tarefa?\n'
          '1) Teste 4.1-a)\n'
          '2) Teste 4.1-b)\n'
          '3) Aplicação treliça\n'
          '4) Gerar GIF\n'
          '5) Gerar GIF com parâmetros customizados\n'
          '\n OBS: RODE SÓ O NÚMERO, SEM PARÊNTESES!')

    auxiliar = input()

    if int(auxiliar) == 1:
        EP.answer_a().show()
    elif int(auxiliar) == 2:
        EP.answer_b().show()
    elif int(auxiliar) == 3:
        EP.answer_c().show()
    elif int(auxiliar) == 4:
        print(f"Vamos gerar um gif!")
        print(f"Atenção: Isso vai criar alguns arquivos PNG no diretório onde você está executando o script")
        truss = Truss.ep_truss()
        ep = EP(truss=truss)
        good_vibes = truss.calculate_sorted_frequencies_and_vibrational_modes(ep.intern.results)
        frames = 100
        magnitude = 100
        animation = Animation("EP", truss, good_vibes, magnitude)
        step = int(8356 / frames)
        for timelapse in range(0, 8356, step):
            print(f"\rCriando GIF: {int(timelapse * 100 / 8356)}%", end="")
            animation.timelapse(timelapse)
            animation.create_lines_figure(str(timelapse))
        animation.build_gif()
        print(f"\rCriando GIF: 100% OK")
        print(f"Arquivo EP.gif gerado!")
    elif int(auxiliar) == 5:
        print(f"Vamos gerar um gif!")
        print(f"Atenção: Isso vai criar alguns arquivos PNG no diretório onde você está executando o script")
        truss = Truss.ep_truss()
        ep = EP(truss=truss)
        good_vibes = truss.calculate_sorted_frequencies_and_vibrational_modes(ep.intern.results)
        print(f"Quantos frames você deseja criar? (Sugerimos 100 frames): ", end="")
        frames = int(input())
        print(f"E por qual fator deseja multiplicar os modos de vibração?\nSugerimos 100 para uma movimentação sutil, ou 500 para uma movimentação exagerada: ", end="")
        magnitude = int(input())
        print("Por favor, aguarde...")
        animation = Animation("EP", truss, good_vibes, magnitude)
        step = int(8356/frames)
        for timelapse in range(0, 8356, step):
            print(f"\rCriando GIF: {int(timelapse*100/8356)}%", end="")
            animation.timelapse(timelapse)
            animation.create_lines_figure(str(timelapse))
        animation.build_gif()
        print(f"\rCriando GIF: 100% OK")
        print(f"Arquivo EP.gif gerado!")
    elif int(auxiliar) == 6:
        print(f"Vamos gerar um gif!")
        print(f"Atenção: Isso vai criar alguns arquivos PNG no diretório onde você está executando o script")
        truss = Truss.triforce_truss()
        ep = EP(truss=truss)
        good_vibes = truss.calculate_sorted_frequencies_and_vibrational_modes(ep.intern.results)
        frames = 100
        magnitude = 100
        animation = Animation("Triforce", truss, good_vibes, magnitude)
        step = int(8356 / frames)
        for timelapse in range(0, 8356, step):
            print(f"\rCriando GIF: {int(timelapse * 100 / 8356)}%", end="")
            animation.timelapse(timelapse)
            animation.create_lines_figure(str(timelapse))
        animation.build_gif()
        print(f"\rCriando GIF: 100% OK")
        print(f"Arquivo EP.gif gerado!")


def user_wants(question, default=False):
    # str_default = str(default)
    print(question)
    aux = input()
    return re.search("^[Ss](?:[Ii][Mm])?$", aux)

main()
