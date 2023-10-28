CREATE TABLE IF NOT EXISTS trn_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , user_name TEXT NOT NULL
    , mail_address TEXT NOT NULL
    , password TEXT NOT NULL
    , token TEXT NOT NULL
    , del_flg TEXT NOT NULL DEFAULT '0'
    , created_at TEXT DEFAULT CURRENT_TIMESTAMP
    , created_by TEXT DEFAULT 'kitting'
    , updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    , updated_by TEXT DEFAULT 'kitting'
);
