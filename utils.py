import os
import json
from datetime import datetime
from dm_interface import send_prompt_to_dm  # AI-driven summaries

SAVE_DIR = "saves"
LOG_FILE = os.path.join(SAVE_DIR, "game_log.txt")
SESSION_STATS_FILE = os.path.join(SAVE_DIR, "session_stats.json")

FACTIONS = ["Vanguard Alliance", "Black Market Syndicate", "Wyrm Pact", "Crimson Court"]  # Default factions

# 📌 Ensure directories exist
def ensure_save_directory():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

# 📌 Save & Load JSON Data
def save_to_file(data, filename):
    ensure_save_directory()
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"✅ Data saved to {filepath}")

def load_from_file(filename):
    filepath = os.path.join(SAVE_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as f:
        return json.load(f)

# 📌 Log Events & Track Unresolved Story Threads
def log_event(event_text, unresolved=False):
    """Logs events and tracks unresolved story threads."""
    ensure_save_directory()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write to log file
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {event_text}\n")

    # Update session stats
    update_session_stats(event_text, unresolved)

# 📌 Generate AI-Based Story Summary & Future Objectives
def generate_session_summary(dm_option="mistral"):
    """Generates an AI-driven game summary & structured future objectives."""
    if not os.path.exists(LOG_FILE):
        print("⚠️ No events logged yet.")
        return

    with open(LOG_FILE, 'r') as f:
        log_content = f.read()

    prompt = (
        "Summarize the following game session logs while ensuring structured storytelling.\n"
        "Focus on major events, character choices, and unresolved threads.\n"
        "Then, suggest structured next steps for the story.\n\n"
        f"{log_content}"
    )

    summary = send_prompt_to_dm(prompt, dm_option)
    print("\n📜 **Session Summary:**")
    print(summary)

    # AI-Generated Future Objectives
    objectives_prompt = (
        "Based on the game session logs, suggest 3 structured future objectives for the player.\n"
        "Keep them directly tied to past decisions and unresolved storylines.\n\n"
        f"{log_content}"
    )
    objectives = send_prompt_to_dm(objectives_prompt, dm_option)
    
    print("\n🎯 **Future Objectives:**")
    print(objectives)
    
    return {"summary": summary, "future_objectives": objectives}

# 📌 Track Player Session Stats, Faction Reputation, & Unresolved Threads
def update_session_stats(event_text, unresolved=False):
    """Tracks player session stats, unresolved storylines, and faction influence."""
    ensure_save_directory()

    stats = load_from_file("session_stats.json") or {
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "playtime": "0:00",
        "events": [],
        "unresolved_threads": [],
        "faction_reputation": {faction: 0 for faction in FACTIONS},
        "last_event_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    stats["events"].append(event_text)

    # Track unresolved threads
    if unresolved:
        stats["unresolved_threads"].append(event_text)

    # Update playtime
    start_time = datetime.strptime(stats["start_time"], "%Y-%m-%d %H:%M:%S")
    elapsed_time = datetime.now() - start_time
    stats["playtime"] = str(elapsed_time).split('.')[0]  # Remove milliseconds
    stats["last_event_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_to_file(stats, "session_stats.json")

# 📌 Adjust Faction Reputation
def adjust_faction_reputation(faction, amount):
    """Modifies reputation with a specific faction."""
    stats = load_from_file("session_stats.json") or {
        "faction_reputation": {faction: 0 for faction in FACTIONS}
    }

    if faction in stats["faction_reputation"]:
        stats["faction_reputation"][faction] += amount
        save_to_file(stats, "session_stats.json")
        print(f"🔺 {faction} reputation adjusted by {amount}. New reputation: {stats['faction_reputation'][faction]}")
    else:
        print(f"⚠️ Faction '{faction}' not found.")

# 📌 Display Player Stats & Faction Reputation
def display_session_stats():
    """Displays playtime, recent events, unresolved storylines, and faction standings."""
    stats = load_from_file("session_stats.json")
    if not stats:
        print("No session stats recorded yet.")
        return

    print("\n📊 **Session Stats:**")
    print(f"🕒 Playtime: {stats['playtime']}")
    print(f"📅 Started on: {stats['start_time']}")
    print(f"🔄 Last Event Logged: {stats['last_event_time']}")
    
    print("\n📝 **Recent Events:**")
    for event in stats["events"][-5:]:  # Show last 5 events
        print(f" - {event}")

    print("\n🚨 **Unresolved Story Threads:**")
    if stats["unresolved_threads"]:
        for thread in stats["unresolved_threads"]:
            print(f" - {thread}")
    else:
        print("None.")

    print("\n🏛️ **Faction Reputation:**")
    for faction, reputation in stats["faction_reputation"].items():
        print(f" - {faction}: {reputation}")

# 📌 Get Valid User Input
def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print(f"⚠️ Invalid choice. Valid options: {', '.join(valid_options)}")

# 📌 Print a Formatted Menu
def print_menu(title, options):
    print(f"\n=== {title} ===")
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    print()

# 📌 Select from a Menu
def select_from_menu(options):
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
        except ValueError:
            pass
        print("⚠️ Invalid selection. Please enter a number from the menu.")
