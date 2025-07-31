# Bibliotecas importadas
import pandas as pd
import numpy as np
import random as rd
import copy
from support_functions import obter_dias_trabalhados_mes_passado, obter_days_off, gerar_escala_days_off, gerar_escala_final
from ga_functions import gerar_fitness, ordenar_populacao, crossover, gerar_mutacao
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# Cria um dataframe com a escala dos funcionários do mês passado
df_mes_anterior = pd.read_excel('Dataset/Mes_Anterior.xlsx')

# Cria um dataframe sem escala definida dos funcionários do mês vigente
df_mes_vigente = pd.read_excel('Dataset/Mes_Vigente.xlsx')

# Cria um dataframe com a escala de days_off solicitadas previamente pelos funcionários para o mês vigente
df_days_off = pd.read_excel('Dataset/Mes_Vigente_Days_Off.xlsx')

# Cria um dataframe com a escala dos funcionários por setor e periodo para o mês vigente
# É importante ressaltar que essa escala informa o número MÍNIMO de funcionários por periodo para aquele setor e não o número máximo
df_escala_setor_periodo = pd.read_excel('Dataset/Escala_Setor_Periodo.xlsx')

# Lista com os domingos do mês anterior
domingo_dias_mes_anterior = [22, 29]

# Lista com os domingos do mês vigente
domingo_dias_mes_vigente = [6, 13, 20, 27]

# Nome do setor selecionado
nom_setor = 'Hortifruti'

# Cria um dataframe que é a cópia do dataframe do mês vigente
df_escala_days_off = df_mes_vigente.copy()


# Função que gera a população
def gerar_populacao(num_populacao, populacao_gerada):
    return[gerar_escala_final(df_escala, nom_setor, domingo_dias_mes_vigente, df_mes_anterior, domingo_dias_mes_anterior) for _ in range(populacao_gerada, num_populacao)]

# Retorna a escala de days off dos funcionários
df_escala = gerar_escala_days_off(df_escala_days_off, df_days_off)

# Retorna a lista de days off de cada funcionário
funcionarios_days_off = obter_days_off(df_escala)

# Total da população
num_populacao = 4

# Contador de geração (mostra em qual geração o algoritmo esta)
num_geracao = 1

# Contador de quantas gerações se passaram sem que uma solução melhor aparecesse
contador_solucao = 1

# Lista com cada individuo da população
populacao_gerada = []

# Probabilidade da mutação ocorrer em algum dos filhos
probabilidade_mutacao = 0.05

# Retorna a população que foi gerada
populacao_gerada = gerar_populacao(num_populacao, len(populacao_gerada))

# Retorna o score de cada solução
fitness_populacao = gerar_fitness(populacao_gerada, df_escala_setor_periodo, nom_setor, domingo_dias_mes_vigente)

# Retorna a população e seu respectivo fitness ordenado por score (ordem decrescente)
populacao_gerada, fitness_populacao = ordenar_populacao(populacao_gerada, fitness_populacao)

# Armazena a melhor solução encontrada naquela geração
melhor_solucao = populacao_gerada[0]

# Armazena o melhor fitness (score) da solução encontrada naquela geração
melhor_fitness = fitness_populacao[0]

# Retorna os filhos gerados a partir do crossover dos melhores pais (soluções com maior score)
populacao_gerada = crossover(populacao_gerada[:2])

# Retorna os mesmos indiviuos que podem ou não ter sofrido a mutação
populacao_gerada = gerar_mutacao(populacao_gerada, 1)

# Imprime o melhor fitness encontrado
print(f'\nGeração: {num_geracao}, Valor de fitness: {melhor_fitness}\n')

# Inicia o loop para a criação das próximas gerações até uma solução aceitavel ser encontrada (se não houver mudança de score 
# por 1000 gerações) ou o algoritmo atingir o número máximo de loops
while num_geracao < 100 and contador_solucao < 1000:
    
    # Gera a próxima geração que irá ajudar a compor a população atual
    # 50% da população são os individuos da antiga geração e 50% da população são os individuos da nova geração
    populacao_gerada.extend(gerar_populacao(num_populacao, len(populacao_gerada)))
    
    # Retorna o score de cada solução
    fitness_populacao = gerar_fitness(populacao_gerada, df_escala_setor_periodo, nom_setor, domingo_dias_mes_vigente)

    # Retorna a população e seu respectivo fitness ordenado por score (ordem decrescente)
    populacao_gerada, fitness_populacao = ordenar_populacao(populacao_gerada, fitness_populacao)

    # Retorna os filhos gerados a partir do crossover dos melhores pais (soluções com maior score)
    populacao_gerada = crossover(populacao_gerada[:2])

    # Retorna os mesmos indiviuos que podem ou não ter sofrido a mutação
    populacao_gerada = gerar_mutacao(populacao_gerada, probabilidade_mutacao)
    
    # Contador de geração recebe +1
    num_geracao += 1
    
    # Verifica se a nova geração produziu uma solução melhor que a geração anterior
    if fitness_populacao[0] > melhor_fitness:
        
        # Melhor solução e fitness recebem os novos valores
        melhor_solucao = populacao_gerada[0]
        melhor_fitness = fitness_populacao[0]
        
        # O contador é zerado
        contador_solucao = 0
        
        # Imprime o melhor fitness encontrado
        print(f'\nGeração: {num_geracao}, Valor de fitness: {melhor_fitness}\n')
    
    else:
        # Contador recebe +1
        contador_solucao += 1


print(f'Melhor solução encontrada:\n{melhor_solucao}')

# Gera o caminho e o nome do arquivo excel onde será exportada a solução final
nome_excel = f'Dataset/Escala_Final_Setor_{nom_setor}.xlsx'

# Cria o arquivo excel com a melhor solução encontrada
melhor_solucao.to_excel(nome_excel, index=False)
