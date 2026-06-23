"""
Recria a tabela veiculos com o schema completo atualizado.
Executa via sqlite3 direto (sem Alembic) para máxima compatibilidade.
"""
import sqlite3
import sys
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sigfrota_dev.db")
OUT_PATH = os.path.join(os.path.dirname(__file__), "recreate_result.txt")

lines = []

def log(msg):
    print(msg)
    lines.append(msg)

log(f"DB: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Colunas atuais
cur.execute("PRAGMA table_info(veiculos)")
existing = {row[1] for row in cur.fetchall()}
log(f"Colunas atuais ({len(existing)}): {sorted(existing)}")

# Colunas que o modelo ORM espera
expected = {
    "id", "placa", "chassi", "renavam", "marca_id", "modelo_id",
    "ano_fabricacao", "ano_modelo", "cor", "combustivel", "motorizacao",
    "observacoes", "situacao", "prefixo", "tipo_frota_id", "categoria_id",
    "numero_patrimonio", "valor_aquisicao", "tipo_aquisicao", "tipo_convenio",
    "nome_locador", "valor_locacao", "secretaria_id", "unidade_id",
    "subunidade_id", "centro_custo_id", "tipo_registro_id", "tipo_controle",
    "hodometro_horimetro_inicial", "capacidade_tanque", "capacidade_passageiros",
    "capacidade_carga", "vencimento_licenciamento", "vencimento_seguro",
    "vencimento_ipva", "cilindrada", "potencia", "transmissao", "tracao",
    "vidros_eletricos", "direcao", "ar_condicionado", "pneu_dimensao",
    "pneu_velocidade", "pneu_carga", "uf", "municipio", "criado_em", "atualizado_em",
}

missing = expected - existing
extra = existing - expected
log(f"Faltando no banco ({len(missing)}): {sorted(missing)}")
log(f"Extras no banco ({len(extra)}): {sorted(extra)}")

# Adicionar colunas que faltam (ALTER TABLE ADD COLUMN)
add_columns = {
    "ano_modelo":                  "SMALLINT",
    "motorizacao":                 "VARCHAR(80) NOT NULL DEFAULT ''",
    "situacao":                    "VARCHAR(10) NOT NULL DEFAULT 'ATIVO'",
    "tipo_convenio":               "VARCHAR(20)",
    "secretaria_id":               "INTEGER",
    "unidade_id":                  "INTEGER",
    "subunidade_id":               "INTEGER",
    "centro_custo_id":             "INTEGER",
    "tipo_registro_id":            "INTEGER",
    "tipo_controle":               "VARCHAR(20) NOT NULL DEFAULT 'QUILOMETRAGEM'",
    "hodometro_horimetro_inicial": "INTEGER NOT NULL DEFAULT 0",
    "capacidade_tanque":           "INTEGER",
    "capacidade_passageiros":      "INTEGER",
    "capacidade_carga":            "INTEGER",
    "vencimento_licenciamento":    "DATE",
    "vencimento_seguro":           "DATE",
    "vencimento_ipva":             "DATE",
    "cilindrada":                  "INTEGER",
    "potencia":                    "INTEGER",
    "transmissao":                 "VARCHAR(20)",
    "tracao":                      "VARCHAR(10)",
    "vidros_eletricos":            "BOOLEAN NOT NULL DEFAULT 0",
    "direcao":                     "VARCHAR(20)",
    "ar_condicionado":             "BOOLEAN NOT NULL DEFAULT 0",
    "pneu_dimensao":               "VARCHAR(20)",
    "pneu_velocidade":             "VARCHAR(5)",
    "pneu_carga":                  "VARCHAR(5)",
    "uf":                          "VARCHAR(2) NOT NULL DEFAULT 'SP'",
    "municipio":                   "VARCHAR(120) NOT NULL DEFAULT ''",
    "criado_em":                   "DATETIME DEFAULT CURRENT_TIMESTAMP",
    "atualizado_em":               "DATETIME DEFAULT CURRENT_TIMESTAMP",
}

errors = []
added = []
for col, typedef in add_columns.items():
    if col not in existing:
        try:
            cur.execute(f"ALTER TABLE veiculos ADD COLUMN {col} {typedef}")
            added.append(col)
            log(f"  ✅ Adicionado: {col} {typedef}")
        except Exception as e:
            errors.append(f"{col}: {e}")
            log(f"  ❌ Erro em {col}: {e}")

conn.commit()

# Verificar resultado final
cur.execute("PRAGMA table_info(veiculos)")
final_cols = [row[1] for row in cur.fetchall()]
log(f"\nColunas finais ({len(final_cols)}): {sorted(final_cols)}")

conn.close()

log(f"\nAdicionadas: {len(added)} colunas")
log(f"Erros: {len(errors)}")

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

sys.exit(0 if not errors else 1)
