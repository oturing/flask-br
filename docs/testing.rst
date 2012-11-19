.. _testing:

Testando aplicações Flask
=========================

   **Qualquer coisa sem testes está quebrada.**

A origem desta citação é desenconhecida, e embora não esteja completamente
certa, também não está longe da verdade. Apliações sem testes tornam difícil
melhorar o código existente e desenvolvedores de aplicações sem testes tendem
a ficar bastante paranóicos. Se sua aplicação tem testes automatizados, você pode fazer alterações com segurança pois saberá imediatamente se algo quebrou.

Flask fornece uma forma de testar sua aplicação dando acesso ao
:class:`~werkzeug.test.Client` da biblioteca Werkzeug, e gerenciando as
variáveis locais do contexto para você. Com isso você pode usar a sua solução
favorita para testes. Nesta documentação, usaremos o pacote :mod:`unittest`
que vem pré-instalado com o Python.

A aplicação
-----------

Primeiro, precisamos de uma aplicação para testar; usaremos a aplicação do
:ref:`tutorial`. Se você ainda não tem essa aplicação, pegue o código fonte do
`exemplo traduzido`_.

.. _exemplo traduzido:
   http://github.com/ramalho/flask-br/tree/master/examples/flaskr/

O esqueleto dos testes
----------------------

Para testar a aplicação, criaremos um segundo módulo (`flaskr_tests.py`) e
nele montaremos o esqueleto dos testes unitários::

    # coding: utf-8

    import os
    import flaskr
    import unittest
    import tempfile

    class FlaskrTestCase(unittest.TestCase):

        def setUp(self):
            self.bd_arq, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
            flaskr.app.config['TESTING'] = True
            self.app = flaskr.app.test_client()
            flaskr.criar_bd()

        def tearDown(self):
            os.close(self.bd_arq)
            os.unlink(flaskr.app.config['DATABASE'])

    if __name__ == '__main__':
        unittest.main()


O código no método :meth:`~unittest.TestCase.setUp` cria um novo cliente de
testes (``test_client``) e inicializa um novo banco de dados. Este método é
invocado antes da execução de cada método de teste na classe
``FlaskrTestCase`` (ainda não escrevemos nenhum teste). Para excluir o banco
de dados após cada teste, fechamos o arquivo e o apagamos do disco em
:meth:`~unittest.TestCase.tearDown`. Além disso, no ``setUp``, a configuração
``TESTING`` é ligada. Isso desabilita a captura de erros durante o tratamento
das requisições, gerando relatórios de erros melhores quando fazemos
requisições de teste.

Este cliente de testes nos oferece uma interface fácil para a aplicação.
Podemos disparar requisições de testes na aplicação, e o cliente também
gerencia os cookies par nós.

Como o SQLite3 é baseado em sistema de arquivos, podemos facilmente usar o módulo ``tempfile`` para criar um banco de dados temporário e incializá-lo. A função :func:`~tempfile.mkstemp` faz duas coisas: devolve um descritor de arquivo aberto e o caminho para o arquivo de nome aleatório; este último usamos como nome do banco de dados. Precisamos guardar o descritor `bd_arq` para podermos depois fechar o arquivo com a função :func:`os.close`.

Se neste momento executarmos a suíte de testes, veremos o seguinte resultado::

    $ python flaskr_tests.py

    ----------------------------------------------------------------------
    Ran 0 tests in 0.000s

    OK


Mesmo não tendo executado nenhum teste, já sabemos que nossa aplicação Flaskr
não tem erros de sintaxe, pois se tivesse o import inicial teria falhado.


Primeiro teste
--------------

Agora é hora de começar a testar a funcionalidade da aplicação. Vamos verificar se a aplicação exibe "nenhuma entrada" ao acessar a raiz da aplicação (``/``).
Para tanto, vamos acrescentar um método de testes em nossa classe, assim::

    class FlaskrTestCase(unittest.TestCase):

        def setUp(self):
            self.bd_arq, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
            flaskr.app.config['TESTING'] = True
            self.app = flaskr.app.test_client()
            flaskr.criar_bd()

        def tearDown(self):
            os.close(self.bd_arq)
            os.unlink(flaskr.app.config['DATABASE'])

        def teste_bd_vazio(self):
            res = self.app.get('/')
            assert 'nenhuma entrada' in res.data

