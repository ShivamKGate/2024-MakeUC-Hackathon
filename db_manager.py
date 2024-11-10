import bcrypt
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
login_data_collection = db["2024MakeUCHackathon"]

def create_user(email, password, player_name):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    new_user = {
        "email": email,
        "password": hashed_password,
        "playerName": player_name,
        "currentLevel": 1,
        "highestScore": 0,
        "previousGames": [],
        "Achievements": []
    }
    login_data_collection.insert_one(new_user)

def login_user(email, password):
    user = login_data_collection.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode(), user["password"]):
        return user  # Return user data for session
    return None

def save_game_session(email, score, trash_collected, level):
    session_data = {
        "score": score,
        "trashCollected": trash_collected,
        "level": level
    }
    login_data_collection.update_one({"email": email}, {"$push": {"previousGames": session_data}})

# New function to fetch user data by email or player name
def fetch_user(identifier):
    """
    Fetch user data from the database by email or playerName.
    :param identifier: The user's email or playerName to fetch data.
    :return: The user document or None if not found.
    """
    query = {"$or": [{"email": identifier}, {"playerName": identifier}]}
    user = login_data_collection.find_one(query)
    return user

def get_current_level(username):
    """Fetch the current level of the user."""
    user = login_data_collection.find_one({"playerName": username})
    if user:
        return user.get("currentLevel", 1)
    return 1  # Default level if not found

def update_current_level(player_name, new_level):
    try:
        result = login_data_collection.update_one({"playerName": player_name}, {"$set": {"currentLevel": new_level}})
        return result.modified_count > 0  # Returns True if the update was successful
    except Exception as e:
        print(f"Failed to update level: {e}")
        return False
