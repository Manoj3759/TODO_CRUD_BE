from fastapi import FastAPI, HTTPException, Depends
from models import Product
from database import session, engine
import database_sechma
from sqlalchemy.orm import Session


app = FastAPI()

database_sechma.Base.metadata.create_all(bind=engine)


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


# to establish the DB connection by session so that session is terminated after excution/error
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def db_init():
    db = session()

    count = db.query(database_sechma.Product).count()

    if (count == 0):
        for product in products:
            db.add(database_sechma.Product(**product.model_dump()))
        db.commit()
        db.close()


db_init()


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    # db:Session = Depends(get_db) is nothing but type hinting for the db parameter which is used to establish the connection with the database
    products = db.query(database_sechma.Product).all()
    # database_sechma.Product basically table name along with sechma
    return products


# in memeory integration
# @app.get("/products/{id}")
# def get_product_by_id(id: int):
#     for product in products:
#         if product.id == id:
#             return product
#     return "not found"

# @app.post("/products")
# def add_product(product: Product):
#     products.append(product)
#     return product


# @app.delete("/products/{id}")
# def delete_product(id: int):
#     try:
#         for i in range(len(products)):
#             if products[i].id == id:
#                 del products[i]
#         return {"message": "Product Deleted Successfully"}
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail="delete_product---> some error occurred while deleting the product")


# @app.put("/products")
# def update_product(id: int, product: Product):
#     for i in range(len(products)):
#         if products[i].id == id:
#             products[i] = product
#             return {"message": "Product Added Successfully", "updated_product": product}
#     raise HTTPException(
#         status_code=404,
#         detail="No Product found")


@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_sechma.Product).filter(
        database_sechma.Product.id == id).first()
    if db_product:
        return db_product
    raise HTTPException(
        status_code=404,
        detail="get_product_by_id---> Product not found")


@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.commit()
    return product


@app.put("/products")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):

    db_product_found = db.query(database_sechma.Product).filter(
        database_sechma.Product.id == id).first()
    if db_product_found:
        for key, value in product.dict().items():
            setattr(db_product_found, key, value)
        db.commit()
        return {"message": "Product Added Successfully", "updated_product": product}


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product_found = db.query(database_sechma.Product).filter(
        database_sechma.Product.id == id).first()
    if not db_product_found:
        raise HTTPException(
            status_code=404,
            detail="delete_product---> Product not found")
    db.delete(db_product_found)
    db.commit()
    return "product deleted"
