.. _tutorial-setup:

Passo 2: Inicialização da aplicação
===================================

Agora que temos um esquema definido, podemos criar o módulo da aplicação.
Vamos chamá-lo de `flaskr.py` dentro da pasta `flaskr`. Para começar vamos
escrever os imports que necessários e um trecho de configuração. Para uma
aplicação pequena é possível embutir a configuração no módulo como faremos
aqui. No entanto uma solução mais limpa seria criar um arquivo `.ini` ou `.py`
e carregar ou importar os dados de lá.

Dentro de `flaskr.py`::

    # coding: utf-8

    # todos os imports
    import sqlite3
    from flask import Flask, request, session, g, redirect, url_for, \
         abort, render_template, flash

    # configuração
    DATABASE = '/tmp/flaskr.db'
    DEBUG = True
    SECRET_KEY = 'development key'
    USERNAME = 'admin'
    PASSWORD = 'default'

Em seguinda criamos nossa aplicação propriamente dita e a inicializamos com a configuração do próprio arquivo, ainda em `flaskr.py`::

    # criar nossa pequena aplicação :)
    app = Flask(__name__)
    app.config.from_object(__name__)

O método :meth:`~flask.Config.from_object` inspeciona o objeto fornecido (se
for uma string, ele importa o módulo correspondente) e lê todas as variáveis
com nomes em maiúsculas encontrados nele. Em nosso caso, são as variáveis de
configuração que escremos logo acima. Você também pode colocá-las em outro
arquivo.

Geralmente, é uma boa idéia carregar a configuração de um arquivo específico
para este fim. É isto que o método :meth:`~flask.Config.from_envvar` faz, no
lugar de da linha com :meth:`~flask.Config.from_object` acima::

    app.config.from_envvar('CONFIG_FLASKR', silent=True)

Desta forma alguém pode setar uma variável de ambiente chamada
:envvar:`CONFIG_FLASKR` para especificar um arquivo de configuração da ser
carregado para sobrescrever os parâmetros da configuração default. A opção
`silent` diz para o Flask não reclamar se tal variável de ambiente não
existir.

A `SECRET_KEY` é necessária para manter as sessões do cliente seguras. Escolha
bem esta chave e assegure-se de que ela é bastante complicada e difícil de
adivinhar. A opção `DEBUG` liga ou desliga o depurador interativo. *Nunca
deixe o modo debug ligado em um sistema em produção*, pois isso permite que os
usuários executem comandos arbitrários em seu servidor!

Tambem criamos um método para facilitar a conexão ao banco de dados
especificado. Isso pode ser usado para abrir uma conexão ao tratarmos uma
requisiçao e também através do console do Python o de algum script. Isso
facilitará as coisas depois.

::

    def conectar_bd():
        return sqlite3.connect(app.config['DATABASE'])

Finalmente, acrescentamos uma linha no final do arquivo que dispara o servidor
caso este módulo seja usado como uma aplicação independente::

    if __name__ == '__main__':
        app.run()


Feito isso, você deverá ser capaz de iniciar a aplicação sem nenhum problema.
Faça isto com o seguinte comando::

   python flaskr.py

Você verá uma mensagem dizendo que o servidor foi iniciado e informando o
endereço onde poderá acessá-lo.

Se visitar com seu navegador o endereço exibido, verá uma página de erro 404
porque ainda não conifiguramos nenhuma *view*. Vamos resolver isso mais tarde.
Primeiro, queremos fazer o banco de dados funcionar.


.. admonition:: Servidor visível externamente

   Quer que o seu servidor esteja disponível para outros via rede?
   Leia a seção :ref:`externally visible server <public-server>`
   para mais informações.

Continue com :ref:`tutorial-dbinit`.
