from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.users.router import router as user_routers
from modules.users.admin_router import router as admin_user_routers
from modules.products.router import router as product_routers
from modules.categories.router import router as category_routers
from modules.carts.router import router as cart_routers
from modules.orders.router import router as order_routers
from core.database import Base, engine



app = FastAPI(
    title="Mini E-commerce API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://shop-fe.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    import modules.users.model
    import modules.products.model
    import modules.carts.model
    import modules.categories.model
    import modules.orders.model
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "message": "Mini E-commerce API"
    }

app.include_router(user_routers)
app.include_router(admin_user_routers)
app.include_router(product_routers)
app.include_router(category_routers)
app.include_router(cart_routers)
app.include_router(order_routers)
