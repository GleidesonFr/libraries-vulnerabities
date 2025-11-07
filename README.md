# Estudo de Vulnerabilidades na Biblioteca PyYAML

## Sobre o Trabalho

Esse repositório tem como objetivo apresentar a biblioteca PyYAML onde foram detectadas falhas de segurança rotuladas pelo [Common Vulnerabilities and Exposures - CVE](https://www.cve.org/). O repositório segue uma estrutura simples baseada em:

1. Versões antigas
2. Versões recentes
3. Versão de mitigação (criadas nesse repositório, portanto, não oficiais)

### [PyYAML](https://pypi.org/project/PyYAML/)

PyYAML é a biblioteca padrão e mais utilizada em Python para trabalhar com o formato de serialização de dados YAML (_YAML Ain't Markup Language_). Ela funciona como um analisador (_parser_) e um emissor (_emitter_), permitindo que programas Python leiam e escrevam dados em arquivos YAML de forma simples e eficiente.

#### _Loaders_

Os _loaders_ no _PyYAML_ são classes ou funções que definem como os dados em formato YAML devem ser interpretados e convertidos em objetos _Python_. A partir da versão 5.1 do _PyYAML_, o uso do parâmetro `Loader` na função `yaml.load()` tornou-se obrigatório para especificar explicitamente o nível de segurança e funcionalidade desejado na análise (_parsing_) dos dados.

##### Principais _Loaders_

Os _loaders_ mais comuns e importantes são:

* `yaml.SafeLoader`: Este é o _loader_ recomendado e mais seguro para a maioria dos casos. Ele analisa apenas um subconjunto seguro da especificação _YAML_ e é incapaz de construir objetos _Python_ arbitrários. Isso previne vulnerabilidades de segurança, como a execução de código malicioso a partir de um arquivo _YAML_.

* `yaml.FullLoader`: Este _loader_ suporta a análise de todas as _tags YAML_ padrão, incluindo a capacidade de construir objetos Python arbitrários, mas ainda com algumas restrições de segurança em comparação com o `UnsafeLoader`.

* `yaml.Loader`: O _loader_ padrão mais antigo. Ele tem a capacidade de carregar objetos _Python_ arbitrários, o que o torna inseguro para uso com entradas não confiáveis, pois pode levar à execução remota de código (RCE). Seu uso sem especificação explícita nafunção `yaml.load()` está obsoleto e foi removido em versões mais recentes do _PyYAML_.

* `yaml.UnsafeLoader`: Equivale ao comportamento do antigo `yaml.Loader`, suporta a construção de objetos _Python_ arbitrários e não é recomendado para dados de fontes não confiáveis.

#### Vulnerabilidade Rotulada ([CVE-2020-14343](https://www.cve.org/CVERecord?id=CVE-2020-14343))
_Data de publicação: 09/02/2021
Data de Atualização: 06/07/2023
Detectado por: Red Hat Inc._

A vulnerabilidade foi descoberta na biblioteca PyYAML em versões anteriores à 5.4, onde ela é suscetível à execução de código arbitrário ao processar arquivos YAML não confiáveis ​​por meio dos métodos `load()` e `full_load()` ou com os carregadores `Loader` e `FullLoader`. Aplicativos que usam a biblioteca para processar entradas não confiáveis ​​podem ser vulneráveis ​​a essa falha. Ela permite que um invasor execute código arbitrário no sistema, abusando do construtor `python/object/new`. Essa falha se deve a uma correção incompleta para o CVE-2020-1747.