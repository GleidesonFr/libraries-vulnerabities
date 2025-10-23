# Nova versão do PyYAML

## Descrição

A versão dessa biblioteca trouxe várias atualizações para mitigar falhas em métodos como `load()` e `full_load()`. Entretanto, o método `safe_load()` ainda continua com falhas ao tratar de âncoras, possibilitando ataques DDoS, caso usado recursão.

### Execução

Para executar o código, é importante acessar a pasta:

`cd PyYAML/new`

E executar o Dockerfile com os comandos

`docker build -t pyyaml-latest -f Dockerfile-pyyaml-latest .`
`docker run --rm -it pyyaml-latest`

Ao executa o último comando, o usuário será conduzido ao root do container. Nele, basta o mesmo digitar

`python app_test_vuln_new.py`

Que o código será executado.