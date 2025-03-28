import firebase_admin
from firebase_admin import credentials,firestore

from google_sheet_conn import send_data_for_firebase

cred = credentials.Certificate(r"C:\Users\Ashish\Documents\Sales Order Scalable - Project\database_connection\key1.json")
firebase_admin.initialize_app(cred)

# database client
db = firestore.client()

collection_name = 'Adventure sports inventory'

# collection reference
collection_ref = db.collection('Adventure sports inventory')
document_id = 'HrcLmGzf6OObxUAYkkDY'

# sample Data 
data = send_data_for_firebase()

# creating batch object
batch = db.batch()

for doc_data in data:
    # generates new doc ID
    doc_ref = collection_ref.document()
    batch.set(doc_ref, doc_data)
    
# commit batch
try:
    batch.commit()
    print(f'Successfully Added{len(data)}')
except Exception as e:
    print(f'Error Adding {e}') 

