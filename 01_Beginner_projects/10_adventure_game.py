# Dungeon Escape: A simple text-based adventure game
import sys

def show_header():
    print("-" * 40)
    print("      Welcome to the Dungeon Escape!")
    print("-" * 40)

def door_one(health, inventory):
    """Treasure door: requires a few decisions to actually obtain the treasure.
    Returns (health, inventory, survived).
    """
    print("You open door 1 and step into a quiet, torchlit vault. Glitter hints at treasure, but something seems off.")

    while True:
        print("Options: 1) Try to open the chest  2) Search the room")
        choice = input("Enter 1 or 2: ")
        if choice == "1":
            # trying to force chest without a key
            if not inventory.get("key"):
                print("The chest is locked. You try forcing it open and trigger a trap — a dart grazes you!")
                damage = 20
                health -= damage
                print(f"You lose {damage} health. Current health: {health}")
                if health <= 0:
                    print("You bleed out from the injury. Game over.\n")
                    return health, inventory, False
                print("You can still search the room for a key or try again.")
                continue
            else:
                # player has key, give final choice how to open
                print("You have a key. How will you open the chest? 1) Unlock carefully  2) Pry it open")
                while True:
                    approach = input("Enter 1 or 2: ")
                    if approach == "1":
                        print("You unlock the chest carefully with the key. Inside is the treasure — you escape with riches!\n")
                        return health, inventory, True
                    elif approach == "2":
                        print("You pry the chest open — it triggers a heavier trap.")
                        damage = 40
                        health -= damage
                        print(f"You lose {damage} health. Current health: {health}")
                        if health <= 0:
                            print("The trap was too severe — you perish. Game over.\n")
                            return health, inventory, False
                        print("Despite the wound, you manage to grab some treasure and escape!\n")
                        return health, inventory, True
                    else:
                        print("Invalid choice. Enter 1 or 2.")
        elif choice == "2":
            # searching can yield a real key or a fake key depending on who you trusted
            if not inventory.get("key") and not inventory.get("fake_key"):
                if inventory.get("trusted_trickster"):
                    print("You search the vault and a small ornate key glints from a crack — it looks real!")
                    print("You pocket the key, but something about its weight feels off.")
                    inventory["fake_key"] = True
                    print("(This key might be a decoy — be careful when using it.)")
                else:
                    print("You search the vault and find an old iron key tucked behind a loose brick!")
                    inventory["key"] = True
                    print("You now have a key. Maybe it opens the chest.")
            elif inventory.get("fake_key") and not inventory.get("key"):
                # finding a fake key first — allow a second search to find the real key
                print("You search more thoroughly and, beneath a loose stone, discover the real iron key!")
                inventory["key"] = True
                print("You now have the real key as well.")
            else:
                print("You search again but find nothing else of interest.")
        else:
            print("Invalid choice. Please enter 1 or 2.")

def door_two(health, inventory):
    """Dangerous door: reduces health, then offers another decision."""
    print("You open door 2 and step into a dark chamber with a sleeping dragon.")
    print("The dragon wakes and lashes out — you manage to flee but not without injury.")
    damage = 30
    health -= damage
    print(f"You lose {damage} health. Current health: {health}")

    if health <= 0:
        print("You were too injured and succumbed to your wounds. Game over.\n")
        return health, inventory, False

    # additional decision after surviving the dragon
    print("As you stagger away from the chamber, you find a narrow passage (1) and a rickety ladder (2).")
    while True:
        sub_choice = input("Do you take the passage (1) or climb the ladder (2)? Enter 1 or 2: ")
        if sub_choice == "1":
            print("You follow the passage and it leads to a hidden exit — you escape the dungeon!")
            # small clue: you notice faint scratch marks leading back towards one of the vault walls
            print("On the wall you notice faint scratch marks — someone might have hidden something here earlier.")
            return health, inventory, True
        elif sub_choice == "2":
            print("You climb the ladder but loose stones fall and hit you.")
            ladder_damage = 20
            health -= ladder_damage
            print(f"You lose {ladder_damage} more health. Current health: {health}")
            if health <= 0:
                print("The injuries are too severe — you collapse and do not make it. Game over.\n")
                return health, inventory, False
            else:
                print("Despite the pain, you pull yourself up and find a small exit. You escape!\n")
                return health, inventory, True
        else:
            print("Invalid choice. Please enter 1 or 2.")


def play_game():
    """Runs one playthrough of the game and returns whether the player survived."""
    health = 100
    inventory = {"key": False, "fake_key": False, "trusted_hermit": False, "trusted_trickster": False}
    print(f"You find yourself in a dark dungeon. Your health: {health}")
    print("There are two doors before you: door 1 and door 2.")

    # optional NPC encounter before choosing a door
    print("As you step in, two figures sit in the dim corridor: a stooped Hermit and a flashy Trickster.")
    while True:
        meet = input("Do you approach the Hermit (h), the Trickster (t), or move on (m)? Enter h/t/m: ")
        if meet.lower() == "h":
            print("The Hermit peers at you and says: 'Search the vault for a loose brick; an old iron key rests there.'")
            inventory["trusted_hermit"] = True
            break
        elif meet.lower() == "t":
            print("The Trickster grins: 'Take the ladder — I saw a shiny key there, and the chest likes a bold hand.'")
            inventory["trusted_trickster"] = True
            break
        elif meet.lower() == "m":
            print("You ignore them and continue towards the doors.")
            break
        else:
            print("Invalid choice. Enter h, t, or m.")

    while True:
        choice = input("Which do you choose? Enter 1 or 2: ")
        if choice == "1":
            health, inventory, survived = door_one(health, inventory)
            return survived
        elif choice == "2":
            health, inventory, survived = door_two(health, inventory)
            return survived
        else:
            print("Invalid choice. Please enter 1 or 2.")


def main():
    show_header()
    try:
        while True:
            survived = play_game()
            # play again prompt
            while True:
                again = input("Play again? (y/n): ").strip().lower()
                if again in ("y", "yes"):
                    print("\nRestarting the dungeon...\n")
                    break
                elif again in ("n", "no"):
                    print("Thanks for playing — goodbye!")
                    return
                else:
                    print("Please answer 'y' or 'n'.")
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
    