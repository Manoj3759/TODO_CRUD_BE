from fastapi import FastAPI, HTTPException
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


@app.delete("/products/{id}")
def delete_product(id: int):
    try:
        for i in range(len(products)):
            if products[i].id == id:
                del products[i]
        return {"message": "Product Deleted Successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="delete_product---> some error occurred while deleting the product")


@app.put("/products")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return {"message": "Product Added Successfully", "updated_product": product}
    raise HTTPException(
        status_code=404,
        detail="No Product found")
