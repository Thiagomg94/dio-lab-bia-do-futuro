import csv
import json
from pathlib import Path
import streamlit as st


def _formatar_moeda(valor: float) -> str:
    """Formata um número como moeda brasileira: 1200.0 -> 'R$ 1.200,00'"""
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {texto}"


def _formatar_transacoes(rows: list) -> str:
    """
    Agrupa transações por mês e calcula resumos já somados (entradas, saídas,
    saldo, gastos por descrição e por categoria) ANTES de montar o texto.

    O objetivo é que o modelo não precise somar ou filtrar valores manualmente
    para responder perguntas como "quanto gastei com aluguel em agosto" — essa
    filtragem manual foi a causa raiz dos erros encontrados nos testes (o
    modelo confundia categoria com descrição e misturava transações de meses
    diferentes). Com os resumos pré-calculados, o modelo só precisa "ler" o
    valor certo, não calculá-lo.
    """
    por_mes = {}
    for row in rows:
        mes = row["data"][:7]  # ex: "2025-08"
        por_mes.setdefault(mes, []).append(row)

    blocos_resumo = []
    blocos_detalhe = []

    for mes in sorted(por_mes.keys()):
        transacoes_mes = por_mes[mes]

        total_entrada = sum(float(r["valor"]) for r in transacoes_mes if r["tipo"] == "entrada")
        total_saida = sum(float(r["valor"]) for r in transacoes_mes if r["tipo"] == "saida")

        por_descricao = {}
        por_categoria = {}
        for r in transacoes_mes:
            if r["tipo"] != "saida":
                continue
            valor = float(r["valor"])
            por_descricao[r["descricao"]] = por_descricao.get(r["descricao"], 0) + valor
            por_categoria[r["categoria"]] = por_categoria.get(r["categoria"], 0) + valor

        linhas_descricao = [
            f"  - {desc}: {_formatar_moeda(v)}"
            for desc, v in sorted(por_descricao.items(), key=lambda item: -item[1])
        ]
        linhas_categoria = [
            f"  - {cat}: {_formatar_moeda(v)}"
            for cat, v in sorted(por_categoria.items(), key=lambda item: -item[1])
        ]

        resumo = (
            f"#### Resumo de {mes}\n"
            f"Total de entradas: {_formatar_moeda(total_entrada)}\n"
            f"Total de saídas: {_formatar_moeda(total_saida)}\n"
            f"Saldo do mês: {_formatar_moeda(total_entrada - total_saida)}\n\n"
            f"Gastos por descrição (valores já somados — use diretamente, NÃO recalcule):\n"
            + "\n".join(linhas_descricao) + "\n\n"
            f"Gastos por categoria (valores já somados — use diretamente, NÃO recalcule):\n"
            + "\n".join(linhas_categoria)
        )
        blocos_resumo.append(resumo)

        linhas_detalhe = [
            f"  - {r['data']} | descricao: {r['descricao']} | "
            f"categoria: {r['categoria']} | valor: {_formatar_moeda(float(r['valor']))} | tipo: {r['tipo']}"
            for r in transacoes_mes
        ]
        blocos_detalhe.append(f"#### Transações de {mes}\n" + "\n".join(linhas_detalhe))

    return (
        "## RESUMOS PRÉ-CALCULADOS (já somados — use estes valores diretamente, sem recalcular)\n\n"
        + "\n\n".join(blocos_resumo)
        + "\n\n## TRANSAÇÕES DETALHADAS (use apenas para consultas sobre datas/transações específicas)\n\n"
        + "\n\n".join(blocos_detalhe)
    )


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
                rows = list(csv.DictReader(file.read_text(encoding="utf-8").splitlines()))

                campos_transacao = {"data", "descricao", "categoria", "valor", "tipo"}
                if rows and campos_transacao.issubset(rows[0].keys()):
                    # CSV de transações financeiras: usa resumo pré-calculado
                    text = _formatar_transacoes(rows)
                elif rows and "data" in rows[0]:
                    # CSV com data, mas sem o formato completo de transação
                    por_mes = {}
                    for row in rows:
                        mes = row["data"][:7]
                        por_mes.setdefault(mes, []).append(row)
                    blocos = [
                        f"#### Mês {mes}\n" + "\n".join(f"  - {dict(r)}" for r in por_mes[mes])
                        for mes in sorted(por_mes.keys())
                    ]
                    text = "\n\n".join(blocos)
                else:
                    # Fallback genérico para CSVs sem coluna "data"
                    text = "\n".join(str(dict(row)) for row in rows)

                content.append(f"### {file.name}\n{text}")
            except Exception as e:
                st.error(f"Erro ao ler arquivo CSV {file.name}: {e}")

    return "\n\n".join(content)