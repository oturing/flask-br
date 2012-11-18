.. _tutorial-dbcon:

Passo 4: Conexão ao banco de dados durante uma requisição
---------------------------------------------------------

Já sabemos como abrir uma conexão de banco de dados para uso em um script ou
no console interativo, mas como podemos fazê-lo de modo elegante a cada
requisição Web? A conexão com o banco de dados será usada em várias funções
então faz sentido abrir a conexão antes de tratar cada requisição e fechar
depois.

Flask permite que façamos isto com os decoradores de função
:meth:`~flask.Flask.before_request`, :meth:`~flask.Flask.after_request` e
:meth:`~flask.Flask.teardown_request`::

    @app.before_request
    def pre_requisicao():
        g.bd = conectar_bd()

    @app.teardown_request
    def encerrar_requisicao(exception):
        g.bd.close()

Funções marcadas com :meth:`~flask.Flask.before_request` são invocadas antes
de uma requisição e não recebem argumentos. Funções marcads com
:meth:`~flask.Flask.after_request` são invocadas após uma requisição e recebem
o objeto response que será enviado ao cliente. Elas têm que devolver este
objeto response ou um objeto response diferente. Entretanto sua invocação não
é garantida caso seja levantada uma exceção no tratamento da requisição. É
para isso que servem as funções marcadas com
:meth:`~flask.Flask.teardown_request`. Elas são invocadas depois que a
resposta é construída. Elas não podem modificar a requisição, e qualquer valor
devolvido por elas é ignorado. Se uma exceção aconteceu duranteo o
processamento da requisição, cada função marcada com `teardown_request` recebe
a exceção; do contrário, elas recebem `None`.

Armazenamos a conexão de banco de dados aberta no objeto especial
:data:`~flask.g` que o Flask fornece. Este objeto armazena informaçõoes apenas
pela duração de uma requisição e está disponível para cada uma de suas
funções. Nunca armazene tais coisas em outros objetos, pois poderá ter
problemas em ambientes multi-thread. O objeto :data:`~flask.g` faz algumas
mágicas por baixo dos panos para garantir que tudo funcione.


Continue com :ref:`tutorial-views`.

.. hint:: Onde eu coloco este código?

   Se você vem acompanhando este tutorial, talvez esteja em dúvida sobre onde
   colocar o código deste passo e o do próximo. Um lugar lógico é agrupar
   estas funções e colocar as novas ``pre_requisicao`` e
   ``encerrar_requisicao`` abaixo da função ``criar_bd`` (se você está
   seguindo o tutorial linha por linha).

   Se precisar se localizar, veja como o `exemplo traduzido`_ está organizado,
   assim como o `exemplo original`_. No Flask, você pode colocar todo o código
   da sua aplicação em um único módulo Python. Mas você não é obrigado a fazer
   isto, e se a sua `aplicação ficar grande <larger-applications>`_, é uma boa
   idéia organizar o código em vários arquivos separados.

.. _exemplo traduzido:
   http://github.com/oturing/flask-br/tree/master/examples/flaskr/

.. _exemplo original:
   http://github.com/mitsuhiko/flask/tree/master/examples/flaskr/

