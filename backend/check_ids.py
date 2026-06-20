import sqlite3

conn = sqlite3.connect('sigfrota_dev.db')
c = conn.cursor()

print("Centro de Custos:")
c.execute('SELECT id, codigo FROM centros_custo LIMIT 5')
for row in c.fetchall():
    print(f"  {row[0]}: {row[1]}")

print("\nTipos de Registro:")
c.execute('SELECT id, nome FROM tipos_registro LIMIT 5')
result = c.fetchall()
if result:
    for row in result:
        print(f"  {row[0]}: {row[1]}")
else:
    print("  (nenhum tipo de registro encontrado)")

print("\nUnidades:")
c.execute('SELECT id, nome FROM unidades LIMIT 5')
for row in c.fetchall():
    print(f"  {row[0]}: {row[1]}")
