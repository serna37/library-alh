CREATE TABLE IF NOT EXISTS trn_rental_temp (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , book_id INTEGER NOT NULL
    , user_id INTEGER NOT NULL
    , rent_num INTEGER NOT NULL DEFAULT 0
    , created_at TEXT DEFAULT CURRENT_TIMESTAMP
    , created_by TEXT DEFAULT 'kitting'
    , updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    , updated_by TEXT DEFAULT 'kitting'
);
