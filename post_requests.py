import requests

urls = {
    'Order':'http://127.0.0.1:8000/place_order'
}

payload = {
      "customer_id": "cust345",
      "items": [
        {
          'doc_id': 'aKBinKrGb3eKZTxrtYVZ',
          "Product ID": "P-6",
          "Quantity": 5
        }
        ]
      }

try:
    res = requests.post(urls['Order'],json=payload)
    print('Request Complete')
    print(res)
except:
    print("Post Request Not Working")

