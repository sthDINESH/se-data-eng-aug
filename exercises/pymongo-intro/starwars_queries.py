from mongo_db_driver import get_db, get_collection

URI = 'mongodb://localhost:27017/'

# Connect to starwars database
starwars = get_db(URI, "starwars")

# Get characters collection from starwars database
if starwars is not None:
    characters = get_collection(starwars, "characters")
else:
    exit(1)

# Queries
# Find Darth Vader's height
result = characters.find_one(
    filter={'name': 'Darth Vader'},
    projection={'name': True, 'height': True, '_id': False}
)
print('Find Darth Vader\'s height:', result)

# Find all the characters with yellow eyes
result = list(characters.find(
    filter={'eye_color': 'yellow'},
    projection={'name': True, 'eye_color': True, '_id': False}
))
print('Characters with yellow eyes:')
for character in result:
    print(character)

# Find all male characters, limit the output to 3
result = characters.find(
    filter={'gender': 'male'},
    projection={'name': True, 'gender': True, '_id': False},
    limit=3
)
print('Male characters(limited to 3):')
for character in result:
    print(character)

# Find the names of all humans with a homeworld of "Alderaan"
result = characters.find(
    filter={'species.name': 'Human', 'homeworld.name':'Alderaan'},
    projection={
            'name': True,
            'species.name': True,
            'homeworld.name': True,
            '_id': False
    }
)
print('Humans with homeworld of Alderaan:')
for character in result:
    print(character)

# Find the average height of all female characters
pipeline = [
    {
        '$match': {
            'gender': 'female',
            'height': {'$type': 'int'}
        }
    },
    {
        '$group': {
            '_id': None,
            'average_height': {'$avg': '$height'}
        }
    }
]
result = list(characters.aggregate(pipeline))
print('Average height of all female characters:')
for entry in result:
    print(entry)


# 7. Find the tallest character
pipeline = [
    {
        '$match': {
            'height': {'$type': 'int'}
        }
    },
    {
        '$sort': {'height': -1}
    },
    {
        '$project': {
            '_id': False,
            'name': True,
            'height': True,
        }
    },
    {
        '$limit': 1
    }
]
result = list(characters.aggregate(pipeline))
print('Tallest character:')
for entry in result:
    print(entry)
