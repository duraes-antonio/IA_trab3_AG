import random

from individuo import Individuo


class Populacao(object):
    n_ind = 4

    def __init__(self):
        # Gera os indiviuos da população
        self.individuos = [Individuo() for i in range(self.n_ind)]

    def get_best(self) -> Individuo:
        """
        :return: O melhor individuo da população com base no fitness (Quanto menor, melhor)
        """

        best = self.individuos[0]
        for ind in self.individuos[1:]:
            best = ind if ind.fitness <= best.fitness else best

        return best

    def select(self):
        """
        Seleciona os melhores individuos usando método de torneio com n = 2
        """

        inds_selected = []
        for i in range(self.n_ind):
            # Escolhe aleatoriamente 2 individuos
            r1 = random.randint(0, self.n_ind - 1)
            r2 = random.randint(0, self.n_ind - 1)

            ind1 = self.individuos[r1]
            ind2 = self.individuos[r2]

            # O Individuo selecionado será o de menor fitness
            inds_selected.append(ind1 if ind1.fitness <= ind2.fitness else ind2)

        # Muda os individuos para os que foram selecionados
        self.individuos = inds_selected

    def make_crossover(self):
        """
        Faz crossover entre individuos pelo método de 1 corte
        """

        children = []

        while len(children) != self.n_ind:
            # Sorteia a taxa de crossover de 0% a 100%
            tax = random.randint(0, 100)

            # Escolhe aleatoriamente 2 individuos
            r1 = random.randint(0, self.n_ind - 1)
            r2 = random.randint(0, self.n_ind - 1)

            ind1 = self.individuos[r1]
            ind2 = self.individuos[r2]

            # Se a taxa for menor que 60%
            if tax <= 60:
                # Sorteia a posição de corte
                cut_pos = random.randint(1, Individuo.n_bits - 2)

                # Gera os bits
                bits1 = ind1.bits[:cut_pos] + ind2.bits[cut_pos:]
                bits2 = ind2.bits[:cut_pos] + ind1.bits[cut_pos:]

                # Gera os filhos
                children.append(Individuo(bits1))
                children.append(Individuo(bits2))
            else:
                # Adiciona os pais como filhos
                children.append(ind1)
                children.append(ind2)

        # Muda os individuos para os filhos gerados
        self.individuos = children

    def apply_mutation(self):
        """
        Aplica mutação bit a bit nos individuos
        """

        # Para cada individuo
        for ind in self.individuos:
            new_bits = ""

            for bit in ind.bits:
                # Sorteia uma taxa entre 0% e 100%
                tax = random.randint(0, 100)

                # Se a taxa for menor ou igual a 1%, sorteia um novo bit, senão mantém o bit atual
                new_bits += str(random.randint(0, 1)) if tax <= 1 else bit

            # Troca os bits do individuos
            ind.set_bits(new_bits)