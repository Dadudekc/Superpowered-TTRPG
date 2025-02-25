import os
from game_engine import GameEngine

def main():
    """Main game loop handling AI selection, save/load, and game interaction."""
    print("\n🔹 **Welcome to Superpowered TTRPG!** 🔹")

    # Select AI backend for Dungeon Master interactions
    print("\n🌟 **Choose your Dungeon Master AI Backend:**")
    print("1️⃣ Mistral 7B (Local via Ollama Run)")
    print("2️⃣ DeepSeek Chat (Local via Ollama Run)")

    while True:
        choice = input("Enter the number of your choice (1 or 2): ").strip()
        if choice == '1':
            dm_option = 'mistral'
            break
        elif choice == '2':
            dm_option = 'deepseek'
            break
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

    # Initialize the game engine with selected AI model
    game = GameEngine(dm_option=dm_option)

    # Check for existing saves before creating a new character
    existing_saves = game.list_saved_games()
    if existing_saves:
        print("\n💾 **Existing Saves Found:**")
        for idx, save_file in enumerate(existing_saves, start=1):
            print(f"{idx}. {save_file}")
        
        while True:
            load_choice = input("Would you like to load a save? (Y/N): ").strip().lower()
            if load_choice == 'y':
                try:
                    save_index = int(input(f"Enter the number of the save to load (1-{len(existing_saves)}): ")) - 1
                    if 0 <= save_index < len(existing_saves):
                        game.load_game(existing_saves[save_index])
                        break
                    else:
                        print("❌ Invalid selection. Choose a valid save file number.")
                except ValueError:
                    print("❌ Invalid input. Enter a number corresponding to the save file.")
            elif load_choice == 'n':
                print("\n🎭 **Creating a New Character...**")
                game.start_game()
                break
            else:
                print("❌ Invalid choice. Enter 'Y' or 'N'.")
    else:
        print("\n🎭 **No save files found. Creating a New Character...**")
        game.start_game()

    # Main game loop
    while True:
        print("\n🔹 **Game Menu** 🔹")
        print("1️⃣ Explore a Location")
        print("2️⃣ Check Character Status")
        print("3️⃣ Save Game")
        print("4️⃣ Load Game")
        print("5️⃣ Start a Campaign Arc")
        print("6️⃣ Quit")

        command = input("\nEnter a command (1-6): ").strip()

        if command == "1":
            location = input("Enter the location to explore: ").strip()
            game.enter_location(location)
        elif command == "2":
            pc = game.player_character
            if pc:
                print(f"\n📜 **Character Status:**\n🔹 Name: {pc.name}\n💖 HP: {pc.hp}\n🌀 Attributes: {pc.attributes}")
            else:
                print("❌ No character found. Please start a new game or load a save.")
        elif command == "3":
            filename = input("Enter filename to save (default: savegame.json): ").strip() or "savegame.json"
            game.save_game(filename)
        elif command == "4":
            existing_saves = game.list_saved_games()
            if not existing_saves:
                print("❌ No saved games available.")
            else:
                print("\n💾 **Available Saves:**")
                for idx, save in enumerate(existing_saves, start=1):
                    print(f"{idx}. {save}")
                
                while True:
                    try:
                        save_index = int(input(f"Enter the number of the save to load (1-{len(existing_saves)}): ")) - 1
                        if 0 <= save_index < len(existing_saves):
                            game.load_game(existing_saves[save_index])
                            break
                        else:
                            print("❌ Invalid selection. Choose a valid save file number.")
                    except ValueError:
                        print("❌ Invalid input. Enter a number corresponding to the save file.")
        elif command == "5":
            print("\n📖 **Available Arcs:**")
            available_arcs = game.list_available_arcs()
            if available_arcs:
                for arc in available_arcs:
                    print(f"🔹 {arc}")

                arc_choice = input("\nEnter the arc number to start: ").strip()
                if arc_choice.isdigit():
                    game.start_campaign_arc(int(arc_choice))
                else:
                    print("❌ Invalid input. Please enter a valid arc number.")
            else:
                print("❌ No campaign arcs available.")
        elif command == "6":
            confirm_exit = input("\n🚪 Are you sure you want to quit? (Y/N): ").strip().lower()
            if confirm_exit == 'y':
                print("\n🚪 **Exiting the game. Goodbye!**")
                break
        else:
            print("❌ Invalid command. Please enter a number between 1-6.")

if __name__ == "__main__":
    main()
