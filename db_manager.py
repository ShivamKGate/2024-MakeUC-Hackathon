# db_manager.py
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