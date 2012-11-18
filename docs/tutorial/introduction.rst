.. _tutorial-introduction:

Apresentando Flaskr
====================

Vamos chamar de flaskr nossa aplicação de blog, mas fique à vontade pare
escolher um nome menos "web-2.0" ;)  Basicamente queremos que a aplicação faça
o seguinte:


1. permitir que o usuário se logue e deslogue utilizando credenciais
   especificadas na configuração. Somente um usuário é suportado.
2. quando o usuário está logado ele pode criar novas entradas no blog,
   que consistem de um título em texto puro e um corpo em HTML. Este
   HTML não passa por nenhum filtro pois confiamos no nosso usuário.
3. a página exibe todas as entradas até o momento em ordem inversa
   (as mais recente no topo) e o usuário pode criar novas entradas
   na página se estiver logado.

Usaremos SQLite3 diretamente para esta aplicação porque ele é bom o bastante
para uma aplicação deste tamanho. Para aplicações maiores entretanto faz
sentido usar `SQLAlchemy`_ que lida com conexões ao banco de dados de forma
mais inteligente, permite acessar vários bancos de dados diferentes e oferece
muitas outras facilidades.

Eis uma tela da aplicação final:

.. image:: ../_static/flaskr.png
   :align: center
   :class: screenshot
   :alt: tela da aplicação concluída

Continue com :ref:`tutorial-folders`.

.. _SQLAlchemy: http://www.sqlalchemy.org/
