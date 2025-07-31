# Bibliotecas importadas
import pandas as pd
import numpy as np
import random as rd
import copy
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# Função que retorna a total de dias da semana e total de domingos trabalhados em sequência (ou seja sem pular um dia) por 
# cada funcionário
def obter_dias_trabalhados_mes_passado(df_mes_anterior, domingo_dias_mes_anterior):
    
    # Inicia a lista dos funcionários com os dias trabalhados vazia
    funcionarios_dias_trabalhados = []
    
    # Inicia o loop para verificar os dias trabalhados de cada funcionário no mês passado
    for index, linha in df_mes_anterior.iterrows():
        
        # Inicia as variáveis de domingo e dias da semana com zero
        total_domingos_trabalhados = 0
        total_dias_semana_trabalhados = 0
        
        # Inicia a lista onde fica armazenado os dias trabalhados de cada funcionário vazia
        dias = []
        
        # Inicia as variáveis funcionário e o setor onde ele esta alocado
        nome_funcionario = linha['Funcionário']
        nome_setor = linha['Setor']
        
        # Inicia o loop que verifica cada dia do mês passado (começando pelo penultimo domingo do mês)
        # Começa na coluna 2 porque as colunas 0 e 1 são funcionário e setor
        for coluna in df_mes_anterior.columns[2:]:
            
            # Extrai o valor do campo selecionado (linha funcionário, coluna dia)
            valor = df_mes_anterior.loc[index, coluna]
            
            # Verifica se o dia em questão é domingo
            if coluna in domingo_dias_mes_anterior:
                # Verifica se o funcionário faltou ou trabalhou no dia, se faltou a variável domingo é zerada senão recebe +1
                if str(valor).upper() != 'F':
                    total_domingos_trabalhados += 1
                else:
                    total_domingos_trabalhados = 0
            
            # Nesse caso o dia em questão não é domingo    
            else:
                # Verifica se o funcionário faltou ou trabalhou no dia, se faltou a variável dia semana é zerada senão recebe +1
                if str(valor).upper() != 'F':
                    total_dias_semana_trabalhados += 1
                else:
                    total_dias_semana_trabalhados = 0
        
        # A lista dia recebe as variáveis de domingo trabalhado e dias da semana trabalhados do funcionário selecionado    
        dias = [total_domingos_trabalhados, total_dias_semana_trabalhados]

        # Cria um dicionário onde a chave é o funcionário + setor e o valor é a lista dias gerada anteriormente
        dias_trabalhados = {(nome_funcionario, nome_setor): dias}
        
        # Adiciona o dicionário gerado a lista funcionarios_dias_trabalhados
        funcionarios_dias_trabalhados.append(dias_trabalhados)
    
    # Retorna a lista funcionarios_dias_trabalhados
    return funcionarios_dias_trabalhados

# Função que retorna os dias de day_off (dias que o funcionário avisou previamente que irá faltar) por cada funcionário
def obter_days_off(df_days_off):
    
    # Inicia a lista dos funcionários com os days off vazia
    funcionarios_days_off = []
    
    # Inicia o loop para verificar os days off de cada funcionário para o mês vigente
    for index, linha in df_days_off.iterrows():
        
        # Inicia a lista onde fica armazenado os days off de cada funcionário vazia
        colunas_filtradas = []
        
        # Inicia as variáveis funcionário e o setor onde ele esta alocado
        nome_funcionario = linha['Funcionário']
        nome_setor = linha['Setor']
        
        # Gera uma tupla com o nome do funcionário + setor
        func_setor = (nome_funcionario, nome_setor)
        
        # Inicia o loop que verifica cada dia do mês vigente
        # Começa na coluna 2 porque as colunas 0 e 1 são funcionário e setor
        for coluna in df_days_off.columns[2:]:
            # Extrai o valor do campo selecionado (linha funcionário, coluna dia)
            valor = df_days_off.loc[index, coluna]
            
            # Verifica se o funcionário possui folga programada para o dia
            if str(valor).upper() == 'F':
                # Caso possua folga programada, o index dessa coluna dia é armazenado na lista colunas_filtrada
                colunas_filtradas.append(df_days_off.columns.get_loc(coluna))

        # Cria um dicionário onde a chave é o funcionário + setor e o valor é a lista de days off gerada anteriormente
        days_off = {(nome_funcionario, nome_setor): colunas_filtradas}
        
        # Adiciona o dicionário gerado a lista funcionarios_days_off
        funcionarios_days_off.append(days_off)
    
    # Retorna a lista funcionarios_days_off
    return funcionarios_days_off

# Função que retorna a escala do mês vigente com os dias de day_off por cada funcionário
def gerar_escala_days_off(df_escala_days_off, df_days_off):
    
    # Armazena a lista de days off de cada funcionário na variável escala_days_off
    escala_days_off = obter_days_off(df_days_off)
    
    # Inicia o loop para inputar o valor 'F' para os days off de cada funcionário para o mês vigente
    for index, linha in df_escala_days_off.iterrows():
        
        # Inicia as variáveis funcionário e o setor onde ele esta alocado
        nome_funcionario = linha['Funcionário']
        nome_setor = linha['Setor']
        
        # Gera uma tupla com o nome do funcionário + setor
        funcionario_setor = (nome_funcionario, nome_setor)
        
        # Inicia a lista dos days off do funcionário vazia
        days_off =[]
        
        # Inicia o loop que verifica os days off de cada funcionário
        for funcionario in escala_days_off:
            if funcionario_setor in funcionario:
                # A variável days_off recebe a lista de days_off do funcionário
                days_off = funcionario[funcionario_setor]
                break
        
        # Inicia o loop que vai inputar os days off na escala dos funcionários do mês vigente   
        for day in days_off:
            # Extrai o nome da coluna com day off
            nome_coluna = df_escala_days_off.columns[day]
            
            # Inputa o valor 'F' para os dias de day off no dataframe
            df_escala_days_off.loc[index, nome_coluna] = 'F'

    # Retorna a escala do mês vigente com os dias que cada funcionário irá faltar
    return df_escala_days_off

