import ollama

def chat_with_llm(model: str, system_prompt: str, chat_history: list) -> str:
    """
    Envia o histórico de mensagens e o system prompt estruturado para o Ollama
    e retorna a resposta gerada pelo modelo.
    """
    # Prepara as mensagens injetando o system prompt como a primeira instrução
    messages = [{"role": "system", "content": system_prompt}]
    
    # Mapeia as chaves do histórico caso haja diferenças de nomes no estado
    for msg in chat_history:
        messages.append({
            "role": msg["role"],
            "content": msg["context"]  # mantendo 'context' para compatibilidade com o estado anterior
        })

    response = ollama.chat(
        model=model,
        messages=messages
    )
    
    return response["message"]["content"]
