import sqlite3
conn = sqlite3.connect("sigfrota_dev.db")
cursor = conn.cursor()
cursor.execute("SELECT id, username, email, perfil FROM usuarios")
usuarios = cursor.fetchall()
print(f"Total de usuários: {len(usuarios)}")
for user in usuarios:
    print(f"  {user[0]}: {user[1]} ({user[3]})")
conn.close()
