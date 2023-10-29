CREATE TABLE IF NOT EXISTS trn_action_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , user_id INTEGER NOT NULL
    , book_id INTEGER NOT NULL
    , action TEXT NOT NULL -- donate / remark / rental / return
    , num INTEGER NOT NULL
    , del_flg TEXT NOT NULL DEFAULT '0'
    , created_at TEXT DEFAULT CURRENT_TIMESTAMP
    , created_by TEXT DEFAULT 'kitting'
    , updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    , updated_by TEXT DEFAULT 'kitting'
);
