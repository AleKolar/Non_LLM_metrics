# src/config/database.py
import sqlite3

DB_PATH = "metrics.db"


def init_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Создаёт подключение к SQLite, создаёт таблицу, если её нет."""
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tp INTEGER NOT NULL,
                tn INTEGER NOT NULL,
                fp INTEGER NOT NULL,
                fn INTEGER NOT NULL,
                first_relevant_rank INTEGER NOT NULL,
                ranks TEXT,
                accuracy REAL,
                precision REAL,
                recall REAL,
                f1 REAL,
                rr REAL,
                mrr REAL,
                analysis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    return conn


def save_metrics(conn: sqlite3.Connection, payload, result: dict) -> None:
    """Сохраняет один результат расчёта в таблицу metrics."""
    if conn is None:
        raise RuntimeError("Нет подключения к БД")

    conn.execute("""
        INSERT INTO metrics 
            (tp, tn, fp, fn, first_relevant_rank, ranks,
             accuracy, precision, recall, f1, rr, mrr, analysis)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        payload.tp,
        payload.tn,
        payload.fp,
        payload.fn,
        payload.first_relevant_rank,
        ",".join(map(str, payload.ranks)) if payload.ranks else None,
        result["accuracy"],
        result["precision"],
        result["recall"],
        result["f1"],
        result["rr"],
        result["mrr"],
        result["analysis"]
    ))
    conn.commit()
