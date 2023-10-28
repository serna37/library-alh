CREATE TABLE IF NOT EXISTS mst_books_stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , book_id INTEGER NOT NULL
    , stock INTEGER DEFAULT 0
    , del_flg TEXT NOT NULL DEFAULT '0'
    , created_at TEXT DEFAULT CURRENT_TIMESTAMP
    , created_by TEXT DEFAULT 'kitting'
    , updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    , updated_by TEXT DEFAULT 'kitting'
);

