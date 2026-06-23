#!/usr/bin/env python
"""
Script para popular dados parametrizados iniciais no banco de dados.
Executa com: python seed_parametrizacoes.py
"""

import sqlite3

DB_PATH = 'sigfrota_dev.db'

def seed_database():
    """Popula dados iniciais no banco de dados usando SQL direto."""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. Categorias
        categorias_data = [
            ('Passeio', True),
            ('Utilitário', True),
            ('Caminhonete', True),
            ('Ambulância', True),
            ('Caminhão', True),
            ('Ônibus', True),
            ('Motocicleta', True),
            ('Máquina Pesada', True),
            ('Equipamento', True),
        ]
        
        for nome, ativo in categorias_data:
            cursor.execute('SELECT id FROM categorias WHERE nome = ?', (nome,))
            if not cursor.fetchone():
                cursor.execute(
                    'INSERT INTO categorias (nome, descricao, ativa) VALUES (?, ?, ?)',
                    (nome, '', ativo)
                )
                print(f"✓ Categoria criada: {nome}")
        
        # 2. Tipos de Frota
        tipos_frota_data = [
            ('Próprio', True),
            ('Locado', True),
            ('Convênio', True),
        ]
        
        for nome, ativo in tipos_frota_data:
            cursor.execute('SELECT id FROM tipos_frota WHERE nome = ?', (nome,))
            if not cursor.fetchone():
                cursor.execute(
                    'INSERT INTO tipos_frota (nome, ativa) VALUES (?, ?)',
                    (nome, ativo)
                )
                print(f"✓ Tipo de Frota criado: {nome}")
        
        # 3. Tipos de Veículo
        tipos_veiculo_data = [
            ('VEICULO', True),
            ('MAQUINA', True),
            ('EQUIPAMENTO', True),
        ]
        
        for nome, ativo in tipos_veiculo_data:
            cursor.execute('SELECT id FROM tipos_veiculo WHERE nome = ?', (nome,))
            if not cursor.fetchone():
                cursor.execute(
                    'INSERT INTO tipos_veiculo (nome, ativo) VALUES (?, ?)',
                    (nome, ativo)
                )
                print(f"✓ Tipo de Veículo criado: {nome}")
        
        # 4. Secretarias
        cursor.execute("SELECT id FROM secretarias WHERE nome = ?", 
                      ('Secretaria de Obras e Serviços',))
        secretaria_id = cursor.fetchone()
        
        if not secretaria_id:
            cursor.execute(
                'INSERT INTO secretarias (nome, sigla, ativa) VALUES (?, ?, ?)',
                ('Secretaria de Obras e Serviços', 'SOS', True)
            )
            secretaria_id = cursor.lastrowid
            print(f"✓ Secretaria criada: Secretaria de Obras e Serviços")
        else:
            secretaria_id = secretaria_id[0]
        
        # 5. Unidades
        unidades_data = [
            ('Frota de Veículos Leves', 'FVL', secretaria_id, True),
            ('Frota de Veículos Pesados', 'FVP', secretaria_id, True),
            ('Máquinas e Equipamentos', 'MAQ', secretaria_id, True),
        ]
        
        unidades_dict = {}
        for nome, sigla, sec_id, ativa in unidades_data:
            cursor.execute(
                'SELECT id FROM unidades WHERE nome = ? AND secretaria_id = ?',
                (nome, sec_id)
            )
            unidade = cursor.fetchone()
            if not unidade:
                cursor.execute(
                    'INSERT INTO unidades (secretaria_id, nome, sigla, ativa) VALUES (?, ?, ?, ?)',
                    (sec_id, nome, sigla, ativa)
                )
                unidade_id = cursor.lastrowid
                print(f"✓ Unidade criada: {nome}")
            else:
                unidade_id = unidade[0]
            unidades_dict[nome] = unidade_id
        
        # 6. Subunidades
        subunidades_data = [
            ('Frotas de Passeio', 'FPA', unidades_dict['Frota de Veículos Leves'], True),
            ('Frotas de Serviço', 'FSV', unidades_dict['Frota de Veículos Leves'], True),
            ('Caminhões', 'CAM', unidades_dict['Frota de Veículos Pesados'], True),
            ('Ônibus', 'ONI', unidades_dict['Frota de Veículos Pesados'], True),
        ]
        
        for nome, sigla, unidade_id, ativa in subunidades_data:
            cursor.execute('SELECT id FROM subunidades WHERE nome = ?', (nome,))
            if not cursor.fetchone():
                cursor.execute(
                    'INSERT INTO subunidades (unidade_id, nome, sigla, ativa) VALUES (?, ?, ?, ?)',
                    (unidade_id, nome, sigla, ativa)
                )
                print(f"✓ Subunidade criada: {nome}")
        
        # 7. Centros de Custo
        centros_custo_data = [
            ('CC001', 'Manutenção de Frota', True),
            ('CC002', 'Combustível', True),
            ('CC003', 'Seguro Veículos', True),
            ('CC004', 'IPVA e Licenciamento', True),
            ('CC005', 'Aluguel de Veículos', True),
        ]
        
        for codigo, nome, ativo in centros_custo_data:
            cursor.execute('SELECT id FROM centros_custo WHERE codigo = ?', (codigo,))
            if not cursor.fetchone():
                cursor.execute(
                    'INSERT INTO centros_custo (codigo, nome, ativa) VALUES (?, ?, ?)',
                    (codigo, nome, ativo)
                )
                print(f"✓ Centro de Custo criado: {codigo} - {nome}")
        
        conn.commit()
        print("\n✅ Seed de dados concluído com sucesso!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro ao popular dados: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    seed_database()
