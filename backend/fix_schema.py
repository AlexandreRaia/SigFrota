#!/usr/bin/env python
import sqlite3

db_path = "sigfrota_dev.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Verificar se coluna já existe
    cursor.execute("PRAGMA table_info(veiculos)")
    columns = [row[1] for row in cursor.fetchall()]
    
    print("Colunas atuais na tabela veiculos:")
    for row in cursor.fetchall():
        print(f"  - {row}")
    
    cursor.execute("PRAGMA table_info(veiculos)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'motorizacao' not in columns:
        print("\nAdicionando coluna motorizacao...")
        cursor.execute("ALTER TABLE veiculos ADD COLUMN motorizacao VARCHAR(80) DEFAULT ''")
        conn.commit()
        print("✓ Coluna motorizacao adicionada com sucesso")
    else:
        print("\n✓ Coluna motorizacao já existe")
    
    print("\nColunas da tabela veiculos após atualização:")
    cursor.execute("PRAGMA table_info(veiculos)")
    for row in cursor.fetchall():
        print(f"  - {row[1]} ({row[2]})")
        
except Exception as e:
    print(f"✗ Erro: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
