import sqlite3
import pandas as pd

# Ler o CSV com separador vírgula
df = pd.read_csv("saida_utf8.csv", sep=",", encoding="utf-8", header=None)

# Conferir se veio com 4 colunas
print(df.shape)   # deve mostrar algo como (N, 4)
print(df.head())  # só pra garantir

# Renomear colunas
df.columns = ["name", "unit", "quantidade", "price"]

# Conectar ao banco
conn = sqlite3.connect("estoque.db")
cursor = conn.cursor()

# Inserir os dados na tabela produtos
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO produtos (name, unit, quantidade, price) VALUES (?, ?, ?, ?)",
        (row["name"], row["unit"], int(row["quantidade"]), float(row["price"]))
    )

conn.commit()
conn.close()

print("Produtos importados com sucesso!")
