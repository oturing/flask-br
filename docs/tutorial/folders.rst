.. _tutorial-folders:

Passo 0: Criando os diretórios
==============================

Antes de começar, vamos criar os diretórios necessários para esta
aplicação::

    /flaskr
        /static
        /templates

A pasta `flaskr` não é um pacote Python, mas apenas um lugar para colocarmos
nossos arquivos. Diretamente nesta pasta colocaremos os arquivos de dados bem
como o módulo principal nos passos seguintes. Os arquivos dentro da pasta
`static` estão disponíveis para os usuários da aplicação via HTTP. Este é
o lugar onde colocaremos os arquivos CSS e JavaScript. O Flask buscará na
pasta `templates` os templates `Jinja2`_. Os templates que criaremos
posteriormente no tutorial irão para este diretório.

Continue com :ref:`tutorial-schema`.

.. _Jinja2: http://jinja.pocoo.org/2/
