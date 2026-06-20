"""
Script para tornar certos campos da tabela veiculos como opcionais (nullable).
"""
import sqlite3

DB_PATH = 'sigfrota_dev.db'

def fix_schema():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = OFF')
    cursor = conn.cursor()
    
    try:
        # Verificar campos atuais
        cursor.execute('PRAGMA table_info(veiculos)')
        columns = {row[1]: row for row in cursor.fetchall()}
        
        print("Iniciando migração de schema...")
        print(f"Total de colunas: {len(columns)}")
        
        # Backup da tabela
        cursor.execute('CREATE TABLE veiculos_backup AS SELECT * FROM veiculos')
        
        # Remover restrições e recriar tabela com schema correto
        cursor.execute('DROP TABLE IF EXISTS veiculos')
        
        # Criar nova tabela com schema correto
        cursor.execute('''
            CREATE TABLE veiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                placa VARCHAR(10) NOT NULL UNIQUE,
                chassi VARCHAR(17) NOT NULL,
                renavam VARCHAR(11) NOT NULL,
                marca_id INTEGER NOT NULL,
                modelo_id INTEGER NOT NULL,
                ano_fabricacao SMALLINT NOT NULL,
                ano_modelo SMALLINT,
                cor VARCHAR(30),
                combustivel VARCHAR(12) NOT NULL,
                motorizacao VARCHAR(80),
                observacoes VARCHAR(500),
                situacao VARCHAR(10) NOT NULL DEFAULT 'ATIVA',
                prefixo VARCHAR(20) NOT NULL,
                tipo_frota_id INTEGER NOT NULL,
                categoria_id INTEGER NOT NULL,
                secretaria_id INTEGER NOT NULL,
                unidade_id INTEGER,
                subunidade_id INTEGER,
                centro_custo_id INTEGER,
                tipo_registro_id INTEGER,
                tipo_controle VARCHAR(20) NOT NULL DEFAULT 'QUILOMETRAGEM',
                hodometro_horimetro_inicial INTEGER NOT NULL DEFAULT 0,
                capacidade_tanque INTEGER,
                capacidade_passageiros INTEGER,
                capacidade_carga INTEGER,
                vencimento_licenciamento DATE,
                vencimento_seguro DATE,
                uf VARCHAR(2) NOT NULL DEFAULT 'SP',
                municipio VARCHAR(120),
                criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (marca_id) REFERENCES marcas(id),
                FOREIGN KEY (modelo_id) REFERENCES modelos(id),
                FOREIGN KEY (tipo_frota_id) REFERENCES tipos_frota(id),
                FOREIGN KEY (categoria_id) REFERENCES categorias(id),
                FOREIGN KEY (secretaria_id) REFERENCES secretarias(id),
                FOREIGN KEY (unidade_id) REFERENCES unidades(id),
                FOREIGN KEY (subunidade_id) REFERENCES subunidades(id),
                FOREIGN KEY (centro_custo_id) REFERENCES centros_custo(id)
            )
        ''')
        
        # Copiar dados de volta (apenas colunas que existem)
        cursor.execute('''
            INSERT INTO veiculos 
            SELECT 
                id, placa, chassi, renavam, marca_id, modelo_id, 
                ano_fabricacao, ano_modelo, cor, combustivel, 
                motorizacao, observacoes, situacao, prefixo, 
                tipo_frota_id, categoria_id, secretaria_id, 
                unidade_id, subunidade_id, centro_custo_id, 
                tipo_registro_id, tipo_controle, hodometro_horimetro_inicial,
                capacidade_tanque, capacidade_passageiros, capacidade_carga,
                vencimento_licenciamento, vencimento_seguro, uf, municipio,
                criado_em, atualizado_em
            FROM veiculos_backup
        ''')
        
        # Remover tabela backup
        cursor.execute('DROP TABLE IF EXISTS veiculos_backup')
        
        conn.commit()
        print("✅ Schema atualizado com sucesso!")
        print("   - Campos opcionais agora permitem NULL")
        print("   - Valores padrão adicionados onde necessário")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        # Recuperar da tabela backup
        cursor.execute('DROP TABLE IF EXISTS veiculos')
        cursor.execute('ALTER TABLE veiculos_backup RENAME TO veiculos')
        conn.commit()
        import traceback
        traceback.print_exc()
    finally:
        conn.execute('PRAGMA foreign_keys = ON')
        conn.close()

if __name__ == "__main__":
    fix_schema()
