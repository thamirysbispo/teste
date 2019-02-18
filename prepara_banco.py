import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='sistemas2014', host='127.0.0.1', port=3306)


#conn.cursor().execute("DROP DATABASE `produtos`;")
#conn.commit()

criar_tabelas = '''SET NAMES latin1;
    CREATE DATABASE `prototipo` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `prototipo`;
    CREATE TABLE `produto` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) COLLATE utf8_bin NOT NULL,
      `categoria` varchar(40) COLLATE utf8_bin NOT NULL,
      `valor` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `usuario` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `nome` varchar(20) COLLATE utf8_bin NOT NULL,
      `senha` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO prototipo.usuario (id, nome, senha) VALUES (%s, %s, %s)',
      [
            ('luan', 'Luan Marques', 'flask'),
            ('nico', 'Nico', '7a1'),
            ('danilo', 'Danilo', 'vegas')
      ])

cursor.execute('select * from prototipo.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo produtos
cursor.executemany(
      'INSERT INTO prototipo.produto (nome, categoria, valor) VALUES (%s, %s, %s)',
      [
            ('Câmera', 'Eletronicos', '164'),
            ('Notebook', 'Eletrônicos', '1200'),
            ('Bola', 'Esportes', '50'),
            ('TV', 'Eletrônicos', '1500'),
            ('Caderno', 'Papelaria', '20'),
            ('Caneta', 'Papelaria', '3'),
      ])

cursor.execute('select * from prototipo.produto')
print(' -------------  Produtos:  -------------')
for produto in cursor.fetchall():
    print(produto[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()