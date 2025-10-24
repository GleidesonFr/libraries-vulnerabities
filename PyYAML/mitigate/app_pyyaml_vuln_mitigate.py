from yaml_loader import safe_load_with_mitigation, YAMLTooComplexError
import copy

yaml_text = """
a: &a ["AAAAAAAAAA", "AAAAAAAAAA", "AAAAAAAAAA", "AAAAAAAAAA", "AAAAAAAAAA", "AAAAAAAAAA", "AAAAAAAAAA", "AAAAAAAAAA", "AAAAAAAAAA", "AAAAAAAAAA"]
b: &b [*a, *a, *a, *a, *a, *a, *a, *a, *a, *a]
c: &c [*b, *b, *b, *b, *b, *b, *b, *b, *b, *b]
d: &d [*c, *c, *c, *c, *c, *c, *c, *c, *c, *c]
e: &e [*d, *d, *d, *d, *d, *d, *d, *d, *d, *d]
f: &f [*e, *e, *e, *e, *e, *e, *e, *e, *e, *e]
g: &g [*f, *f, *f, *f, *f, *f, *f, *f, *f, *f]
h: &h [*g, *g, *g, *g, *g, *g, *g, *g, *g, *g]
i: &i [*h, *h, *h, *h, *h, *h, *h, *h, *h, *h]
j: &j [*i, *i, *i, *i, *i, *i, *i, *i, *i, *i]
"""

try:
    data = safe_load_with_mitigation(yaml_text)
    print(f"YAML carregado com sucesso: {data}")
    copia = copy.deepcopy(data)
    # processar `data`
except YAMLTooComplexError as e:
    # reporter/log e rejeitar input
    print("YAML rejeitado:", e)
except Exception as e:
    # outros erros (parsing, etc.)
    print("Erro:", e)