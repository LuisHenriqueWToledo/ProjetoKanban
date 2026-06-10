from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import engine
import models
from routers import auth, contas, quadros, cartoes, membros, raias


def _column_exists(conn, table_name: str, column_name: str) -> bool:
    rows = conn.execute(text(f"PRAGMA table_info({table_name})")).fetchall()
    return any(r[1] == column_name for r in rows)


def _migrar_schema_legado():
    """Aplica migracao minima para bases SQLite antigas sem raias."""
    with engine.begin() as conn:
        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS raias (
                id_raia INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                codigo_quadro VARCHAR(4) NOT NULL,
                nome VARCHAR NOT NULL,
                responsavel VARCHAR NOT NULL,
                ordem_exibicao INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (codigo_quadro) REFERENCES quadros(codigo),
                CONSTRAINT uq_raia_nome_no_quadro UNIQUE (codigo_quadro, nome)
            )
            """
        ))
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_raias_codigo_quadro ON raias (codigo_quadro)"))

        if not _column_exists(conn, "cartoes", "id_raia"):
            conn.execute(text("ALTER TABLE cartoes ADD COLUMN id_raia INTEGER"))

        quadros = conn.execute(text("SELECT codigo FROM quadros")).fetchall()
        for (codigo_quadro,) in quadros:
            responsaveis = conn.execute(text(
                """
                SELECT DISTINCT responsavel
                FROM cartoes
                WHERE codigo_quadro = :codigo_quadro
                  AND responsavel IS NOT NULL
                  AND TRIM(responsavel) <> ''
                """
            ), {"codigo_quadro": codigo_quadro}).fetchall()

            ordem = 0
            for (responsavel,) in responsaveis:
                raia = conn.execute(text(
                    """
                    SELECT id_raia
                    FROM raias
                    WHERE codigo_quadro = :codigo_quadro
                      AND responsavel = :responsavel
                    LIMIT 1
                    """
                ), {"codigo_quadro": codigo_quadro, "responsavel": responsavel}).fetchone()

                if not raia:
                    conn.execute(text(
                        """
                        INSERT INTO raias (codigo_quadro, nome, responsavel, ordem_exibicao)
                        VALUES (:codigo_quadro, :nome, :responsavel, :ordem)
                        """
                    ), {
                        "codigo_quadro": codigo_quadro,
                        "nome": responsavel,
                        "responsavel": responsavel,
                        "ordem": ordem,
                    })
                    raia = conn.execute(text(
                        """
                        SELECT id_raia
                        FROM raias
                        WHERE codigo_quadro = :codigo_quadro
                          AND responsavel = :responsavel
                        LIMIT 1
                        """
                    ), {"codigo_quadro": codigo_quadro, "responsavel": responsavel}).fetchone()
                    ordem += 1

                conn.execute(text(
                    """
                    UPDATE cartoes
                    SET id_raia = :id_raia
                    WHERE codigo_quadro = :codigo_quadro
                      AND responsavel = :responsavel
                      AND (id_raia IS NULL OR id_raia = 0)
                    """
                ), {
                    "id_raia": raia[0],
                    "codigo_quadro": codigo_quadro,
                    "responsavel": responsavel,
                })

            sem_raia = conn.execute(text(
                """
                SELECT COUNT(*)
                FROM cartoes
                WHERE codigo_quadro = :codigo_quadro
                  AND (id_raia IS NULL OR id_raia = 0)
                """
            ), {"codigo_quadro": codigo_quadro}).scalar_one()

            if sem_raia > 0:
                fallback = conn.execute(text(
                    """
                    SELECT id_raia
                    FROM raias
                    WHERE codigo_quadro = :codigo_quadro
                      AND nome = 'Sem Raia'
                    LIMIT 1
                    """
                ), {"codigo_quadro": codigo_quadro}).fetchone()
                if not fallback:
                    conn.execute(text(
                        """
                        INSERT INTO raias (codigo_quadro, nome, responsavel, ordem_exibicao)
                        VALUES (:codigo_quadro, 'Sem Raia', 'Sem Raia', 999)
                        """
                    ), {"codigo_quadro": codigo_quadro})
                    fallback = conn.execute(text(
                        """
                        SELECT id_raia
                        FROM raias
                        WHERE codigo_quadro = :codigo_quadro
                          AND nome = 'Sem Raia'
                        LIMIT 1
                        """
                    ), {"codigo_quadro": codigo_quadro}).fetchone()

                conn.execute(text(
                    """
                    UPDATE cartoes
                    SET id_raia = :id_raia,
                        responsavel = COALESCE(NULLIF(TRIM(responsavel), ''), 'Sem Raia')
                    WHERE codigo_quadro = :codigo_quadro
                      AND (id_raia IS NULL OR id_raia = 0)
                    """
                ), {"id_raia": fallback[0], "codigo_quadro": codigo_quadro})

# Criar tabelas no banco
models.Base.metadata.create_all(bind=engine)
_migrar_schema_legado()

app = FastAPI(
    title="Kanban API",
    description="Sistema de gestão Kanban — UnB Engenharia de Software",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(contas.router)
app.include_router(quadros.router)
app.include_router(cartoes.router)
app.include_router(raias.router)
app.include_router(membros.router)

# Servir frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
def root():
    return FileResponse("static/index.html")
