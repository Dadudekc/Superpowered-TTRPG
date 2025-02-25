from dataclasses import dataclass, field
from typing import List, Optional, Dict
import random

from character import Character, Power
# Remove direct top-level import of CombatAI to avoid circular dependency.
# Instead, lazy import when creating the Combat instance.

ELEMENTAL_WEAKNESSES = {
    "Fire": "Water",
    "Water": "Lightning",
    "Lightning": "Earth",
    "Earth": "Wind",
    "Wind": "Fire",
    "Ice": "Fire",
    "Dark": "Light",
    "Light": "Dark",
}

ELEMENTAL_RESISTANCES = {
    "Fire": "Wind",
    "Water": "Ice",
    "Lightning": "Dark",
    "Earth": "Lightning",
    "Wind": "Earth",
    "Ice": "Water",
    "Dark": "Lightning",
    "Light": "Fire",
}

@dataclass
class Combatant:
    character: Character
    initiative: int = 0
    is_player: bool = True
    status_effects: List[str] = field(default_factory=list)  # Buffs/Debuffs
    cooldowns: Dict[str, int] = field(default_factory=dict)  # Track power cooldowns

@dataclass
class Combat:
    participants: List[Combatant]
    turn_order: List[Combatant] = field(default_factory=list)
    current_turn: int = 0
    # Lazy import of CombatAI to avoid circular dependency issues.
    ai: object = field(default_factory=lambda: __import__("combat_ai").CombatAI(difficulty="Adaptive"))

    def roll_initiative(self) -> None:
        """Roll initiative for all combatants and determine the turn order."""
        print("\nThe tension mounts as each combatant prepares for battle...")
        for combatant in self.participants:
            dex_bonus = combatant.character.attributes.get("DEX", 0)
            combatant.initiative = random.randint(1, 20) + dex_bonus
        self.turn_order = sorted(self.participants, key=lambda c: c.initiative, reverse=True)

        print("\n📜 **Initiative Order:**")
        for idx, combatant in enumerate(self.turn_order, 1):
            print(f"{idx}. {combatant.character.name} (Initiative: {combatant.initiative})")
        print("Let the battle begin!\n")

    def start_combat(self) -> None:
        """Start the combat loop until one side is defeated."""
        self.roll_initiative()
        while not self.is_combat_over():
            current = self.turn_order[self.current_turn]
            if current.character.hp > 0:
                self.handle_turn(current)
            self.current_turn = (self.current_turn + 1) % len(self.turn_order)
        self.conclude_battle()

    def handle_turn(self, combatant: Combatant) -> None:
        """Handle a single turn for a combatant with narrative flair."""
        print(f"\n🔄 The spotlight falls on {combatant.character.name} as they prepare to act...")
        self.reduce_cooldowns(combatant)

        # Player-controlled combatants receive a prompt with a narrative hook.
        if combatant.is_player:
            print(f"{combatant.character.name} feels the weight of destiny. What will you do?")
            action = input("Choose action: (attack, use power, defend, pass): ").strip().lower()
            # Inform the AI of player action for adaptive learning.
            self.ai.adapt_strategy(action)
        else:
            target = self.select_target(combatant)
            action = self.ai.decide_enemy_move(combatant, target)
            print(f"{combatant.character.name} contemplates the battle... and decides to {action}.")

        if action == "attack":
            self.handle_attack(combatant)
        elif action == "use power":
            self.handle_use_power(combatant)
        elif action == "defend":
            self.apply_defense(combatant)
        else:
            print(f"{combatant.character.name} hesitates and lets the moment pass.")

    def handle_attack(self, attacker: Combatant) -> None:
        """Process a standard attack with dramatic narrative details."""
        target = self.select_target(attacker)
        if not target:
            print("In the chaos, no enemy can be found...")
            return

        strength_bonus = attacker.character.attributes.get("STR", 0)
        attack_roll = random.randint(1, 20) + strength_bonus
        target_ac = 12  # Base Armor Class for enemies
        print(f"⚔️ {attacker.character.name} lunges forward with determination, rolling a {attack_roll} against {target.character.name}'s defenses (AC {target_ac}).")

        if attack_roll >= target_ac:
            damage = random.randint(1, 6) + strength_bonus
            target.character.hp -= damage
            print(f"💥 A powerful strike lands! {target.character.name} reels from the blow, suffering {damage} damage (HP left: {target.character.hp}).")
            if target.character.hp <= 0:
                print(f"☠️ In a final, dramatic moment, {target.character.name} collapses, defeated!")
        else:
            print("❌ The attack misses, leaving only the echo of what might have been.")

    def handle_use_power(self, combatant: Combatant) -> None:
        """Narrate the use of a superpower with rich descriptive language."""
        if not combatant.character.powers:
            print("⚠️ A surge of anticipation fills the air... but no powers are available!")
            return

        print("\n🌀 A burst of energy surrounds the battlefield. Available Powers:")
        for idx, power in enumerate(combatant.character.powers, start=1):
            cd = combatant.cooldowns.get(power.name, 0)
            status = f"(Cooldown: {cd} turns)" if cd > 0 else ""
            print(f"{idx}. {power.name} - {power.description} {status}")

        choice = input("Select a power by number: ").strip()
        try:
            selected_power = combatant.character.powers[int(choice) - 1]
            if combatant.cooldowns.get(selected_power.name, 0) > 0:
                print(f"⚠️ {selected_power.name} remains dormant for {combatant.cooldowns[selected_power.name]} more turns!")
                return

            print(f"✨ With a flourish, {combatant.character.name} unleashes {selected_power.name}!")
            target = self.select_target(combatant)
            if target:
                self.resolve_power_effect(combatant, target, selected_power)
                if selected_power.cooldown:
                    combatant.cooldowns[selected_power.name] = selected_power.cooldown
        except (ValueError, IndexError):
            print("⚠️ The power selection falters, leaving the hero uncertain.")

    def resolve_power_effect(self, attacker: Combatant, target: Combatant, power: Power) -> None:
        """Resolve power effects with dramatic narrative and elemental flair."""
        base_damage = power.damage
        narrative = f"{attacker.character.name}'s {power.name} surges forward"
        if power.element:
            weakness = ELEMENTAL_WEAKNESSES.get(power.element)
            resistance = ELEMENTAL_RESISTANCES.get(power.element)
            if target.character.element == weakness:
                base_damage = int(base_damage * 1.5)
                narrative += f", exploiting {target.character.name}'s weakness to {power.element}!"
            elif target.character.element == resistance:
                base_damage = int(base_damage * 0.5)
                narrative += f", though {target.character.name}'s resilience to {power.element} tempers the blow."
            else:
                narrative += f", radiating the pure force of {power.element}."
        else:
            narrative += " in a raw display of power."

        target.character.hp -= base_damage
        print(f"💥 {narrative} The impact is devastating—{target.character.name} takes {base_damage} damage (HP left: {target.character.hp}).")

    def reduce_cooldowns(self, combatant: Combatant) -> None:
        """Reduce power cooldowns, symbolizing the slow rekindling of energy."""
        for power in list(combatant.cooldowns.keys()):
            if combatant.cooldowns[power] > 0:
                combatant.cooldowns[power] -= 1

    def apply_defense(self, combatant: Combatant) -> None:
        """Narrate a defensive stance that shields against the onslaught."""
        combatant.status_effects.append("Defending")
        print(f"🛡️ {combatant.character.name} adopts a resolute defensive stance, preparing for the enemy's next strike.")

    def select_target(self, attacker: Combatant) -> Optional[Combatant]:
        """Select a random valid target with a hint of fate's randomness."""
        enemies = [c for c in self.participants if c.is_player != attacker.is_player and c.character.hp > 0]
        if not enemies:
            return None
        return random.choice(enemies)

    def is_combat_over(self) -> bool:
        """Determine if the battle has reached its dramatic conclusion."""
        players_alive = any(c.is_player and c.character.hp > 0 for c in self.participants)
        enemies_alive = any(not c.is_player and c.character.hp > 0 for c in self.participants)
        return not (players_alive and enemies_alive)

    def conclude_battle(self) -> None:
        """Narrate the final moments of the battle."""
        if self.is_combat_over():
            print("\n🏆 The clash of titans has ended. Amid the fading echoes of combat, a victor emerges!")
        else:
            print("\nThe battle continues...")
