import sqlite3
import os


class Index:
    def __init__(self, index_path="gho_index.db"):
        self.index_path = index_path
        self.conn = None
        if os.path.exists(index_path):
            self.conn = sqlite3.connect(index_path)
            self.conn.row_factory = sqlite3.Row

    def _ensure_table(self):
        self.conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS indicators USING fts5(code, description)"
        )
        self.conn.commit()

    def build_index(self, codes):
        if self.conn is None:
            dir_path = os.path.dirname(self.index_path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            self.conn = sqlite3.connect(self.index_path)
            self.conn.row_factory = sqlite3.Row
        self._ensure_table()
        self.conn.execute("DELETE FROM indicators")
        for row in codes.itertuples():
            self.conn.execute(
                "INSERT INTO indicators(code, description) VALUES (?, ?)",
                (row.Label, row.Display),
            )
        self.conn.commit()

    def search(self, query):
        if self.conn is None:
            return []
        try:
            cursor = self.conn.execute(
                "SELECT code, description FROM indicators WHERE indicators MATCH ?",
                (query,),
            )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.OperationalError:
            return []
