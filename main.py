import os
from matplotlib import pyplot as pl

from individuo import Individuo
from populacao import Populacao


diretorio = "CSVs"  # Diretório em que serão salvo os arquivos
bests = []          # Estrutura para armazenar os melhores fitness de cada execução para cada geração

# Cria pasta se não existir
if not os.path.exists(diretorio):
    os.makedirs(diretorio)

# Para cada execução
for t in range(1, 11):
    bests.append({5: [], 10: []})   # Cria as listas da execução de cada número de gerações máximas

    for max_generations in [5, 10]:
        # Abre arquivo
        arq = open(f"{diretorio}/{Populacao.n_ind}i_{max_generations}g_{t}exec.csv", "wt")

        # Gera população
        populacao = Populacao()

        for i in range(max_generations):
            populacao.select()
            populacao.make_crossover()
            populacao.apply_mutation()

            best = Individuo(populacao.elite.bits)

            # Escreve no arquivo e adiciona o melhor fitness na estrutura
            arq.write(f"{i+1};{best}\n")
            bests[-1][max_generations].append(best.fitness)

        arq.close()

# Estrutura que armazena a soma de cada geração de cada execução
fitness_sum = {5: [0] * 5, 10: [0] * 10}

# Faz as somas
for best_exec in bests:
    for generation in [5, 10]:
        for i in range(generation):
            fitness_sum[generation][i] += best_exec[generation][i]


# Calcula médias e plota
for generation in [5, 10]:
    media = []
    for i in range(generation):
        media.append(fitness_sum[generation][i] / 10)

    val_eixo_x = [i for i in range(1, generation + 1)]

    pl.plot(val_eixo_x, media, marker='o')

    # Nomeie os eixos X e Y
    pl.xlabel("Número da geração")
    pl.ylabel("Fitness i-ésimo individuo")

    # Marque os valores de fitness, forma destacada (em vermelho) no gráfico
    for i in range(len(media)):
        pl.text(val_eixo_x[i], media[i], f"{media[i]:.5}", color="red", fontsize=10)

    pl.show()
