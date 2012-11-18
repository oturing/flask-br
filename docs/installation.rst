.. _installation:

Instalação
============

O Flask depende de duas bibliotecas externas, `Werkzeug
<http://werkzeug.pocoo.org/>`_ e `Jinja2 <http://jinja.pocoo.org/2/>`_.
Werkzeug é um toolkit para WSGI, a interface padrão entre aplicações web
Python e servidores HTTP para desenvolvimento e implantação. Jinja2 renderiza
templates.

Mas como botar tudo isso rapidamente funcionando no seu computador? Existem
várias formas, mas o método mais irado é o virtualenv, então, vamos dar uma
olhada nele primeiro.

Você vai precisar de Python 2.5 ou superior para começar, então, verifique se
está com uma instalação atualizada do Python 2.x. Quando escrevi este texto, a
especificação do WSGI ainda não tinha sido finalizada para Python 3, portanto,
o Flask ainda não suporta a série 3.x do Python. [#]_

.. _virtualenv:

virtualenv
----------

O virtualenv é super apropriado para desenvolvimento, e se você tiver acesso
ao shell das máquinas de produção, provavelmente vai querer usá-lo lá também.

Que tipo de problema o virtualenv resolve? Se você gosta de Python tanto
quanto eu, aposto que vai querer usar a linguagem em outros projetos, além de
aplicações web baseadas em Flask. Mas, quanto mais projetos você tiver, maior
a chance de que irá trabalhar com diferentes versões do Python em si, ou pelo
menos diferentes versões de bibliotecas Python. Falando francamente:
bibliotecas frequentemente quebram a compatibilidade com versões anteriores, e
é pouco provável que qualquer aplicação séria tenha zero dependências. Então,
quê fazer se dois ou mais projetos tiverem dependências conflitantes?

Virtualenv é a salvação! O virtualenv permite múltiplas instalações paralelas
de Python, uma para cada projeto. Na verdade, não é que o virtualenv instala
cópias separadas de Python, mas, sim, fornece um jeito inteligente de manter
isolados diferentes ambientes de projeto. Vamos ver como o virtualenv
funciona.

No Mac OS X ou Linux, é quase certo que um desses dois comandos funcione::

    $ sudo easy_install virtualenv

ou, melhor ainda::

    $ sudo pip install virtualenv

Provavelmente, um desses comandos vai instalar o virtualenv no sistema. Talvez
até mesmo no gerenciador de pacotes. No Ubuntu, tente usar este comando::

    $ sudo apt-get install python-virtualenv

No Windows, se você não tiver o comando `easy_install`, primeiro é preciso
instalá-lo. Dê uma olhada na seção :ref:`windows-easy-install` para mais
instruções de como fazer isso. Depois de instalar, execute os mesmos comandos
anteriores, mas sem o prefixo `sudo`.

Criando um ambiente para seu projeto
::::::::::::::::::::::::::::::::::::

Depois de instalar o virtualenv, basta abrir um shell e criar o seu próprio
ambiente. Eu costumo criar uma pasta de projeto com uma subpasta `venv`::

    $ mkdir myproject
    $ cd myproject
    $ virtualenv venv
    New python executable in venv/bin/python
    Installing distribute............done.

Daí, sempre que você quiser trabalhar num projeto, basta ativar o ambiente
correspondente. No OS X e no Linux, faça o seguinte ::

    $ . venv/bin/activate

Se for usuário de Windows, use o seguinte comando::

    $ venv\scripts\activate

Um dos dois procedimentos irá ativar o seu virtualenv (observe que o prompt do
seu shell muda, passando a mostrar o ambiente que está ativo).

Em seguida, para ativar o Flask no seu virtualenv, digite o seguinte comando::

    $ pip install Flask

Aguarde alguns segundos e estará tudo pronto para usar.


Instalação no sistema como um todo
----------------------------------

É também possível instalar no sistema como um todo, embora eu não recomende.
É Basta executar `pip` com privilégios de root::

    $ sudo pip install Flask

(No Windows, execute-o numa janela de prompt, com privilégios de
(administrador, e não coloque `sudo`).


Vivendo no limite
------------------

Se quiser trabalhar com a versão mais recente do Flask, escolha uma dessas
opções: deixe `pip` baixar a versão de desenvolvimento, ou faça com que opere
um git checkout. O virtualenv é recomendado nos dois casos.

Pegue o git checkout num novo virtualenv e execute-o no modo de
desenvolvimento::

    $ git clone http://github.com/mitsuhiko/flask.git
    Initialized empty Git repository in ~/dev/flask/.git/
    $ cd flask
    $ virtualenv venv --distribute
    New python executable in venv/bin/python
    Installing distribute............done.
    $ . venv/bin/activate
    $ python setup.py develop
    ...
    Finished processing dependencies for Flask

Isso vai baixar as dependências e ativar o *git head* como a versão corrente
dentro do virtualenv. Daí, basta executar o ``git pull origin`` para atualizar
para a versão mais recente.

Para obter apenas a versão de desenvolvimento, sem git, faça isto::

    $ mkdir flask
    $ cd flask
    $ virtualenv venv --distribute
    $ . venv/bin/activate
    New python executable in venv/bin/python
    Installing distribute............done.
    $ pip install Flask==dev
    ...
    Finished processing dependencies for Flask==dev

.. _windows-easy-install:

`pip` e `distribute` no Windows
-----------------------------------

No Windows, a instalação do `easy_install` é um pouco mais complicada, mas
ainda assim muito fácil. A maneira mais fácil de fazer isso é baixar o arquivo
`distribute_setup.py`_ e executá-lo. O jeito mais fácil de executar o arquivo
é abrir a pasta de downloads e clicar duas vezes no arquivo.

Em seguida, adicione o comando `easy_install` e outros scripts em Python ao
caminho do comando de busca, adicionando a sua pasta de Scripts de instalação
do Python à variável do ambiente `PATH`. Para fazer isso, clique com o botão
direito do mouse no ícone "Computador", no Desktop ou no menu Iniciar, e
selecione "Propriedades". Depois, clique em "Configurações avançadas do
sistema" (ser for Windows XP, clique na aba "Avançado"). Daí, clique no botão
"Variáveis ​​de ambiente". Por fim, clique duas vezes na variável "Caminho",
na seção "Variáveis ​​do sistema", e adicione o caminho da sua pasta de
Scripts interpretadores de Python. Use ponto e vírgula, para não misturá-lo
com valores existentes. Supondo que você está usando Python 2.7 no caminho
padrão, adicione o seguinte valor::


    ;C:\Python27\Scripts

Pronto! Para verificar se funcionou, abra o Prompt de Comando e execute
``easy_install``. Se você tiver o User Account Control ativado no Windows
Vista ou Windows 7, serão solicitados privilégios de administrador.

Você pode agora usar o ``easy_install`` para instalar o ``pip``::

    > easy_install pip

Se tudo deu certo, finalmente você pode instalar o virtualenv::

    > pip install virtualenv

Feito isso, pode continuar a partir de `Criando um ambiente para seu projeto`_.


.. _distribute_setup.py: http://python-distribute.org/distribute_setup.py


.. rubric:: Notas da tradução

.. [#] A especificação WSGI adaptada para Python 3 foi publicada como
   `PEP 3333`_ em setembro de 2010. Em novembro de 2012 vários frameworks
   Python já suportam ou estão em estágio adiantado de desenvolvimento
   para suportar o Python 3. Ao mesmo tempo, embora o Flask continue
   sendo ativamente atualizado pelo autor no Github, a biblioteca
   Werkzeug teve pouca atividade em 2012, e é nela que está a maior parte da
   dificuldade na migração para Python 3. Em agosto de 2012 Armin Ronacher,
   autor do Flask e do Werkzeug, escreveu "Entretanto, com com Python 3
   tornando-se cada vez mais interessante, atualmente estou brincando com
   algumas idéias para evoluir as bibliotecas de maneiras interessantes."
   (blog_)

.. _PEP 3333: http://www.python.org/dev/peps/pep-3333/

.. _blog: http://lucumr.pocoo.org/2012/8/27/about-the-lack-of-updates/
