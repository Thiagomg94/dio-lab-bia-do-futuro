# 📸 Capturas de Tela — ShieldMind

Este diretório reúne screenshots do agente em funcionamento, organizados por cenário. Para o contexto completo do projeto, ver o [README principal](../README.md).

> **Como adicionar uma nova captura:** salve a imagem nesta pasta (`assets/`) e referencie com `![descrição](nome-do-arquivo.png)`. Sugestão: use nomes em minúsculas, sem espaços e sem acentos.

---

## Funcionalidades principais

### Tela inicial
![Tela inicial do ShieldMind](tela-inicial.png)
*Interface de chat ao abrir a aplicação.*

### Consulta de gastos por categoria
![Consulta de gastos](consulta-gastos.png)
*O agente analisa as transações do cliente e responde com valores já pré-calculados por mês e categoria.*

### Recomendação de produto compatível com o perfil
![Recomendação de investimento](recomendacao-investimento.png)
*Sugestão de investimento considerando o perfil de risco e as metas ativas do cliente.*

---

## Guardrails de segurança

### Recusa de conselho tributário
![Recusa de conselho tributário](recusa-tributaria.png)
*O agente reconhece a pergunta como tributária — mesmo sem o termo "Imposto de Renda" — e indica um profissional qualificado.*

### Recusa de produto incompatível com o perfil
![Recusa de produto de alto risco](recusa-risco.png)
*Mesmo com pedido explícito do cliente, o agente recusa recomendar um produto de risco incompatível com o perfil moderado.*

### Proteção de dados sensíveis
![Proteção de dados sensíveis](protecao-dados.png)
*O agente recusa armazenar credenciais do usuário e explica por quê.*

### Pergunta fora do escopo
![Pergunta fora do escopo](fora-escopo.png)
*Resposta a uma pergunta sem relação com finanças pessoais.*

---

*Capturas de tela atualizadas em: 21/06/2026*
