from .database import get_connection


class ProductModel:
    @staticmethod
    def create_product(name: str, category: str, quantity: int, min_quantity: int, unit: str):
        conn = get_connection()
        conn.execute(
            '''INSERT INTO products (name, category, quantity, min_quantity, unit)
               VALUES (?, ?, ?, ?, ?)''',
            (name, category, quantity, min_quantity, unit)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update_product(product_id: int, name: str, category: str, min_quantity: int, unit: str):
        conn = get_connection()
        conn.execute(
            '''UPDATE products
               SET name = ?, category = ?, min_quantity = ?, unit = ?
               WHERE id = ?''',
            (name, category, min_quantity, unit, product_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def list_products():
        conn = get_connection()
        rows = conn.execute('SELECT * FROM products ORDER BY name').fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_product(product_id: int):
        conn = get_connection()
        row = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        conn.close()
        return row

    @staticmethod
    def search_products(term: str):
        conn = get_connection()
        rows = conn.execute(
            'SELECT * FROM products WHERE name LIKE ? OR category LIKE ? ORDER BY name',
            (f'%{term}%', f'%{term}%')
        ).fetchall()
        conn.close()
        return rows
