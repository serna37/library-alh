CREATE TABLE IF NOT EXISTS mst_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , book_name TEXT NOT NULL
    , author_name TEXT NOT NULL
    , publisher_cd TEXT NOT NULL
    , published_at TEXT DEFAULT CURRENT_TIMESTAMP
    , donator_user_id INTEGER NOT NULL
    , del_flg TEXT NOT NULL DEFAULT '0'
    , created_at TEXT DEFAULT CURRENT_TIMESTAMP
    , created_by TEXT DEFAULT 'kitting'
    , updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    , updated_by TEXT DEFAULT 'kitting'
);
