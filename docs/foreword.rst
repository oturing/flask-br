Introdução
==========

Leia esta introdução antes de começar a trabalhar com Flask. Este texto
procura esclarecer a finalidade e os objetivos do projeto, e quando ele deve
ou não ser usado.

O que quer dizer "micro"?
-------------------------

"Micro" não significa que a sua aplicação web inteira tenha que se encaixar em
um único arquivo Python, embora isso seja totalmente possível. Também não quer
dizer que falte funcionalidade ao Flask. "Micro" em microframework significa
que o Flask procura manter o núcleo simples, mas extensível. O Flask não toma
muitas decisões por você, tipo, que banco de dados usar. Por outro lado, é
fácil mudar as coisas que já decidiu, tipo, o mecanismo de templates. Todo o
resto fica por sua conta decidir, de modo que você pode obter do Flask tudo o
que precisa e dispensar tudo o que não quer.

Por padrão, o Flask não inclui uma camada de abstração de banco de dados,
validação de formulário, ou qualquer outra coisa para a qual já existam
diferentes bibliotecas. Em vez disso, suporta extensões para adicionar uma
determinada funcionalidade à sua aplicação como se ela tivesse sido
implementada no Flask em si. Muitas extensões fornecem integração de banco de
dados, validação de formulários, manipulação de upload, diversas tecnologias
de autenticação abertas, entre outras coisas. O Flask pode ser "micro", mas
está pronto para uso em produção, preenchendo uma gama variada de
necessidades.

Configuração e convenções
-------------------------

O Flask tem vários valores de configuração, com defaults sensatos, e algumas
convenções. Por padrão, templates e arquivos estáticos são armazenados em
subdiretórios `templates` e `static` dentro da árvore-fonte do aplicativo
Python. Isso pode ser alterado, mas em geral não é necessário, especialmente
quando estiver apenas começando.

Crescendo com o Flask
---------------------

Depois que o Flask estiver instalado e funcionando, você vai encontrar à
disposição na comunidade diversas extensões para integrar seu projeto para
produção. A equipe central do Flask analisa as extensões e assegura que
extensões aprovadas permaneçam funcionais em lançamentos futuros.

À medida que a sua base de código vai crescendo, você pode ir escolhendo o
design mais apropriado ao seu projeto. O Flask continuará proporcionando uma
descomplicada camada de integração ao que Python tem de melhor a oferecer.
Você pode implementar padrões avançados em SQLAlchemy ou outra ferramenta de
banco de dados, introduzir persistência de dados não-relacionais quando for o
caso, e tirar proveito das ferramentas para WSGI, a interface web do Python,
que não são atreladas a nenhum framework específico.

O Flask tem muitos ganchos (*hooks* [#]_) para customizar seu comportamento.
Se você precisar de mais customização, saiba que a classe Flask foi construída
para ser estendida por herança. Se tiver interesse nisso, dê uma olhada no
capítulo :ref:`becomingbig`. Se tiver curiosidade sobre os princípios de
projeto do Flask, leia a seção :ref:`design`.

Continue lendo em :ref:`installation`, :ref:`quickstart`, ou
:ref:`advanced_foreword`.

.. rubric:: Notas da tradução

.. [#] *hook*, literalmente *gancho*, é um mecanismo usado em APIs
   extensíveis que permite ao programador criar uma função que será
   invocada pelo framework em determinado momento do processamento,
   por exemplo, uma função que será chamada sempre que o framework
   estiver pronto para gerar uma resposta HTTP. Leia mais na Wikipédia
   em português: hooking_.

.. _hooking: http://pt.wikipedia.org/wiki/Hooking
