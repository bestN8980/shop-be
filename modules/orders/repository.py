from sqlalchemy.orm import Session
from app.modules.orders.model import Order, OrderItem


def create_order(db: Session, user_id: int, total_amount: float):
    order = Order(
        user_id=user_id,
        total_amount=total_amount
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def add_order_item(
    db: Session,
    order_id: int,
    product_id: int,
    quantity: int,
    price: float
):
    item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        price=price
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_orders_by_user(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_order_items(db: Session, order_id: int):
    return db.query(OrderItem).filter(
        OrderItem.order_id == order_id
    ).all()


def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order:
        db.delete(order)
        db.commit()

    return order