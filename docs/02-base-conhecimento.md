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



Os dados de transações foram expandidos, totalizando 36 transações entre agosto e outubro de 2025, com o intuito de ampliar o que o agente consegue responder. Alguns comportamentos foram variados intencionalmente entre os meses para enriquecer a análise:

- Gastos com alimentação apresentam tendência de queda (R$ 730 em agosto → R$ 675 em setembro → R$ 570 em outubro), permitindo ao agente identificar melhora no padrão de gastos.
- Gastos com saúde variam com eventos esporádicos, como uma consulta médica em setembro (R$ 180), simulando imprevistos reais.
- Agosto e setembro incluem aportes no Tesouro Selic (R$ 300 cada), enquanto outubro não registra investimento, o que permite ao agente identificar a ausência e sugerir retomada.
- Agosto inclui um gasto extra de lazer (show, R$ 120), demonstrando variação de comportamento entre meses.

---

## Estratégia de Integração

### Como os dados são carregados?

O agente acessa a base de dados de forma automatizada e otimizada por meio do utilitário [data_loader.py](file:///c:/Users/Thiago/OneDrive/Documentos/Projeto%20Agente%20Dio/src/utils/data_loader.py). Em vez de usar bibliotecas como Pandas, a leitura é feita com módulos nativos do Python (`json` e `csv`), garantindo leveza e velocidade.

Para evitar carregamentos repetitivos em cada interação do usuário, a função possui cache nativo do Streamlit utilizando o decorador `@st.cache_resource`.

```python
import csv
import json
from pathlib import Path
import streamlit as st

@st.cache_resource
def load_files(pasta: Path) -> str:
    """
    Carrega todos os arquivos .json e .csv de um diretório e
    os formata em uma string estruturada para servir de contexto à LLM.
    """
    content = []

    if not pasta.exists() or not pasta.is_dir():
        return ""

    # Ordena os arquivos para garantir consistência no prompt gerado
    for file in sorted(pasta.iterdir()):
        if file.suffix == ".json":
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                text = json.dumps(data, ensure_ascii=False, indent=2)
                content.append(f"### {file.name}\n{text}")
            except Exception as e:
                st.error(f"Erro ao ler arquivo JSON {file.name}: {e}")

        elif file.suffix == ".csv":
            try:
                reader = csv.DictReader(file.read_text(encoding="utf-8").splitlines())
                lines = [str(dict(row)) for row in reader]
                text = "\n".join(lines)
                content.append(f"### {file.name}\n{text}")
            except Exception as e:
                st.error(f"Erro ao ler arquivo CSV {file.name}: {e}")

    return "\n\n".join(content)
```

### Como os dados são usados no prompt?

Os dados agregados em formato de string estruturada são injetados diretamente no system prompt. O módulo [config.py](file:///c:/Users/Thiago/OneDrive/Documentos/Projeto%20Agente%20Dio/src/config.py) carrega as instruções do template de prompt contido em [system_prompt.txt](file:///c:/Users/Thiago/OneDrive/Documentos/Projeto%20Agente%20Dio/src/prompts/system_prompt.txt) e injeta o texto gerado dinamicamente no campo `{context}`.

A chamada de montagem ocorre no ponto de entrada:
```python
# No app.py:
context = load_files(DOCS_PATH)
system_prompt = get_system_prompt(context)
```

---

## Exemplo de Contexto Montado

O trecho abaixo representa um exemplo real de como a base de conhecimento é formatada em string e injetada no prompt de sistema enviado ao Ollama:

```text
Você é o ShieldMind, um assistente de planejamento financeiro pessoal.
Seu papel é orientar o cliente com base nos dados fornecidos abaixo, de forma clara, 
acolhedora e sem jargões técnicos desnecessários.

## Base de conhecimento:
### historico_atendimento.csv
{'data': '2025-09-15', 'canal': 'chat', 'tema': 'CDB', 'resumo': 'Cliente perguntou sobre rentabilidade e prazos', 'resolvido': 'sim'}
{'data': '2025-09-22', 'canal': 'telefone', 'tema': 'Problema no app', 'resumo': 'Erro ao visualizar extrato foi corrigido', 'resolvido': 'sim'}
{'data': '2025-10-01', 'canal': 'chat', 'tema': 'Tesouro Selic', 'resumo': 'Cliente pediu explicação sobre o funcionamento do Tesouro Direto', 'resolvido': 'sim'}
{'data': '2025-10-12', 'canal': 'chat', 'tema': 'Metas financeiras', 'resumo': 'Cliente acompanhou o progresso da reserva de emergência', 'resolvido': 'sim'}
{'data': '2025-10-25', 'canal': 'email', 'tema': 'Atualização cadastral', 'resumo': 'Cliente atualizou e-mail e telefone', 'resolvido': 'sim'}

### perfil_investidor.json
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.0,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.0,
  "reserva_emergencia_atual": 10000.0,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.0,
      "prazo": "2026-06"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.0,
      "prazo": "2027-12"
    }
  ]
}

### produtos_financeiros.json
[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.0,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.0,
    "indicado_para": "Quem busca segurança com rendimento diário"
  }
]

### transacoes.csv
{'data': '2025-08-01', 'descricao': 'Salário', 'categoria': 'receita', 'valor': '5000.00', 'tipo': 'entrada'}
{'data': '2025-08-02', 'descricao': 'Aluguel', 'categoria': 'moradia', 'valor': '1200.00', 'tipo': 'saida'}
```