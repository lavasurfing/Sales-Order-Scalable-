from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class maths(BaseModel):
    val1: int
    val2: int
    label: str
    
    
    

inventory = {
    1:{
        'name':'cbr',
        'cc': 1000,
        'price':30000
    }
}


def addy(x,y):
    return x+y

@app.get('/home')
def send_data():
    return {
        'Car':'BMW'
    }
    
@app.get('/get_bike')
def get_bike_by_id(*,id: int, name: Optional[str]):
    for id in inventory:
        if  inventory[id]['name'] == name:
            return inventory[id]
        
    return {'data':'not found'}


@app.post('/get_math')
def add_these_two(a :int, b :int):
    ans = addy(a,b)
    return {'data': ans}
    

    
    
