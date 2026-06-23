"""Script para aplicar migration e verificar resultado."""
import subprocess
import sqlite3
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Rodar alembic
print("=== Rodando alembic upgrade head ===")
result = subprocess.run(
    [sys.executable, "-m", "alembic", "upgrade", "head"],
    capture_output=True,
    text=True
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)

# Verificar colunas depois
print("\n=== Colunas da tabela veiculos após migration ===")
conn = sqlite3.connect("sigfrota_dev.db")
rows = conn.execute("PRAGMA table_info(veiculos)").fetchall()
for r in rows:
    print(f"  {r[1]:35s} {r[2]}")
conn.close()
