#!/usr/bin/env python
import sqlite3
from app.core.security import hash_password

db_path = "sigfrota_dev.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Verificar se existe admin
    cursor.execute("SELECT id FROM usuarios WHERE username = ?", ("admin",))
    admin = cursor.fetchone()
    
    if admin:
        print("Admin já existe. Atualizando senha...")
        cursor.execute(
            "UPDATE usuarios SET hashed_password = ? WHERE username = ?",
            (hash_password("1234"), "admin")
        )
        conn.commit()
        print("✓ Senha atualizada para '1234'")
    else:
        print("Criando novo admin...")
        # Primeiro, buscar ou criar uma secretaria
        cursor.execute("SELECT id FROM secretarias LIMIT 1")
        secretaria = cursor.fetchone()
        
        if not secretaria:
            cursor.execute(
                "INSERT INTO secretarias (nome, sigla, ativa, criado_em, atualizado_em) VALUES (?, ?, ?, datetime('now'), datetime('now'))",
                ("Padrão", "PAD", 1)
            )
            conn.commit()
            secretaria_id = cursor.lastrowid
        else:
            secretaria_id = secretaria[0]
        
        # Criar admin
        cursor.execute(
            """INSERT INTO usuarios 
               (username, email, first_name, last_name, hashed_password, 
                perfil, secretaria_id, telefone, ativo, is_superuser, criado_em, atualizado_em) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))""",
            ("admin", "admin@example.com", "Administrador", "Sistema",
             hash_password("1234"), "ADMIN", secretaria_id, "", 1, 1)
        )
        conn.commit()
        print("✓ Usuário admin criado com sucesso!")
        print(f"  Username: admin")
        print(f"  Senha: 1234")
        print(f"  Perfil: ADMIN")

except Exception as e:
    print(f"✗ Erro: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
