# Bibliotecas importadas
import pandas as pd
import numpy as np
import random as rd
import copy
import time
from support_functions import obter_dias_trabalhados_mes_passado, obter_days_off, gerar_escala_days_off, gerar_escala_final, avaliar_resultado_final
from ga_functions import gerar_fitness, ordenar_populacao, crossover, gerar_mutacao
import warnings
from pathlib import Path

# pasta src/ ➡️  parent  ➡️  raiz do projeto (tech-challenge/)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"        #  tech-challenge/data
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

warnings.simplefilter(action='ignore', category=FutureWarning)

# Cria um dataframe com a escala dos funcionários do mês passado
df_mes_anterior = pd.read_excel(DATA_DIR / "Mes_Anterior.xlsx")

# Cria um dataframe sem escala definida dos funcionários do mês vigente
df_mes_vigente = pd.read_excel(DATA_DIR / "Mes_Vigente.xlsx")

# Cria um dataframe com a escala de days_off solicitadas previamente pelos funcionários para o mês vigente
df_days_off = pd.read_excel(DATA_DIR / "Mes_Vigente_Days_Off.xlsx")

# Cria um dataframe com a escala dos funcionários por setor e periodo para o mês vigente
# É importante ressaltar que essa escala informa o número MÍNIMO de funcionários por periodo para aquele setor e não o número máximo
df_escala_setor_periodo = pd.read_excel(DATA_DIR / "Escala_Setor_Periodo.xlsx")

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
num_populacao = 81

# Contador de geração (mostra em qual geração o algoritmo esta)
num_geracao = 1

# Contador de quantas gerações se passaram sem que uma solução melhor aparecesse
contador_solucao = 1

# Lista com cada individuo da população
populacao_gerada = []

# Probabilidade da mutação ocorrer em algum dos filhos
probabilidade_mutacao = 0.03

# Retorna a população que foi gerada
populacao_gerada = gerar_populacao(num_populacao, len(populacao_gerada))

# Retorna o score de cada solução
fitness_populacao = gerar_fitness(populacao_gerada, df_escala_setor_periodo, nom_setor, domingo_dias_mes_vigente)

# Retorna a população e seu respectivo fitness ordenado por score (ordem decrescente)
populacao_gerada, fitness_populacao = ordenar_populacao(populacao_gerada, fitness_populacao)

# Armazena a melhor solução encontrada naquela geração
melhor_solucao = copy.deepcopy(populacao_gerada[0])

# Armazena o melhor fitness (score) da solução encontrada naquela geração
melhor_fitness = fitness_populacao[0]

# Imprime o melhor fitness encontrado
print(f'\nGeração: {num_geracao}, Valor de fitness: {melhor_fitness}\n')

# Inicializa a variável que vai armazenar o horário que esse bloco de código começou a ser executado
inicio = time.time()

# Inicia o loop para a criação das próximas gerações até o algoritmo atingir o número máximo de loops
while num_geracao < 1000:

    # Aplica o decaying diversity
    if num_geracao % 50 == 0 and num_populacao >= 16:
      num_populacao -= 8

    # Lista com cada individuo da nova população
    nova_populacao = []

    # Retorna os filhos gerados a partir do crossover dos melhores pais (soluções com maior score)
    novos_filhos = crossover(populacao_gerada[:8])

    # Retorna os mesmos filhos que podem ou não ter sofrido a mutação
    novos_filhos = gerar_mutacao(novos_filhos, probabilidade_mutacao)

    # Aplica o elitismo como forma de seleção
    nova_populacao.append(copy.deepcopy(melhor_solucao))

    # Adiciona os filhos gerados a nova população
    nova_populacao.extend(novos_filhos)

    # Gera os próximos individuos que irão ajudar a compor a nova população
    nova_populacao.extend(gerar_populacao(num_populacao, len(nova_populacao)))

    # Retorna o score de cada solução
    fitness_populacao = gerar_fitness(nova_populacao, df_escala_setor_periodo, nom_setor, domingo_dias_mes_vigente)

    # Retorna a população e seu respectivo fitness ordenado por score (ordem decrescente)
    populacao_gerada, fitness_populacao = ordenar_populacao(nova_populacao, fitness_populacao)

    # Contador de geração recebe +1
    num_geracao += 1

    # Verifica se a nova geração produziu uma solução melhor que a geração anterior
    if fitness_populacao[0] > melhor_fitness:

        # Melhor solução e fitness recebem os novos valores
        melhor_solucao = copy.deepcopy(populacao_gerada[0])
        melhor_fitness = fitness_populacao[0]

        # O contador é zerado
        contador_solucao = 0

        # Imprime o melhor fitness encontrado
        print(f'\nGeração: {num_geracao}, Valor de fitness: {melhor_fitness}\n')

    else:
        # Contador recebe +1
        contador_solucao += 1

        # Aumenta a chance de mutação caso o algoritmo fique estagnado em uma solução
        if contador_solucao > 100 and probabilidade_mutacao < 0.1:
          probabilidade_mutacao += 0.01

# Imprime a melhor solução encontrada
print(f'Melhor solução encontrada:\n{melhor_solucao}')

#Exportar a melhor escala como Excel
best_path = OUTPUT_DIR / "best_schedule.xlsx"
melhor_solucao.to_excel(best_path, index=False)
print(f"Escala salva em: {best_path}")

# Inicializa a variável que vai armazenar o horário que esse bloco de código terminou de ser executado
fim = time.time()

# Armazena quanto tempo levou para esse bloco de código ser executado
tempo_execucao = round((fim - inicio) / 60)


# Imprime o tempo de execução
print(f'\nTempo de Execução: {tempo_execucao}')

# Gera o score final da solução encontrada
resultado = avaliar_resultado_final(melhor_solucao, df_escala_setor_periodo, nom_setor, domingo_dias_mes_vigente)


#armazena resultados finais e logs
with open(OUTPUT_DIR / "run_log.txt", "a") as log:
    log.write(
        f"Geração final: {num_geracao} | "
        f"Melhor fitness: {melhor_fitness} | "
        f"Score final: {resultado}% | "
        f"Tempo (min): {tempo_execucao}\n"
    )


# Imprime o score da solução final
print(resultado)
