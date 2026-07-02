import sqlite3
import bcrypt

# Hash da senha "1234"
password = "1234"
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Conectar ao banco SQLite
conn = sqlite3.connect('sigfrota.db')
cursor = conn.cursor()

# Remover usuário anterior se existir
cursor.execute("DELETE FROM usuarios WHERE username = ?", ("admin",))

# Inserir novo usuário
cursor.execute("""
    INSERT INTO usuarios (username, email, first_name, last_name, hashed_password, perfil, telefone, ativo, is_superuser)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", ("admin", "admin@sigfrota.local", "Admin", "User", password_hash, "ADM", "(00) 00000-0000", True, True))

conn.commit()
conn.close()

print("✓ Usuário admin/1234 criado com sucesso!")

