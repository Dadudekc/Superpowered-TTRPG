import os
import json
from character import create_character, Character, character_to_dict, dict_to_character
from combat import Combat, Combatant
from dm_interface import interactive_story_session
from game_data_loader import get_locations, get_organizations, get_npcs, get_arcs, update_json

SAVE_DIR = "saves"

class GameEngine:
    def __init__(self, dm_option: str = 'mistral'):
        """Initializes the game engine with dynamic JSON-loaded data."""
        self.player_character = None
        self.npcs = get_npcs()
        self.locations = get_locations()
        self.organizations = get_organizations()
        self.arcs = get_arcs()
        self.dm_option = dm_option  # AI model being used (e.g., Mistral, DeepSeek)
        self.story_state = {"arc": None, "events_completed": []}  # Tracks structured progression

    def start_game(self):
        """Starts a new game and initializes character creation or loads an existing save."""
        existing_saves = self.list_saved_games()
        if existing_saves:
            print("\n💾 **Existing save files found. Load a saved game?**")
            load_choice = input("Enter (Y) to load, or (N) to create a new character: ").strip().lower()
            if load_choice == 'y':
                self.load_game(existing_saves[0])  # Load first available save by default
                return

        print("\n🎭 **Creating a New Character...**")
        self.player_character = create_character()
        self.story_state["arc"] = 1  # Default starting arc
        self.intro_scene()
        self.auto_save_game()  # Save immediately after character creation

    def intro_scene(self):
        """Ensures AI follows the structured introduction of the game."""
        prompt = (
            f"Setting up the introduction for {self.player_character.name}, a new metahuman in Paragon City.\n"
            f"Keep responses within the pre-defined story arc:\n"
            f"Arc 1: 'The Awakening' – A mysterious power surge grants metahuman abilities.\n"
            f"Describe the character awakening in the city and their first impressions."
        )
        interactive_story_session(prompt, self.dm_option)

    def enter_location(self, location_name: str):
        """Generates AI-driven scene descriptions for known locations."""
        location = next((loc for loc in self.locations if loc["name"].lower() == location_name.lower()), None)
        if not location:
            print("❌ Location not found.")
            return

        prompt = (
            f"Describe {self.player_character.name} arriving at {location['name']}.\n"
            f"Do NOT introduce new NPCs or factions. Keep the scene within:\n"
            f"🌍 **Location Description:** {location['description']}\n"
            f"🎭 **Existing NPCs:** {', '.join(npc['name'] for npc in self.npcs if location['name'] in npc.get('known_locations', []))}"
        )
        interactive_story_session(prompt, self.dm_option)

    def trigger_arc_events(self, arc_number: int):
        """Triggers structured events for a given arc."""
        arc_data = next((arc for arc in self.arcs if arc["id"] == arc_number), None)
        if not arc_data:
            print("❌ Error: Arc data not found.")
            return

        self.story_state["arc"] = arc_number
        update_json("game_state.json", "arc", arc_number, {"events_completed": []})  # Reset completed events

        prompt = (
            f"📖 **Arc {arc_number}: '{arc_data['name']}'**\n"
            f"Stay within the pre-defined plotline:\n"
            f"📝 **Storyline:** {arc_data['description']}\n"
            f"🔹 **Key Events:** {', '.join(arc_data['key_events'])}\n"
            f"🎭 Describe how {self.player_character.name} gets involved in the first event."
        )
        interactive_story_session(prompt, self.dm_option)

    def save_game(self, filename="savegame.json"):
        """Saves game state into a structured JSON file."""
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        if not self.player_character:
            print("❌ Error: No player character to save.")
            return

        save_data = {
            "player_character": character_to_dict(self.player_character),
            "story_state": self.story_state
        }

        filepath = os.path.join(SAVE_DIR, filename)
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=4)

        print(f"💾 Game saved successfully as {filename}.")

    def auto_save_game(self):
        """Automatically saves the game progress without user input."""
        self.save_game("autosave.json")

    def load_game(self, filename="savegame.json"):
        """Loads game progress from a saved file."""
        filepath = os.path.join(SAVE_DIR, filename)
        if not os.path.exists(filepath):
            print("❌ No save file found.")
            return

        with open(filepath, 'r') as f:
            data = json.load(f)

        if "player_character" not in data:
            print(f"❌ Error: Save file {filename} is missing player character data. Starting new game instead.")
            self.start_game()
            return

        self.player_character = dict_to_character(data["player_character"])
        self.story_state = data.get("story_state", {"arc": None, "events_completed": []})
        print(f"✅ Game loaded successfully from {filename}.")

    def list_saved_games(self):
        """Returns a list of available save files."""
        if not os.path.exists(SAVE_DIR):
            return []
        return [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]

    def list_available_arcs(self):
        """Returns a list of available arcs."""
        return [f"{arc['id']}: {arc['name']} - {arc['description']}" for arc in self.arcs]

    def start_campaign_arc(self, arc_number: int):
        """Loads and starts a structured campaign arc with AI-driven storytelling."""
        arc_data = next((arc for arc in self.arcs if arc["id"] == arc_number), None)
        if not arc_data:
            print(f"❌ Invalid arc number. Available arcs: {self.list_available_arcs()}")
            return

        self.story_state["arc"] = arc_number
        self.story_state["events_completed"] = []

        relevant_npcs = [npc["name"] for npc in self.npcs if "relevant_arc" in npc and arc_number in npc["relevant_arc"]]
        relevant_locations = [loc["name"] for loc in self.locations if "arc_restricted" in loc and arc_number in loc["arc_restricted"]]

        prompt = (
            f"📖 **Begin Arc {arc_number}: '{arc_data['name']}'**\n"
            f"🔹 **Storyline:** {arc_data['description']}\n"
            f"🎭 **NPCs:** {', '.join(relevant_npcs) if relevant_npcs else 'None'}\n"
            f"🌍 **Locations:** {', '.join(relevant_locations) if relevant_locations else 'None'}\n"
            f"Describe how {self.player_character.name} enters this arc while staying within known lore."
        )
        interactive_story_session(prompt, self.dm_option)
