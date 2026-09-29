import sqlite3

DB = "results.db"

def _conn():
    c = sqlite3.connect(DB, timeout=10)
    c.execute("CREATE TABLE IF NOT EXISTS results "
              "(id TEXT PRIMARY KEY, status TEXT, result TEXT)")
    return c

def put(rid, status, result=None):
    c = _conn()
    with c:
        c.execute("INSERT OR REPLACE INTO results VALUES (?,?,?)",
                  (rid, status, result))
    c.close()

def get(rid):
    c = _conn()
    row = c.execute("SELECT status, result FROM results WHERE id=?",
                    (rid,)).fetchone()
    c.close()
    return {"status": row[0], "result": row[1]} if row else None