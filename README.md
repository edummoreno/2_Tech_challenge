# Tech Challenge – Escalonamento Otimizado com Algoritmo Genético

> **Fase 2 – Pós‑Tech IA para Devs**
> Projeto de otimização de escalas de supermercado usando Algoritmos Genéticos (AGs).

---

## 1 🔍 Visão Geral

O objetivo é gerar automaticamente a escala mensal de um setor do supermercado garantindo:

## Restrições consideradas

Este algoritmo genético tem como objetivo otimizar a geração da **escala de setores de um supermercado** observando as seguintes restrições:

1. **Folgas solicitadas** – o funcionário não pode ser escalado para trabalhar nos dias em que pediu folga/ausência previamente.

A legislação brasileira proíbe:

2. O funcionário de **trabalhar 3 domingos seguidos**.  
3. O funcionário de **trabalhar 7 dias úteis seguidos**.  
4. O **intervalo entre dois expedientes** de um funcionário ser **menor que 11 horas**; isto é, se ele trabalhou à noite, não pode ser escalado para o turno da manhã do dia seguinte.

O algoritmo foi desenvolvido para gerar escalas de trabalho observando essas restrições. Elas podem, entretanto, **impossibilitar o preenchimento ideal** dos turnos em todos os dias do mês (o algoritmo pode não alcançar 100 % de score).

> **Exemplo:** se a escala mínima exigir 4 funcionários num dia e 2 deles estiverem em folga obrigatória ou férias, aquele dia ficará abaixo do mínimo.

Em resumo, o algoritmo **busca a melhor solução possível sem violar as restrições** acima.

---

## Sobre a solução desenvolvida

| Questão |        Resposta             |
|---------|-----------------------------|
| **O que está sendo otimizado?**       | A geração da escala de funcionários em cada setor do supermercado, respeitando as restrições acima. |
| **Representação da solução (genoma)** | A própria escala final de funcionários do setor selecionado (DataFrame). |
| **Função de fitness**                 | Para cada dia, verifica-se: (1) se cada período tem o **número mínimo** de funcionários; (2) somam-se os acertos diários obtendo-se o score mensal. |
| **Método de seleção**                 | **Elitismo**; em seguida, cria-se uma lista permutada e cruzam-se pares adjacentes (1º×2º, 3º×4º …). |
| **Método de crossover**               | Troca de linha(s) da solução A com a(s) mesma(s) linha(s) da solução B. O **Filho 1** herda ≈ 75–85 % do Pai 1 e o restante do Pai 2; o **Filho 2**, o inverso. |
| **Método de inicialização**           | **Hot-start** (inicialização heurística baseada em regras de negócio). |
| **Critério de parada**                | O algoritmo encerra após **1000 gerações**. |
| **Tipo de codificação**               | **Híbrida**, adequada à natureza combinatória do problema. |

---

## 2 📁 Estrutura de Pastas

```
tech-challenge/
├── data/                      # Arquivos de entrada (Excel)
│   ├── Mes_Anterior.xlsx
│   ├── Mes_Vigente.xlsx
│   ├── Mes_Vigente_Days_Off.xlsx
│   └── Escala_Setor_Periodo.xlsx
│
├── src/                       # Código‑fonte principal
│   ├── support_functions.py   # Funções de ETL e regras de negócio
│   ├── ga_functions.py        # Núcleo do Algoritmo Genético (fitness, crossover, mutação)
│   └── main.py                # Script de execução (main)
│
├── notebooks/                 # (opcional) prototipagem/explorações
│   └── prototyping.ipynb
│
├── outputs/                   # Resultados gerados
│   ├── best_schedule.xlsx     # Melhor escala encontrada
│   └── logs/                  # Logs de execução
│
├── requirements.txt           # Dependências Python
├── README.md                  # Você está aqui ;‑)
└── Tech Challenge.pdf         # Arquivo final de entrega (links do vídeo e Git)
```

> **Obs.:** Essa estrutura é apenas sugestão; sinta‑se livre para renomear diretórios desde que mantenha clareza.
> O único nome obrigatório segundo o edital é **Tech Challenge.pdf**.

---

## 3 ⚙️ Pré‑requisitos

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # pandas numpy openpyxl
```

---

## 4 🚀 Como Rodar

### 📂 Ordem de Execução dos Arquivos `src/`

| Ordem | Arquivo                 | Função principal                                                                                                                     |
|-------|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| 1️⃣    | `support_functions.py`  | Define funções utilitárias (ETL, verificação de CLT, geração de escala inicial). **Não é executado diretamente** – apenas importado. |
| 2️⃣    | `ga_functions.py`       | Implementa todo o núcleo do AG: `gerar_fitness`, `crossover`, `gerar_mutacao` etc. Também é apenas importado.                        |
| 3️⃣    | `main.py`               | **Script principal**: carrega dados, invoca funções dos dois módulos acima, executa o loop evolutivo e grava/mostra a melhor escala. |

#### 👉 Como rodar localmente e no Colab
```bash
python src/main.py

O script:

