# world.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Location:
    name: str
    description: str

@dataclass
class Organization:
    name: str
    type: str  # Heroic, Villainous, Neutral
    description: str

@dataclass
class NPC:
    name: str
    role: str
    affiliation: str
    description: str

# Example data
def get_core_locations():
    return [
        Location("Apex District", "Financial and political center. Headquarters of the Vanguard Alliance."),
        Location("Shadow Row", "Crime-ridden slums plagued by gang violence."),
        Location("Steel Haven", "Industrial zone full of factories and warehouses."),
        Location("Emerald Quarter", "High-tech residential area."),
        Location("Oldtown", "Historical district with ancient secrets."),
        Location("Docklands", "Smuggling hub and battleground for aquatic villains."),
    ]

def get_global_locations():
    return [
        Location("Frostspire Tundra", "Frozen wasteland hiding ancient ruins."),
        Location("Crimson Savannah", "A scorched desert filled with mutated wildlife."),
        Location("Omega Zone", "Radioactive wasteland with dangerous mutants."),
        Location("Neptune’s Graveyard", "Sunken cities teeming with aquatic adversaries."),
        Location("Obsidian Peaks", "Volcanic range with fiery enemies."),
        Location("Skyshard Archipelago", "Floating islands with unstable portals."),
        Location("Silverwood Forest", "Mystical forest filled with ancient magic."),
        Location("Starlight Cradle", "A space station orbiting Earth."),
    ]

def get_organizations():
    return [
        Organization("The Vanguard Alliance", "Heroic", "Elite superhero team based in Paragon City."),
        Organization("Global Peace Initiative", "Heroic", "UN-backed group monitoring global superpowered threats."),
        Organization("Crimson Court", "Villainous", "Vampiric cabal led by Crimson King."),
        Organization("Iron Syndicate", "Villainous", "Tech-driven crime empire led by Iron Maw."),
        Organization("The Wyrm Pact", "Neutral", "Mystics seeking ancient magical power."),
        Organization("The Revenant Corps", "Neutral", "Mercenaries working for the highest bidder."),
    ]

def get_npcs():
    return [
        # Heroes
        NPC("Starlight", "Hero", "The Vanguard Alliance", "Solar energy manipulator."),
        NPC("Zephyr", "Hero", "The Vanguard Alliance", "Wind controller and speedster."),
        NPC("Phoenix", "Hero", "The Vanguard Alliance", "Fire manipulator with regenerative abilities."),
        NPC("Bolt", "Hero", "The Vanguard Alliance", "Electric speedster."),
        NPC("Guardian", "Hero", "The Vanguard Alliance", "Indestructible tank."),
        NPC("Titanium", "Hero", "The Vanguard Alliance", "Metal-skinned powerhouse."),
        NPC("Radiant", "Hero", "The Vanguard Alliance", "Solar healer and light manipulator."),
        NPC("Sentinel", "Hero", "The Vanguard Alliance", "Master of defensive barriers."),
        NPC("Oracle", "Hero", "The Vanguard Alliance", "Precognitive visionary."),
        NPC("Warden", "Hero", "The Vanguard Alliance", "Summons ethereal chains."),
        NPC("Blazewing", "Hero", "The Vanguard Alliance", "Flame-winged fighter."),
        NPC("Earthshaker", "Hero", "The Vanguard Alliance", "Seismic ground-shaker."),
        NPC("Spectra", "Hero", "The Vanguard Alliance", "Colorful energy beams."),
        NPC("Lumina", "Hero", "The Vanguard Alliance", "Light illusionist."),
        NPC("Aquarius", "Hero", "The Vanguard Alliance", "Water manipulator."),
        # Villains
        NPC("Oblivion Nexus", "Villain", "Crimson Court", "Cosmic manipulator."),
        NPC("Lady Venom", "Villain", "Crimson Court", "Assassin with toxic abilities."),
        NPC("Iron Maw", "Villain", "Iron Syndicate", "Indestructible crime lord."),
        NPC("Crimson King", "Villain", "Crimson Court", "Vampiric overlord."),
        NPC("Void Monarch", "Villain", "Iron Syndicate", "Alien conqueror."),
        NPC("Pulse", "Villain", "Iron Syndicate", "Energy disruptor."),
        NPC("Frostlock", "Villain", "Crimson Court", "Vengeful ice manipulator."),
        NPC("Rampage", "Villain", "Crimson Court", "Berserker mutant."),
        NPC("Shadowweaver", "Villain", "Crimson Court", "Nightmare manipulator."),
        NPC("Pyroclast", "Villain", "Crimson Court", "Explosive fire controller."),
        NPC("Mirrorblade", "Villain", "Iron Syndicate", "Assassin reflecting powers."),
        NPC("Chromaflux", "Villain", "Iron Syndicate", "Chaos-wielding reality warper."),
        NPC("Spectral Scythe", "Villain", "Crimson Court", "Ghostly energy-blade assassin."),
        NPC("Nebula Twins", "Villain", "Crimson Court", "Alien thieves."),
        NPC("Gearhead", "Villain", "Iron Syndicate", "Tech thief."),
    ]
