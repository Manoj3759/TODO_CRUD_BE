from fastapi import FastAPI
from models import Product


app = FastAPI()


@app.get("/")
def greet():
    return "hello world"


# using class constructure
# products = [
#     Product(1, "phone", 100, 10),
#     Product(2, "pen", 10, 100)
# ]


products = [
    Product(id=1, name="phone", price=100.0, quantity=10),
    Product(id=2, name="pen", price=10, quantity=100),
    Product(id=7, name="pencil", price=9.99, quantity=10)
]


@app.get("/products")
def get_all_products():
    return products


@app.get("/products/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    return "not found"


@app.post("/products")
def add_product(product: Product):
    products.append(product)
    return product
