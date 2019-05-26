# Inteligência Artificial - Trabalho 3 - Algoritmo Genético

<p align="center"/>
<img src="https://3718aeafc638f96f5bd6-d4a9ca15fc46ba40e71f94dec0aad28c.ssl.cf1.rackcdn.com/journal-genetics.png" alt="Smiley face" width="420">

## APRESENTAÇÃO

INTEGRANTES:
* Antônio Carlos D. da Silva
* Joel Will Belmiro

CONTEXTO:
* Disciplina: Inteligência Artificial (Sistemas de Informação, optativa do 8º Período)
* Implementação e Exploração do Algoritmo Genético (com cromossomo em binário e seleção por torneio)


## 1. EXPLICAÇÃO TEÓRICA DO ALGORITMO
<p align="justify"/>
Inspirado em conceitos pertencentes à Teoria da Seleção Natural, registrada em nome de Charles Robert Darwin [1], o algorítimo genético visa tirar proveito de mecanismos semelhantes aos naturais para selecionar, modificar ou criar uma nova solução para um problema a partir de soluções pais.
<br>

<p align="justify"/>
O algorítimo genético herda da Biologia não só os mecanismos para encontrar a melhor solução mas também a modelagem utilizada para definir a estrutura de uma solução, ou melhor, de um indivíduo. Cada valor que representa uma solução pode ser modelado como um indivíduo, contendo seu código genético e sua aptidão.
<br>

<p align="justify"/>
É possível traçar uma analogia, em que uma fórmula matemática ou objetivo representa esse ambiente responsável por definir quem é mais adequado. Dessa forma, o código genético (simboliza um parâmetro) do indivíduo aliado ao ambiente (fórmula ou processamento que recebe a entrada) determina o quão apto (valor fitness) cada indivíduo é, sendo possível, selecionar tal indivíduo, reproduzi-lo e impulsionar pequenas alterações em sua genética.
<br>

<p align="justify"/>
O algoritmo favorece a descoberta de bons resultados para, principalmente, problemas em que sua solução final não é conhecida ou que não há uma solução ótima alcançável [2], sendo satisfatórias, soluções que oscilem entre uma faixa de aceitabilidade, graças à sua aleatoriedade, seleção e variação de soluções promissoras.
<br>

## 2. PROBLEMA PROPOSTO

<p align="justify"/>
O algorítimo teve como tarefa encontrar o valor para o parâmetro X que minimizasse o resultado da função abaixo:
<h3 align="center">f(x) = x² − 3x + 4</h3>

<p align="justify"/>
Após plotar o gráfico 2D da função acima na ferramenta Geogebra, fica claro que seu ponto de mínimo é de 1.75, e é atingido para X com valor de 1.5.

<p align="center"/>
<img src="https://github.com/duraes-antonio/IA_trab3_AG/blob/master/doc/imgs/graf_1.png" alt="gráfico da função" width="450">
<br>

## 3. IMPLEMENTAÇÃO

### 3.1 Modelagem

### 3.1.1 Indivíduo

*Modelagem: Cada indivíduo foi modelado como uma classe contendo seu número de bits (comprimento de seu cromossomo), a cadeia de bit em si, um valor máximo e um valor mínimo de aptidão.*

```Python
class Individuo(object):
  """Representa um indivíduo biológico com código genético e valor de aptdão."""
    
  n_bits = 10 # Comprimento do cromossomo
  dMax = 10   # Valor máximo dentro do domínio da função
  dMin = -10  # Valor mínimo dentro do domínio da função
```

*Instanciação: Para instanciar um indivíduo é necessário pasar o tamanho de sua cadeia genética. Também é possível passar uma cadeia genética já existente, para 'clonar' um indivíduo.*
```Python
  def __init__(self, n_bits: int, bits: str = None):
    """Instancia um indivíduo novo ou a partir de um código genético existente."""

    self.n_bits = n_bits

    # Senão informar os bits, eles são gerados
    self.bits = bits if bits else self.__generate_bits()
```

*Geração de código genético: Se a cadeia de bits estiver vazia, a função abaixo gera uma cadeia randomicamente para inicializar o código genético do indivíduo.*
```Python
  def __generate_bits(self) -> str:
    """
    :return: String de tamanho Individuo.n_bits com cada caracter podendo ser 0 ou 1
    """
    return "".join([str(random.randint(0, 1)) for i in range(self.n_bits)])
```
<br>

