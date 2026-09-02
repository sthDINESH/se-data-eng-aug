import requests
from mongo_db_driver import get_db, get_collection


def get_json(endpoint):
    try:
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()  # Raise exception for bad status
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    exit(1)


def get_pilot_name(endpoint):
    pilot_json = get_json(endpoint)
    return pilot_json['name']


# get starships data
# -------------------------------------------------------
STARSHIPS_ENDPOINT = 'https://swapi.info/api/starships'
starships = get_json(STARSHIPS_ENDPOINT)

# get pilot ids from mongodb and transform starships by
# adding ObjectIDs for pilots
# -------------------------------------------------------
MONGODB_URI = 'mongodb://localhost:27017/'
# Connect to starwars database
starwars = get_db(MONGODB_URI, "starwars")

# Get characters collection from starwars database
characters = get_collection(starwars, "characters")


for starship in starships:
    pilot_ids = []
    for endpoint in starship['pilots']:
        pilot_name = get_pilot_name(endpoint)
        pilot_obj_id = characters.find_one(
            filter={
                'name': pilot_name
            },
            projection={
                '_id': True
            }
        )['_id']
        pilot_ids.append(pilot_obj_id)

    # Replace pilots list with ObjectIDs
    starship['pilots'] = pilot_ids
    print('Updated starship pilots:', starship['name'], starship['pilots'])

# add transformed data to mongo database
# -------------------------------------------------------

if "starships" not in starwars.list_collection_names():
    # Create starships collection
    starwars.create_collection("starships")
    print("✓ Created 'starships' collection")

    # Insert all starships with pilot ObjectID references
    starships_collection = get_collection(starwars, "starships")
    result = starships_collection.insert_many(starships)
    print(f"✓ Inserted {len(result.inserted_ids)} starships into MongoDB")
else:
    print("✗ Starships Collection already exists")
