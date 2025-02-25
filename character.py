from dataclasses import dataclass, field
from typing import List, Optional
import random
import json

# --- Data Classes ---
@dataclass
class Power:
    name: str
    cost: int
    description: str
    activation_type: str  # Action, Bonus Action, Reaction, Passive
    effect: Optional[dict] = field(default_factory=dict)

@dataclass
class Character:
    name: str
    codename: str
    attributes: dict
    skills: List[str]
    powers: List[Power]
    origin: str
    motivation: str
    flaw: str
    hp: int
    temp_hp: int = 0
    level: int = 1
    proficiency_bonus: int = 2
    backstory: str = ""

    def __post_init__(self):
        self.calculate_hp()
        self.generate_backstory()

    def calculate_hp(self):
        """Calculate HP based on Constitution. Starting HP is 12 + CON modifier."""
        self.hp = 12 + self.attributes.get('CON', 0)

    def generate_backstory(self):
        """Generates a dynamic backstory based on character choices."""
        self.backstory = (
            f"{self.name}, known as {self.codename}, grew up as {self.origin.lower()} who was shaped "
            f"by their motivation for {self.motivation.lower()}. Throughout their life, they struggled with "
            f"{self.flaw.lower()}, which often tested their resolve. Now, they harness their abilities to carve a path "
            f"toward their destiny, wielding powers such as {', '.join([power.name for power in self.powers])}. "
            f"With skills in {', '.join(self.skills)}, they are prepared for the battles ahead."
        )

# --- Utility Functions for Point-Buy and Conversions ---
def calculate_cost(old: int, new: int) -> int:
    """
    Calculate the cost to raise an attribute from old to new value using a D&D 5e–inspired point-buy system.
    Scores 8 to 13 cost 1 point per increase; 14 and 15 cost 2 points per increase.
    """
    point_cost = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
    if new not in point_cost or old not in point_cost:
        raise ValueError("Attributes must be between 8 and 15.")
    return point_cost[new] - point_cost[old]

def character_to_dict(character: Character) -> dict:
    """Converts a Character object into a serializable dictionary."""
    return {
        'name': character.name,
        'codename': character.codename,
        'attributes': character.attributes,
        'skills': character.skills,
        'powers': [power.__dict__ for power in character.powers],
        'origin': character.origin,
        'motivation': character.motivation,
        'flaw': character.flaw,
        'hp': character.hp,
        'temp_hp': character.temp_hp,
        'level': character.level,
        'proficiency_bonus': character.proficiency_bonus,
        'backstory': character.backstory,
    }

def dict_to_character(data: dict) -> Character:
    """Recreates a Character object from a dictionary."""
    powers = [Power(**p) for p in data.get('powers', [])]
    return Character(
        name=data['name'],
        codename=data['codename'],
        attributes=data['attributes'],
        skills=data['skills'],
        powers=powers,
        origin=data['origin'],
        motivation=data['motivation'],
        flaw=data['flaw'],
        hp=data['hp'],
        temp_hp=data.get('temp_hp', 0),
        level=data.get('level', 1),
        proficiency_bonus=data.get('proficiency_bonus', 2),
        backstory=data.get('backstory', "")
    )

def save_character(character: Character, filename: str = "character_save.json"):
    """Saves the character to a JSON file."""
    with open(filename, "w") as f:
        json.dump(character_to_dict(character), f, indent=4)
    print(f"Character saved to {filename}.")

def load_character(filename: str = "character_save.json") -> Character:
    """Loads a character from a JSON file."""
    with open(filename, "r") as f:
        data = json.load(f)
    character = dict_to_character(data)
    print(f"Character loaded from {filename}.")
    return character

# --- Character Creation Process ---
def create_character() -> Character:
    print("\n=== Welcome to Superpowered TTRPG Character Creation! ===")

    name = input("Enter your character's name: ").strip()
    codename = input("Enter your hero codename: ").strip()

    attributes = assign_attributes()
    skills = choose_skills()
    origin = select_from_list("Origin", ORIGINS)
    motivation = select_from_list("Motivation", MOTIVATIONS)
    flaw = select_from_list("Flaw", FLAWS)
    powers = choose_powers()

    character = Character(
        name=name,
        codename=codename,
        attributes=attributes,
        skills=skills,
        powers=powers,
        origin=origin,
        motivation=motivation,
        flaw=flaw,
        hp=0  # Will be set in __post_init__
    )

    print("\n=== Character Created Successfully! ===")
    print(f"Name: {character.name} | Codename: {character.codename}")
    print(f"Origin: {character.origin}")
    print(f"Motivation: {character.motivation}")
    print(f"Flaw: {character.flaw}")
    print(f"Skills: {', '.join(character.skills)}")
    print(f"Powers: {', '.join([power.name for power in character.powers])}")
    print("\nGenerated Backstory:")
    print(character.backstory)

    # Optionally, save the newly created character.
    save_choice = input("Would you like to save this character? (Y/N): ").strip().lower()
    if save_choice == "y":
        save_character(character)
    return character