### 3.1.2 População

*Modelagem: A população ficou responsável por armazenar informações como o número de indivíduos, a taxa de mutação, taxa de crossover, além de armazenar o melhor (indivíduo elitizado) a cada geração.*
```Python
class Populacao(object):
  """Representa um conjunto de indivíduos. Contém operações de seleção, crossover e mutação."""
  elite = None  # Não há elite até a população ser preenchida
  n_ind = 0     # Só haverá indivíduos quando a população for preenchida

  def __init__(self, tx_mutacao: int, tx_cross: int, n_individ: int,
	             n_bits: int, interv_min: int = None, interv_max: int = None):
    """
    Instancia uma população com N indivíduos e com as taxas recebidas.
    :param tx_mutacao: Inteiro (entre 0 e 100) que representa a chance de um bit ser alterado.
    :param tx_cross: Inteiro (entre 0 e 100) que representa a chance de ocorrer um crossover.
    :param n_individ: Inteiro positivo. É a quantidade de indivíduos da população.
    :param n_bits: Inteiro positivo. É o tamanho da cadeia genética de cada indivíduo.
    :param interv_min: Valor real que representa o valor mínimo que um código genético pode assumir.
    :param interv_max: Valor real que representa o valor máximo que um código genético pode assumir.
    """

    # Atualize as propriedades com os valores recebidos
    self.n_ind = n_individ
    self.__taxa_mut = tx_mutacao
    self.__taxa_cross = tx_cross
    self.__n_bits = n_bits

    # Gera os indiviuos da população
    self.individuos: [Individuo] = [Individuo(n_bits=n_bits) for i in range(self.n_ind)]
    self.elite = Individuo(self.__n_bits, self.get_best_or_worst().bits)
```

*Elitização: O processo de elitização garante que entre os indivíduos de cada geração, haverá o indivíduo com o código genético mais apto de todas gerações até então.*
```Python
  def __apply_elite(self):
  
    # Obtenha o mais apto indivíduo
    temp_best = self.get_best_or_worst()
    
    # Se o indivíduo acima for mais apto que o da elite, atualize a elite
    if temp_best.fitness <= self.elite.fitness:
      self.elite = Individuo(self.__n_bits, temp_best.bits)

    # Se o pior individuo for menos apto que o da elite
    else:
      worst = self.get_best_or_worst(best=False)
      
      # Substitua o pior pela elite
      if worst.fitness > self.elite.fitness:
        idx = self.individuos.index(worst)
        self.individuos[idx] = Individuo(self.__n_bits, self.elite.bits)
```

*Seleção: O processo de seleção utiliza a técnica de torneio, ou seja, N indivíduos (neste caso, n = 2) são sorteados e o que for mais apto permanece na população. O processo ocorre K (número de indivíduos na população) vezes.*
```Python
  def select(self):
    """Seleciona os melhores individuos usando método de torneio com n = 2"""

    inds_selected = []
    
    # Para i, de 0 até o número de indivíduos
    for i in range(self.n_ind):

      # Escolha aleatoriamente 2 individuos
      ind1 = choice(self.individuos)
      ind2 = choice(self.individuos)

      # O Individuo selecionado será o de menor fitness
      inds_selected.append(ind1 if ind1.fitness <= ind2.fitness else ind2)

    # Atualiza a população para os indivíduos que foram selecionados
    self.individuos = inds_selected
    
    # Aplica a elitização
    self.__apply_elite()
```

*Crossover: O processo de cruzamento é responsável por gerar novos indivíduos a partir de dois indivíduos pais. Alé da taxa de crossover, o ponto onde o DNA dos pais é cortado define significativamente a aptidão do indivíduo filho.*
```Python
  def make_crossover(self):
    """Faz crossover entre individuos pelo método de 1 corte"""

    children: [Individuo] = []

    while len(children) <= self.n_ind:
    
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
        children.append(Individuo(self.__n_bits, bits1))
        children.append(Individuo(self.__n_bits, bits2))
      
      # Se a taxa não ficou dentro do aceitável
      else:
      
        # Adiciona os pais como filhos
        children.append(ind1)
        children.append(ind2)

    # Muda os individuos para os filhos gerados
    self.individuos = children

    self.__apply_elite()
```

