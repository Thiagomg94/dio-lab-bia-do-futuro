# 🛡️ ShieldMind — Assistente de Planejamento Financeiro Pessoal

Agente conversacional de planejamento financeiro construído com IA Generativa local (Ollama), desenvolvido como desafio de bootcamp a partir do template [`lab-agente-financeiro`](#).

> O ShieldMind simula um assistente financeiro bank-facing: ajuda o cliente a entender seus gastos, acompanhar metas e receber sugestões de produtos compatíveis com seu perfil de investidor — sempre dentro de guardrails explícitos contra conselho jurídico/tributário e exposição de dados sensíveis.

---

## Sobre o projeto

O ShieldMind responde perguntas sobre a vida financeira de um cliente com base em dados mockados (transações, metas, perfil de investidor e produtos disponíveis), rodando 100% local via [Ollama](https://ollama.ai) — sem custo de API e sem enviar dados a serviços externos.

**O que o agente faz:**
- Analisa gastos por categoria e por mês
- Acompanha o progresso de metas financeiras (ex: reserva de emergência)
- Recomenda produtos financeiros compatíveis com o perfil de risco do cliente
- Explica conceitos financeiros de forma simples e sem jargão

**O que o agente *não* faz (por design):**
- Não fornece conselho jurídico, tributário ou atuarial — sempre redireciona para um profissional qualificado
- Não executa transações nem armazena credenciais ou dados sensíveis
- Não garante rentabilidade ou retorno de produtos financeiros
- Não recomenda produtos com risco incompatível com o perfil declarado do cliente, mesmo que solicitado explicitamente

## Cliente mockado

Os testes e exemplos deste projeto usam um cliente fictício único — **João Silva**, perfil de investidor **moderado**, com duas metas ativas: completar uma reserva de emergência (R$ 15.000 até junho/2026) e juntar entrada para um apartamento (R$ 50.000 até dezembro/2027). Os dados de transações cobrem três meses (ago-out/2025) com variações intencionais de comportamento (queda em gastos com alimentação, ausência de aporte em outubro) para enriquecer a análise.

---

## Arquitetura

```
Pergunta do usuário (Streamlit)
        │
        ▼
data/*.json, *.csv ──► data_loader.py ──► contexto pré-processado
        │                                  (somas pré-calculadas por
        │                                   mês/categoria/descrição)
        ▼
src/prompts/system_prompt.txt + contexto ──► system_prompt final
        │
        ▼
llm_service.py ──► Ollama (llama3.1:8b, num_ctx=8192) ──► resposta
```

**Stack:**

| Camada | Tecnologia |
|--------|------------|
| Interface | Streamlit |
| LLM | Ollama (local) — `llama3.1:8b` |
| Linguagem | Python |
| Dados | JSON + CSV mockados (sem banco de dados) |

> RAG foi avaliado e descartado para este projeto, dado o prazo do desafio — a estratégia adotada foi injeção direta de contexto pré-processado no system prompt.

### Estrutura do repositório

```
📁 ShieldMind/
│
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 .env.example
│
├── 📁 data/                          # Dados mockados (cliente João Silva)
│   ├── transacoes.csv
│   ├── historico_atendimento.csv
│   ├── perfil_investidor.json
│   └── produtos_financeiros.json
│
├── 📁 docs/                          # Documentação do projeto
│   ├── 01-documentacao-agente.md     # Caso de uso e arquitetura
│   ├── 02-base-conhecimento.md       # Estratégia de dados
│   ├── 03-prompts.md                 # Engenharia de prompts (regras + few-shot)
│   ├── 04-metricas.md                # Testes, métricas e ciclo de depuração
│   └── 05-pitch.md                   # Roteiro do pitch
│   └── 06-ShieldMind-Pitch.pptx      # Slides do pitch
│
├── 📁 src/
│   ├── app.py                        # Interface Streamlit
│   ├── config.py                     # Variáveis de ambiente e carregamento do prompt
│   ├── prompts/
│   │   └── system_prompt.txt         # System prompt em produção
│   ├── utils/
│   │   └── data_loader.py            # Leitura e pré-processamento dos dados
│   └── services/
│       └── llm_service.py            # Integração com o Ollama
│
├── 📁 assets/                        # Imagens e diagramas
```

---

## Como executar

**Pré-requisitos:** Python 3.10+, [Ollama](https://ollama.ai) instalado.

```bash
# 1. Clone o repositório
git clone <https://github.com/Thiagomg94/dio-lab-bia-do-futuro/tree/main>
cd ShieldMind

# 2. Crie e ative um ambiente virtual
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate   # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Baixe o modelo no Ollama
ollama pull llama3.1:8b

# 5. Configure as variáveis de ambiente
copy .env.example .env      # Windows
# cp .env.example .env        # Linux/Mac
# Edite o .env se necessário (OLLAMA_MODEL=llama3.1:8b)

# 6. Rode a aplicação
streamlit run src/app.py
```

---

## Decisões técnicas e aprendizados

Esta seção documenta as decisões mais relevantes tomadas durante o desenvolvimento — incluindo bugs encontrados e corrigidos, não só o resultado final (ver histórico completo em [`docs/04-metricas.md`](./docs/04-metricas.md)):

- **Modelo:** iniciado com `llama3.2` (3B) e migrado para `llama3.1:8b` — o modelo menor alucinava conceitos financeiros e tinha dificuldade em generalizar regras de comportamento para frases não vistas explicitamente nos exemplos do prompt.
- **Pré-cálculo de somas (`data_loader.py`):** consultas sobre gastos por categoria/mês falhavam quando o LLM precisava filtrar e somar transações brutas manualmente — confundia o campo `descricao` com `categoria` e misturava meses. A correção move a soma para Python; o modelo só localiza o valor já calculado.
- **Janela de contexto (`num_ctx`):** o maior bug encontrado no projeto não estava no modelo nem no prompt — era a ausência de `num_ctx` explícito na chamada ao Ollama. O padrão do Ollama corta silenciosamente o início do prompt quando o total excede o limite, o que removia as regras de comportamento e os dados de perfil/metas sem nenhum erro visível, parecendo um problema de comportamento do agente.
- **Few-shot prompting:** regras descritas em texto não foram suficientes para o modelo generalizar para variações de fraseado (ex: pergunta tributária sobre aluguel sem mencionar "Imposto de Renda"). Exemplos literais com os dados reais do cliente mockado resolveram esse gap.

## Testes e métricas

8 cenários de teste cobrindo assertividade, segurança, coerência com o perfil e conformidade com as regras de comportamento. Após o ciclo de correções acima, o agente passa em **8/8 testes**.

Ver detalhamento completo de cada teste, incluindo o histórico de falhas e as causas raiz identificadas, em [`docs/04-metricas.md`](./docs/04-metricas.md).

## Possíveis melhorias futuras

- Padronizar formatação de moeda (uso consistente de "R$")
- Monitorar `num_ctx` conforme o histórico de conversa cresce (todo o histórico é reenviado a cada turno)
- Resolver pequenas imprecisões técnicas em explicações de conceitos macroeconômicos (ex: distinção entre renda fixa pré e pós-fixada)

---

## Documentação completa

| Documento | Conteúdo |
|-----------|----------|
| [`docs/01-documentacao-agente.md`](./docs/01-documentacao-agente.md) | Caso de uso, persona e arquitetura |
| [`docs/02-base-conhecimento.md`](./docs/02-base-conhecimento.md) | Estratégia de dados mockados |
| [`docs/03-prompts.md`](./docs/03-prompts.md) | System prompt, regras e exemplos de few-shot |
| [`docs/04-metricas.md`](./docs/04-metricas.md) | Testes, métricas e ciclo de depuração |
| [`docs/05-pitch.md`](./docs/05-pitch.md) | Roteiro do pitch |

---

*Projeto desenvolvido como desafio de bootcamp, a partir do template `lab-agente-financeiro`.*

