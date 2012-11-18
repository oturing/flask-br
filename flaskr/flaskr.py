# coding: utf-8

# todos os imports
import sqlite3
from contextlib import closing

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuração
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# criar nossa pequena aplicação :)
app = Flask(__name__)
app.config.from_object(__name__)

def conectar_bd():
    return sqlite3.connect(app.config['DATABASE'])

def criar_bd():
    with closing(conectar_bd()) as bd:
        with app.open_resource('esquema.sql') as sql:
            bd.cursor().executescript(sql.read())
        bd.commit()
            
@app.before_request
def pre_requisicao():
    g.bd = conectar_bd()

@app.teardown_request
def encerrar_requisicao(exception):
    g.bd.close()
        
if __name__ == '__main__':
    app.run()
