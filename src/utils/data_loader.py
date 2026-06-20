import csv
import json
from pathlib import Path
import streamlit as st

@st.cache_resource
def load_files(pasta: Path) -> str:
    """
    Carrega todos os arquivos .json e .csv de um diretório e
    os formata numa string estruturada para servir de contexto à LLM.
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