# Função que retorna a escala de cada funcionário do mês vigente
def gerar_escala_final(df_escala, nom_setor, domingo_dias_mes_vigente, df_mes_anterior, domingo_dias_mes_anterior):
    
    # Lista com os possiveis valores que o funcionário pode receber
    lista_opcoes = ['M', 'T', 'N', 'F']
    
    # Cria uma cópia do df escala filtrando pelo setor selecionado
    df_escala_setor = df_escala[df_escala['Setor'] == nom_setor].copy()
    
    # Cria uma cópia do df do mês anterior filtrando pelo setor selecionado
    df_mes_anterior_setor = df_mes_anterior[df_mes_anterior['Setor'] == nom_setor].copy()
    
    # Roda a função para obter os dias da semana e domingos trabalhados em sequência por cada funcionário no mês passado
    funcionarios_dias_trabalhados = obter_dias_trabalhados_mes_passado(df_mes_anterior_setor, domingo_dias_mes_anterior)
    
    # Transforma a lista em um dicionário
    funcionarios_dias_trabalhados = {k: v for funcionario in funcionarios_dias_trabalhados for k, v in funcionario.items()}
    
    # Extrai os dias do mês do df escala
    colunas_dias = df_escala_setor.columns[2:]
    
    # Transforma os dias do mês em string e os coloca numa lista
    colunas_dias_str = list(map(str, colunas_dias))
    
    # Inicia o loop para imputar os valores de cada funcionário para o mês vigente
    for index, linha in df_escala_setor.iterrows():
        
        # Inicia as variáveis funcionário e o setor onde ele esta alocado
        nome_funcionario = linha['Funcionário']
        nome_setor = linha['Setor']
        
        # Gera uma tupla com o nome do funcionário + setor
        funcionario_setor = (nome_funcionario, nome_setor)
        
        # Inicia o loop que verifica cada dia do mês vigente
        for coluna in colunas_dias:
            
            # Extrai o valor do campo selecionado (linha funcionário, coluna dia)
            valor = df_escala_setor.loc[index, coluna]
            
            # Recebe o dia em análise como número inteiro
            dia_atual = int(coluna)
            
            # Recebe o dia anterior (no mínimo o seu valor será 1 para evitar erro no programa)
            dia_anterior = max(1, dia_atual - 1)
            
            # Verifica se o nome da coluna do dia anterior deve ser uma string ou um inteiro para evitar erro no programa
            col_dia_anterior = str(dia_anterior) if coluna in colunas_dias_str else dia_anterior
            
            # Verifica se esta programado para o funcionário faltar naquele dia e caso a condição seja verdadeira ele pula o 
            # restante do loop
            if str(valor).upper() == 'F':
                continue
            else:
                # Sorteia uma dos valores disponíveis
                opcao_selecionada = rd.choice(lista_opcoes)
                
                # Checa cada dia (coluna) do mês vigente
                if col_dia_anterior in df_escala_setor.columns:
                    # Recebe o valor do dia anterior
                    valor_dia_anterior = df_escala_setor.loc[index, col_dia_anterior]
                    
                    # A condição abaixo é necessária porque há uma regra que impede que o funcionário que trabalhou a noite no dia
                    # anterior seja escalado para trabalhar de manhã no dia seguinte.
                    # Continua realizando o sorteio enquanto o valor do dia anterior for 'N' e o valor sorteado for 'M'
                    while opcao_selecionada == 'M' and valor_dia_anterior == 'N':
                        opcao_selecionada = rd.choice(lista_opcoes)
                
                # Verifica cada funcionário do setor
                if funcionario_setor in funcionarios_dias_trabalhados:
                    
                    # Verifica se o dia em análise é ou não um domingo 
                    if coluna in domingo_dias_mes_vigente:
                        # Verifica se o funcionário trabalhou 2 domingos seguidos ou a opção sorteada é 'F', caso uma das condições
                        # seja verdadeira o funcionário recebe o valor 'F' para aquele dia e sua contagem é resetada para 0 novamente,
                        # senão, ele recebe +1 em sua contagem de domingos trabalhados em sequencia
                        if funcionarios_dias_trabalhados[funcionario_setor][0] == 2 or opcao_selecionada == 'F':
                            df_escala_setor.loc[index, coluna] = 'F'
                            funcionarios_dias_trabalhados[funcionario_setor][0] = 0
                        else:
                            df_escala_setor.loc[index, coluna] = opcao_selecionada
                            funcionarios_dias_trabalhados[funcionario_setor][0] += 1
                    else:
                        # Verifica se o funcionário trabalhou 6 dias seguidos (domingo não conta) ou a opção sorteada é 'F', caso 
                        # uma das condições seja verdadeira o funcionário recebe o valor 'F' para aquele dia e sua contagem é 
                        # resetada para 0 novamente, senão, ele recebe +1 em sua contagem de dias da semana trabalhados em sequencia
                        if funcionarios_dias_trabalhados[funcionario_setor][1] == 6 or opcao_selecionada == 'F':
                            df_escala_setor.loc[index, coluna] = 'F'
                            funcionarios_dias_trabalhados[funcionario_setor][1] = 0
                        else:
                            df_escala_setor.loc[index, coluna] = opcao_selecionada
                            funcionarios_dias_trabalhados[funcionario_setor][1] += 1

    # Retorna a escala do mês vigente dos funcionários para o setor selecionado
    return df_escala_setor
