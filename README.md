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
