# Bibliotecas importadas
import pandas as pd
import numpy as np
import random as rd
import copy
from .support_functions import (
    obter_dias_trabalhados_mes_passado,
    obter_days_off,
    gerar_escala_days_off,
    gerar_escala_final,
)
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# Função que gera o score de cada individuo da população
def gerar_fitness(populacao_gerada, df_escala_setor_periodo, nom_setor, domingo_dias_mes_vigente):
    
    # Inicia a lista dos scores de cada individuo vazia
    score = []
    
    # Inicia as variáveis de escalas para dias da semana e domingo para o setor selecionado
    escala_setor_dia_semana = df_escala_setor_periodo[(df_escala_setor_periodo['Setor'] == nom_setor) & (df_escala_setor_periodo['Flag_Domingo'] == 0)].copy()
    escala_setor_domingo = df_escala_setor_periodo[(df_escala_setor_periodo['Setor'] == nom_setor) & (df_escala_setor_periodo['Flag_Domingo'] == 1)].copy()
    
    # Inicia o loop para gerar o score de cada individuo da população
    for populacao in populacao_gerada:
        
        # Transformar aquele elemento da lista em um df para poder fazer a manipulação dele
        pd_populacao_gerada = pd.DataFrame(populacao)
        
        # Essa variável será utilizada para calcular o score do dia em análise (ela armazena o sub total)
        score_sub_total = 0
        
        # Inicia o loop que verifica o score de cada dia
        # Começa na coluna 2 porque as colunas 0 e 1 são funcionário e setor
        for coluna in pd_populacao_gerada.columns[2:]:
            
            # Inicializa as variáveis que armazenam o total de funcionários que trabalhararam em cada período do dia em análise
            total_M = 0    # Total de funcionários que trabalharam no período da manhã
            total_N = 0    # Total de funcionários que trabalharam no período da noite
            peso_periodo_dia = 0    # Determina o peso que será atribuido a solução ao acertar os periodos daquele dia
            
            # Verifica se o dia em análise é domingo ou dia da semana para selecionar a escala correta (escala de domingo ou 
            # escala para dia da semana)
            # A escala de domingo tem um peso maior porque temos apenas de 4-5 domingos no mês e queremos que o algoritmo de 
            # importância a esses dias tanto quanto aos dias úteis do mês
            if coluna in domingo_dias_mes_vigente:
                escala_setor_selecionada = escala_setor_domingo
                peso_periodo_dia = 8
                
            else:
                escala_setor_selecionada = escala_setor_dia_semana
                peso_periodo_dia = 2.5
                
            valor_M = escala_setor_selecionada.iloc[0,2]    # Recebe o valor mínimo de funcionários escalados para a manhã
            valor_N = escala_setor_selecionada.iloc[0,3]    # Recebe o valor mínimo de funcionários escalados para a noite
            
            # Inicia o loop para verificar o status de cada funcionário no dia em análise
            for index, linha in pd_populacao_gerada.iterrows():
                # Extrai o valor do campo selecionado (linha funcionário, coluna dia)
                valor = pd_populacao_gerada.loc[index, coluna]
                
                # Verifica qual período o funcionário trabalhou e adiciona +1 a variável correspondente
                match valor:
                    case 'M':
                        total_M += 1
                    case 'N':
                        total_N += 1
            
	        # Verifica se o número de funcionários que trabalhou naquele período é igual ou maior ao número na escala, caso 
            # a condição seja verdadeira o score sub total recebe pontos
            if total_M >= valor_M:
                score_sub_total += (valor_M * peso_periodo_dia)

            if total_N >= valor_N:
                score_sub_total += (valor_N * peso_periodo_dia)
 
        # Adiciona o score daquele individuo a lista de scores
        score.append(round(score_sub_total, 2))
    
    # Retorna a lista com os scores de cada solução
    return score

# Função que ordena a população de acordo com o valor de fitness
def ordenar_populacao(populacao_gerada, fitness_populacao):
    
    # Gera pares de tuplas da população com os seus respectivos scores e armazena essas tuplas em uma lista
    par_listas = list(zip(populacao_gerada, fitness_populacao))
    
    # Ordena a população de acordo com o seu score (ordem decrescente)
    lista_ordenada = sorted(par_listas, key=lambda x: x[1], reverse=True)
    
    # Desfaz as tuplas (agora ordenadas pelo score) e armazena nas variáveis populacao_sorteada e fitness_sorteado
    populacao_sorteada, fitness_sorteado = zip(*lista_ordenada)
    
    # Retorna as variáveis populacao_sorteada e fitness_sorteado
    return populacao_sorteada, fitness_sorteado

