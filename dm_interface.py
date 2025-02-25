import subprocess
import openai  # If using OpenAI's API
import os
import logging

# Ensure the logs directory exists
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Set up logging for DM interactions
LOG_FILE = os.path.join(LOG_DIR, "dm_interface.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

# DM Configuration Settings
DM_CONFIG = {
    "tone": "epic",        # Options: epic, humorous, serious, etc.
    "randomness": 0.7,     # Temperature for DM responses.
    "log_file": LOG_FILE,
    "max_tokens": 500,     # Limit AI response length
}

def preprocess_prompt(prompt: str) -> str:
    """
    Injects structured guidance to keep AI responses within the game’s storyline.
    """
    tone = DM_CONFIG.get("tone", "neutral")
    structured_guidance = (
        "IMPORTANT: You are the Dungeon Master in a structured TTRPG setting. "
        "Stay within the pre-defined plotlines, avoid adding unauthorized factions, and ensure all "
        "descriptions fit the established lore. "
        "Follow a classic TTRPG format: Provide descriptions, ask the player for actions, and react accordingly."
    )
    return f"{structured_guidance}\n[Tone: {tone}] {prompt}"

def send_prompt_to_dm(prompt: str, dm_option: str = 'mistral') -> str:
    """
    Sends a prompt to the chosen AI backend and returns the response.
    
    Parameters:
    - prompt (str): The prompt to send to the DM.
    - dm_option (str): 'openai', 'mistral', or 'deepseek' to choose the backend.
    
    Returns:
    - response (str): The AI-generated DM response.
    """
    processed_prompt = preprocess_prompt(prompt)
    logging.info(f"🔹 Sending prompt to DM ({dm_option}): {processed_prompt}")

    # Ensure a valid DM option is selected
    if dm_option not in ["openai", "mistral", "deepseek"]:
        logging.error(f"Invalid DM option selected: {dm_option}")
        return "Invalid DM option selected. Please restart and choose a valid AI model."

    # Route the request to the selected AI model
    if dm_option == "openai":
        response = send_prompt_to_openai(processed_prompt)
    elif dm_option == "mistral":
        response = send_prompt_to_mistral(processed_prompt)
    elif dm_option == "deepseek":
        response = send_prompt_to_deepseek(processed_prompt)

    logging.info(f"📝 DM Response: {response}")
    return response

def send_prompt_to_openai(prompt: str) -> str:
    """
    Sends a prompt to OpenAI's ChatGPT API.
    """
    openai.api_key = os.getenv('OPENAI_API_KEY')
    try:
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=DM_CONFIG.get("max_tokens", 500),
            n=1,
            stop=None,
            temperature=DM_CONFIG.get("randomness", 0.7),
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"⚠️ Error communicating with OpenAI: {e}")
        return "An error occurred while communicating with the OpenAI DM."

def send_prompt_to_mistral(prompt: str, model_name="mistral:latest") -> str:
    """
    Sends a prompt to Mistral running locally via Ollama Run and returns the response.
    """
    try:
        logging.info(f"Running: ollama run {model_name} \"{prompt}\"")
        
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",  # ✅ Fixes UnicodeDecodeError
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error communicating with Mistral via Ollama Run: {e}, Output: {e.output}")
        print("Error communicating with Mistral via Ollama Run:", e)
        print("Output:", e.output)
        return "An error occurred while communicating with the local AI."

def send_prompt_to_deepseek(prompt: str) -> str:
    """
    Sends a prompt to DeepSeek Chat running locally via Ollama.
    """
    try:
        model_name = "deepseek-r1:latest"
        logging.info(f"🔹 Running: ollama run {model_name} \"{prompt}\"")

        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"⚠️ Error communicating with DeepSeek: {e}, Output: {e.output}")
        return "An error occurred while communicating with the local DeepSeek DM."

# ✅ **NEW: Interactive Story Session**
def interactive_story_session(initial_prompt: str, dm_option="mistral"):
    """
    Allows back-and-forth interaction between the user and the DM to progress through the story.
    
    Parameters:
    - initial_prompt (str): The opening narrative provided by the DM.
    - dm_option (str): The selected AI backend for responses.
    """
    print("\n🎭 **Starting Interactive Story Session...** 🎭")
    print("Type 'exit' anytime to end the session.")

    response = send_prompt_to_dm(initial_prompt, dm_option)
    print(f"\n📝 [DM]: {response}")

    while True:
        player_input = input("\n🎮 Your action: ").strip()

        if player_input.lower() == "exit":
            print("\n🚪 **Exiting interactive session...**")
            break

        # Continue the story based on player actions
        new_prompt = f"Player chose: {player_input}\n\nContinue the story based on their action."
        response = send_prompt_to_dm(new_prompt, dm_option)
        print(f"\n📝 [DM]: {response}")

# ✅ Testing Script
if __name__ == "__main__":
    print("\n🛠 **Testing DM Interface...**")
    test_prompt = "Describe a mysterious portal opening in the sky above Paragon City."
    dm_backend = os.getenv("DM_BACKEND", "mistral")  # Default to Mistral
    response = send_prompt_to_dm(test_prompt, dm_option=dm_backend)
    print(f"\n🎭 **DM Response:** {response}")

    # Optional: Start interactive session
    interactive_story_session("A strange energy surge is detected in the city square. What does the player do?", dm_backend)