# --- Supporting Functions ---
def assign_attributes() -> dict:
    attributes = {'STR': 8, 'DEX': 8, 'CON': 8, 'INT': 8, 'WIS': 8, 'CHA': 8}
    points = 27
    print("\nDistribute 27 points across STR, DEX, CON, INT, WIS, CHA (each must be between 8 and 15).")

    # For each attribute, loop until valid input is received.
    for attr in attributes:
        while True:
            try:
                value = int(input(f"{attr} (current: {attributes[attr]}): "))
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue

            if value < 8 or value > 15:
                print("Invalid input! Attributes must be between 8 and 15.")
                continue

            cost = calculate_cost(attributes[attr], value)
            if cost > points:
                print(f"Not enough points! You have {points} points remaining.")
                continue

            attributes[attr] = value
            points -= cost
            print(f"{attr} is now {value}. Points remaining: {points}")
            break

    # Apply bonus attributes.
    print("\nSelect a +2 and a +1 bonus to attributes.")
    bonus_attr1 = choose_attribute(attributes)
    attributes[bonus_attr1] += 2
    print(f"{bonus_attr1} receives a +2 bonus!")
    bonus_attr2 = choose_attribute(attributes, exclude=bonus_attr1)
    attributes[bonus_attr2] += 1
    print(f"{bonus_attr2} receives a +1 bonus!")
    return attributes

def choose_skills() -> List[str]:
    """User selects 4 skills from the available options using number-based selection."""
    print("\nChoose 4 skills from the list below:")
    for idx, skill in enumerate(SKILLS, 1):
        print(f"{idx}. {skill}")
    
    chosen_skills = []
    while len(chosen_skills) < 4:
        try:
            choice = int(input(f"Select skill {len(chosen_skills) + 1} (enter the number): ").strip())
        except ValueError:
            print("Invalid input! Please enter a number corresponding to the skill.")
            continue
        
        if choice < 1 or choice > len(SKILLS):
            print("Number out of range. Please try again.")
            continue
        
        selected_skill = SKILLS[choice - 1]
        if selected_skill in chosen_skills:
            print("You have already selected that skill. Please choose a different one.")
            continue
        
        chosen_skills.append(selected_skill)
        print(f"Added: {selected_skill}")
    
    return chosen_skills

def choose_powers() -> List[Power]:
    """User selects powers based on available power points (PP) using number-based selection."""
    available_points = 8
    chosen_powers = []
    print("\nYou have 8 Power Points (PP) to spend on powers.")
    
    while available_points > 0:
        print("\nAvailable Powers:")
        for idx, p in enumerate(POWERS, 1):
            print(f"{idx}. {p['name']} ({p['cost']} PP): {p['description']}")
        print("0. Done selecting powers")
        
        try:
            choice = int(input(f"Select a power by number (PP remaining: {available_points}): ").strip())
        except ValueError:
            print("Invalid input! Please enter a valid number.")
            continue
        
        if choice == 0:
            break
        
        if choice < 1 or choice > len(POWERS):
            print("Number out of range. Please try again.")
            continue
        
        power_data = POWERS[choice - 1]
        if power_data['cost'] > available_points:
            print(f"Not enough PP. You have {available_points} PP remaining. Choose a cheaper power.")
            continue
        
        chosen_powers.append(Power(**power_data))
        available_points -= power_data['cost']
        print(f"Added {power_data['name']}. PP remaining: {available_points}")
    
    return chosen_powers

def select_from_list(prompt: str, options: List[str]) -> str:
    """Display a numbered list of options and return the user's selection."""
    print(f"\nChoose a {prompt} from the list below:")
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    while True:
        try:
            choice = int(input(f"Enter the number of your chosen {prompt}: ").strip())
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue
        
        if 1 <= choice <= len(options):
            return options[choice - 1]
        else:
            print("Number out of range. Please try again.")

def select_option(option_type: str, options: List[str]) -> str:
    """Wrapper for select_from_list to maintain naming consistency."""
    return select_from_list(option_type, options)