# Função que realiza o cruzamento entre os individuos com maior score
def crossover(populacao_gerada):
    
    # Inicia a lista da nova geracao vazia
    nova_geracao = []
    
    # Transforma a população gerada em uma lista
    populacao_lista = list(populacao_gerada)
    
    # Recebe o número total de individuos na população
    qtd_populacao = len(populacao_lista)
    
    # Recebe a quantidade de funcionários (cada linha é uma funcionário) que o individuo possui
    qtd_linhas_total = len(populacao_lista[0])
    
    # Selecionar uma determinada porcentagem de linhas (isso vária de acordo com o número de linhas porém na maioria dos casos 
    # o valor será algo em torno de 15-25% das linhas)
    qtd_linhas_selecionadas = round(qtd_linhas_total / 5)
    
    # Quantidade de linhas que serão alteradas pelo crossover (ao menos 1 linha é alterada)
    intensidade_crossover = max(1, qtd_linhas_selecionadas)
    
    # Fazer uma permutação dos individuos da população
    lista_crossover = rd.sample(populacao_lista, len(populacao_lista))
    
    # Inicia a lista de linhas sorteadas vazia
    linhas_sorteadas = []
    
    # Inicia o loop que irá sortear quais linhas do individuo serão alteradas
    for _ in range(0, qtd_linhas_selecionadas):
        valor_sorteado = rd.randint(0, (qtd_linhas_total -1))
        
        # Essa condição é para impedir que a mesma linha seja sorteada +1 vez
        while valor_sorteado in linhas_sorteadas:
            valor_sorteado = rd.randint(0, (qtd_linhas_total -1))
        
        # Adiciona a linha sorteada a lista
        linhas_sorteadas.append(valor_sorteado)
    
    # Inicia o loop que irá realizar o cruzamento entre os individuos
    for i in range(0, qtd_populacao-1, 2):
        
        # Inicializa as variáveis pais
        parent1 = pd.DataFrame(lista_crossover[i])
        parent2 = pd.DataFrame(lista_crossover[i+1])
        
        # Inicializa as variáveis filhos (eles começam inicialmente sendo uma cópia exata dos pais)
        child1 = parent1.copy()
        child2 = parent2.copy()
        
        # Inicializa o loop que irá realizar o crossover
        for linha in linhas_sorteadas:
            # Filho1 recebe as linhas sorteadas do pai2 enquanto que filho2 recebe as linhas sorteadas do pai1
            child1.iloc[linha] = parent2.iloc[linha]
            child2.iloc[linha] = parent1.iloc[linha]
        
        # Adiciona os filhos gerados a nova geração
        nova_geracao.append(child1)
        nova_geracao.append(child2)
    
    # Retorna a nova geração
    return nova_geracao

# Função que realiza o cruzamento entre os individuos com maior score
def gerar_mutacao(nova_geracao, probabilidade_mutacao):
    
    # Cria uma cópia completa da nova geração gerada pelo crossover
    mutacao = copy.deepcopy(nova_geracao)
    
    # Recebe a quantidade de funcionários (cada linha é uma funcionário) que o individuo possui
    qtd_linhas_total = len(mutacao[0])
    
    # Selecionar uma determinada porcentagem de linhas (isso vária de acordo com o número de linhas porém na maioria dos casos 
    # o valor será algo em torno de 15-25% das linhas)
    qtd_linhas_selecionadas = round(qtd_linhas_total / 5)
    
    # Quantidade de linhas que serão alteradas pela mutação (ao menos 1 linha é alterada)
    intensidade_mutacao = max(1, qtd_linhas_selecionadas)
    
    # Inicia a lista de linhas sorteadas vazia
    linhas_sorteadas = []
    
    # Lista com os possiveis valores que o funcionário pode receber (Menos a opção 'F')
    lista_opcoes = ['M', 'N']
    
    # Inicia o loop que irá sortear quais linhas do individuo serão alteradas
    for _ in range(0, qtd_linhas_selecionadas):
        valor_sorteado = rd.randint(0, (qtd_linhas_total -1))
        
        # Essa condição é para impedir que a mesma linha seja sorteada +1 vez
        while valor_sorteado in linhas_sorteadas:
            valor_sorteado = rd.randint(0, (qtd_linhas_total -1))
        
        # Adiciona a linha sorteada a lista
        linhas_sorteadas.append(valor_sorteado)

    # Inicia o loop que irá passar cada individuo pelo teste da mutação
    for individuo in mutacao:
        # Sorteia de forma aleatória se o individuo sofrerá ou não a mutação
        if rd.random() <= probabilidade_mutacao:
            
            # Transformar aquele elemento da lista em um df para poder fazer a manipulação dele
            df_individuo = pd.DataFrame(individuo)
                
            # Inicia o loop para verificar quais linhas serão alteradas
            for index, linha in df_individuo.iterrows():
                # Verifica se essa linha deve sofrer a mutação
                if index in linhas_sorteadas:
                    
                    # Sorteia uma dos valores disponíveis
                    opcao_selecionada = rd.choice(lista_opcoes)
            
                    # Inicia o loop que irá percorrer cada dia do mês
                    for coluna in df_individuo.columns[2:]:
                    
                        # Extrai o valor do campo selecionado (linha funcionário, coluna dia)
                        valor = df_individuo.loc[index, coluna]
            
                        # A mutação não altera dias iguais a 'F' porque isso pode gerar uma solução invalida
                        if str(valor).upper() == 'F':
                            opcao_selecionada = rd.choice(lista_opcoes)
                        else:
                            df_individuo.loc[index, coluna] = opcao_selecionada

    # Retorna a geração com os indiviuos que podem ou não ter sofrido a mutação
    return mutacao