1. Carrega os dados em `data/`.
2. Gera uma população inicial **hot‑start** com restrições básicas.
3. Executa até 1000 gerações (ou convergência) aplicando elitismo, crossover e mutação.
4. Salva a melhor escala em `outputs/best_schedule.xlsx` e imprime métricas no console.

Parâmetros importantes estão declarados no topo de `main.py` (tamanho da população, taxa de mutação, etc.).

---

## 4B 📓 Executando passo a passo no Google Colab

1. **Crie um novo notebook** em [https://colab.research.google.com](https://colab.research.google.com).
2. **Carregue os dados e o código**:

   * Menu ▸ *Files* ▸ *Upload* ▸ envie toda a pasta `data/` e os três arquivos `.py` de `src/`.
   * Ou, se o repositório estiver no GitHub, use:

     ```python
     !git clone https://github.com/edummoreno/2_Tech_challenge
     %cd tech-challenge
     ```
3. **Instale dependências** dentro da primeira célula:

   ```python
   !pip install pandas numpy openpyxl
   ```
4. **Importe as funções**. Exemplo de célula:

   ```python
   from src.main import main  # se você embrulhar o loop em função main()
   main()
   ```

   > Se preferir rodar tal qual o script, use:
   >
   > ```python
   > !python src/main.py
   > ```
5. **Acompanhe a saída** direto no console do Colab; ao final você verá o fitness por geração.
6. **Baixe o resultado**: se o script salvar `outputs/best_schedule.xlsx`, use:

   ```python
   from google.colab import files
   files.download('outputs/best_schedule.xlsx')
   ```

> **Dica:** para não ter que fazer upload manual a cada vez, coloque seus arquivos em um repositório Git público ou privado e apenas `git clone` dentro do Colab.

---

## 5 🧬 Descrição do Algoritmo Genético

| Etapa             | Implementação                                                      | Arquivo                                |
| ----------------- | ------------------------------------------------------------------ | -------------------------------------- |
| **Genoma**        | Escala mensal (DataFrame)                                          | *support\_functions* / *ga\_functions* |
| **Inicialização** | Heurística (hotstart)                                              | `support_functions.gerar_escala_final` |
| **Fitness**       | Pontua o atendimento diário por turno, com peso maior aos domingos | `ga_functions.gerar_fitness`           |
| **Seleção**       | Elitismo + pares randômicos para crossover                         | `main.py`                 |
| **Crossover**     | Troca de linhas (funcionários) entre dois pais                     | `ga_functions.crossover`               |
| **Mutação**       | Alteração de linhas aleatórias com taxa adaptativa                 | `ga_functions.gerar_mutacao`           |
| **Parada**        | 1000 gerações ou estagnação                                        | `main.py`                 |

---

## 6 🔎 Como funciona cada módulo

* **support\_functions.py** – ETL + regras de domínio (dias trabalhados seguidos, domingos, folgas, etc.).
* **ga\_functions.py** – calcula fitness, ordena população, realiza crossover e mutação.
* **setor\_selecionado.py** – ponto de entrada; orquestra o GA, ajusta a diversidade e produz saída.

---

## 7 📊 Resultados & Benchmark

### 📈 Melhor solução encontrada

<details>
<summary>Clique para ver a escala</summary>

```text
       Funcionário       Setor  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
0   Jorge de Jesus  Hortifruti  N  N  N  F  N  N  N  N  F  M  M  M  M  F  M  M  M  M  M  F  N  F  N  N  N  N  N  N  N  F  F
1   Thiago Machado  Hortifruti  M  M  M  M  M  M  M  F  N  N  N  N  F  M  M  F  N  N  N  N  N  N  N  F  M  M  M  M  M  M  M
2     José Fonseca  Hortifruti  M  M  M  M  M  M  F  M  M  F  N  N  F  N  N  F  M  M  M  M  M  M  M  F  N  N  N  N  N  N  N
3  Willian Machado  Hortifruti  N  N  N  N  F  M  M  M  M  M  M  M  M  F  F  N  N  N  N  F  N  N  F  M  M  M  M  M  M  M  F
4  Marcelo Ribeiro  Hortifruti  F  N  F  N  N  F  N  N  N  N  F  M  N  N  N  N  N  N  F  M  M  M  M  N  N  N  F  F  N  N  N
```

</details>



## 📹 Vídeo Explicativo

[🔗 Assista ao Vídeo da Apresentação no YouTube]()


---

## 9 🚧 Próximos Passos

* Roda multiprocessamento para acelerar fitness.
* Permitir vários setores simultâneos.
* UI (Streamlit).

---

© 2025 – Pós‑Tech IA para Devs  – Projeto acadêmico

## 📬 Contato do grupo


**Marco Antonio**
- [🔗 LinkedIn](https://www.linkedin.com/in/marco-antonio-augusto-58b73794)

**Eduardo Moreno Neto**
- [🔗 LinkedIn](https://www.linkedin.com/in/eduardo-moreno-neto/)

**Robert Harada**
- [🔗 LinkedIn](https://www.linkedin.com/in/)

**Alexandre Santana**
- [🔗 LinkedIn](https://www.linkedin.com/in/franciscoeduardo-granado)