Observe que os métodos de teste usam o prefixo `test` [#]_; isso permite que o
:mod:`unittest` identifique automaticamente estes métodos como testes a serem executados.

O método `self.app.get` envia para a aplicação uma requisição HTTP GET para o
caminho especificado. O valor devolvido será um objeto
:class:`~flask.Flask.response_class`. Então podemos usar o atributo
:attr:`~werkzeug.wrappers.BaseResponse.data` para inspecionar o conteúdo
devolvido pela aplicação, que é uma string. Neste caso, verificamos que a sub-
string ``'nenhuma entrada'`` está presente.

Rode o teste de novo e você verá que agora temos um teste passando::

    $ python flaskr_tests.py
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.034s

    OK

Logando e deslogando
--------------------

A maior parte das funcionalidades da nossa aplicação só está disponível para o
usuário administrador, por isso precisamos de uma maneira de fazer o nosso
cliente de teste logar e deslogar. Para tanto, vamos disparar requisições para
as páginas de login e logout com os dados do obrigatórios do formulário
(usuário e senha). E, como as páginas de login e logout fazem
redirecionamentos, ordenamos que o cliente ``follow_redirects`` (seguir
redirecionamento).

Coloque estes dois métodos na continuação da sua classe `FlaskrTestCase`::

    def login(self, username, password):
        return self.app.post('/entrar', data=dict(
                username=username,
                password=password
            ), follow_redirects=True)

    def logout(self):
        return self.app.get('/sair', follow_redirects=True)

Agora podemos facilmente verificar que logar e deslogar funciona, e que o
login exige as credenciais corretas. Acrescente este novo teste à classe
[#]_::

    def teste_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'Login OK' in rv.data
        rv = self.logout()
        assert 'Logout OK' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Usuário inválido' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Senha inválida' in rv.data


Testar inserção de entradas
---------------------------

Também devemos testar que é possível inserir entradas no blog. Crie um novo
método de teste assim::

    def teste_nova_entrada(self):
        self.login('admin', 'default')
        rv = self.app.post('/inserir', data=dict(
            titulo='<Olá>',
            texto='<strong>HTML</strong> é permitido aqui'
        ), follow_redirects=True)
        assert rv.status_code == 200
        assert 'nenhuma entrada' not in rv.data
        assert '&lt;Olá&gt;' in rv.data
        assert '<strong>HTML</strong> é permitido aqui' in rv.data

Aqui verificamos que é permitido usar HTML no texto mas não no título, que é o
comportamento desejado.

Ao executar os testes agora devemos ter três passando::

    $ python flaskr_tests.py
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.332s

    OK


Para ver testes mais complexos verificando cabeçalhos e códigos de statos,
veja o exemplo `MiniTwit`_ no repositório do Flask, que possui uma suite de
testes mais extensa.

.. _MiniTwit:
   http://github.com/mitsuhiko/flask/tree/master/examples/minitwit/


Outros truques para testes
--------------------------

Além de usar o cliente de testes apresentado acima, há também o método
:meth:`~flask.Flask.test_request_context` que pode ser usado em combinação
com a instrução ``with`` para ativar um contexto de requisição temporariamente. Com isso você pode acessar os objetos :class:`~flask.request`,
:class:`~flask.g` e :class:`~flask.session` como se estivesse em uma função de view. Eis um exemplo que ilustra esta técnica::

    app = flask.Flask(__name__)

    with app.test_request_context('/?nome=Pedro'):
        assert flask.request.path == '/'
        assert flask.request.args['nome'] == 'Pedro'

Todos os demais objetos que são vinculados ao contexto pode ser usados da
mesma maneira.

Se você quer testar sua aplicação com diferentes configurações e procuar uma
boa forma de fazer isso, considere o uso de uma fábrica de aplicações (veja
:ref:`app-factories`).

Note no entanto que se você está usando um contexto de requisição de teste, as
funções :meth:`~flask.Flask.before_request` e
:meth:`~flask.Flask.after_request` não são automaticamente invocadas. No
entanto, as funções :meth:`~flask.Flask.teardown_request` são invocadas quando
o bloco ``with`` é encerrado. Se você precisa que as funções funções
:meth:`~flask.Flask.before_request` sejam invocadas, precisa chamar
:meth:`~flask.Flask.preprocess_request` em seu teste::

    app = flask.Flask(__name__)

    with app.test_request_context('/?nome=Pedro'):
        app.preprocess_request()
        ...

Isto pode ser necessário para abrir a conexão com o banco de dados ou realizar
alguma outra operação do gênero, dependendo de como sua aplicação foi
projetada.

Se quiser acionar as funções :meth:`~flask.Flask.after_request` terá que
invocar :meth:`~flask.Flask.process_response`, que precisa receber um objeto
`response`::

    app = flask.Flask(__name__)

    with app.test_request_context('/?nome=Pedro'):
        resp = Response('...')
        resp = app.process_response(resp)
        ...


Porém isso em geral não é tão util, porque neste ponto vale mais a pena usar o
cliente de testes.


Mantendo o contexto por mais tempo
----------------------------------

.. versionadded:: 0.4

Às vezes pode ser útil disparar uma requisição normalmente mas ainda assim
manter o contexto vivo por mais um tempo para permitir alguma introspecção
adicional. A partir do Flask 0.4 isso é possível usando o
:meth:`~flask.Flask.test_client` em um bloco ``with``::

    app = flask.Flask(__name__)

    with app.test_client() as c:
        rv = c.get('/?tequila=42')
        assert request.args['tequila'] == '42'

Se você usasse apenas o :meth:`~flask.Flask.test_client` sem o bloco ``with``
o ``assert`` geraria um erro porque o ``request`` não está mais disponível
(você estaria tentando acessá-lo fora do contexto de uma requisição).


Acessar e modificar sessões
---------------------------

.. versionadded:: 0.8

Às vezes pode ser muito útil acessar ou modificar uma sessão a partir do
cliente de testes. Geralmente há duas formas de fazer isto. Se você apenas
quer verificar que a sessão tem determinadas chaves com certos valores, pode
simplesmente manter o contexto ativo e acessar :data:`flask.session`::

    with app.test_client() as c:
        rv = c.get('/')
        assert flask.session['foo'] == 42

Entretanto, desta maneira não é possível modificar a sessão ou acessar a
sessão antes da requisição ser disparada. A partir do Flask 0.8 fornecemos uma
"transação de sessão" que simula as chamadas apropriadas para se abrir uma
sessão no contexto do cliente de testes e modificá-la. Ao final da transação,
a sessão é armazenada. Isto funciona independente do backend de sessão que
estiver sendo usado::

    with app.test_client() as c:
        with c.session_transaction() as sessao:
            sessao['uma_chave'] = 'um valor'

        # ao chegar aqui a sessão estará armazenada

Note que neste caso você deve usar o objeto ``sessao`` em vez do proxy
:data:`flask.session`. Entretanto o este objeto implementa a mesma interface.


.. rubric:: Notas da tradução

.. [#] Os métodos de teste podem começar com a palavra `teste` também. O
   importante é que as primeiras letras sejam ``test``, pois este é o prefixo
   default definido em ``unittest.TestLoader.testMethodPrefix``.

.. [#] Este teste revela uma armadilha sobre a representação das respostas
   HTTP no Flask: ao incluir textos acentuados na resposta, como fazemos em
   caso de erro na função ``flaskr.login``, precisamos passar este textos
   como strings Unicode (instâncias de ``unicode``, denotadas pelo prefixo
   ``u`` nas mensagens como ``u'Senha inválida'``). Se isso não for feito lá,
   encontramos uma exceção porque o Flask assume que as strings de bytes
   ``str`` passadas como parâmetro para o template são strings ASCII. No entanto, ao testar a resposta em ``teste_login_logout` somos obrigados a
   usar strings de bytes ``str``, porque se usarmos ``unicode`` o Python
   assume que a resposta em ``rv.data`` é uma string ASCII e ao tentar
   converter para Unicode para poder comparar, uma exceção
   ``UnicodeDecodeError`` é gerada. Por isso temos strings de bytes ``str``,
   e neste caso funciona porque o nosso código-fonte está em UTF-8 (veja
   o comentário na linha 1), e a resposta produzida pelo Flask utiliza este
   mesmo encoding. Uma alternativa que também funciona é escrever os testes
   assim::

        assert u'Usuário inválido' in rv.data.decode('utf-8')

   Aqui estamos explicitamente convertendo os dados da resposta de UTF-8
   para Unicode, e assim podemos testar com segurança contra nossa string
   ``unicode``. O problema que descrevemos aqui não acontece no tutorial
   original do Flask, pois ele foi escrito em inglês, e lá todas as strings
   são ASCII puro.

