import random


class Individuo(object):
    dMax = 10
    dMin = -10
    n_bits = 10

    def __init__(self, bits: str = None):

        # Senão informar os bits, eles são gerados
        self.bits = bits if bits else self.__generate_bits()

    @property
    def bits(self) -> str:
        return self.__bits

    @bits.setter
    def bits(self, value: str):
        """
        :param bits: String com os bits
        """

        # Valida se a quantidade de bits é a mesma que está definida no individuo
        if len(value) != self.n_bits:
            raise Exception(f"Número de bits é inválido: Esperado - {self.n_bits}; Recebido - {len(value)}")

        # Faz todos os calculos novamente para o novo valor de bits
        self.__bits = value
        self.x = int(self.bits, 2)
        self.x_normalized = self.__normalize()
        self.fitness = self.__calc_fitness()

    def __generate_bits(self) -> str:
        """
        :return: String de tamanho Individuo.n_bits com cada caracter podendo ser 0 ou 1
        """
        return "".join([str(random.randint(0, 1)) for i in range(self.n_bits)])

    def __normalize(self) -> float:
        """
        :return: Valor normalizado dentro do valor do dominio
        """
        return self.dMin + (self.dMax - self.dMin) * (self.x / (2 ** self.n_bits - 1))

    def __calc_fitness(self) -> float:
        return self.x_normalized ** 2 - 3 * self.x_normalized + 4

    def __repr__(self):
        return f'Bits = {self.bits};X = {self.x};X_normalizado = {self.x_normalized};Fitness = {self.fitness}'

    def __eq__(self, item):
        return item.bits == self.bits