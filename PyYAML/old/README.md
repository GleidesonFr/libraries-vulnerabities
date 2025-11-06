# Demonstração de Vulnerabilidades na Biblioteca PyYAML Versão 5.3.1

## Descrição

Nessa parte de estudo dessa biblioteca, estarei apresentando a execução de um comando _Python_ que executa um subprocesso, cujo o objetivo é listar os arquivos do diretório atual, evidenciando que um atacante pode obter controle total ao utilizar da falha de **desserialização insegura**. É apenas um exemplo demonstrativo para provar que o arquivo ```.yaml``` malicioso pode apresentar afetar um sistema que utilize essa versão.

**Autoria:** Gleideson Freitas de Paiva Vieira
**Data:** 11/2025

## Vulnerabilidade Demonstrada

| Vulnerabilidade | Tipo de Ataque | Função Insegura | Solução Essencial |
| :-------------- | :------------- | :-------------- | :---------------- |
| Execução Remota de Código (RCE) | Desserialização Insegura (```!!python/object/apply```) | ```yaml.load(Loader=yaml.Loader)``` | ```yaml.safe_load()``` |

## Execução

Por motivos de privacidade aos usuário do repositório, foi criado um container para exemplificar o ataque. Por favor, **NÃO EXECUTAR DERIVADOS NOCIVOS DESSE CÓDIGO EM UM AMBIENTE HOST. ISSO PODE OCASIONAR DANOS AOS DADOS OU EXPOSIÇÃO DELES!**

### Pré-Requisitos:

* _Docker Desktop_ ou _Docker CLI_ (Instalado e em Execução. **Não esquecer de ativar o VT-x, caso o computador seja _Intel_ ou AMD-V, caso _AMD_**).
* Terminal (_CMD_, _PowerShell_ ou _Bash_).

### Passos da Execução

**1. Clonar o Repositório**

```bash
git clone https://github.com/GleidesonFr/libraries-vulnerabities.git
```

**2. Ir Para a Pasta**

```bash
cd PyYAML/old
```

**3. Executar o Dockerfile com os Comandos:**

```bash
docker build -t pyyaml-vuln-demo -f Dockerfile-pyyaml-vuln .

docker run --rm -it pyyaml-vuln-demo
```

Caso esteja usando sistemas POSIX sem privilégios de administrador, executar com o `sudo`.

## Detalhamento de Provas (Resultados Esperados)

A saída deve demonstrar o contraste entre o `loader` e a mitigação.

**1. Prova da RCE (Execução Remota de Código)**

* Arquivo de Teste: `app_test_vuln_old.py`
* Payload: Tenta executar o comando `ls -l /etc/`
* Resultado Esperado: 

| Teste	| Função Python | Saída no Terminal	| Conclusão |
| :---- | :------------ | :---------------- | :-------- |
| Estado Inseguro | `yaml.load(Loader=yaml.Loader)` |	Exibição do usuário do contêiner (root) ou listagem de arquivos. |	RCE com sucesso. |
| Estado Seguro | `yaml.safe_load()` |	`yaml.YAMLError: tag: !python/object/apply...` |	Mitigação bem-sucedida. |

## Detalhes de Implementação

* Versão do PyYAML Testada: 5.3.1 (Versão notoriamente vulnerável ao RCE e insegura em relação ao `Loader`).