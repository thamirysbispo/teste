from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory

from protoripo_dao import ProdutoDao
from protoripo_dao import UsuarioDao

from flask_mysqldb import MySQL
import os

from modelo import Usuario, Produto

app_web = Flask(__name__)
app_web.secret_key = 'flask'

app_web.config['MYSQL_HOST'] = "127.0.0.1"
app_web.config['MYSQL_USER'] = "root"
app_web.config['MYSQL_PASSWORD'] = "sistemas2014"
app_web.config['MYSQL_DB'] = "prototipo"
app_web.config['MYSQL_PORT'] = 3306
app_web.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/imagens'

db = MySQL(app_web)

produto_dao = ProdutoDao(db)

usuario_dao = UsuarioDao(db)

@app_web.route('/')
def index():
    lista = produto_dao.listar()
    return render_template('lista_produtos.html', titulo='Produtos', produtos=lista)


@app_web.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app_web.route('/autentica_usuario', methods=['POST',])
def autentica_usuario():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Login ou senha incorretos')
        return redirect(url_for('login'))


@app_web.route('/novo')
def novo_produto():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo_produto')))
    return render_template('novo_produto.html', titulo='Cadastrar Produto')


@app_web.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

@app_web.route('/inserir_produto', methods=['POST', ])
def inserir_produto():
    nome = request.form['nome']
    categoria = request.form['categoria']
    valor = request.form['valor']
    produto = Produto(nome, categoria, valor)

    produto = produto_dao.salvar(produto)

    arquivo = request.files['arquivo']
    upload_path = app_web.config['UPLOAD_PATH']
    arquivo.save('{}/capa{}.jpg'.format(upload_path, produto.id))
    return redirect(url_for('index'))

@app_web.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    produto =  produto_dao.busca_por_id(id)

    return render_template('edita_produtos.html', titulo='Editar Produto', produto=produto,capa_produto = 'capa{}.jpg'.format(id))

@app_web.route('/atualizar', methods=['POST',])
def atualizar():

    nome = request.form['nome']
    categoria = request.form['categoria']
    valor = request.form['valor']
    produto = Produto(nome, categoria, valor, id=request.form['id'])
    produto_dao.salvar(produto)

    arquivo = request.files['arquivo']
    upload_path = app_web.config['UPLOAD_PATH']
    arquivo.save('{}/capa{}.jpg'.format(upload_path, produto.id))
    return redirect(url_for('index'))

@app_web.route('/teste')
def teste():
    lista = produto_dao.listar()
    return render_template('altera_produto.html', titulo='Editar Produto', produtos=lista)

@app_web.route('/deletar/<int:id>')
def deletar(id):
    produto_dao.deletar(id)
    flash('O produto foi removido com sucesso!')
    return redirect(url_for('index'))


@app_web.route('/imagens/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('imagens', nome_arquivo)

@app_web.route('/servicos')
def servicos():
    lista = produto_dao.listar()
    return render_template('produtos_imagens.html', produtos = lista)


app_web.run(debug=True)

