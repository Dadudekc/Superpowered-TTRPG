# main.py
from game_engine import GameEngine

def main():
    print("Welcome to Superpowered TTRPG!")
    print("Choose your Dungeon Master backend:")
    print("1. OpenAI ChatGPT")
    print("2. Mistral 7B (Local via Ollama Run)")
    
    while True:
        choice = input("Enter the number of your choice (1 or 2): ")
        if choice == '1':
            dm_option = 'openai'
            break
        elif choice == '2':
            dm_option = 'mistral'
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    game = GameEngine(dm_option=dm_option)
    game.start_game()

    while True:
        command = input("\nEnter a command (explore, status, save, load, start arc, quit): ").lower()
        if command == "explore":
            location = input("Enter the location to explore: ")
            game.enter_location(location)
            # Potentially trigger events or encounters
        elif command == "status":
            pc = game.player_character
            print(f"\nCharacter Status:\nName: {pc.name}\n"
                  f"HP: {pc.hp}\nAttributes: {pc.attributes}")
        elif command == "save":
            filename = input("Enter filename to save (default: savegame.json): ") or "savegame.json"
            game.save_game(filename)
        elif command == "load":
            filename = input("Enter filename to load (default: savegame.json): ") or "savegame.json"
            game.load_game(filename)
        elif command.startswith("start arc"):
            try:
                arc_number = int(command.split()[-1])
                game.start_campaign_arc(arc_number)
            except (IndexError, ValueError):
                print("Please specify a valid arc number (1-8). Example: start arc 1")
        elif command == "quit":
            print("Exiting game. Goodbye!")
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
