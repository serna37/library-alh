CREATE TABLE IF NOT EXISTS trn_remarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , mark_type TEXT NOT NULL
    , book_id INTEGER NOT NULL
    , user_id INTEGER NOT NULL
    , comments TEXT NOT NULL
    , stars INTEGER NOT NULL
    , favorit TEXT NOT NULL
    , del_flg TEXT NOT NULL DEFAULT '0'
    , created_at TEXT DEFAULT CURRENT_TIMESTAMP
    , created_by TEXT DEFAULT 'kitting'
    , updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    , updated_by TEXT DEFAULT 'kitting'
);
