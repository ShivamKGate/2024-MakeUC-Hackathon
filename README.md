# Cleanify 

**Cleanify** is an educational Python game focused on environmental awareness. Players collect trash at different POVs, leveling up to unlock real-world environmental facts. The game encourages learning & educates users about pollution and conservation through gameplay.

## Features
- **Account Management**: Create Account, Log In, and Track Progress.
- **Exploration**: Navigate a virtual POVs and collect trash items that spawn at random locations.
- **Storage and Scoring Mechanic**: Collect as much trash as your storage allows, deposit it in the central trash bin to free up storage, and continue collecting.
- **Leveling System**: Level up as you collect more trash and complete quests, which increases your storage capacity and challenges.
- **Environmental Facts**: Unlock real-world environmental facts based on your score. Higher levels reveal more impactful facts, educating players on the effects of pollution and conservation efforts.
- **Session History**: View previous sessions, unlocked facts, and your cumulative impact on environmental conservation.

## Game Flow
1. **Account Creation**: Register to start at Level 1.
2. **Gameplay**: Collect trash on the beach, deposit it to clear storage, and gain points.
3. **Level Progression**: Unlock harder challenges and impactful facts with each level.
4. **Session Summary**: View total trash collected, score, and new facts at the end of each game.


## Installation

1. **Clone the Repo**:
   git clone https://github.com/ShivamKGate/2024-MakeUC-Hackathon
2. **Install Dependencies**:
    python -m pip install -r requirements.txt
3. **Create a .env file**:
    create a .env file, and add ```MONGO_PASSWORD=2024-MakeUC-Hackathon```
3. **Run the Game**:
    python main.py

## Tech Stack
- **Python**: Main programming language
- **MongoDB**: Database for user data and game sessions
- **Pygame**: For graphical interface
- **pymongo**: MongoDB connection
- **bcrypt**: Password hashing for security

## Future Enhancements
- **Expanded Maps**: Add different ecosystems.
- **Leaderboard**: Track top scores for competitive play.