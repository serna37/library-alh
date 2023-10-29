CREATE TABLE IF NOT EXISTS mst_attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , attribute_id INTEGER NOT NULL
    , attribute TEXT NOT NULL
    , del_flg TEXT NOT NULL DEFAULT '0'
    , created_at TEXT DEFAULT CURRENT_TIMESTAMP
    , created_by TEXT DEFAULT 'kitting'
    , updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    , updated_by TEXT DEFAULT 'kitting'
);

