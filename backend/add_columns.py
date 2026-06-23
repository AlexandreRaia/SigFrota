import sqlite3

conn = sqlite3.connect('sigfrota.db')
cursor = conn.cursor()

# Verificar colunas existentes
cursor.execute("PRAGMA table_info(veiculos)")
existing_columns = {row[1] for row in cursor.fetchall()}

print(f"Colunas existentes: {existing_columns}")

# Colunas a adicionar
columns_to_add = {
    'numero_patrimonio': 'VARCHAR(50)',
    'valor_aquisicao': 'FLOAT',
    'tipo_aquisicao': 'VARCHAR(20)',
    'nome_locador': 'VARCHAR(120)',
    'valor_locacao': 'FLOAT',
}

# Adicionar apenas as colunas que não existem
for col_name, col_type in columns_to_add.items():
    if col_name not in existing_columns:
        try:
            cursor.execute(f"ALTER TABLE veiculos ADD COLUMN {col_name} {col_type}")
            print(f"✓ Adicionada coluna: {col_name}")
        except sqlite3.OperationalError as e:
            print(f"✗ Erro ao adicionar {col_name}: {e}")
    else:
        print(f"→ Coluna {col_name} já existe")

conn.commit()
conn.close()

print("\n✓ Banco de dados atualizado!")
