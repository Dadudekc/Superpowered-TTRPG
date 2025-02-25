import random
import logging
from typing import Dict, Optional, Any
from combat import Combatant, ELEMENTAL_WEAKNESSES, ELEMENTAL_RESISTANCES
from character import Power

logger = logging.getLogger(__name__)

class CombatAI:
    def __init__(self, difficulty: str = "Normal") -> None:
        self.difficulty: str = difficulty  # Options: Easy, Normal, Hard, Adaptive
        self.player_patterns: Dict[str, int] = {}  # Tracks player move frequencies
        self.ai_playstyle: str = self.set_playstyle()  # Options: Aggressive, Defensive, Balanced, Random, Learning

    def set_playstyle(self) -> str:
        """Assign an AI playstyle based on the selected difficulty."""
        if self.difficulty == "Easy":
            return "Random"
        elif self.difficulty == "Normal":
            return random.choice(["Balanced", "Aggressive", "Defensive"])
        elif self.difficulty == "Hard":
            return "Aggressive"
        elif self.difficulty == "Adaptive":
            return "Learning"
        return "Balanced"

    def track_player_pattern(self, player_action: str) -> None:
        """Track repeated player actions to allow for strategic counterplay."""
        self.player_patterns[player_action] = self.player_patterns.get(player_action, 0) + 1

    def analyze_battle_state(self, combatant: Combatant, enemy: Combatant) -> Dict[str, Any]:
        """
        Analyze the current combat scenario and determine the best move.
        
        Returns a dictionary with keys:
            - recommended_action: The action the AI should take.
            - reasoning: Explanation behind the decision.
            - (Optional) power_choice: If using a power, the selected power's name.
        """
        decision: Dict[str, Any] = {"recommended_action": "pass", "reasoning": "No valid action found."}
        
        # Check for low HP. Assumes character has a 'max_hp' attribute.
        if hasattr(combatant.character, "max_hp") and combatant.character.hp < 0.3 * combatant.character.max_hp:
            # Look for a defensive power (by name, case-insensitive).
            if any(p.name.lower() == "defend" for p in combatant.character.powers):
                decision = {"recommended_action": "defend", "reasoning": "With wounds deep and spirit wavering, defense is paramount."}
                return decision

        # Identify enemy weaknesses and try to pick an optimal power.
        effective_power = self.select_optimal_power(combatant, enemy)
        if effective_power:
            decision = {
                "recommended_action": "use power",
                "power_choice": effective_power.name,
                "reasoning": f"Analyzing the foe, it is clear they are vulnerable to {effective_power.element}—a chance to strike decisively."
            }
            return decision

        # Fallback to a standard attack.
        decision = {"recommended_action": "attack", "reasoning": "No clear advantage presents itself; a direct assault will do."}
        return decision

    def select_optimal_power(self, combatant: Combatant, enemy: Combatant) -> Optional[Power]:
        """
        Select the best power based on enemy elemental weaknesses and power cooldowns.
        
        Returns:
            The Power object that offers the highest expected damage, or None if none available.
        """
        best_power: Optional[Power] = None
        best_damage: float = 0.0

        for power in combatant.character.powers:
            if power.cooldown > 0:
                continue

            expected_damage: float = power.damage

            if power.element and hasattr(enemy.character, "element") and enemy.character.element:
                if enemy.character.element == ELEMENTAL_WEAKNESSES.get(power.element):
                    expected_damage *= 1.5  # 50% bonus damage
                elif enemy.character.element == ELEMENTAL_RESISTANCES.get(power.element):
                    expected_damage *= 0.5  # 50% reduced damage

            if expected_damage > best_damage:
                best_damage = expected_damage
                best_power = power

        return best_power

    def adapt_strategy(self, last_player_move: str) -> None:
        """
        Adjust the AI's strategy based on the player's tendencies.
        In Adaptive mode, if a player repeats the same move frequently, the AI will counteract.
        """
        self.track_player_pattern(last_player_move)
        if self.difficulty == "Adaptive":
            most_used_move = max(self.player_patterns, key=self.player_patterns.get, default=None)
            if most_used_move:
                logger.info(f"AI recognized player pattern: {most_used_move} is being used frequently.")
                if most_used_move == "attack":
                    self.ai_playstyle = "Defensive"
                elif most_used_move == "defend":
                    self.ai_playstyle = "Aggressive"
                else:
                    self.ai_playstyle = "Balanced"

    def decide_enemy_move(self, combatant: Combatant, enemy: Combatant) -> str:
        """
        Decide the move for an AI-controlled combatant based on the current playstyle.
        A dramatic whisper of calculated risk guides the enemy's choice.
        """
        if self.ai_playstyle == "Aggressive":
            return "use power" if enemy.character.powers else "attack"
        elif self.ai_playstyle == "Defensive":
            return "defend" if random.random() < 0.5 else "attack"
        elif self.ai_playstyle == "Balanced":
            return random.choice(["attack", "use power", "defend"])
        elif self.ai_playstyle in ["Random", "Learning"]:
            return random.choice(["attack", "use power", "defend"])
        return "attack"
