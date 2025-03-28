from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

import uuid

# firebase_package import
import firebase_admin
from firebase_admin import credentials,firestore


# firebase authentication
cred = credentials.Certificate(r"C:\Users\Ashish\Documents\Sales Order Scalable - Project\database_connection\key1.json")
firebase_admin.initialize_app(cred)

# firbase client object
db = firestore.client()


# Initializing FastAPI app
app = FastAPI()

# Models
class OrderItem(BaseModel):
    product_id:str
    quantity:int
    
class Order(BaseModel):
    customer_id:str
    items:List[OrderItem]
    
class Invoice(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    

META_DATA = {
    'collection_name':'adv_sports'
}


collection_ref = db.collection(META_DATA["collection_name"])
    
    
# helper functions
def validate_order_items(order_items):
    for item in order_items:
        product_ref = collection_ref.document(item.doc_id)
        product = product_ref.get()
        if not product.exists:
            raise HTTPException(status_code=404, detail=f"Product {item['Product ID']}- {item['Product ID']} not found.")
        product_data = product.to_dict()
        if product_data["Qty"] < item['Quantity']:
            raise HTTPException(
                status_code=400, detail=f"Insufficient stock for product {item.product_id}."
            )
        else:
            print('Order Validated')
            
def update_inventory(order_items):
    for item in order_items:
        product_ref = collection_ref.document(item['doc_id'])
        product = product_ref.get().to_dict()
        new_quantity = product["Qty"] - item['Quantity']
        product_ref.update({"Qty": new_quantity})





# API Endpoints
@app.post("/place_order", status_code=201)
def place_order(order):
    # Validate order items
    validate_order_items(order['items'])

    # Calculate total
    total = 0
    for item in order['items']:
        product_ref = collection_ref.document(item['doc_id'])
        product = product_ref.get().to_dict()
        total += product["Price"] * item['Quanity']

    # Generate order ID
    order_id = str(uuid.uuid4())

    # Update inventory
    update_inventory(order['items'])

    # Save order to Firestore
    db.collection("Orders").document(order_id).set({
        "Order ID" : uuid.uuid1(),
        "customer_id": order.customer_id,
        "items": [item.model_dump() for item in order.items],
        "total": total,
    })

    print('Order Taken and Backend Updated')
    
    # Return invoice
    # return print(Invoice(order_id=order_id, total=total))
    

# @app.get("/inventory", response_model=List[Product])
# def get_inventory():
#     products = db.collection("inventory").stream()
#     return [
#         Product(
#             product_id=product.id,
#             name=product.to_dict()["name"],
#             price=product.to_dict()["price"],
#             quantity=product.to_dict()["quantity"]
#         )
#         for product in products
#     ]

# @app.post("/inventory/add", response_model=Product)
# def add_product(product: Product):
#     product_ref = db.collection("inventory").document(product.product_id)
#     product_ref.set({
#         "name": product.name,
#         "price": product.price,
#         "quantity": product.quantity
#     })
#     return product

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 
    