*Mutação: Além do cruzamento, há outra fonte de variabilidade genética, o processo de mutação. Dada uma taxa em porcentagem, calcula-se a chance de cada bit (gene) sofrer alteração.*
```Python
  def __mutar_bit(self, bit: str):
    # Sorteie a porcentagem entre 1 e 100, se o valor for aceito, retorne o bit inverso
    return ("0" if bit == "1" else "1") if randint(1, 100) < self.__taxa_mut else bit

	def apply_mutation(self):
		"""Aplica mutação bit a bit nos individuos"""

    # Para cada individuo
    for ind in self.individuos:
      new_bits = "".join([self.__mutar_bit(bit) for bit in ind.bits])

      # Troca os bits do individuo
      ind.bits = new_bits
    
    self.__apply_elite()
```

### 3.2 Função principal

*Modelagem: Cada indivíduo foi modelado como uma classe contendo seu número de bits (comprimento de seu cromossomo), a cadeia de bit em si, um valor máximo e um valor mínimo de aptidão.*

```Python
def main():
	padrao_print = "Arquivo com melhor x para {} gerações = {}i_{}g_{}exec.csv"
  diretorio = "CSVs"  # Diretório em que serão salvo os arquivos
  bests = []  # Estrutura para armazenar os melhores fitness de cada execução para cada geração
  num_exec = 10
  generations = [5, 10]

  best_x = {generation: None for generation in generations}

  # Para cada execução
  for t in range(1, num_exec + 1):

    # Cria as listas da execução de cada número de gerações máximas
    bests.append({generation: [] for generation in generations})

    for max_generations in generations:

      # Abre arquivo
      arq = open(f"{diretorio}/{n_individuos}i_{max_generations}g_{t}exec.csv", "wt")

      # Gera população
      populacao = Populacao(taxa_mutacao, taxa_crossover, n_individuos, n_bits)

      for i in range(max_generations):
        populacao.select()
        populacao.make_crossover()
        populacao.apply_mutation()

        best = Individuo(n_bits, populacao.elite.bits)
        
        if not best_x[max_generations] or best_x[max_generations][0].fitness > best.fitness:
          best_x[max_generations] = (best, t)

        # Escreve no arquivo e adiciona o melhor fitness na estrutura
        arq.write(f"{i+1};{best}\n")
        bests[-1][max_generations].append(best.fitness)

    arq.close()


  # - - - - - TRECHO REFERENTE À PLOTAGEM DO GRÁFICO - - - - -
  
  # Estrutura que armazena a soma de cada geração de cada execução
  # Gerará o dicionário: {5: [0, 0, 0, 0, 0], 10: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
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

    print(padrao_print.format(generation, n_indiv, generation, best_x[generation][1]))

    pl.show()

  return 0
```

## 4. EXEMPLO DE USO

### 4.1 Exemplo de chamada e entradas

O algoritmo foi estruturado sob uma aplicação de linha de comando (CLI), portanto, os parâmetros e taxas envolvidas são livres para entrada do usuário. Abaixo está um exemplo de chamada num terminal Linux com 4 indivíduos na população, 1% de taxa de mutação, e 60% de taxa de crossover respectivamente:
`$ python3 main.py -i 4 -m 1 -c 60`

Em caso de dúvidas sobre cada parâmetro, basta chamar a aplicação passando o parâmetro '-h':
`$ python3 main.py -h`

Explicação sobre parâmetros de entrada:
* -i / --individuo: Número de indivíduos;
* -m / --mutacao: Porcentagem de chance de ocorrer mutação por bit;
* -c / --crossover: Porcentagem de chance de ocorrer crossover entre 2 indivíduos;

### 4.2 Saída

A saída após a execução do programa é um arquivo .CSV para cada iteração e configuração. Por exemplo, para 5 gerações, 10 execuções, serão gerados 10 arquivos, um para cada execução.
<br>

O nome do arquivo segue o padrão:
{número_indivíduos}i_{número_gerações}g_{número_execução_atual}exec.csv
<br>

* Exemplos: 4i_5g_1exec.csv, 4i_5g_2exec.csv, 4i_5g_3exec.csv, ...

Cada linha do arquivo contém o número da geração, os bits do indivíduo mais apto, seu valor de X, o valor normalizado de X e valor obtido a partir da função fitness:<br>
1;Bits = 1001010110;X = 598;X_normalizado = 1.691104594330401;Fitness = 1.7865209659741872

## 5. RESULTADOS E OBSERVAÇÕES

....
