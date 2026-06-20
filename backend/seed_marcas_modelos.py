#!/usr/bin/env python
"""
Script para popular marcas e modelos no banco de dados.
"""

import sqlite3

DB_PATH = 'sigfrota_dev.db'

def seed_marcas_modelos():
    """Popula marcas e modelos iniciais."""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. Inserir Marcas
        marcas_data = [
            ('Fiat', True),
            ('Chevrolet', True),
            ('Volkswagen', True),
            ('Hyundai', True),
            ('Ford', True),
            ('Toyota', True),
        ]
        
        marcas_dict = {}
        for nome, ativo in marcas_data:
            cursor.execute('SELECT id FROM marcas WHERE nome = ?', (nome,))
            marca = cursor.fetchone()
            
            if not marca:
                cursor.execute(
                    'INSERT INTO marcas (nome, ativo) VALUES (?, ?)',
                    (nome, ativo)
                )
                marca_id = cursor.lastrowid
                print(f"✓ Marca criada: {nome}")
            else:
                marca_id = marca[0]
            
            marcas_dict[nome] = marca_id
        
        # 2. Inserir Modelos por Marca
        modelos_por_marca = {
            'Fiat': [
                'Uno',
                'Palio',
                'Siena',
                'Strada',
                'Ducato',
            ],
            'Chevrolet': [
                'Onix',
                'Prisma',
                'Spin',
                'S10',
                'D-Max',
            ],
            'Volkswagen': [
                'Gol',
                'Voyage',
                'Fox',
                'Saveiro',
                'Amarok',
            ],
            'Hyundai': [
                'HB20',
                'Creta',
                'Tucson',
            ],
            'Ford': [
                'Fiesta',
                'Focus',
                'Ranger',
            ],
            'Toyota': [
                'Corolla',
                'Hilux',
                'Etios',
            ],
        }
        
        for marca_nome, modelos in modelos_por_marca.items():
            marca_id = marcas_dict.get(marca_nome)
            if not marca_id:
                continue
            
            for modelo_nome in modelos:
                cursor.execute(
                    'SELECT id FROM modelos WHERE nome = ? AND marca_id = ?',
                    (modelo_nome, marca_id)
                )
                if not cursor.fetchone():
                    cursor.execute(
                        'INSERT INTO modelos (marca_id, nome, ativo) VALUES (?, ?, ?)',
                        (marca_id, modelo_nome, True)
                    )
                    print(f"  ✓ Modelo criado: {marca_nome} {modelo_nome}")
        
        conn.commit()
        print("\n✅ Marcas e modelos populados com sucesso!")
        
    except Exception as e:
        print(f"✗ Erro: {e}")
        conn.rollback()
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    seed_marcas_modelos()
