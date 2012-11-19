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

    def teste_bd_vazio(self):
        rv = self.app.get('/')
        assert 'nenhuma entrada' in rv.data

    def login(self, username, password):
        return self.app.post('/entrar', data=dict(
                username=username,
                password=password
            ), follow_redirects=True)

    def logout(self):
        return self.app.get('/sair', follow_redirects=True)

    def teste_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'Login OK' in rv.data
        rv = self.logout()
        assert 'Logout OK' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Usuário inválido' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Senha inválida' in rv.data

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


if __name__ == '__main__':
    unittest.main()
