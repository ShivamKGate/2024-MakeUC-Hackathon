import bcrypt
import random
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from factsdb_manager import get_random_facts_by_level
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
        "currentCurrency": 0,  # Initialize with 0 currency
        "previousGames": {},
        "Achievements": []
    }
    login_data_collection.insert_one(new_user)

def login_user(email, password):
    user = login_data_collection.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode(), user["password"]):
        return user  # Return user data for session
    return None

def save_last_game(player_name, level, score, trash_collected, facts):
    """
    Adds the latest game data to the user's profile in the 'previousGames' array.
    Only keeps the latest game.
    """
    game_data = {
        "level": level,
        "score": score,
        "trash_collected": trash_collected,
        "facts_learned": facts
    }
    login_data_collection.update_one(
        {"playerName": player_name},
        {"$set": {"previousGames": game_data}}
    )

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

def update_currency(player_name, amount):
    login_data_collection.update_one(
        {"playerName": player_name},
        {"$inc": {"currentCurrency": amount}}
    )

def get_currency(player_name):
    user = login_data_collection.find_one({"playerName": player_name})
    return user.get("currentCurrency", 0) if user else 0

def purchase_item(player_name, item_cost):
    user = login_data_collection.find_one({"playerName": player_name})
    if user and user.get("currentCurrency", 0) >= item_cost:
        update_currency(player_name, -item_cost)
        return True  # Purchase successf

def fetch_user_data(username):
    """
    Fetch complete user data from the database by username (playerName).
    Saves the data to currentUser.json and returns it.
    
    :param username: The user's playerName.
    :return: The user document or None if not found.
    """
    user = login_data_collection.find_one({"playerName": username})
    
    if user:
        # Remove MongoDB's default ObjectId to make it JSON-serializable
        user["_id"] = str(user["_id"])
        user.pop("password", None)  # Remove the "password" field, if it exists
        
        # Save user data to currentUser.json
        with open("currentUser.json", "w") as file:
            json.dump(user, file, indent=4)
        
        return user  # Return the user data as a dictionary
    
    return None  # Return None if user not found

def get_all_achievements(player_name):
    """
    Retrieve all achievements (facts) for the user by player name.
    :param player_name: The player's name in the database.
    :return: Dictionary of achievements or an empty dictionary if none found.
    """
    user = login_data_collection.find_one({"playerName": player_name})
    return user.get("achievements", {}) if user else {}

def add_achievements(player_name, level, facts):
    """
    Add new facts to the user's achievements for a specific level.
    :param player_name: The player's name in the database.
    :param level: Level number (key in the achievements dictionary).
    :param facts: List of facts to add to the achievements.
    """
    try:
        # Use MongoDB's $addToSet to avoid duplicate facts in the array
        login_data_collection.update_one(
            {"playerName": player_name},
            {"$addToSet": {f"achievements.{level}": {"$each": facts}}}
        )
        print(f"Successfully added achievements for level {level}")
    except Exception as e:
        print(f"Error updating achievements: {e}")

def generate_and_save_facts(player_name, num_facts):
    """
    Generate random environmental facts for a random level and save them as achievements.
    
    :param player_name: The name of the player
    :param num_facts: The number of facts to generate
    :return: A list of facts generated for this purchase
    """
    # Generate a random level between 1 and 10
    random_level = random.randint(1, 10)
    
    # Get the specified number of random facts for that level
    random_facts = get_random_facts_by_level(random_level)[:num_facts]
    
    # Save the facts as achievements in the database
    add_achievements(player_name, random_level, random_facts)
    
    return random_facts

def get_previous_game(player_name):
    """
    Fetches the last game stats for the specified player.
    :param player_name: The player's name.
    :return: Dictionary containing the last game details or None if not found.
    """
    user = login_data_collection.find_one({"playerName": player_name})
    if user and "previousGames" in user and user["previousGames"]:
        # Return the most recent game from the previousGames array
        return user["previousGames"]
    return None