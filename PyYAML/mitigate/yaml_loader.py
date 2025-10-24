from __future__ import annotations
import re
import yaml
from typing import Tuple, Optional


# ----- Configurações (ajustáveis) -----
DEFAULT_MAX_TOTAL_ALIASES = 200        # número total de aliases aceitável
DEFAULT_MAX_ALIASES_PER_LINE = 50      # número máximo de aliases numa única linha
DEFAULT_MAX_SEQUENTIAL_LEVELS = 7      # se detectar lol1..lol7 -> suspeita forte
DEFAULT_EXPANSION_FACTOR_LIMIT = 1_000_000  # heurística: limite conservador de expansão


# ----- Funções de análise heurística -----


def analyze_yaml_text(yaml_text: str) -> dict:
    """
    Retorna métricas básicas do YAML de entrada.
    """
    anchors = re.findall(r'&([A-Za-z0-9_\-]+)', yaml_text)
    aliases = re.findall(r'\*([A-Za-z0-9_\-]+)', yaml_text)

    total_anchors = len(anchors)
    total_aliases = len(aliases)

    # máximo de aliases por linha (heurística simples)
    max_aliases_per_line = 0
    for line in yaml_text.splitlines():
        count = len(re.findall(r'\*([A-Za-z0-9_\-]+)', line))
        if count > max_aliases_per_line:
            max_aliases_per_line = count

    # detectar sequências numéricas em nomes de anchors (ex: lol1, lol2, lol3...)
    # mapeamos prefixos -> lista de inteiros encontrados
    seq_map = {}
    for a in anchors:
        m = re.match(r'^([A-Za-z_\-]+)(\d+)$', a)
        if m:
            prefix, num = m.group(1), int(m.group(2))
            seq_map.setdefault(prefix, []).append(num)

    longest_sequence = 0
    for prefix, nums in seq_map.items():
        unique_sorted = sorted(set(nums))
        # calcular o maior run consecutivo (1,2,3,...)
        current_run = 1
        best_run = 1
        for i in range(1, len(unique_sorted)):
            if unique_sorted[i] == unique_sorted[i - 1] + 1:
                current_run += 1
                if current_run > best_run:
                    best_run = current_run
            else:
                current_run = 1
        if best_run > longest_sequence:
            longest_sequence = best_run

    return {
        "total_anchors": total_anchors,
        "total_aliases": total_aliases,
        "max_aliases_per_line": max_aliases_per_line,
        "longest_numeric_sequence": longest_sequence,
        "anchors_sample": anchors[:10],
        "aliases_sample": aliases[:10],
    }


def estimate_expansion_factor(metrics: dict) -> int:
    """
    Heurística conservadora para estimar fator relativo de expansão.
    Não pretende ser precisa — só servir como sinalizador de perigo.
    Estratégia (simplificada):
      - assume que cada alias multiplica por N onde N ~ max_aliases_per_line (mínimo 1)
      - usa comprimento da sequência numérica para elevar exponencialmente:
          est = max_aliases_per_line ** longest_numeric_sequence
      - limita o resultado para evitar overflow
    """
    base = max(1, metrics.get("max_aliases_per_line", 1))
    levels = max(1, metrics.get("longest_numeric_sequence", 1))
    est = 1
    try:
        # calcule base ** levels, mas com proteção
        est = pow(base, levels)
        if est > 10**12:  # corte seguro
            est = 10**12
    except OverflowError:
        est = 10**12
    return int(est)


# ----- API pública: safe_load_with_mitigation -----


class YAMLTooComplexError(Exception):
    """Lançada quando o YAML parece excessivamente complexo / perigoso."""
    pass


def safe_load_with_mitigation(
    yaml_text: str,
    *,
    max_total_aliases: int = DEFAULT_MAX_TOTAL_ALIASES,
    max_aliases_per_line: int = DEFAULT_MAX_ALIASES_PER_LINE,
    max_sequential_levels: int = DEFAULT_MAX_SEQUENTIAL_LEVELS,
    expansion_factor_limit: int = DEFAULT_EXPANSION_FACTOR_LIMIT,
) -> object:
    """
    Realiza pré-validação heurística e, se passar, carrega com yaml.safe_load().

    Lança YAMLTooComplexError em caso de detecção.
    """
    metrics = analyze_yaml_text(yaml_text)

    # Regras simples e explicativas
    if metrics["total_aliases"] > max_total_aliases:
        raise YAMLTooComplexError(
            f"Total de aliases ({metrics['total_aliases']}) excede limite "
            f"({max_total_aliases}). Rejeitando para evitar expansão."
        )

    if metrics["max_aliases_per_line"] > max_aliases_per_line:
        raise YAMLTooComplexError(
            f"Aliases por linha ({metrics['max_aliases_per_line']}) excede limite "
            f"({max_aliases_per_line}). Rejeitando para evitar expansão."
        )

    if metrics["longest_numeric_sequence"] >= max_sequential_levels:
        raise YAMLTooComplexError(
            f"Detectada sequência numérica longa de anchors ({metrics['longest_numeric_sequence']} níveis). "
            f"Isso é típico de payloads exponenciais (p.ex. lol1..lolN)."
        )

    # heurística de expansão
    est = estimate_expansion_factor(metrics)
    if est > expansion_factor_limit:
        raise YAMLTooComplexError(
            f"Fator de expansão estimado = {est} > limite ({expansion_factor_limit}). "
            f"Rejeitando para evitar uso exponencial de memória."
        )

    # Se passou nos checks, carregar com safe_load
    return yaml.safe_load(yaml_text)


# ----- execução de exemplo (CLI) -----
def _demo_cli(yaml_text: Optional[str] = None):
    sample = yaml_text or """
lol1: &lol1 [ "l" ]
lol2: &lol2 [ *lol1, *lol1, *lol1, *lol1, *lol1, *lol1, *lol1, *lol1, *lol1, *lol1 ]
lol3: &lol3 [ *lol2, *lol2, *lol2, *lol2, *lol2, *lol2, *lol2, *lol2, *lol2, *lol2 ]
final_payload: *lol3
"""
    print("=== Iniciando demonstração do carregador mitigado ===")
    print("Analisando YAML (pré-scan)...")
    m = analyze_yaml_text(sample)
    for k, v in m.items():
        print(f"  {k}: {v}")
    print("Estimando fator de expansão...")
    print("  estimativa:", estimate_expansion_factor(m))

    try:
        obj = safe_load_with_mitigation(sample)
        print("Carregado com sucesso (safe_load):", type(obj).__name__)
    except YAMLTooComplexError as e:
        print("Rejeitado pela mitigação:", e)
    except Exception as e:
        print("Erro ao carregar (não relacionado à heurística):", e)


if __name__ == "__main__":
    _demo_cli()