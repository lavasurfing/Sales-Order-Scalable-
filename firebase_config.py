import firebase_admin
from firebase_admin import credentials,firestore


cred = credentials.Certificate(r"C:\Users\Ashish\Documents\Sales Order Scalable - Project\database_connection\key1.json")
firebase_admin.initialize_app(cred)

# database client
db = firestore.client()

collection_name = 'adv_sports'

# collection reference
collection_ref = db.collection(collection_name)



# To migrate data into another collection ( firebase config)
def copy_collection():
    desti_collec = 'adv_sports'
    source = db.collection(collection_name)
    desti = db.collection(desti_collec)
    
    docs = source.stream()
    for doc in docs:
        doc_ref = desti.document(doc.id)
        doc_ref.set(doc.to_dict())
        


def rename_field_in_collection():
    """
    Renames a field in all documents within a specified collection.

    This function assumes the old field exists in all documents.
    """
    old_field_name= 'Quantity'
    new_field_name = 'Qty'
    
    docs = collection_ref.stream()
    for doc in docs:
        doc_ref = doc.reference
        data = doc.to_dict()

        # Check if the old field exists in the document
        if old_field_name in data:
            new_data = {new_field_name: data.pop(old_field_name)} 
            doc_ref.update(new_data)
            
# Update quantity
def update_quantity():
    doc_id = 'i0i2vFs1dB0kdZQXV3Zi'
    collection_ref.document(doc_id).update({'Qty':29})
    # doc.update({'Avilablity':"Yes"})
    
    # print(doc.get().to_dict())
    
update_quantity()   