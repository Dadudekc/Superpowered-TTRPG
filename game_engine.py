# game_engine.py
from character import create_character, Character
from combat import Combat, Combatant
from world import get_core_locations, get_organizations, get_npcs
from dm_interface import send_prompt_to_dm

from typing import List, Optional

class GameEngine:
    def __init__(self, dm_option: str = 'mistral'):
        self.player_character: Optional[Character] = None
        self.npcs = get_npcs()
        self.locations = get_core_locations()
        self.organizations = get_organizations()
        self.dm_option = dm_option  # 'openai' or 'mistral'

    def start_game(self):
        self.player_character = create_character()
        self.intro_scene()

    def intro_scene(self):
        prompt = (
            f"Introduce the setting for {self.player_character.name}, a superpowered individual in Paragon City."
        )
        response = send_prompt_to_dm(prompt, self.dm_option)
        print(f"\n[DM]: {response}")

    def enter_location(self, location_name: str):
        location = next((loc for loc in self.locations if loc.name.lower() == location_name.lower()), None)
        if not location:
            print("Location not found.")
            return
        prompt = f"Describe {self.player_character.name} entering {location.name}. {location.description}"
        response = send_prompt_to_dm(prompt, self.dm_option)
        print(f"\n[DM]: {response}")

    def initiate_combat(self, enemies: List[Character]):
        combatants = [Combatant(character=self.player_character, is_player=True)]
        for enemy in enemies:
            combatants.append(Combatant(character=enemy, is_player=False))
        combat = Combat(participants=combatants)
        combat.start_combat()

    def save_game(self, filename: str = "savegame.json"):
        import json
        with open(filename, 'w') as f:
            json.dump(self.player_character.__dict__, f, default=lambda o: o.__dict__, indent=4)
        print("Game saved successfully.")

    def load_game(self, filename: str = "savegame.json"):
        import json
        from character import Character, Power  # Ensure Power is imported
        with open(filename, 'r') as f:
            data = json.load(f)
        # Reconstruct Character object
        # Handle nested objects like Power if necessary
        # This example assumes powers are simple dictionaries
        powers = [Power(**power) for power in data.get('powers', [])]
        self.player_character = Character(
            name=data['name'],
            attributes=data['attributes'],
            skills=data['skills'],
            powers=powers,
            origin=data['origin'],
            motivation=data['motivation'],
            flaw=data['flaw'],
            hp=data['hp'],
            temp_hp=data.get('temp_hp', 0),
            level=data.get('level', 1),
            proficiency_bonus=data.get('proficiency_bonus', 2)
        )
        print("Game loaded successfully.")

    def start_campaign_arc(self, arc_number: int):
        arcs = {
            1: "Rise of Heroes: Players face minor villains (e.g., Gearhead, Lady Venom) and establish their presence in Paragon City.",
            2: "Shadows in the Row: Gang wars in Shadow Row escalate into a larger conspiracy involving the Crimson Court.",
            3: "Industrial Sabotage: Players uncover the Iron Syndicate’s weapons trade in Steel Haven, leading to battles against Iron Maw.",
            4: "Cosmic Threat: Void Monarch’s forces arrive, seeking Starlight Cradle’s secrets. Players must repel an alien invasion.",
            5: "Frozen Secrets: The Frostspire Tundra reveals an ancient artifact that could shift the balance of power. Villains race to claim it.",
            6: "Reality Unbound: Chromaflux destabilizes reality in Skyshard Archipelago, forcing players to battle in warped environments.",
            7: "The Vampire’s Gambit: Crimson King’s forces spread chaos worldwide, culminating in a showdown in Oldtown.",
            8: "Final Showdown: Oblivion Nexus’s master plan threatens the fabric of reality. Players must unite to stop the ultimate cosmic catastrophe."
        }
        if arc_number not in arcs:
            print("Invalid arc number.")
            return
        prompt = f"Start Arc {arc_number}: {arcs[arc_number]}"
        response = send_prompt_to_dm(prompt, self.dm_option)
        print(f"\n[DM]: {response}")
        # Trigger specific events based on the arc
