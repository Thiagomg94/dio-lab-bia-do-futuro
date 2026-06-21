# 🎤 Pitch — ShieldMind

> Este pitch é apresentado em formato de **slides**.

## Apresentação

📊 [`ShieldMind-Pitch.pptx`](./ShieldMind-Pitch.pptx)

8 slides, pensados para uma apresentação de até 3 minutos — cada slide inclui notas do apresentador (visíveis no modo apresentador do PowerPoint/LibreOffice) com sugestão do que falar em cada momento.

---

## Resumo do conteúdo

| # | Slide | O que mostra |
|---|-------|---------------|
| 1 | Capa | Apresentação do ShieldMind |
| 2 | O problema | Por que assistentes financeiros tradicionais ainda são limitados |
| 3 | A solução | Os quatro pilares do ShieldMind |
| 4 | Como funciona | Fluxo da pergunta até a resposta, passando pelos guardrails |
| 5 | Na prática | Dois exemplos reais de recusa segura e coerente com o perfil do cliente |
| 6 | Diferenciais | Custo zero, guardrails testados, rigor de engenharia |
| 7 | Resultados | Evolução de 62,5% para 100% nos testes, com as correções que levaram até lá |
| 8 | Encerramento | Fechamento e onde encontrar a documentação completa |

---

## Roteiro resumido (versão texto)

### Qual problema o ShieldMind resolve?
Assistentes financeiros tradicionais costumam ser reativos, pouco personalizados e correm o risco de alucinar informações — um problema sério quando o assunto é dinheiro. O ShieldMind nasce com guardrails de segurança como parte do design, não como camada adicional.

### Como ele funciona na prática?
A pergunta do cliente chega à interface (Streamlit). Os dados do cliente (perfil, metas, transações) já são pré-processados em Python — incluindo somas pré-calculadas, para evitar erro de cálculo do modelo. Esse contexto, junto com as regras de comportamento do system prompt, é enviado ao Ollama (`llama3.1:8b`, rodando localmente), que gera a resposta final.

### Por que essa solução é inovadora?
- **Custo zero e dados locais:** sem API paga, sem dados saindo do ambiente do usuário
- **Guardrails testados, não só descritos:** cada regra de comportamento foi validada com cenários de teste reais — incluindo casos de falha documentados, não só os de sucesso
- **Rigor de engenharia:** os bugs mais significativos do projeto não estavam no modelo, e sim em decisões de arquitetura (pré-processamento de dados, configuração da janela de contexto do Ollama) — identificados e corrigidos ao longo do ciclo de testes

---

📄 Documentação completa do projeto: [`docs/01-documentacao-agente.md`](./01-documentacao-agente.md) · [`docs/03-prompts.md`](./03-prompts.md) · [`docs/04-metricas.md`](./04-metricas.md)

