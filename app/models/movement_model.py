from .database import get_connection


class MovementModel:
    @staticmethod
    def create_movement(product_id: int, movement_type: str, quantity: int, user_id: int, note: str):
        conn = get_connection()
        conn.execute(
            '''INSERT INTO movements (product_id, movement_type, quantity, user_id, note)
               VALUES (?, ?, ?, ?, ?)''',
            (product_id, movement_type, quantity, user_id, note)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def list_movements():
        conn = get_connection()
        rows = conn.execute(
            '''SELECT m.id, p.name AS product_name, m.movement_type, m.quantity, u.username,
                      m.note, m.created_at
               FROM movements m
               JOIN products p ON p.id = m.product_id
               JOIN users u ON u.id = m.user_id
               ORDER BY m.created_at DESC, m.id DESC'''
        ).fetchall()
        conn.close()
        return rows
