import sqlite3
import bcrypt
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / 'sigfrota_dev.db'
if not DB.exists():
    print('DB not found:', DB)
    raise SystemExit(1)

conn = sqlite3.connect(str(DB))
cur = conn.cursor()
new_hash = bcrypt.hashpw('1234'.encode(), bcrypt.gensalt()).decode()
cur.execute('UPDATE usuarios SET hashed_password = ? WHERE username = ?', (new_hash, 'admin'))
conn.commit()
print('Senha do admin atualizada para 1234')
cur.execute('SELECT username FROM usuarios WHERE username = ?', ('admin',))
print('Encontrado:', cur.fetchone())
conn.close()
