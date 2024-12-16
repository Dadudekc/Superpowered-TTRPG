# combat.py
from dataclasses import dataclass, field
from typing import List, Optional
import random

from character import Character

@dataclass
class Combatant:
    character: Character
    initiative: int = 0
    is_player: bool = True

@dataclass
class Combat:
    participants: List[Combatant]
    turn_order: List[Combatant] = field(default_factory=list)
    current_turn: int = 0

    def roll_initiative(self):
        for combatant in self.participants:
            combatant.initiative = random.randint(1, 20) + combatant.character.attributes['DEX']
        self.turn_order = sorted(self.participants, key=lambda x: x.initiative, reverse=True)
        print("\nInitiative Order:")
        for idx, combatant in enumerate(self.turn_order, 1):
            print(f"{idx}. {combatant.character.name} (Initiative: {combatant.initiative})")

    def start_combat(self):
        self.roll_initiative()
        while not self.is_combat_over():
            current = self.turn_order[self.current_turn]
            self.handle_turn(current)
            self.current_turn = (self.current_turn + 1) % len(self.turn_order)

    def handle_turn(self, combatant: Combatant):
        print(f"\nIt's {combatant.character.name}'s turn.")
        # Placeholder for turn actions
        # Integrate with DM Interface for narrative and choices
        action = input("Choose action: (attack, use power, pass): ").lower()
        if action == "attack":
            self.handle_attack(combatant)
        elif action == "use power":
            self.handle_use_power(combatant)
        else:
            print(f"{combatant.character.name} passes the turn.")

    def handle_attack(self, attacker: Combatant):
        # Simplified attack mechanic
        target_name = input("Enter the name of the target: ")
        target = self.find_combatant_by_name(target_name)
        if not target:
            print("Target not found.")
            return
        attack_roll = random.randint(1, 20) + attacker.character.attributes['STR']
        target_ac = 10  # Simplified AC
        print(f"{attacker.character.name} attacks {target.character.name} with a roll of {attack_roll} vs AC {target_ac}.")
        if attack_roll >= target_ac:
            damage = random.randint(1, 6) + attacker.character.attributes['STR']
            target.character.hp -= damage
            print(f"Hit! {target.character.name} takes {damage} damage. HP left: {target.character.hp}")
            if target.character.hp <= 0:
                print(f"{target.character.name} has been defeated!")
        else:
            print("Miss!")

    def handle_use_power(self, combatant: Combatant):
        # Placeholder for power usage
        print("Power usage not yet implemented.")

    def find_combatant_by_name(self, name: str) -> Optional[Combatant]:
        for c in self.participants:
            if c.character.name.lower() == name.lower():
                return c
        return None

    def is_combat_over(self):
        # Simplified combat end condition
        # Implement team-based conditions as needed
        alive = [c for c in self.participants if c.character.hp > 0]
        return len(alive) <= 1
