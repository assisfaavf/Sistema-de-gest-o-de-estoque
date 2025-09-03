import sqlite3
import os


DB_NAME = "estoque.db"

def get_connection():
  return sqlite3.connect(DB_NAME)

def create_table():
  with get_connection() as conn:  
    cursor = conn.cursor()
    #Criando a tabela de usuários da base de dados, é definido tipo de variável e outras caracteristicas
    #AUTOINCREMENT = Se cria sozinha
    #PRIMARY KEY = Chave de identificação primaria
    #UNIQUE = Unica, não aceita mais de um com o mesmo nome
    #NOT NULL =  Não nula
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS usuarios (                 
          id INTEGER PRIMARY KEY AUTOINCREMENT,   
          username TEXT UNIQUE NOT NULL,
          password TEXT NOT NULL
        )
    """)

    #Criando tabela de produtos da base de dados
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS produtos (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          price REAL NOT NULL,
          quantidade INTEGER NOT NULL  
          )
    """)

    #Criando tabela de fornecedores na base de dados
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS fornecedores (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cellphone TEXT NOT NULL,
            email TEXT     
          )
    """)

    conn.commit()