import math
import random
from colorama import init, Fore, Back, Style

def get_valid_input(prompt, valid_options):
    """Get input from user and validate it's in valid_options list"""
    valid = False
    choice = None
    
    while not valid:
        try:
            choice = int(input(prompt))
            if choice in valid_options:
                valid = True
            else:
                print(f"Invalid choice. Please enter one of: {valid_options}")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return choice

rolls = []

def rolldice(x):
    for i in range(x):
        y = random.randint(1, 6)
        print(Style.BRIGHT + Fore.BLACK + f"{y}" + Style.RESET_ALL)
        rolls.append(y)

print("Welcome to DICE DUNGEON.")

print("In Dice Dungeon, You will use your magical dice to activate spellcards to fight the evil forces on your adventures. Try each class, refine your strategy, and triumph!")

charname = input("What is your name?")

print("Choose your character...")
print(Style.BRIGHT + Fore.CYAN + "F E N C E R" + Style.RESET_ALL + "\nOnce per turn, may reroll a die.") #on upgrade, can be used more times per turn
print(Style.BRIGHT + Fore.RED + "K N I G H T" + Style.RESET_ALL + "\nRoll dice individually. If your limit is exceeded, your turn immediately ends. If you match your limit exactly, you get to choose from 3 powerful boons") #on upgrade, the limit increases by 6.
print(Style.BRIGHT + Fore.YELLOW + "C L E R I C" + Style.RESET_ALL + "\nWhen rolling doubles, you heal by that much. At full health, you may remove negative status effects from yourself.") #on level 2 and above, excess healing converts to a temporary shield.
print(Style.BRIGHT + Fore.BLUE + "W A R L O C K" + Style.RESET_ALL + "\nWhen applying status effects, apply that many plus one.") #on upgrade, add an extra each time.
print(Style.BRIGHT + Fore.GREEN + "D R U I D" + Style.RESET_ALL + "\nOn a roll of 1, you may \"plant\" it. 2 turns later, it will bloom into a 6 that  doesn't count towards that turn's rolls.") #On even levels, can 'plant' dies of a higher level (level 2 unlocks planting 2's, level 4 unlocks 3's). On odd levels, planted seeds produce 1 extra die when 'blooming' (level 3 means each planted die produces 2 sixes when they bloom, level 5 means 3 for each seed, etc).
print(Style.BRIGHT + Fore.MAGENTA + "R O G U E" + Style.RESET_ALL + "\nYou select a lucky number at the start of each combat. Whenever that number is rolled, you deal 2 damage to an enemy") #on upgrade, add 2 per level

clas=get_valid_input(Style.BRIGHT + "Make your choice...\n"+Fore.CYAN+"1) Fencer\n"+Fore.RED+"2) Knight\n"+Fore.YELLOW+"3) Cleric\n"+Fore.BLUE+"4) Warlock\n"+Fore.GREEN+"5) Druid\n"+Fore.MAGENTA+"6) Rogue"+Style.RESET_ALL, [1,2,3,4,5,6])

if clas == 1:
    charclass = "Fencer"
    title = "Ser"
if clas == 2:
    charclass = "Knight"
    title = "Ser"
if clas == 3:
    charclass = "Cleric"
    title = "Vicar"
if clas == 4:
    charclass = "Warlock"
    title = "Pactist"
if clas == 5:
    charclass = "Druid"
    title = "Warden"
if clas == 6:
    charclass = "Rogue"
    title = "Asset"



# rolldice(20)
# print(f"TEST: {str(rolls)}")
# for roll in rolls:
#     if roll == 6:
#         print("Anotha one")

if clas == 1:
    hp = 40
elif clas == 2:
    hp = 42
elif clas == 3:
    hp = 42
elif clas == 4:
    hp = 38
elif clas == 5:
    hp = 40
elif clas == 6:
    hp = 38

# Track unlocked stages (1 = Plains is unlocked by default)
unlocked_stages = 1
stage_names = {1: "Plains", 2: "Caves", 3: "Mountains"}

currenthp = hp

"""
Card types:
0) Blank entry (whatever the value of the entered die)
1) Only evens
Only odds 
Only below/above set number (Could all be confined to just a limited form)
2) Build up to limit (Enter multiple dice until threshold is met, like 12 or 15)
"""

#Class stuff to add:
#Damage type? or just effect when activated

class card:
    def __init__(card, name, card_type, reusable, level, limit, accepted_numbers=None):
        card.name = name
        card.card_type = card_type
        card.reusable = reusable
        card.level = level # adjust stats?
        card.limit = limit # used for type 2 cards
        card.accepted_numbers = accepted_numbers
        
    def get_card_type(card):
        if card.card_type == 0:
            return [0, 1, 2, 3, 4, 5, 6]
        elif card.card_type == 1:
            return card.accepted_numbers
        elif card.card_type == 2:
            return card.limit - (card.level * 6)

    # def display_stats(self):
    #     print(f"Name: {self.name}")
    #     print(f"Health: {self.health}")
    #     print(f"Strength: {self.get_strength()}")
    #     print(f"Defense: {self.defense}")

sword = card("Sword", 0, 0, [1,2,3,4,5,6])
peash = card("Peashooter", )

class enemy:
    def __init__(enemy, name, max_hp, currenthp, cardpool):
        enemy.name = name
        enemy.max_hp = max_hp
        enemy.currenthp = currenthp
        enemy.cardpool = cardpool


#Game loop begins

while currenthp >= 0:
    # Build the stage options list based on unlocked stages
    print("Level select:")
    for i in range(1, unlocked_stages + 1):
        print(f"{i}) {stage_names[i]}")
    
    # Create valid options list (only unlocked stages)
    valid_stages = list(range(1, unlocked_stages + 1))
    
    # Get player's choice with validation
    stage = get_valid_input("Where will you venture? ", valid_stages)
    if stage == 1:
        print("These fields are where you grew up. You remember rushing through the golden stalks, playing games with your brothers and sisters when you found the time. Now, though, the fields look... grey. There's a sadness that you don't remember being there when you left. Rustling alerts you to the fact you are not alone. A dark shape is circling you, and closing in. You ready yourself. This place gave you a childhood, and it's time to return the favor.")