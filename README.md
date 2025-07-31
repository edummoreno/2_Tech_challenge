# Projeto: Otimizador de Escalas de Trabalho com Algoritmos Geneticos

Este projeto utiliza um Algoritmo Genético (GA) para otimizar a geração da escala de trabalho de setores de um supermercado, respeitando restrições legais e operacionais.

## 🚀 Objetivo

Gerar automaticamente escalas mensais para setores do supermercado que:

* Respeitem as folgas previamente solicitadas por funcionários;
* Evitem violações da CLT (como trabalhar 3 domingos seguidos, 7 dias úteis seguidos ou menos de 11h de intervalo entre turnos);
* Garantam que a escala cumpra a quantidade mínima de pessoas por turno (manhã/noite).

## 🧰 Lógica do Algoritmo Genético

* **Representação (Genoma):** Cada indivíduo representa uma escala mensal completa de um setor.
* **Inicialização:** Heurística (hotstart) com regras básicas aplicadas.
* **Fitness:** Avalia cada escala verificando se atende à demanda de cada dia/turno. Penaliza escalas que desrespeitam restrições.
* **Seleção:** Elitismo (melhor indivíduo sempre preservado).
* **Crossover:** Troca de linhas (funcionários) entre dois pais.
* **Mutação:** Altera aleatoriamente a escala de alguns funcionários.
* **Critério de parada:** 1000 gerações ou estagnação.

## 📁 Estrutura

```
.
├── Dataset/
│   ├── Mes_Anterior.xlsx
│   ├── Mes_Vigente.xlsx
│   ├── Mes_Vigente_Days_Off.xlsx
│   └── Escala_Setor_Periodo.xlsx
├── Notebook/
│   ├── support_functions.py
│   ├── ga_functions.py
│   └── setor_selecionado.py
├── Business Case.txt
└── README.md
```

## 🔧 Como executar

### 1. Instalar dependências:

```bash
pip install pandas numpy openpyxl
```

### 2. Executar o script principal:

```bash
python Notebook/setor_selecionado.py
```

### 3. Saída esperada

* Fitness (score) da melhor solução por geração
* Tempo total de execução
* Escala final gerada (impressa no console ou exportável para Excel)

## 🧵 Dados de entrada

* **Mes\_Anterior.xlsx:** escala usada para calcular restrições de domingos e dias consecutivos
* **Mes\_Vigente.xlsx:** base de preenchimento da nova escala
* **Mes\_Vigente\_Days\_Off.xlsx:** dias de folga solicitados
* **Escala\_Setor\_Periodo.xlsx:** número mínimo de funcionários por turno por dia

## 🌟 Possíveis melhorias

* Exportar a escala final para Excel
* Suporte a múltiplos setores simultaneamente
* Interface gráfica
* Validação com dados reais

## 📄 Licença

Este projeto é apenas para fins educacionais no contexto do Tech Challenge da pós-graduação em IA para Devs.

