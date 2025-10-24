# Versão de mitigação do PyYAML

## Descrição

A maneira mais simples de mitigar uma classe de problemas como a de _parsing_ apresentada pelo PyYAML é contabilizando ou identificando as regiões de risco. No caso dos arquivos YAML, o grande risco está nos aliases e âncoras que podem ser interpretado de forma recursiva, podendo gerar um DoS.

### Solução

Para resolver esse problema, o código proposto tem como o objetivo analisar e identificar os aliases e âncoras, além de validar o YAML combase a quantidade dos mesmos, pois quanto maior for a quantidade de referências recursivas, maior o processamento e maior o risco.

### Execução

Nessa parte,foram elaborados dois arquivos para melhor entendimento:

o `app_pyyaml_vuln_mitigate.py` e o `yaml_loader.py`

O primeiro é responsável por analisar a string que será carregada como YAML e validar sua periculosidade com base a alguns parâmetros. Esses parâmetros estão presentes no arquivo `yaml_loader.py` e são eles:

```bash
DEFAULT_MAX_TOTAL_ALIASES       # número total de aliases aceitável
DEFAULT_MAX_ALIASES_PER_LINE    # número máximo de aliases numa única linha
DEFAULT_MAX_SEQUENTIAL_LEVELS   # se detectar lol1..lol7 -> suspeita forte
DEFAULT_EXPANSION_FACTOR_LIMIT  # heurística: limite conservador de expansão
```

Esses parâmetros podem ser alterados, caso haja necessidade de reduzir o limiar de detecção de um YAML suspeito.

Para executar os códigos, basta aplicar os seguintes comandos no terminal:

`docker build -t pyyaml-mitigacao -f Dockerfile-pyyaml-mitigate .`
`docker run --rm -it pyyaml-mitigacao`

Caso o usuário esteja em um dispositivo POSIX e não for administrador do sistema,utilizar o `sudo`.