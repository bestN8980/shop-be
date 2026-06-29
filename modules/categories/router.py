from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.database import get_db
from dependencies.rbac import require_role

from modules.categories.schema import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)

from modules.categories.service import (
    create_category_service,
    update_category_service,
    delete_category_service,
)

from core.enums import UserRole

from modules.categories.repository import get_all_categories

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    admin = Depends(require_role([UserRole.ADMIN]))
):
    return create_category_service(db, category)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    admin = Depends(require_role([UserRole.ADMIN]))
):
    return update_category_service(db, category_id, category)


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin = Depends(require_role([UserRole.ADMIN]))
):
    return delete_category_service(db, category_id)


@router.get("/", response_model=list[CategoryResponse])
def get_all_categories_route(db: Session = Depends(get_db)):
    return get_all_categories(db)