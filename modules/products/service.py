from app.modules.products.repository import get_product_by_category_id,get_product_by_id, create_product, delete_product, update_product, get_all_product, get_product_by_name
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.modules.products.schema import ProductCreate, ProductResponse, ProductUpdate, Message
from app.modules.products.model import Product

def create_product_service(db: Session, product:ProductCreate)->ProductResponse:
    existing = get_product_by_name(db, product.name)
    if existing:
        raise HTTPException(status_code=400, detail="Product is existed")
    return create_product(db, product)

def update_product_service(db, product_id:int, product: ProductUpdate)->ProductResponse:
    found_product = get_product_by_id(db, product_id)
    if not found_product :
        raise HTTPException(status_code=404, detail="Product not found")
    
    return update_product(db, product, product_id)

def delete_product_service(db: Session, product_id: int) -> Message:
    found_product = get_product_by_id(db, product_id)

    if not found_product:
        raise HTTPException(status_code=404, detail="Product not found")

    delete_product(db, product_id)

    return Message(message="Product is deleted successfully")

def get_all_product_service(db: Session):
    return get_all_product(db)