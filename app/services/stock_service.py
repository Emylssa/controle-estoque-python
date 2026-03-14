from app.models.database import get_connection
from app.models.product_model import ProductModel
from app.models.movement_model import MovementModel


class StockService:
    @staticmethod
    def add_product(name: str, category: str, quantity: int, min_quantity: int, unit: str):
        ProductModel.create_product(name, category, quantity, min_quantity, unit)

    @staticmethod
    def update_product(product_id: int, name: str, category: str, min_quantity: int, unit: str):
        ProductModel.update_product(product_id, name, category, min_quantity, unit)

    @staticmethod
    def move_stock(product_id: int, movement_type: str, quantity: int, user_id: int, note: str):
        product = ProductModel.get_product(product_id)
        if not product:
            raise ValueError('Produto não encontrado.')

        current_qty = int(product['quantity'])
        if movement_type == 'Saída' and quantity > current_qty:
            raise ValueError('Quantidade de saída maior que o estoque disponível.')

        new_qty = current_qty + quantity if movement_type == 'Entrada' else current_qty - quantity

        conn = get_connection()
        conn.execute('UPDATE products SET quantity = ? WHERE id = ?', (new_qty, product_id))
        conn.commit()
        conn.close()

        MovementModel.create_movement(product_id, movement_type, quantity, user_id, note)
