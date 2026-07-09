CREATE TABLE IF NOT EXISTS contests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    contest_no TEXT NOT NULL,

    theme1 TEXT NOT NULL,
    judge1 TEXT NOT NULL,

    theme2 TEXT NOT NULL,
    judge2 TEXT NOT NULL,

    free_judge TEXT NOT NULL,

    status TEXT NOT NULL DEFAULT 'created',
    deadline_at TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    contest_id INTEGER NOT NULL,

    pen_name TEXT NOT NULL,
    pen_name_kana TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(contest_id) REFERENCES contests(id)
);

CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    participant_id INTEGER NOT NULL,

    theme TEXT NOT NULL,

    poem TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(participant_id) REFERENCES participants(id)
);

CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
