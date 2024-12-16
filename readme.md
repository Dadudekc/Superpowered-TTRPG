1. Project Overview
Objectives:
Develop a Python-based TTRPG that incorporates character creation, combat mechanics, power selection, and storytelling elements.
Use Ollama Run to facilitate the execution and management of the game.
Integrate ChatGPT (OpenAI) and Mistral 7B (local via Ollama Run) as the DM, allowing users to choose their preferred backend.
Key Components:
Character Creation Module
Game Mechanics Engine
Combat System
World and Story Management
NPC and Faction Handling
Integration with Ollama Run and ChatGPT/Mistral 7B

2. Setting Up Your Development Environment
Prerequisites:
Python 3.8+
Ollama Run Installation: Ensure Ollama is installed and properly configured on your system. Ollama Documentation
Mistral 7B Model: Ensure you have the Mistral 7B model downloaded and available locally via Ollama Run.
OpenAI API Access: If you plan to use OpenAI's API for ChatGPT, ensure you have the necessary API keys.
Libraries:
dataclasses for structured data
random for dice rolls and randomness
json for saving/loading game states
cmd or cmd2 for building a command-line interface (CLI)
rich for enhanced terminal output (optional)
subprocess for interacting with Ollama Run
requests for API calls (if using OpenAI)
Setting Up the Environment:
bash
Copy code
# Create a virtual environment
python -m venv ttrpg_env
source ttrpg_env/bin/activate  # On Windows: ttrpg_env\Scripts\activate

# Install necessary libraries
pip install rich cmd2 requests

3. Architectural Design
Modules Breakdown:
character.py: Handles character creation, attributes, skills, powers, origins, motivations, and flaws.
combat.py: Manages combat mechanics, initiative, turns, actions, and reactions.
world.py: Contains information about settings, locations, organizations, and NPCs.
game_engine.py: Coordinates the overall game flow, integrating other modules.
dm_interface.py: Facilitates interaction with ChatGPT (OpenAI) or Mistral 7B (local via Ollama Run) as the DM.
main.py: Entry point for the game, handling user inputs and starting the game loop.
Data Structures:
Classes: Use Python classes to represent characters, NPCs, powers, and other entities.
Dataclasses: Utilize @dataclass for cleaner and more manageable code.

5. Integrating Ollama Run and ChatGPT/Mistral 7B as the DM
Understanding DM Options:
OpenAI ChatGPT:

Utilizes the OpenAI API to communicate with ChatGPT models.
Requires an API key and internet connectivity.
Mistral 7B (Local via Ollama Run):

Runs locally on your machine using Ollama Run.
Does not require internet connectivity once set up.
Leverages your local Mistral 7B model.
Setting Up Ollama Run with Mistral 7B:
Install Ollama: Follow the Ollama installation guide.

Download and Configure Mistral 7B:

Ensure the Mistral 7B model is available and properly set up in Ollama.
Verify by running a test prompt:
bash
Copy code
ollama run mistral-7b "Hello, DM! Describe the scene."
If the above command returns a coherent response, the setup is correct.
Adjust the dm_interface.py:

Ensure the model name in the subprocess command matches your Ollama model configuration (e.g., mistral-7b).
Configuring OpenAI ChatGPT:
Obtain an OpenAI API Key:

Sign up or log in to OpenAI and navigate to the API section to obtain your API key.
Set the API Key as an Environment Variable:

For security, it's best to set your API key as an environment variable rather than hardcoding it.
On Unix/Linux/macOS:
bash
Copy code
export OPENAI_API_KEY='your-api-key-here'
On Windows:
cmd
Copy code
set OPENAI_API_KEY=your-api-key-here
Alternatively, you can use a .env file with libraries like python-dotenv to manage environment variables.

