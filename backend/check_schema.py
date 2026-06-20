import sqlite3

conn = sqlite3.connect('sigfrota_dev.db')
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in c.fetchall()]

print('Tabelas existentes:')
for t in sorted(tables):
    print(f'  - {t}')

print("\nVerificando schema de veiculos - colunas com NOT NULL:")
c.execute('PRAGMA table_info(veiculos)')
cols = c.fetchall()
for col in cols:
    cid, name, type_, not_null, default_val, pk = col
    if not_null == 1:
        # Tentar encontrar relacionados
        if 'id' in name and name != 'id':
            # Verificar se tabela existe
            table_name = name.replace('_id', '') + 's'
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            exists = c.fetchone()
            print(f'  {name}: table "{table_name}" {"EXISTS" if exists else "NOT FOUND"} (default: {default_val})')
        else:
            print(f'  {name}: {type_} (default: {default_val})')
