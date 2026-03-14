from .database import get_connection
from app.utils.security import hash_password


class UserModel:
    @staticmethod
    def create_user(name: str, username: str, password: str, profile: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO users (name, username, password_hash, profile) VALUES (?, ?, ?, ?)',
            (name, username, hash_password(password), profile)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_username(username: str):
        conn = get_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        return user

    @staticmethod
    def list_users():
        conn = get_connection()
        rows = conn.execute('SELECT id, name, username, profile, created_at FROM users ORDER BY id').fetchall()
        conn.close()
        return rows

    @staticmethod
    def create_default_admin():
        if not UserModel.get_by_username('admin'):
            UserModel.create_user('Administrador', 'admin', 'admin123', 'Administrador')
