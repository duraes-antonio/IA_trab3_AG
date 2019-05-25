from random import randint, choice

from individuo import Individuo


class Populacao(object):
	n_ind = 4
	elite = None

	def __init__(self, tx_mutacao: int, tx_cross: int, n_individ: int = None):

		if(n_individ): self.n_ind = n_individ

		# Gera os indiviuos da população
		self.individuos: [Individuo] = [Individuo() for i in range(self.n_ind)]
		self.elite = Individuo(self.get_best_or_worst().bits)
		self.__taxa_mut = tx_mutacao
		self.__taxa_cross = tx_cross

	def get_best_or_worst(self, best: bool = True) -> Individuo:
		"""
		:best: Flag que indica se é para buscar o melhor ou o pior individuo
		:return: O melhor ou pior individuo da população com base no fitness (Quanto menor, melhor)
		"""

		aux = self.individuos[0]
		mult = 1 if best else -1

		for ind in self.individuos[1:]:
			aux = ind if ind.fitness * mult <= aux.fitness * mult else aux

		return aux

	def __apply_elite(self):
		temp_best = self.get_best_or_worst()

		if temp_best.fitness <= self.elite.fitness:
			self.elite = Individuo(temp_best.bits)

		# Se o pior individuo tiver o fitness pior que o da elite
		# Coloca a elite no lugar dele
		else:
			worst = self.get_best_or_worst(best=False)

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
			ind1 = choice(self.individuos)
			ind2 = choice(self.individuos)

			# O Individuo selecionado será o de menor fitness
			inds_selected.append(ind1 if ind1.fitness <= ind2.fitness else ind2)

		# Muda os individuos para os que foram selecionados
		self.individuos = inds_selected

		self.__apply_elite()

	def make_crossover(self):
		"""
		Faz crossover entre individuos pelo método de 1 corte
		"""

		children: [Individuo] = []

		while len(children) != self.n_ind:
			# Sorteia a taxa de crossover de 0% a 100%
			tax = randint(0, 100)

			# Escolhe aleatoriamente 2 individuos
			ind1: Individuo = choice(self.individuos)
			ind2: Individuo = choice(self.individuos)

			# Se a taxa estiver no valor aceitável
			if tax <= self.__taxa_cross:
				# Sorteia a posição de corte
				cut_pos = randint(1, Individuo.n_bits - 2)

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

		self.__apply_elite()

	def __mutar_bit(self, bit: str):
		return ("0" if bit == "1" else "1") if randint(1, 100) < self.__taxa_mut else bit

	def apply_mutation(self):
		"""
		Aplica mutação bit a bit nos individuos
		"""

		# Para cada individuo
		for ind in self.individuos:
			new_bits = "".join([self.__mutar_bit(bit) for bit in ind.bits])

			# Troca os bits do individuos
			ind.bits = new_bits

		self.__apply_elite()