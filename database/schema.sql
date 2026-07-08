CREATE TABLE IF NOT EXISTS contests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    contest_no TEXT NOT NULL,

    theme1 TEXT NOT NULL,
    judge1 TEXT NOT NULL,

    theme2 TEXT NOT NULL,
    judge2 TEXT NOT NULL,

    free_judge TEXT NOT NULL,

    status TEXT NOT NULL DEFAULT 'created',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);