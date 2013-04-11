.. _tutorial-dbinit:

Passo 3: Criando o banco de dados
=================================

Flaskr é uma aplicação movida a banco de dados, conforme já descrevemos, e,
mais precisamente, é uma aplicação baseada em um sistema de banco de dados
relacional. Tais sistemas precisam de um esquema que define como os dados
devem ser armazenados. Assim, antes de iniciar o servidor pela primeira vez é
preciso criar o tal esquema.

O esquema pode ser criado redirecionando o arquivo `esquema.sql` para o
comando `sqlite3` desta forma::

    sqlite3 /tmp/flaskr.db < esquema.sql


A desvantagem de fazer assim é que precisamos usar o comando sqlite3 que pode
não estar instalado em algum ambiente. Além disso, temos que fornecer
novamente o caminho para o banco de dados, correndo o risco de errar. É uma
boa idéia criar uma função que inicializa o banco de dados na própria
aplicação.

Para fazer isso, primeiro precisamos importar a função
:func:`contextlib.closing` do pacote `contextlib`. Se precisar usar Python
2.5, também será necessário habilitar o comando `with` (lembre-se que um
import de `__future__` deve ser o primeiro import em um módulo). Conforme o
caso, coloque essas duas linhas em seu `flaskr.py`, ou apenas a segunda se
estiver usando Python 2.6 ou 2.7::

    from __future__ import with_statement
    from contextlib import closing

Agora podemos criar uma função chamada `criar_bd` que inicializa o banco de
dados. Para isso podemos usar a função `conectar_bd` que definimos antes.
Coloque esta função abaixo da função `conectar_bd` em `flaskr.py`::

    def criar_bd():
        with closing(conectar_bd()) as bd:
            with app.open_resource('esquema.sql') as sql:
                bd.cursor().executescript(sql.read())
            bd.commit()

A função auxiliar :func:`~contextlib.closing` permite que nossa aplicação
mantenha a conexão aberta enquando o bloco `with` é executado [#]_. O método
:func:`~flask.Flask.open_resource` do objeto aplicação já implementa esta
funcionalidade, por isso pode ser usado diretamente no segundo comando `with`.
Esta função abre para leitura um arquivo do local dos recursos (a pasta
`flaskr`). Neste caso estamos abrindo um script SQL para executá-lo através da conexão com o banco de dados.


Quando conectamos a um banco de dados obtemos um objeto conexão (aqui
denominado `bd`) que pode nos fornecer um cursor. No cursor existe um método
para executar um script SQL completo. Finalmente, precisamos fazer `commit`
nas alterações. SQLite3 e outros bancos de dados transacionais não fazem
`commit` a menos que você solicite explicitamente.

Agora podemos criar o banco de dados iniciando um console do Python, importando e invocando aquela função::

>>> from flaskr import criar_bd
>>> criar_bd()

.. admonition:: Em caso de erro

   Se posteriormente você encontrar uma exceção de que a tabela não foi
   encontrada, verifique que você invocou a função `criar_db` sem erros
   e que o nome da tabela está correto (ex.: singular e não plural).


Continue com :ref:`tutorial-dbcon`

.. rubric:: Notas da tradução

.. [#] Além disso, a função `closing` garante que o recurso aberto seja
   fechado ao final do bloco `with`. Isso é crucial quando usamos o SQLite3,
   pois ao contrário de um servidor de banco de dados rodando em um processo
   independente, o SQLite3 é gerenciado diretamente pela sua aplicação e se
   ela abortar sem fechar a conexão, o arquivo de banco de dados ficará
   travado, exigindo uma intervenção manual antes de ser acessado novamente.
