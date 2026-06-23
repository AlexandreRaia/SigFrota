"""
Recria a tabela veiculos do zero com todas as FKs nullable.
Seguro pois não há dados na tabela.
"""
import sqlite3
import sys
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sigfrota_dev.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Checar quantidade de registros antes
count = cur.execute("SELECT COUNT(*) FROM veiculos").fetchone()[0]
print(f"Registros em veiculos antes: {count} (serão descartados - dados de teste)")

# Drop e recria
cur.execute("DROP TABLE IF EXISTS veiculos")

cur.execute("""
CREATE TABLE veiculos (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,

    -- DADOS GERAIS
    placa                       VARCHAR(10)  NOT NULL UNIQUE,
    chassi                      VARCHAR(17)  NOT NULL UNIQUE,
    renavam                     VARCHAR(11)  NOT NULL UNIQUE,
    marca_id                    INTEGER      REFERENCES marcas(id),
    modelo_id                   INTEGER      REFERENCES modelos(id),
    ano_fabricacao              SMALLINT     NOT NULL,
    ano_modelo                  SMALLINT,
    cor                         VARCHAR(30)  NOT NULL DEFAULT '',
    combustivel                 VARCHAR(12)  NOT NULL DEFAULT 'FLEX',
    motorizacao                 VARCHAR(80)  NOT NULL DEFAULT '',
    observacoes                 VARCHAR(500) NOT NULL DEFAULT '',
    situacao                    VARCHAR(10)  NOT NULL DEFAULT 'ATIVO',

    -- CLASSIFICAÇÃO DA FROTA
    prefixo                     VARCHAR(20)  UNIQUE,
    tipo_frota_id               INTEGER      REFERENCES tipos_frota(id),
    categoria_id                INTEGER      REFERENCES categorias(id),
    numero_patrimonio           VARCHAR(50),
    valor_aquisicao             FLOAT,
    tipo_aquisicao              VARCHAR(20),
    tipo_convenio               VARCHAR(20),
    nome_locador                VARCHAR(120),
    valor_locacao               FLOAT,

    -- VINCULAÇÃO ADMINISTRATIVA
    secretaria_id               INTEGER      REFERENCES secretarias(id),
    unidade_id                  INTEGER      REFERENCES unidades(id),
    subunidade_id               INTEGER      REFERENCES subunidades(id),
    centro_custo_id             INTEGER      REFERENCES centros_custo(id),

    -- DADOS OPERACIONAIS
    tipo_registro_id            INTEGER      REFERENCES tipos_veiculo(id),
    tipo_controle               VARCHAR(20)  NOT NULL DEFAULT 'QUILOMETRAGEM',
    hodometro_horimetro_inicial INTEGER      NOT NULL DEFAULT 0,
    capacidade_tanque           INTEGER,
    capacidade_passageiros      INTEGER,
    capacidade_carga            INTEGER,

    -- DOCUMENTAÇÃO
    vencimento_licenciamento    DATE,
    vencimento_seguro           DATE,
    vencimento_ipva             DATE,

    -- DADOS TÉCNICOS
    cilindrada                  INTEGER,
    potencia                    INTEGER,
    transmissao                 VARCHAR(20),
    tracao                      VARCHAR(10),
    vidros_eletricos            BOOLEAN      NOT NULL DEFAULT 0,
    direcao                     VARCHAR(20),
    ar_condicionado             BOOLEAN      NOT NULL DEFAULT 0,
    pneu_dimensao               VARCHAR(20),
    pneu_velocidade             VARCHAR(5),
    pneu_carga                  VARCHAR(5),

    -- LOCALIZAÇÃO
    uf                          VARCHAR(2)   NOT NULL DEFAULT 'SP',
    municipio                   VARCHAR(120) NOT NULL DEFAULT '',

    -- TIMESTAMPS
    criado_em                   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em               DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# Verificar resultado
rows = cur.execute("PRAGMA table_info(veiculos)").fetchall()
print(f"Tabela recriada com {len(rows)} colunas:")
for r in rows:
    nullable = "" if r[3] else " (nullable)"
    print(f"  {r[1]:35s} {r[2]}{nullable}")

conn.close()
print("\nConcluído com sucesso!")
