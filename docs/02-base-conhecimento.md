# Base de Conhecimento

## Dados Utilizados

| Arquivo                     | Formato | Utilização no Agente                                                          |
| --------------------------- | ------- | ----------------------------------------------------------------------------- |
| `historico_atendimento.csv` | CSV     | Contextualizar interações anteriores afim de dar continuidade ao atendimento. |
| `perfil_investidor.json`    | JSON    | Personalizar recomendações sobre dúvidas e necessidades do cliente.           |
| `produtos_financeiros.json` | JSON    | Sugerir produtos adequados ao perfil do cliente                               |
| `transacoes.csv`            | CSV     | Analisar padrão de gastos do cliente                                          |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Sim. Expandi os dados de transações, totalizando 36 transações entre agosto e outubro de 2025, com o intuito de ampliar o que o agente consegue responder. Alguns comportamentos foram variados intencionalmente entre os meses para enriquecer a análise:

- Gastos com alimentação apresentam tendência de queda (R$ 730 em agosto → R$ 675 em setembro → R$ 570 em outubro), permitindo ao agente identificar melhora no padrão de gastos.
- Gastos com saúde variam com eventos esporádicos, como uma consulta médica em setembro (R$ 180), simulando imprevistos reais.
- Agosto e setembro incluem aportes no Tesouro Selic (R$ 300 cada), enquanto outubro não registra investimento, o que permite ao agente identificar a ausência e sugerir retomada.
- Agosto inclui um gasto extra de lazer (show, R$ 120), demonstrando variação de comportamento entre meses.

---

## Estratégia de Integração

### Como os dados são carregados?

> Descreva como seu agente acessa a base de conhecimento.

```python
import pandas as pd
import json

# Arquivos CSV
historico_atendimento = pd.read_csv("data/historico_atendimento.csv", sep=",",encoding="utf-8")
transacoes = pd.read_csv("data/transacoes.csv", sep=",", encoding="utf-8")

# Arquivos JSON
with open("data/perfil_investidor.json", "r", encoding="utf-8") as archive:
    perfil = json.load(archive)

with open("data/produtos_financeiros.json", "r", encoding="utf-8") as archive:
    produtos = json.load(archive)

```

### Como os dados são usados no prompt?

> Os dados vão no system prompt? São consultados dinamicamente?

De forma simplificada, os dados serão injetados no system prompt, garantindo que o agente tenha o melhor contexto possível antes de responder. É válido lembrar que em soluções robustas o ideal é que os dados sejam consultados dinamicamente, via RAG ou chamadas a APIs.

```text

PERFIL DO CLIENTE

{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}

PRODUTOS FINANCEIROS

[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.00,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "indicado_para": "Quem busca segurança com rendimento diário"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
  },
  {
    "nome": "Fundo Multimercado",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "CDI + 2%",
    "aporte_minimo": 500.00,
    "indicado_para": "Perfil moderado que busca diversificação"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "Variável",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil arrojado com foco no longo prazo"
  }
]

HISTÓRICO DE ATENDIMENTO

data,canal,tema,resumo,resolvido
2025-09-15,chat,CDB,Cliente perguntou sobre rentabilidade e prazos,sim
2025-09-22,telefone,Problema no app,Erro ao visualizar extrato foi corrigido,sim
2025-10-01,chat,Tesouro Selic,Cliente pediu explicação sobre o funcionamento do Tesouro Direto,sim
2025-10-12,chat,Metas financeiras,Cliente acompanhou o progresso da reserva de emergência,sim
2025-10-25,email,Atualização cadastral,Cliente atualizou e-mail e telefone,sim

TRANSAÇÕES

data,descricao,categoria,valor,tipo
2025-08-01,Salário,receita,5000.00,entrada
2025-08-02,Aluguel,moradia,1200.00,saida
2025-08-04,Supermercado,alimentacao,520.00,saida
2025-08-05,Netflix,lazer,55.90,saida
2025-08-06,Farmácia,saude,42.00,saida
2025-08-08,Restaurante,alimentacao,95.00,saida
2025-08-10,Uber,transporte,38.00,saida
2025-08-12,Conta de Luz,moradia,165.00,saida
2025-08-15,Academia,saude,99.00,saida
2025-08-18,Combustível,transporte,230.00,saida
2025-08-20,Show de música,lazer,120.00,saida
2025-08-22,Supermercado,alimentacao,210.00,saida
2025-08-28,Aplicação Tesouro Selic,investimento,300.00,saida
2025-09-01,Salário,receita,5000.00,entrada
2025-09-02,Aluguel,moradia,1200.00,saida
2025-09-03,Supermercado,alimentacao,480.00,saida
2025-09-05,Netflix,lazer,55.90,saida
2025-09-07,Farmácia,saude,67.50,saida
2025-09-09,Restaurante,alimentacao,140.00,saida
2025-09-11,Uber,transporte,52.00,saida
2025-09-13,Conta de Luz,moradia,172.00,saida
2025-09-15,Academia,saude,99.00,saida
2025-09-18,Combustível,transporte,245.00,saida
2025-09-20,Consulta médica,saude,180.00,saida
2025-09-23,Supermercado,alimentacao,195.00,saida
2025-09-26,Aplicação Tesouro Selic,investimento,300.00,saida
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O trecho abaixo representa como o system prompt é montado na prática — combinando a instrução de comportamento do agente com os dados do cliente já processados e formatados para leitura do modelo.

```
Você é o ShieldMind, um assistente de planejamento financeiro pessoal.
Seu papel é orientar o cliente com base nos dados fornecidos abaixo,
de forma clara, acolhedora e sem jargões técnicos desnecessários.
Não execute transações, não forneça aconselhamento jurídico e sempre
indique um profissional qualificado quando a situação exigir.

=== PERFIL DO CLIENTE ===
Nome: João Silva | Idade: 32 anos | Profissão: Analista de Sistemas
Renda mensal: R$ 5.000 | Perfil: Moderado | Aceita risco: Não

=== METAS ===
1. Reserva de emergência: R$ 10.000 de R$ 15.000 concluídos (prazo: jun/2026)
2. Entrada do apartamento: R$ 0 de R$ 50.000 concluídos (prazo: dez/2027)

=== GASTOS DE OUTUBRO/2025 ===
Moradia:      R$ 1.380  (27,6% da renda)
Alimentação:  R$   570  (11,4% da renda)
Transporte:   R$   295  (5,9% da renda)
Saúde:        R$   188  (3,8% da renda)
Lazer:        R$    55  (1,1% da renda)
Investimento: R$     0  (0% da renda) sem aporte neste mês

=== HISTÓRICO DE ATENDIMENTO (últimas interações) ===
- out/2025: Acompanhou progresso da reserva de emergência (chat)
- out/2025: Perguntou sobre Tesouro Selic (chat)
- set/2025: Perguntou sobre CDB — rentabilidade e prazos (chat)

=== PRODUTOS DISPONÍVEIS ===
- Tesouro Selic (risco baixo) — indicado para reserva de emergência
- CDB Liquidez Diária (risco baixo) — 102% do CDI, resgate diário
- LCI/LCA (risco baixo) — isento de IR, carência de 90 dias
- Fundo Multimercado (risco médio) — indicado para perfil moderado
- Fundo de Ações (risco alto) — não indicado para este perfil
```