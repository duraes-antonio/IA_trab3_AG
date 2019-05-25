import os
from matplotlib import pyplot as pl

from individuo import Individuo
from populacao import Populacao


diretorio = "CSVs"  # Diretório em que serão salvo os arquivos
bests = []          # Estrutura para armazenar os melhores fitness de cada execução para cada geração

# Cria pasta se não existir
if not os.path.exists(diretorio):
    os.makedirs(diretorio)

num_exec = 10
generations = [5, 10]

best_x = {generation: None for generation in generations}

# Para cada execução
for t in range(1, num_exec + 1):
    bests.append({generation: [] for generation in generations})   # Cria as listas da execução de cada número de gerações máximas

    for max_generations in generations:
        # Abre arquivo
        arq = open(f"{diretorio}/{Populacao.n_ind}i_{max_generations}g_{t}exec.csv", "wt")

        # Gera população
        populacao = Populacao()

        for i in range(max_generations):
            populacao.select()
            populacao.make_crossover()
            populacao.apply_mutation()

            best = Individuo(populacao.elite.bits)

            if best_x[max_generations] is None or best_x[max_generations][0].fitness > best.fitness:
                best_x[max_generations] = (best, t)

            # Escreve no arquivo e adiciona o melhor fitness na estrutura
            arq.write(f"{i+1};{best}\n")
            bests[-1][max_generations].append(best.fitness)

        arq.close()

# Estrutura que armazena a soma de cada geração de cada execução
fitness_sum = {generation: [0] * generation for generation in generations}

# Faz as somas
for best_exec in bests:
    for generation in generations:
        for i in range(generation):
            fitness_sum[generation][i] += best_exec[generation][i]


# Calcula médias e plota
for generation in generations:
    media = []
    for i in range(generation):
        media.append(fitness_sum[generation][i] / num_exec)

    val_eixo_x = [i for i in range(1, generation + 1)]

    pl.plot(val_eixo_x, media, marker='o')

    # Nomeie os eixos X e Y
    pl.xlabel("Número da geração")
    pl.ylabel("Fitness i-ésimo individuo")

    # Marque os valores de fitness, forma destacada (em vermelho) no gráfico
    for i in range(len(media)):
        pl.text(val_eixo_x[i], media[i], f"{media[i]:.5}", color="red", fontsize=10)

    pl.text(1, media[-1], f"{best_x[generation][0].x_normalized}", color="blue", fontsize=10)

    print(f"Arquivo com melhor x para {generation} gerações = {Populacao.n_ind}i_{generation}g_{best_x[generation][1]}exec.csv")

    pl.show()
