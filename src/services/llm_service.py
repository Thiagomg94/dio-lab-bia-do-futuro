import ollama


def chat_with_llm(model: str, system_prompt: str, chat_history: list, num_ctx: int = 8192) -> str:
    """
    Envia o histórico de mensagens e o system prompt estruturado para o Ollama
    e retorna a resposta gerada pelo modelo.

    num_ctx define a janela de contexto em tokens. Sem isso, o Ollama usa um
    padrão pequeno (2048-4096) e corta silenciosamente o INÍCIO do prompt
    quando o total excede o limite — sem erro, sem aviso. Como o system
    prompt (regras + exemplos) e os dados de perfil/metas são carregados
    antes das transações, são eles que ficam de fora quando isso acontece.
    8192 dá margem confortável para o tamanho atual da base de conhecimento;
    pode subir para 16384 sem problema dado o hardware disponível (32GB RAM,
    GPU com 16GB de VRAM).
    """
    messages = [{"role": "system", "content": system_prompt}]

    for msg in chat_history:
        messages.append({
            "role": msg["role"],
            "content": msg["context"]  # mantendo 'context' para compatibilidade com o estado anterior
        })

    response = ollama.chat(
        model=model,
        messages=messages,
        options={"num_ctx": num_ctx}
    )

    return response["message"]["content"]
