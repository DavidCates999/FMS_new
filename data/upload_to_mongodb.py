import json
from pymongo import MongoClient
from datetime import datetime, timezone

def upload_leads_to_mongodb():
    # MongoDB connection settings
    MONGO_URI = "mongodb+srv://Anthony:yVXMtGOZKbRqSDNN@cluster0.rdt20jh.mongodb.net/"  # Update with your MongoDB URI
    DATABASE_NAME = "FMS"  # Update with your database name
    COLLECTION_NAME = "proposals"
    
    # Connect to MongoDB
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        return
    
    # Read JSON file
    try:
        with open("proposals_response.json", "r", encoding="utf-8") as f:  # Changed from servicecontracts_response.json to servicecontracts_response.json
            data = json.load(f)
        print(f"✅ Loaded JSON file successfully!")
    except Exception as e:
        print(f"❌ Failed to read JSON file: {e}")
        return
    
    # Get the leads collection
    collection = db[COLLECTION_NAME]
    
    # Extract content array from the response
    if isinstance(data, dict) and "content" in data:
        records = data["content"]
        total_elements = data.get("totalElements", len(records))
        print(f"📊 Total elements in API: {total_elements}")
        print(f"📦 Records to upload: {len(records)}")
    elif isinstance(data, dict) and "onDemand" in data:
        records = data["onDemand"]
        print(f"📦 Records to upload (onDemand): {len(records)}")
    elif isinstance(data, dict) and "rows" in data:
        # General ledger format - upload the entire document structure
        records = [data]  # Wrap the entire response as a single document
        print(f"📦 Uploading general ledger report (full document)")
        print(f"   - Account Summary items: {len(data.get('accountSummary', []))}")
        print(f"   - Transaction rows: {len(data.get('rows', []))}")
    elif isinstance(data, dict) and any(key in data for key in ['Account Manager', 'Operations Manager', 'GM', 'AGM']):
        # Users by authority format - flatten all users from all roles
        records = []
        for role_name, role_data in data.items():
            if isinstance(role_data, dict) and "content" in role_data:
                for user in role_data["content"]:
                    user["_role"] = role_name  # Add role to each user
                    records.append(user)
        print(f"📦 Uploading users by authority")
        print(f"   - Total users across all roles: {len(records)}")
        for role_name, role_data in data.items():
            if isinstance(role_data, dict) and "content" in role_data:
                print(f"   - {role_name}: {len(role_data['content'])} users")
    elif isinstance(data, list):
        records = data
        print(f"📦 Records to upload: {len(records)}")
    else:
        print(f"❌ Unexpected data format. Keys found: {list(data.keys()) if isinstance(data, dict) else type(data)}")
        return
    
    # Add metadata to each document
    for record in records:
        record["_importedAt"] = datetime.now(timezone.utc)
        record["_source"] = "api_import"
    
    # Insert documents
    try:
        if records:
            result = collection.insert_many(records)
            print(f"✅ Successfully inserted {len(result.inserted_ids)} documents into '{COLLECTION_NAME}' collection")
        else:
            print("⚠️ No documents to insert")
    except Exception as e:
        print(f"❌ Failed to insert documents: {e}")
        return
    
    # Print collection stats
    doc_count = collection.count_documents({})
    print(f"📈 Total documents in '{COLLECTION_NAME}' collection: {doc_count}")
    
    # Close connection
    client.close()
    print("🔌 MongoDB connection closed")

if __name__ == "__main__":
    upload_leads_to_mongodb()

