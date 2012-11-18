.. _tutorial-templates:

Passo 6: Templates
==================

Agora vamos começar a trabalhar nos templates (modelos de página). Se acessar
as URLs definidas até agora apenas veremos exceções pois o Flask não consegue
encontrar os templates. Os templates neste exemplo usam a sintaxe `Jinja2`_ e
têm *autoescaping* ativado por default. Isso significa que Jinja2 substituirá
caracteres especiais como ``<`` ou ``>`` pelas entidades XML equivalentes
(ex.: ``&lt;``), a não ser que você forneça o valor usando a classe
:class:`~flask.Markup` ou use o filtro ``|safe`` no template.

Também usaremos herança de templates, possibilitando o reuso do layout básico
do site em todas as páginasa.

Coloque os templates a seguir no diretório `flaskr/templates`:

.. _Jinja2: http://jinja.pocoo.org/2/documentation/templates

layout.html
-----------

Este template contém o esqueleto do HTML, um cabeçalho e uma link para fazer
login (ou logout, se o usuário já estiver logado). Também exibe as mensagens
produzidas pela função `flash`, se existirem. O bloco ``{% block corpo %}``
pode ser substituído por um bloco de mesmo nome (``corpo``) em um template
derivado deste.

O dict :class:`~flask.session` está disponível para o template também, e pode
ser usado para verificar se o usuário está logado ou não. Note que no Jinja
você pode acessar atributos ou itens inexistentes em objetos e coleções sem
disparar um erro, por isso este código funciona mesmo que a chave ``'logado'``
não exista na ``session``.

.. literalinclude:: ../../examples/flaskr/templates/layout.html
   :language: html+jinja


exibir_entradas.html
--------------------

Este template extende o `layout.html` acima para exibir as entradas do blog.
Note que o laço `for` itera sobre as entradas que passamos ao invocar a função
:func:`~flask.render_template` na view `exibir_entradas`. Se o usuário estiver
logado, exibimos o formulário, que enviará os dados para `inserir_entrada`
usando o método POST do protocolo HTTP:

.. literalinclude:: ../../examples/flaskr/templates/exibir_entradas.html
   :language: html+jinja


login.html
----------

Finalmente, o template de login que apenas exibe o formulário para o usuário se logar:

.. literalinclude:: ../../examples/flaskr/templates/login.html
   :language: html+jinja


Continue com :ref:`tutorial-css`.
