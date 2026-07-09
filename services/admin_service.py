import os
from sqlite3 import OperationalError

from database import get_connection
from werkzeug.security import check_password_hash, generate_password_hash


ADMIN_PASSWORD_KEY = "admin_password_hash"
DEFAULT_ADMIN_PASSWORD = os.environ.get("HISUI_ADMIN_PASSWORD", "hisui")


def ensure_settings_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )


def get_setting(key):
    conn = get_connection()

    try:
        row = conn.execute(
            """
            SELECT value
            FROM app_settings
            WHERE key = ?
            """,
            (key,),
        ).fetchone()
    except OperationalError:
        row = None

    conn.close()

    if not row:
        return None

    return row["value"]


def set_setting(key, value):
    conn = get_connection()

    ensure_settings_table(conn)

    conn.execute(
        """
        INSERT INTO app_settings (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """,
        (key, value),
    )

    conn.commit()
    conn.close()


def check_admin_password(password):
    password_hash = get_setting(ADMIN_PASSWORD_KEY)

    if password_hash:
        return check_password_hash(password_hash, password)

    return password == DEFAULT_ADMIN_PASSWORD


def change_admin_password(new_password):
    password_hash = generate_password_hash(new_password)
    set_setting(ADMIN_PASSWORD_KEY, password_hash)
