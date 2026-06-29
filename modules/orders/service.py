from sqlalchemy.orm import Session
from app.modules.orders import repository
from app.modules.products.model import Product


def create_order(db: Session, user_id: int, data):
    total_price = 0

    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            continue

        total_price += product.price * item.quantity

    order = repository.create_order(
        db=db,
        user_id=user_id,
        total_amount=total_price
    )

    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            continue

        repository.add_order_item(
            db=db,
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )

    return order


def get_orders(db: Session, user_id: int):
    return repository.get_orders_by_user(db, user_id)


def get_order(db: Session, order_id: int):
    return repository.get_order_by_id(db, order_id)