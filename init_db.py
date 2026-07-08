import sqlite3

connection = sqlite3.connect("data/hisui.db")

with open("database/schema.sql", encoding="utf-8") as f:
    connection.executescript(f.read())

connection.commit()
connection.close()

print("データベースを作成しました。")