def choose_attribute(attributes: dict, exclude: Optional[str] = None) -> str:
    """User selects an attribute for bonus; selection is via free text but with fixed options."""
    valid_attributes = list(attributes.keys())
    if exclude and exclude in valid_attributes:
        valid_attributes.remove(exclude)
    print("\nChoose one of the following attributes for a bonus:")
    for idx, attr in enumerate(valid_attributes, 1):
        print(f"{idx}. {attr}")
    while True:
        try:
            choice = int(input("Enter the number corresponding to your chosen attribute: ").strip())
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue
        
        if 1 <= choice <= len(valid_attributes):
            return valid_attributes[choice - 1]
        else:
            print("Number out of range. Please try again.")

# --- Constants ---
MOTIVATIONS = [
    "Justice", "Redemption", "Vengeance", "Fame", "Power", "Protect loved ones", "Survival",
    "Legacy", "Balance", "Freedom", "Knowledge", "Chaos", "Control", "Hope"
]

FLAWS = [
    "Recklessness", "Distrust of authority", "Addiction to power", "Guilt over past actions",
    "Compulsion to prove worth", "Quick to anger", "Weak ties to humanity", "Overconfidence",
    "Fear of failure", "Emotional detachment", "Unstable powers", "Ego-driven"
]

SKILLS = [
    "Athletics", "Acrobatics", "Stealth", "Sleight of Hand", "Endurance", "Investigation", "Arcana",
    "Technology", "History", "Perception", "Insight", "Medicine", "Survival", "Persuasion",
    "Deception", "Intimidation", "Performance", "Tactics", "Hacking", "Engineering",
    "Alchemy", "Forgery", "Tracking"
]

ORIGINS = [
    "Mutant", "Experiment", "Cosmic Entity", "Magic Wielder", "Tech Augmented", "Alien Hybrid",
    "Accidental Hero", "Chosen One", "Artificial Being", "Cybernetic Human", "Ancient Bloodline",
    "Summoned Entity", "Super Soldier", "Radiation Exposure", "Lost Heir of a Forgotten Realm"
]

POWERS = [
    {
        "name": "Super Strength",
        "cost": 4,
        "description": "Exhibit extraordinary physical strength, allowing you to lift massive objects and deal enhanced melee damage.",
        "activation_type": "Passive"
    },
    {
        "name": "Energy Blasts",
        "cost": 4,
        "description": "Fire a blast of energy at a target within 60 feet, choosing between fire, lightning, force, or radiant damage.",
        "activation_type": "Action"
    },
    {
        "name": "Teleportation",
        "cost": 5,
        "description": "Instantly teleport up to 60 feet to a location you can see.",
        "activation_type": "Bonus Action"
    },
    {
        "name": "Healing Factor",
        "cost": 4,
        "description": "Regenerate health passively and resist damage.",
        "activation_type": "Passive"
    },
    {
        "name": "Super Speed",
        "cost": 5,
        "description": "Increase movement speed drastically, enhancing combat effectiveness.",
        "activation_type": "Bonus Action"
    },
    {
        "name": "Time Manipulation",
        "cost": 6,
        "description": "Alter the flow of time, slowing down enemies or speeding up your own actions.",
        "activation_type": "Action"
    },
    {
        "name": "Invisibility",
        "cost": 5,
        "description": "Turn invisible for a short duration, evading enemies and avoiding detection.",
        "activation_type": "Bonus Action"
    },
    {
        "name": "Telekinesis",
        "cost": 6,
        "description": "Manipulate objects and enemies at a distance with the power of your mind.",
        "activation_type": "Action"
    },
    {
        "name": "Shapeshifting",
        "cost": 7,
        "description": "Alter your appearance or transform parts of your body into weapons or defensive forms.",
        "activation_type": "Action"
    },
    {
        "name": "Elemental Control",
        "cost": 6,
        "description": "Manipulate a chosen element (fire, water, air, or earth) to attack, defend, or reshape the environment.",
        "activation_type": "Action"
    }
]

# --- Main Execution ---
if __name__ == "__main__":
    choice = input("Enter (Y) to load an existing character, or (N) to create a new character: ").strip().lower()
    if choice == 'n':
        character = create_character()
    elif choice == 'y':
        try:
            character = load_character()
            print("\n=== Loaded Character ===")
            print(f"Name: {character.name} | Codename: {character.codename}")
            print(f"Origin: {character.origin}")
            print(f"Motivation: {character.motivation}")
            print(f"Flaw: {character.flaw}")
            print(f"Skills: {', '.join(character.skills)}")
            print(f"Powers: {', '.join([power.name for power in character.powers])}")
            print("\nBackstory:")
            print(character.backstory)
        except Exception as e:
            print(f"Error loading character: {e}")
            print("Falling back to character creation...")
            character = create_character()
    else:
        print("Invalid selection. Creating a new character by default.")
        character = create_character()
