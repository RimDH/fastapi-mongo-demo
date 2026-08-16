from pymongo import AsyncMongoClient

from app.core.config import settings

#This layer is responsible for our database connection.
#Creates the MongoDB client:
client = AsyncMongoClient(
    settings.mongodb_url
)
# This gives us access to the database and collections:
database = client[
    settings.database_name
]

users_collection = database["users"]

products_collection = database["products"]