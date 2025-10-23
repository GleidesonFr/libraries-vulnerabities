# Versão Antiga do PyYAML (5.3.1)
(Por enquanto, somente o código vulnerável foi feito. Código para mitigação na próxima atualização)

## Descrição

Nessa parte de estudo dessa biblioteca, foram detectados vulnerabilidades referente a função `safe_load()`. O objetivo dessa função é carregar dados de uma string formatada em YAML de forma segura. Entretanto, ao se tratar de ancoras de referência embutidas na string, o código consegue ler as mesmas de forma independente sem tratamento.

### Riscos

É possivel criar uma lista utilizando as âncoras, o que pode ser muito útil na estruturação de um YAML. Contudo, o uso recursivo pode ser aplicado, podendo gerar um loop infinito no código. Mesmo que o Python possa tratar o erro, em uma aplicação, um `RecursionError` ainda pode ser tratado como um _crash_ no sistema, impedindo com que a leitura do YAML ocorra, tornando a função inviável.

### Execução

Para executar esse código, é importante acessar a pasta:

`cd PyYAML/old`

E executar o Dockerfile com os comandos:

`docker build -t pyyaml-vuln-demo -f Dockerfile-pyyaml-vuln .`

`docker run --rm -it pyyaml-vuln-demo`

Caso esteja usando sistemas POSIX sem privilégios de administrador, executar com o `sudo`.