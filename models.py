from pydantic import BaseModel

# creating models using class constructure
# class Product:
#     id: int
#     name: str
#     price: int
#     quantity: int

#     def __init__(self, id: int,
#                  name: str,
#                  price: int,
#                  quantity: int):
#         self.id = id
#         self.name = name
#         self.price = price
#         self.quantity = quantity




# No need to create constructure Basemodel does it
class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int




