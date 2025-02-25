from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Location:
    name: str
    description: str
    associated_faction: str = "Neutral"  # Which faction controls or influences the area
    missions: List[str] = field(default_factory=list)  # Missions available in the location

@dataclass
class Organization:
    name: str
    type: str  # Heroic, Villainous, Neutral
    description: str
    influence_level: int = 50  # Faction power level (0-100)

@dataclass
class NPC:
    name: str
    role: str
    affiliation: str
    description: str
    reputation: Dict[str, int] = field(default_factory=dict)  # Tracks faction reputation
    evolving_state: str = "Base"  # Changes based on player interaction

# 📌 Core City Locations
def get_core_locations():
    return [
        Location("Apex District", "Financial and political center.", "Vanguard Alliance", ["Defend the Council", "Expose Corrupt Officials"]),
        Location("Shadow Row", "Crime-ridden slums plagued by gang violence.", "Crimson Court", ["Break Up Gang War", "Infiltrate Crimson Hideout"]),
        Location("Steel Haven", "Industrial zone full of factories and warehouses.", "Iron Syndicate", ["Sabotage Syndicate Tech", "Secure Shipment"]),
        Location("Emerald Quarter", "High-tech residential area.", "Neutral", ["Stop AI Outbreak", "Investigate Rogue Hacker"]),
        Location("Oldtown", "Historical district with ancient secrets.", "Wyrm Pact", ["Recover Arcane Relic", "Protect Hidden Library"]),
        Location("Docklands", "Smuggling hub and battleground.", "Black Market Syndicate", ["Intercept Shipment", "Undercover Negotiation"]),
    ]

# 📌 Global Locations for Major Arcs
def get_global_locations():
    return [
        Location("Frostspire Tundra", "Frozen wasteland hiding ancient ruins.", "Wyrm Pact", ["Retrieve Lost Artifact"]),
        Location("Crimson Savannah", "A scorched desert filled with mutated wildlife.", "Crimson Court", ["Hunt Mutant Leader"]),
        Location("Omega Zone", "Radioactive wasteland with dangerous mutants.", "Iron Syndicate", ["Eliminate Rogue Experiments"]),
        Location("Neptune’s Graveyard", "Sunken cities teeming with aquatic adversaries.", "Neutral", ["Recover Lost Technology"]),
        Location("Obsidian Peaks", "Volcanic range with fiery enemies.", "Crimson Court", ["Survive the Lava Trials"]),
        Location("Skyshard Archipelago", "Floating islands with unstable portals.", "Wyrm Pact", ["Stabilize the Rift"]),
        Location("Silverwood Forest", "Mystical forest filled with ancient magic.", "Wyrm Pact", ["Speak with the Elders"]),
        Location("Starlight Cradle", "A space station orbiting Earth.", "Vanguard Alliance", ["Prevent an Alien Attack"]),
    ]

# 📌 Organizations with Influence Tracking
def get_organizations():
    return [
        Organization("The Vanguard Alliance", "Heroic", "Elite superhero team.", 80),
        Organization("Global Peace Initiative", "Heroic", "Monitors superpowered threats.", 70),
        Organization("Crimson Court", "Villainous", "Vampiric cabal.", 60),
        Organization("Iron Syndicate", "Villainous", "Tech-driven crime empire.", 75),
        Organization("The Wyrm Pact", "Neutral", "Arcane power seekers.", 50),
        Organization("The Revenant Corps", "Neutral", "Mercenaries working for the highest bidder.", 65),
        Organization("Black Market Syndicate", "Villainous", "Criminal network controlling illicit trades.", 55),
    ]

# 📌 NPCs with Dynamic Reputation System
def get_npcs():
    return [
        # **Heroes**
        NPC("Starlight", "Hero", "Vanguard Alliance", "Solar energy manipulator.", {"Vanguard Alliance": 20}),
        NPC("Zephyr", "Hero", "Vanguard Alliance", "Wind controller and speedster.", {"Vanguard Alliance": 15, "Neutral": 5}),
        NPC("Titanium", "Hero", "Vanguard Alliance", "Metal-skinned powerhouse.", {"Vanguard Alliance": 10, "Iron Syndicate": -10}),
        NPC("Oracle", "Hero", "Vanguard Alliance", "Precognitive visionary.", {"Vanguard Alliance": 30, "Wyrm Pact": 10}, "Awakened"),

        # **Villains**
        NPC("Oblivion Nexus", "Villain", "Crimson Court", "Cosmic manipulator.", {"Crimson Court": 25, "Wyrm Pact": 5}),
        NPC("Iron Maw", "Villain", "Iron Syndicate", "Indestructible crime lord.", {"Iron Syndicate": 30, "Vanguard Alliance": -20}),
        NPC("Void Monarch", "Villain", "Iron Syndicate", "Alien conqueror.", {"Iron Syndicate": 40}, "Corrupted"),

        # **Neutral Characters (Can be Allies or Enemies)**
        NPC("Lady Venom", "Neutral", "Crimson Court", "Assassin with toxic abilities.", {"Crimson Court": 10, "Black Market Syndicate": 10}, "Unaligned"),
        NPC("Spectral Scythe", "Neutral", "Revenant Corps", "Ghostly assassin.", {"Revenant Corps": 20, "Crimson Court": 5}),
        NPC("Warp Stalker", "Neutral", "Black Market Syndicate", "Metahuman smuggler.", {"Black Market Syndicate": 15}, "Shifting Loyalties"),
        NPC("Chimera", "Neutral", "Wyrm Pact", "Shapeshifting spy.", {"Wyrm Pact": 20, "Crimson Court": -10}, "Evolving"),
    ]

# 📌 Function to Track NPC Evolution
def evolve_npc(npc_name, new_state):
    """Updates the evolving state of an NPC."""
    npcs = get_npcs()
    for npc in npcs:
        if npc.name == npc_name:
            npc.evolving_state = new_state
            print(f"🔄 {npc_name} has evolved to state: {new_state}")
            return
    print(f"⚠️ NPC '{npc_name}' not found.")

# 📌 Function to Adjust Faction Influence
def adjust_faction_influence(faction_name, amount):
    """Modifies the influence level of a faction."""
    organizations = get_organizations()
    for org in organizations:
        if org.name == faction_name:
            org.influence_level = max(0, min(100, org.influence_level + amount))  # Keep within 0-100 range
            print(f"📈 {faction_name} influence adjusted to {org.influence_level}")
            return
    print(f"⚠️ Faction '{faction_name}' not found.")
