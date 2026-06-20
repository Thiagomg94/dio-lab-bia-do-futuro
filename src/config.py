import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env, se existir
load_dotenv()

# Caminho base do projeto (raiz)
ROOT_DIR = Path(__file__).resolve().parent.parent

# Configurações globais
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
DOCS_PATH = ROOT_DIR / "data"
PROMPT_PATH = ROOT_DIR / "src" / "prompts" / "system_prompt.txt"

def get_system_prompt(context: str) -> str:
    """
    Carrega o template do prompt do sistema a partir do arquivo txt
    e injeta a base de conhecimento (contexto).
    """
    if not PROMPT_PATH.exists():
        # Fallback de segurança se o arquivo não estiver disponível
        return (
            "Você é o ShieldMind, um assistente de planejamento financeiro pessoal. "
            "Seu papel é orientar o cliente com base nos dados fornecidos abaixo.\n\n"
            f"## Base de conhecimento:\n{context}"
        )
    
    template = PROMPT_PATH.read_text(encoding="utf-8")
    return template.format(context=context)
