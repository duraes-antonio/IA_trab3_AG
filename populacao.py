import random

from individuo import Individuo


class Populacao(object):
    n_ind = 100
    elite = None

    def __init__(self):
        # Gera os indiviuos da população
        self.individuos = [Individuo() for i in range(self.n_ind)]
        self.elite = Individuo(self.get_best_or_worst().bits)

    def get_best_or_worst(self, best: bool = True) -> Individuo:
        """
        :best: Flag que indica se é para buscar o melhor ou o pior individuo
        :return: O melhor ou pior individuo da população com base no fitness (Quanto menor, melhor)
        """

        aux = self.individuos[0]
        for ind in self.individuos[1:]:
            if best:
                aux = ind if ind.fitness <= aux.fitness else aux
            else:
                aux = ind if ind.fitness >= aux.fitness else aux

        return aux

    def __apply_elite(self):
        temp_best = self.get_best_or_worst()
        if temp_best.fitness <= self.elite.fitness:
            self.elite = Individuo(temp_best.bits)

        # Se o pior individuo tiver o fitness pior que o da elite
        # Coloca a elite no lugar dele
        else:
            worst = self.get_best_or_worst(False)
            if worst.fitness > self.elite.fitness:
                idx = self.individuos.index(worst)
                self.individuos[idx] = Individuo(self.elite.bits)

    def select(self):
        """
        Seleciona os melhores individuos usando método de torneio com n = 2
        """

        inds_selected = []
        for i in range(self.n_ind):
            # Escolhe aleatoriamente 2 individuos
            ind1 = random.choice(self.individuos)
            ind2 = random.choice(self.individuos)

            # O Individuo selecionado será o de menor fitness
            inds_selected.append(ind1 if ind1.fitness <= ind2.fitness else ind2)

        # Muda os individuos para os que foram selecionados
        self.individuos = inds_selected

        self.__apply_elite()

    def make_crossover(self):
        """
        Faz crossover entre individuos pelo método de 1 corte
        """

        children = []

        while len(children) != self.n_ind:
            # Sorteia a taxa de crossover de 0% a 100%
            tax = random.randint(0, 100)

            # Escolhe aleatoriamente 2 individuos
            ind1 = random.choice(self.individuos)
            ind2 = random.choice(self.individuos)

            # Se a taxa for menor que 60%
            if tax <= 60:
                # Sorteia a posição de corte
                cut_pos = random.randint(1, Individuo.n_bits - 2)

                # Gera os bits
                bits1 = ind1._bits[:cut_pos] + ind2._bits[cut_pos:]
                bits2 = ind2._bits[:cut_pos] + ind1._bits[cut_pos:]

                # Gera os filhos
                children.append(Individuo(bits1))
                children.append(Individuo(bits2))
            else:
                # Adiciona os pais como filhos
                children.append(ind1)
                children.append(ind2)

        # Muda os individuos para os filhos gerados
        self.individuos = children

        self.__apply_elite()

    def apply_mutation(self):
        """
        Aplica mutação bit a bit nos individuos
        """

        # Para cada individuo
        for ind in self.individuos:
            new_bits = ""

            for bit in ind._bits:
                # Sorteia uma taxa entre 0% e 100%
                tax = random.randint(0, 100)

                # Se a taxa for menor ou igual a 1%, sorteia um novo bit, senão mantém o bit atual
                new_bits += str(0 if bit == 1 else 1) if tax <= 1 else bit

            # Troca os bits do individuos
            ind.bits = new_bits

        self.__apply_elite()