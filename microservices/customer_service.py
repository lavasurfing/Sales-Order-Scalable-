# Starter block
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

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

# stater block end

# Class base models
class Customer(BaseModel):
    cust_it: str
    ord_id : str
    customer_name : Optional[str] | None
    customer_email : Optional[str] | None
    customer_address : Optional[str] | None
    
    

# endpoints
# @app.get("/")
# def get_root():
#     return {'Ping':'Pong - Customer Service'}

# @app.post("/save_details")
# def save_customer_details(customer: Customer):
    
    

    

