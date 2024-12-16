# character.py
from dataclasses import dataclass, field
from typing import List, Optional
import random

@dataclass
class Character:
    name: str
    attributes: dict
    skills: List[str]
    powers: List['Power']
    origin: str
    motivation: str
    flaw: str
    hp: int
    temp_hp: int = 0
    level: int = 1
    proficiency_bonus: int = 2

    def __post_init__(self):
        self.calculate_hp()

    def calculate_hp(self):
        # Example: Base HP could be 10 + CON modifier
        self.hp = 10 + self.attributes['CON']

@dataclass
class Power:
    name: str
    cost: int
    description: str
    activation_type: str  # Action, Bonus Action, Reaction, Passive
    effect: Optional[dict] = field(default_factory=dict)

# Example function to create a character
def create_character():
    print("Welcome to Superpowered TTRPG Character Creation!")
    name = input("Enter your character's name: ")

    # Initialize attributes
    attributes = {
        'STR': 8,
        'DEX': 8,
        'CON': 8,
        'INT': 8,
        'WIS': 8,
        'CHA': 8
    }

    points = 27
    print("\nAssign 27 points to the following attributes:")
    for attr in attributes:
        print(f"{attr}: {attributes[attr]}")

    # Implement point-buy system
    while points > 0:
        print(f"\nPoints remaining: {points}")
        attr = input("Choose an attribute to increase (STR, DEX, CON, INT, WIS, CHA): ").upper()
        if attr not in attributes:
            print("Invalid attribute. Try again.")
            continue
        # Define the cost structure
        costs = {9:1, 10:2, 11:3, 12:4,13:5,14:7,15:9}
        current = attributes[attr]
        if current >= 15:
            print(f"{attr} is already at maximum (15).")
            continue
        new_value = current + 1
        if new_value > 15:
            print("Cannot exceed 15.")
            continue
        cost = costs.get(new_value, 9)
        if points < cost:
            print(f"Not enough points to increase {attr} to {new_value}.")
            continue
        attributes[attr] = new_value
        points -= cost
        print(f"{attr} increased to {new_value}.")

    # Attribute Bonuses
    print("\nChoose a +2 bonus to an attribute.")
    bonus_attr1 = choose_attribute(attributes)
    attributes[bonus_attr1] += 2

    print("Choose a +1 bonus to another attribute.")
    bonus_attr2 = choose_attribute(attributes, exclude=bonus_attr1)
    attributes[bonus_attr2] += 1

    # Select origin, motivation, flaw
    origin = select_origin()
    motivation = select_option("motivation", [
        "Justice", "Redemption", "Vengeance", "Fame", "Power", "Protect loved ones", "Survival"
    ])
    flaw = select_option("flaw", [
        "Recklessness", "Distrust of authority", "Addiction to power", "Guilt over past actions",
        "Compulsion to prove worth", "Quick to anger", "Weak ties to humanity"
    ])

    # Initialize skills and powers (simplified)
    skills = select_skills(attributes)
    powers = select_powers()

    # Create character instance
    character = Character(
        name=name,
        attributes=attributes,
        skills=skills,
        powers=powers,
        origin=origin,
        motivation=motivation,
        flaw=flaw,
        hp=0  # Will be set in __post_init__
    )

    print(f"\nCharacter {name} created successfully!")
    return character

def choose_attribute(attributes, exclude=None):
    while True:
        attr = input("Choose an attribute (STR, DEX, CON, INT, WIS, CHA): ").upper()
        if attr not in attributes:
            print("Invalid attribute.")
            continue
        if exclude and attr == exclude:
            print(f"{attr} already has a bonus.")
            continue
        return attr

def select_option(option_type, options):
    print(f"\nChoose a {option_type}:")
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    while True:
        choice = input(f"Enter the number of your chosen {option_type}: ")
        if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
            print("Invalid choice.")
            continue
        return options[int(choice)-1]

def select_origin():
    origins = [
        "Mutant", "Experiment", "Cosmic Entity", "Magic Wielder",
        "Tech Augmented", "Alien Hybrid", "Accidental Hero"
    ]
    return select_option("origin", origins)

def select_skills(attributes):
    # Simplified: Assign proficiency based on attributes
    skills = []
    # Example: Add one skill per primary attribute
    # Implement detailed skill selection as needed
    return skills

def select_powers():
    # Simplified: Assign default powers or allow selection
    return []
