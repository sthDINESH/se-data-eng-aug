from pymongo import MongoClient


def get_db(uri, database):
    """
    Connect to MongoDB and return a database object.
    Args:
        uri (str): MongoDB connection URI (e.g., 'mongodb://localhost:27017/')
        database (str): Name of the database to connect to
    Returns:
        Database: MongoDB database object if connection successful,
        None otherwise
    Raises:
        Prints error messages to console on connection failure
    """
    client = MongoClient(uri)

    try:
        # Verify connection
        client.admin.command('ping')
        print("✓ Successfully connected to MongoDB")

        # Check database exists
        available_dbs = client.list_database_names()

        if database in available_dbs:
            print(f"✓ Database '{database}' found.")
            return client.get_database(database)
        else:
            print(f"✗ Database '{database}' not found.")
            print(f"Available databases: {available_dbs}")
            return None

    except Exception as e:
        print(f"✗ Error connecting to MongoDB: {e}")
        return None


def get_collection(db, collection):
    """
    Get a collection from a MongoDB database.
    Args:
        db: MongoDB database object
        collection (str): Name of the collection to retrieve
    Returns:
        Collection: MongoDB collection object if it exists, None otherwise
    """
    try:
        # Check if collection exists
        available_collections = db.list_collection_names()
        if collection in available_collections:
            print(f"✓ Collection '{collection}' found.")
            return db.get_collection(collection)
        else:
            print(f"✗ Collection '{collection}' not found.")
            print(f"Available collections: {available_collections}")
            return None
    except Exception as e:
        print(f"✗ Error retrieving collection: {e}")
        return None
