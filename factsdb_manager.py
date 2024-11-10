import json
import random
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# Retrieve the password from the environment variable
mongo_password = os.getenv("MONGO_PASSWORD")

# MongoDB setup
uri = f"mongodb+srv://Nandini:{mongo_password}@2024-makeuc-hackathon.r3ow1.mongodb.net/?retryWrites=true&w=majority&appName=2024-MakeUC-Hackathon"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["2024MakeUCHackathonDB"]
facts_collection = db["2024MakeUCHackathonFacts"]

def fetch_level_facts():
    """
    Fetches the level_facts dictionary from the MongoDB collection.
    Assumes the dictionary is stored as a single document with a 'level_facts' key.
    
    :return: Dictionary containing level facts, or None if not found.
    """
    facts_document = facts_collection.find_one({}, {"_id": 0})
    if facts_document and "level_facts" in facts_document:
        return facts_document["level_facts"]
    return None

def get_random_facts_by_level(level):
    """
    Fetches 3 random facts from the specified level in the level_facts dictionary.

    :param level: Integer representing the level (1-10).
    :return: List of 3 random facts for the specified level or an empty list if level not found.
    """
    level_facts = fetch_level_facts()
    if not level_facts or str(level) not in level_facts:
        print(f"No facts found for level {level}.")
        return []

    # Get the list of facts for the specified level and select 3 random facts
    facts_list = level_facts[str(level)]
    return random.sample(facts_list, 3) if len(facts_list) >= 3 else facts_list