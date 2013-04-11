.. _tutorial-views:

Passo 5: As funções de view
===========================

Agora que a conexão com o banco de dados está funcionando, podemos começar a
escrever as funções de *view*, que geram o corpo das respostas HTTP. Vamos
precisar de quatro funções:

Exibir entradas
---------------

Esta view mostra todas as entradas armazenadas no banco de dados. Ela recebe
requisições feitas na raiz do aplicativo (`/`) e seleciona o título e o texto
das entradas no banco de dados. Aquela com o maior `id` (a entrada mais
recente) vai aparecer no topo. Os registros devolvidos pelo cursor são tuplas
com as colunas ordenadas conforme enumeradas no comando `select`. Isso basta
para uma aplicação pequena como esta, mas às vezes pode ser interessante obter
os registros como dicionários. Se estiver interessado em ver como se faz isso,
dê uma olhada no exemplo em :ref:`easy-querying`.

A função view renderiza o template `show_entries.html` passando as entradas como uma lista de dicts::

    @app.route('/')
    def exibir_entradas():
        sql = '''select titulo, texto from entradas order by id desc'''
        cur = g.bd.execute(sql)
        entradas = [dict(titulo=titulo, texto=texto)
                        for titulo, texto in cur.fetchall()]
        return render_template('exibir_entradas.html', entradas=entradas)

Inserir entrada
---------------

Esta view permite que o usuário insira uma nova entrada se ele estiver logado. Ela responde apenas a requisições HTTP POST, pois o formulário é exibido no template de `exibir_entradas`. Se tudo funcionou bem, usaremos a função
:func:`~flask.flash` para exibir uma mensagem informativa na próxima resposta e redirecionar para a página `exibir_entradas`::

    @app.route('/inserir', methods=['POST'])
    def inserir_entrada():
        if not session.get('logado'):
            abort(401)
        sql = '''insert into entradas (titulo, texto) values (?, ?)'''
        g.bd.execute(sql, [request.form['titulo'], request.form['texto']])
        g.bd.commit()
        flash('Nova entrada registrada com sucesso')
        return redirect(url_for('exibir_entradas'))

Note que verificamos se o usuário está logado (a chave `logado` está
presente na sessão e seu valor é `True`).

.. admonition:: Observação de segurança

   Assegure-se de usar sempre as interrogações `?` ao construir comandos SQL
   parametrizados, como feito no exemplo acima. Se em vez disso você construir
   o SQL concatenando ou interpolando strings, sua aplicação será vulnerável a
   ataques de injeção de SQL. Veja :ref:`sqlite3` para saber mais.

Login e logout
--------------

Estas funções são usadas para logar e deslogar o usuário. A função `login`
compara o nome de usuário e a senha com as credenciais configuradas e define a
chave `logado` na sessão. Se o usuário se logou com sucesso, o valor da chave
`logado` é definido como `True`, e o usuário é redirecionado para a página
`exibir_entradas`. Além disso, na próxima página aparecerá uma mensagem
confirmando que o usário se logou. Se ocorrer um erro, uma mensagem de erro é
passada para o template, e a página de login é exibida novamente::

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        erro = None
        if request.method == 'POST':
            if request.form['username'] != app.config['USERNAME']:
                error = 'Usuário inválido'
            elif request.form['password'] != app.config['PASSWORD']:
                error = 'Senha inválida'
            else:
                session['logado'] = True
                flash('Login OK')
                return redirect(url_for('exibir_entradas'))
        return render_template('login.html', erro=erro)

A função de saída, por outro lado, retira a chave `logado` da sessão. Aqui
usamos um truque: invocando o método meth:`~dict.pop` do dict e passando um
segundo parâmetro (o default), o método excluirá a chave do dicionário se
presente, ou não fará nada se ela não estiver lá. Isso é útil porque assim não
temos de verificar se o usuário já estava logado.

::

    @app.route('/logout')
    def logout():
        session.pop('logado', None)
        flash('Logout OK')
        return redirect(url_for('exibir_entradas'))

Continue com :ref:`tutorial-templates`.
