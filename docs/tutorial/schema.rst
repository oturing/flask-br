.. _tutorial-schema:

Passo 1: O esquema do banco de dados
====================================

Primeiro vamos criar o esquema do banco de dados. Para esta aplicação
precisamos de apenas uma tabela e vamos usar somente SQLite então isto é bem
fácil. Coloque o código a seguir num arquivo chamado `esquema.sql` na pasta
`flaskr` que acabou de criar:

.. sourcecode:: sql

    drop table if exists entradas;
    create table entradas (
      id integer primary key autoincrement,
      titulo string not null,
      texto string not null
    );

Este esquema consiste de uma única tabela chamada `entradas` e cada registro
nessa tabela tem um `id`, um `título` e um `texto`. O `id` é um inteiro
automaticamente incrementado e uma chave primária, e os outros dois campos
são strings e não podem ser nulos.

Continue com :ref:`tutorial-setup`.
