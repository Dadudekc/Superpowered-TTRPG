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

# function to create a character
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
    print("\nYou have 27 points to distribute among your attributes (STR, DEX, CON, INT, WIS, CHA).")
    print("Each attribute starts at 8. Assign additional points using the following costs:")
    print("""
    9 = 1 point
    10 = 2 points
    11 = 3 points
    12 = 4 points
    13 = 5 points
    14 = 7 points
    15 = 9 points
    Maximum value for any attribute is 15.
    """)

    while True:
        print("\nEnter the desired final values for each attribute.")
        print(f"Remaining points: {points}")
        try:
            # Input all attributes at once
            for attr in attributes:
                value = int(input(f"{attr} (current: {attributes[attr]}): "))
                if value < 8 or value > 15:
                    raise ValueError(f"Attribute {attr} must be between 8 and 15.")
                cost = calculate_cost(attributes[attr], value)
                if cost > points:
                    raise ValueError(f"Not enough points to increase {attr} to {value}. Required: {cost}, Remaining: {points}")
                attributes[attr] = value
                points -= cost
            break
        except ValueError as e:
            print(f"Error: {e}")
            print("Let's try again.")

    print("\nFinal attributes:")
    for attr, value in attributes.items():
        print(f"{attr}: {value}")

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

def calculate_cost(current, target):
    """
    Calculate the total cost of increasing an attribute from `current` to `target`.
    """
    costs = {9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
    total_cost = 0
    for value in range(current + 1, target + 1):
        total_cost += costs[value]
    return total_cost

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
