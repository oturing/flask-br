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
ser usado para verificar se o usuário está logado ou não. Note que no Jinga
você pode acessar atributos ou itens inexistentes em objetos e coleções sem
disparar um erro, por isso este código funciona mesmo que a chave ``'logado'``
não exista na ``session``.

.. sourcecode:: html+jinja

  <!doctype html>
  <title>Flaskr</title>
  <link rel="stylesheet" type="text/css"
        href="{{ url_for('static', filename='style.css') }}">
  <div class="page">
    <h1>Flaskr</h1>
    <div class="metanav">
    {% if not session.logado %}
      <a href="{{ url_for('login') }}">login</a>
    {% else %}
      <a href="{{ url_for('logout') }}">logout</a>
    {% endif %}
    </div>
    {% for mensagem in get_flashed_messages() %}
      <div class="flash">{{ mensagem }}</div>
    {% endfor %}
    {% block corpo %}{% endblock %}
  </div>

exibir_entradas.html
--------------------

Este template extende o `layout.html` acima para exibir as entradas do blog.
Note que o laço `for` itera sobre as entradas que passamos ao invocar a função
:func:`~flask.render_template` na view `exibir_entradas`. Se o usuário estiver
logado, exibimos o formulário, que enviará os dados para `inserir_entrada`
usando o método POST do protocolo HTTP:

.. sourcecode:: html+jinja

  {% extends "layout.html" %}
  {% block corpo %}
    {% if session.logado %}
      <form action="{{ url_for('inserir_entrada') }}" method="post"
            class="add-entry">
        <dl>
          <dt>Título:
          <dd><input type="text" size="30" name="title">
          <dt>Texto:
          <dd><textarea name="text" rows="5" cols="40"></textarea>
          <dd><input type="submit" value="Publicar">
        </dl>
      </form>
    {% endif %}
    <ul class="entries">
    {% for entrada in entradas %}
      <li><h2>{{ entrada.titulo }}</h2>{{ entrada.texto|safe }}
    {% else %}
      <li><em>Inacreditável. Até agora nenhuma entrada.</em>
    {% endfor %}
    </ul>
  {% endblock %}


login.html
----------

Finalmente, o template de login que apenas exibe o formulário para o usuário se logar:

.. sourcecode:: html+jinja

  {% extends "layout.html" %}
  {% block body %}
    <h2>Login</h2>
    {% if erro %}<p class="erro"><strong>Erro:</strong> {{ erro }}{% endif %}
    <form action="{{ url_for('login') }}" method=post>
      <dl>
        <dt>Username:
        <dd><input type="text" name="username">
        <dt>Password:
        <dd><input type="password" name="password">
        <dd><input type="submit" value="Login">
      </dl>
    </form>
  {% endblock %}


Continue com :ref:`tutorial-css`.
