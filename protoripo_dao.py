from modelo import Usuario, Produto

SQL_DELETA_PRODUTO = 'delete from produto where id = %s'
SQL_PRODUTO_POR_ID = 'SELECT id, nome, categoria, valor from produto where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_PRODUTO = 'UPDATE produto SET nome=%s, categoria=%s, valor=%s where id = %s'
SQL_BUSCA_PRODUTOS = 'SELECT id, nome, categoria, valor from produto'
SQL_CRIA_PRODUTO = 'INSERT into produto (nome, categoria, valor) values (%s, %s, %s)'


class ProdutoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, produto):
        cursor = self.__db.connection.cursor()

        if (produto.id):
            cursor.execute(SQL_ATUALIZA_PRODUTO, (produto.nome, produto.categoria, produto.valor, produto.id))
        else:
            cursor.execute(SQL_CRIA_PRODUTO, (produto.nome, produto.categoria, produto.valor))
            produto.id = cursor.lastrowid
        self.__db.connection.commit()
        return produto

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_PRODUTOS)
        produtos = traduz_produtos(cursor.fetchall())
        return produtos

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_PRODUTO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Produto(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_PRODUTO, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_produtos(produtos):
    def cria_produto_com_tupla(tupla):
        return Produto(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_produto_com_tupla, produtos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])
