from sqlalchemy.orm import Session
from modules.orders import repository
from modules.products.model import Product


def create_order(db: Session, user_id: int, items):
    total = 0

    order = repository.create_order_record(db, user_id, 0)
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            continue

        price = product.price * item.quantity
        total += price

        repository.add_order_item(
            db,
            order.id,
            product.id,
            item.quantity,
            product.price
        )

    order.total_amount = total
    db.commit()

    return order


def get_orders(db: Session, user_id: int):
    return repository.get_orders_by_user(db, user_id)


def get_order(db: Session, order_id: int):
    return repository.get_order_by_id(db, order_id)