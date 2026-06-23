import sqlite3
import os

print(f"Arquivo existe: {os.path.exists('sigfrota.db')}")
print(f"Tamanho: {os.path.getsize('sigfrota.db')} bytes")

conn = sqlite3.connect('sigfrota.db')
cursor = conn.cursor()

# Listar tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"\nTabelas no banco: {tables}")

if tables:
    cursor.execute("PRAGMA table_info(veiculos)")
    columns = cursor.fetchall()
    print("\nColunas da tabela veiculos:")
    for col in columns:
        print(f"  {col[1]} - {col[2]}")
else:
    print("Nenhuma tabela encontrada!")

conn.close()
