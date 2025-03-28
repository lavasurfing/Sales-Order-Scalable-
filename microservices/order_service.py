from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

import asyncio

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

class Items(BaseModel):
    product_id: str
    qty : int
    doc_id: str
    
class Order_Base(BaseModel):
    ord_id: str
    cust_id : str
    
class Order(BaseModel):
    order_details : Order_Base
    items : List[Items]
    
class Invoice(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    

    
    
    
META_DATA = {
    'collection_name':'adv_sports',
    'order_collection' : 'Orders',
    'customer_collection':'Customer',
    'invoice_collection':'Invoices'
}

collection_ref = db.collection(META_DATA["collection_name"])



# helper functions
def validate_order_items(order_items):
    round_total = []
    for item in order_items:
        product_ref = collection_ref.document(item.doc_id)
        product = product_ref.get()
        if not product.exists:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id}- {item.product_id} not found.")
        product_data = product.to_dict()
        

        if product_data["Quantity"] < item.qty:
            print('Falling in Less quantity')
            raise HTTPException(
                status_code=400, detail=f"Insufficient stock for product {item.product_id}."
            )
        else:
            round_total.append({
            'doc_id' : item.doc_id,
            'p_id' : product_data["Product ID"],
            'p_name' : product_data["Product Name"],
            'quantity' : item.qty,
            'price' : product_data['Price']
            
        })
        
            print('Order Validated')
    return round_total

# Inventory Updater
def inventory_updater(order_items):
    for item in order_items:
        product_ref = collection_ref.document(item['doc_id'])
        product = product_ref.get().to_dict()
        # print(product)
        new_qty = int(product['Quantity']) - int(item['quantity'])
        product_ref.update({'Quantity': new_qty})
        print('Product Quantity updated for',item['p_name'])
        
        
# Save order details
async def customer_details_saving(order_details):
    # save customer ID 
    
    def add_customer():
        customer_coll_ref = db.collection(META_DATA['customer_collection'])
        customer_coll_ref.document().create({
            "Customer ID":order_details['cust_id'],
        })
        
        
    
    
    #save order details
    def add_order():
        order_coll_ref = db.collection(META_DATA['order_collection'])
        order_coll_ref.document().create({
            "Order ID": order_details['ord_id']
            # get product details and add here 
        })
    
        
        

    

@app.post('/test_orders')
def test_order(order: Order):
    # validate order
    total = validate_order_items(order.items)
    
    for each in total:
        print(each['quantity'])
        print(each['price'])
    
    
    qty = order.items[0]
    return {'data': 'Avilable', 'qty': qty}


# API Endpoints
# Root 
@app.get("/")
def get_root():
    return {'Ping':'Pong'}

# Order Place
@app.post("/place_order")
async def place_order(order: Order):
    
    # printing customer details
    print(order.order_details)
    
    # Validate order items
    total =  await validate_order_items(order.items)
    
    # calculating total
    p=0
    for t in total:
        print('Item Price' , t['price'])
        print('Item Quantity' , t['quantity'])
        print( 'Item Name'+t["p_name"])
        print("-----------------------------")
        p += int(t['quantity'])*int(t['price'])
    
    print(f'Order Taken and Backend Updated --- Your bill is : {p}')
    
    # Database entries 
    #  For each item entries must be deduct it's quantity
    await inventory_updater(total)
    
    
    # creating invoice
    
    
    # Saving cutomer details
    
    
    
    
    

    
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000) 