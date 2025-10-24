# Estudo de Vulnerabilidades em Bibliotecas Python

## Sobre o Trabalho

Esse repositório tem como objetivo apresentar algumas bibliotecas utilizadas em linguagem de programação Python, onde foram detectadas falhas de segurança rotuladas pelo [Common Vulnerabilities and Exposures - CVE](https://www.cve.org/). O repositório segue uma estrutura simples baseada em:

1. Versões antigas
2. Versões recentes
3. Versão de mitigação (criadas nesse repositório, portanto, não oficiais)

### Bibliotecas

#### [PyYAML](https://pypi.org/project/PyYAML/)

PyYAML é a biblioteca padrão e mais utilizada em Python para trabalhar com o formato de serialização de dados YAML (_YAML Ain't Markup Language_). Ela funciona como um analisador (_parser_) e um emissor (_emitter_), permitindo que programas Python leiam e escrevam dados em arquivos YAML de forma simples e eficiente.

##### Vulnerabilidade Rotulada ([CVE-2020-14343](https://www.cve.org/CVERecord?id=CVE-2020-14343))
_Data de publicação: 09/02/2021
Data de Atualização: 06/07/2023
Detectado por: Red Hat Inc._

A vulnerabilidade foi descoberta na biblioteca PyYAML em versões anteriores à 5.4, onde ela é suscetível à execução de código arbitrário ao processar arquivos YAML não confiáveis ​​por meio do método `full_load()` ou com o carregador `FullLoader`. Aplicativos que usam a biblioteca para processar entradas não confiáveis ​​podem ser vulneráveis ​​a essa falha. Ela permite que um invasor execute código arbitrário no sistema, abusando do construtor `python/object/new`. Essa falha se deve a uma correção incompleta para o CVE-2020-1747.

Essa correção incompleta também diz respeito ao `safe_loader()` que é um dos carregadores do PyYAML que visa o carregamento seguro contra criação de objetos python no YAML. Entretanto, acerca das âncora e aliases que ainda persiste em versões atuais, o método ainda é insuficiente, podendo ser feito recursividade por meio de referência utilizando esses identificadores.