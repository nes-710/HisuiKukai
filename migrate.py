import sqlite3
from database import DATABASE
import os

def column_exists(conn, table_name, column_name):
    columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return any(column[1] == column_name for column in columns)


def add_column_if_missing(conn, table_name, column_name, column_definition):
    if not column_exists(conn, table_name, column_name):
        conn.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
        )
        print(f"追加しました: {table_name}.{column_name}")
    else:
        print(f"既に存在します: {table_name}.{column_name}")


def main():
    conn = sqlite3.connect(DATABASE)

    add_column_if_missing(
        conn,
        "contests",
        "deadline_at",
        "TEXT",
    )

    conn.commit()
    conn.close()

    print("マイグレーションが完了しました。")

if not os.path.exists(DATABASE):
    print("データベースが存在しないため初期化します。")
    import init_db

if __name__ == "__main__":
    main()