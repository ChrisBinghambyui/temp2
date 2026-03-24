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

print("In Dice Dungeon, You will use your magical dice to activate spellcards to ensure victory on your adventures. Try each class, refine your strategy, and triumph!")

charname = input("What is your name?\n\t>")

print("Choose your character...")
print(Style.BRIGHT + Fore.CYAN + "F E N C E R" + Style.RESET_ALL + "\nOnce per turn, may reroll a die.") #on upgrade, can be used more times per turn
print(Style.BRIGHT + Fore.RED + "K N I G H T" + Style.RESET_ALL + "\nRoll dice individually. If your limit is exceeded, your turn immediately ends. If you match your limit exactly, you get to choose from 3 powerful boons.") #on upgrade, the limit increases by 6.
print(Style.BRIGHT + Fore.YELLOW + "C L E R I C" + Style.RESET_ALL + "\nWhen rolling doubles, you heal by that much.") #on level 2 and above, excess healing converts to a temporary shield.
print(Style.BRIGHT + Fore.BLUE + "W A R L O C K" + Style.RESET_ALL + "\nWhen applying status effects, apply that many plus one.") #on upgrade, add an extra each time.
print(Style.BRIGHT + Fore.GREEN + "D R U I D" + Style.RESET_ALL + "\nYou may \"plant\" your dice. Next turn, it will \"bloom\" with 2 dice of the same value that don't count towards your dice total.") #On even levels, each planted die will bloom with +x (at level two, plantin a 1 will produce two 2's. At level 4, planting a 1 will produce 3's). On odd levels, planted seeds produce 1 extra die when 'blooming' (level 3 means each planted die produces 3 dice when they bloom, level 5 means 4, etc).
print(Style.BRIGHT + Fore.MAGENTA + "R O G U E" + Style.RESET_ALL + "\nYou select a lucky number at the start of each combat. Whenever that number is rolled, you deal 2 damage to enemy.") #on upgrade, add 2 per level

clas=get_valid_input(Style.BRIGHT + "Make your choice...\n"+Fore.CYAN+"1) Fencer\n"+Fore.RED+"2) Knight\n"+Fore.YELLOW+"3) Cleric\n"+Fore.BLUE+"4) Warlock\n"+Fore.GREEN+"5) Druid\n"+Fore.MAGENTA+"6) Rogue"+Style.RESET_ALL+"\n\t>", [1,2,3,4,5,6])

if clas == 1:
    charclass = "Fencer"
    title = "Nimble"
    char_style = Style.BRIGHT + Fore.CYAN
if clas == 2:
    charclass = "Knight"
    title = "Ser"
    char_style = Style.BRIGHT + Fore.RED
if clas == 3:
    charclass = "Cleric"
    title = "Vicar"
    char_style = Style.BRIGHT + Fore.YELLOW
if clas == 4:
    charclass = "Warlock"
    title = "Pactist"
    char_style = Style.BRIGHT + Fore.BLUE
if clas == 5:
    charclass = "Druid"
    title = "Warden"
    char_style = Style.BRIGHT + Fore.GREEN
if clas == 6:
    charclass = "Rogue"
    title = "Shade"
    char_style = Style.BRIGHT + Fore.MAGENTA

print(f"And so begins the tale of {char_style + title + " " + charname.capitalize()}, the {charclass.lower()+Style.RESET_ALL}.")

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
status effects:
1) vampirism (heal X when dealing damage, based on number of vampirism stacks
2) blind (when rolling dice, lose x stacks and turn that many dice hidden. the value doesnt change, they're just hidden)
3) poison (take x damage at end of turn)
4) shield (block damage)
5) thorn (deal damage when attacked)
6) weaken (each rolled die has their value reduced by 1, to a minimum of 1)
"""
# reduce is when the stack reduces. end of turn? when rolling? when attacking?
# class status_effect:
#     def __init__(stat, name, type, reduce, effect, damage=False):
#         stat.name = name
#         stat.type = type
#         stat.damage = damage
#         stat.effect = effect
#         stat.reduce = reduce



"""
Card types:
0) Blank entry (whatever the value of the entered die)
1) Only evens
Only odds 
Only below/above set number (Could all be confined to just a limited form)
2) Build up to limit (Enter multiple dice until threshold is met, like 12 or 15)
"""

class Card:
    """
    A flexible card class for Dicey Dungeons-style gameplay.
    
    Card Types:
    - 'single': Takes one die
    - 'multi': Takes multiple dice up to max_dice
    - 'passive': Always active effect
    
    Effect Types:
    - 'damage': Deal damage to target
    - 'heal': Restore HP
    - 'shield': Add shield/block
    - 'status': Apply status effect
    - 'manipulate': Change dice values
    - 'reroll': Reroll dice
    - 'lock': Lock dice from being used
    - 'poison': deal damage equal to amount of poison at start of turn, thenr educe by one
    - 'bleed' : deal 2 damage when a card is used
    """
    
    def __init__(self, name, card_type='single', effect_type='damage', 
                 base_value=0, uses_dice_value=True, reusable=True, 
                 max_uses=None, cooldown=0, max_dice=1,
                 dice_restriction=None, target='enemy', 
                 status_effect=None, status_duration=0,
                 upgrade_level=1, description="", class_restricted=None, value_fn=None):
        """
        Initialize a card.
        
        Args:
            name: Card name
            card_type: 'single', 'multi', 'countdown', or 'passive'
            effect_type: Type of effect (see class docstring)
            base_value: Base value for effect (added to dice)
            uses_dice_value: Whether dice value affects the effect
            reusable: Can be used multiple times per turn
            max_uses: Max times per turn (None = unlimited if reusable)
            cooldown: Turns before card can be used again
            max_dice: Maximum number of dice this card can accept
            dice_restriction: Function or dict to validate dice
            target: 'enemy', 'self', 'all_enemies', 'choose'
            status_effect: Name of status to apply
            status_duration: How long status lasts
            upgrade_level: Current upgrade level
            description: Card description text
            class_restricted: is this restricted to a class?
        """
        self.name = name
        self.card_type = card_type
        self.effect_type = effect_type
        self.base_value = base_value
        self.uses_dice_value = uses_dice_value
        self.reusable = reusable
        self.max_uses = max_uses
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.max_dice = max_dice
        self.dice_restriction = dice_restriction or {}
        self.target = target
        self.status_effect = status_effect
        self.status_duration = status_duration
        self.upgrade_level = upgrade_level
        self.description = description
        self.value_fn = value_fn  # Optional custom effect calculator
        
        self.class_restricted = class_restricted

        # Track uses this turn
        self.uses_this_turn = 0
        self.dice_slots = []  # Dice currently in this card
        
    def can_accept_die(self, die_value):
        """Check if this card can accept a die of this value."""
        if self.current_cooldown > 0:
            return False
            
        if not self.reusable and self.uses_this_turn > 0:
            return False
            
        if self.max_uses and self.uses_this_turn >= self.max_uses:
            return False
            
        if len(self.dice_slots) >= self.max_dice:
            return False
            
        # Check dice restrictions
        if isinstance(self.dice_restriction, dict):
            if 'min' in self.dice_restriction and die_value < self.dice_restriction['min']:
                return False
            if 'max' in self.dice_restriction and die_value > self.dice_restriction['max']:
                return False
            if 'only_even' in self.dice_restriction and self.dice_restriction['only_even'] and die_value % 2 != 0:
                return False
            if 'only_odd' in self.dice_restriction and self.dice_restriction['only_odd'] and die_value % 2 == 0:
                return False
            if 'exact_values' in self.dice_restriction and die_value not in self.dice_restriction['exact_values']:
                return False
                
        return True
    
    def add_die(self, die_value):
        """Add a die to this card's slots."""
        if self.can_accept_die(die_value):
            self.dice_slots.append(die_value)
            return True
        return False
    
    def is_ready(self):
        """Check if card has enough dice to activate."""
        if self.card_type == 'countdown':
            return self.current_cooldown == 0
        elif self.card_type == 'passive':
            return True
        else:
            # Single or multi - check if we have at least one die
            return len(self.dice_slots) > 0
    
    def calculate_effect(self, user=None, target_entity=None):
        """Calculate the effect value based on dice and base value."""
        if self.value_fn:
            return self.value_fn(user, target_entity)
        total = self.base_value
        
        if self.uses_dice_value:
            total += sum(self.dice_slots)
            
        return total
    
    def activate(self, user, target_entity):
        """
        Activate the card's effect.
        
        Returns: dict with effect results
        """
        if not self.is_ready():
            return {'success': False, 'message': 'Card not ready'}
        
        effect_value = self.calculate_effect(user, target_entity)
        result = {
            'success': True,
            'card_name': self.name,
            'effect_type': self.effect_type,
            'value': effect_value,
            'dice_used': self.dice_slots.copy()
        }
        
        # Apply the effect based on type
        if self.effect_type == 'damage':
            result['damage_dealt'] = effect_value
            result['message'] = f"{self.name} deals {effect_value} damage!"
            
        elif self.effect_type == 'heal':
            result['heal_amount'] = effect_value
            result['message'] = f"{self.name} heals {effect_value} HP!"
            
        elif self.effect_type == 'shield':
            result['shield_amount'] = effect_value
            result['message'] = f"{self.name} grants {effect_value} shield!"
            
        elif self.effect_type == 'status':
            result['status'] = self.status_effect
            result['stacks'] = effect_value
            result['duration'] = self.status_duration
            result['message'] = f"{self.name} applies {effect_value} {self.status_effect}!"
            
        # Clear dice slots and increment usage
        self.dice_slots = []
        self.uses_this_turn += 1
        
        # Set cooldown if applicable
        if self.cooldown > 0:
            self.current_cooldown = self.cooldown
            
        return result
    
    def reset_turn(self):
        """Reset card state for new turn."""
        self.uses_this_turn = 0
        self.dice_slots = []
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
    
    def upgrade(self):
        """Upgrade this card to next level."""
        self.upgrade_level += 1
        # Implement upgrade logic (increase base_value, reduce cooldown, etc.)
        self.base_value += 1
        
    def get_display_text(self):
        """Get formatted display text for the card."""
        text = f"{self.name}"
        if self.upgrade_level > 1:
            text += f" +{self.upgrade_level - 1}"
        
        # Show dice slots
        slots = "□" * (self.max_dice - len(self.dice_slots)) + "■" * len(self.dice_slots)
        text += f" [{slots}]"
        
        if self.current_cooldown > 0:
            text += f" (CD: {self.current_cooldown})"
            
        return text


# Example card definitions
def create_sword(level=1):
    """Basic damage card - deals damage equal to die value."""
    return Card(
        name="Sword",
        card_type='single',
        effect_type='damage',
        base_value=0,
        uses_dice_value=True,
        reusable=False,
        max_dice=1,
        upgrade_level=level,
        description="Deal damage equal to the die."
    )

def create_dagger(level=1):
    """Quick reusable weapon."""
    return Card(
        name="Dagger",
        card_type='single',
        effect_type='damage',
        base_value=0,
        uses_dice_value=True,
        reusable=True,
        max_dice=1,
        dice_restriction={'only_odd': True},
        upgrade_level=level,
        description="Reusable. Odds. Deal damage equal to the die."
    )

def create_hammer(level=1):
    """High damage but restricted to high dice."""
    return Card(
        name="Hammer",
        card_type='single',
        effect_type='damage',
        base_value=3,
        uses_dice_value=True,
        reusable=False,
        max_dice=1,
        dice_restriction={'min': 4},
        upgrade_level=level,
        description="Only accepts 4-6. Deal damage plus 3."
    )

def create_poison_dart(level=1):
    """Applies poison status."""
    return Card(
        name="Poison Dart",
        card_type='single',
        effect_type='status',
        base_value=-1,
        uses_dice_value=True,
        reusable=True,
        max_uses=2,
        max_dice=1,
        status_effect='poison',
        status_duration=3,
        upgrade_level=level,
        description="Apply poison equal to die value minus 1. 2 uses per turn."
    )

def create_healing_spell(level=1):
    """Heal yourself."""
    return Card(
        name="Healing Spell",
        card_type='single',
        effect_type='heal',
        base_value=2,
        uses_dice_value=True,
        reusable=False,
        max_dice=1,
        target='self',
        dice_restriction={'only_even': True},
        upgrade_level=level,
        description="Evens. Heal for die value plus 2."
    )

def create_shield_bash(level=1):
    """Gain shield based on die."""
    return Card(
        name="Shield Bash",
        card_type='single',
        effect_type='damage',
        base_value=0,
        uses_dice_value=False,
        reusable=True,
        max_dice=1,
        target='enemy',
        upgrade_level=level,
        description="Deal damage equal to your current shield.",
        value_fn=lambda user, _: getattr(user, 'shield', getattr(user, 'current_shield', 0))
    )

def create_fireball(level=1):
    """Multi-die damage card."""
    return Card(
        name="Fireball",
        card_type='multi',
        effect_type='damage',
        base_value=0,
        uses_dice_value=True,
        reusable=False,
        max_dice=3,
        cooldown=2,
        upgrade_level=level,
        description="Add up to 3 dice. Deal damage equal to total. Cooldown: 2"
    )


# Legacy compatibility - keeping old card instance
sword = create_sword()
peash = Card(name="Peashooter", card_type='multi', effect_type='damage', 
             base_value=0, uses_dice_value=True, reusable=True, 
             max_dice=3, dice_restriction={'max': 3}, upgrade_level=1,
             description="Add dice up to 3 total value.")
fortify = Card(name="Fortify", card_type='single',
               effect_type='shield',
               base_value=4,
               uses_dice_value=False,
               reusable=False,
               max_dice=1,
               upgrade_level=1,
               description="Gain 4 shield.")

dagger = create_dagger()
hammer = create_hammer()
poison_dart = create_poison_dart()
healing_spell = create_healing_spell()
shield_bash = create_shield_bash()
fireball = create_fireball()






class enemy:
    def __init__(enemy, name, max_hp, currenthp, cardpool, xp_value):
        enemy.name = name
        enemy.max_hp = max_hp
        enemy.currenthp = currenthp
        enemy.cardpool = cardpool
        enemy.xp_value = xp_value

dummy = enemy("Dummy", 15, 15, [], 10)

def draw_cards(deck, discard, hand, num_cards):
    """Draw cards from deck into hand. If deck is empty, shuffle discard into deck first."""
    cards_drawn = 0
    
    for _ in range(num_cards):
        # If deck is empty, shuffle discard back in
        if not deck and discard:
            deck.extend(discard)
            discard.clear()
            random.shuffle(deck)
        
        # Draw a card if available
        if deck:
            card = deck.pop(0)
            hand.append(card)
            cards_drawn += 1
        else:
            break  # No cards left
    
    return cards_drawn


def discard_used_cards(hand, discard, cards_to_discard_indices):
    """Move used cards from hand to discard pile. Keep others in hand."""
    # Sort indices in reverse to avoid index shifting issues
    for idx in sorted(cards_to_discard_indices, reverse=True):
        if 0 <= idx < len(hand):
            discard.append(hand.pop(idx))



edam = 0

play = 1
deck=[sword, dagger, hammer, poison_dart, healing_spell, peash, shield_bash, fireball, fortify]
hand_size=3
dice_count=3

def player_roll():
    """Roll dice equal to dice_count and return list of results."""
    roll_results = []
    print("Rolling dice...")
    for i in range(dice_count):
        die_value = random.randint(1, 6)
        roll_results.append(die_value)
        print(f"Die {i+1}: {die_value}")
    return roll_results

def display_hand(hand):
    """Display the player's current hand of cards."""
    print("\n=== YOUR HAND ===")
    for i, card in enumerate(hand):
        print(f"{i+1}) {card.get_display_text()} - {card.description}")
    print("=" * 40)

def display_dice(dice_list):
    """Display available dice."""
    if dice_list:
        print(f"\nAvailable Dice: {dice_list}")
    else:
        print("\nNo dice remaining!")

def combat_loop(player_deck, player_discard, player_hand_size, player_dice_count,
                enemy_obj, enemy_deck, enemy_discard, enemy_hand_size, enemy_dice_count,
                player_hp, player_name):
    """Main combat loop between player and enemy."""
    
    # Initialize hands
    player_hand = []
    enemy_hand = []
    
    # Draw initial hands
    draw_cards(player_deck, player_discard, player_hand, player_hand_size)
    draw_cards(enemy_deck, enemy_discard, enemy_hand, enemy_hand_size)
    
    turn = 0
    player_current_hp = player_hp
    
    while player_current_hp > 0 and enemy_obj.currenthp > 0:
        turn += 1
        print(f"\n{'='*60}")
        print(f"TURN {turn}")
        print(f"{player_name} HP: {player_current_hp}/{player_hp} | {enemy_obj.name} HP: {enemy_obj.currenthp}/{enemy_obj.max_hp}")
        print(f"{'='*60}")
        
        # === PLAYER TURN ===
        print(f"\n>>> {player_name.upper()}'S TURN <<<")
        
        # Draw back to hand size
        cards_to_draw = player_hand_size - len(player_hand)
        if cards_to_draw > 0:
            drawn = draw_cards(player_deck, player_discard, player_hand, cards_to_draw)
            if drawn > 0:
                print(f"Drew {drawn} card(s).")
        
        # Reset card states for new turn
        for card in player_hand:
            card.reset_turn()
        
        # Roll dice
        available_dice = player_roll()
        
        # Player action phase
        while available_dice and player_hand:
            display_hand(player_hand)
            display_dice(available_dice)
            
            print("\nOptions:")
            print("0) End Turn")
            for i in range(len(player_hand)):
                print(f"{i+1}) Add die to {player_hand[i].name}")
            
            valid_options = list(range(len(player_hand) + 1))
            choice = get_valid_input("\nWhat will you do? ", valid_options)
            
            if choice == 0:
                print("Ending turn...")
                break
            
            # Player chose a card
            card_idx = choice - 1
            selected_card = player_hand[card_idx]
            
            # Show which dice can be used
            print(f"\nSelected: {selected_card.name}")
            print(f"Available dice: {available_dice}")
            
            die_choice = get_valid_input(f"Which die to use? (1-{len(available_dice)}, 0 to cancel) ", 
                                        list(range(len(available_dice) + 1)))
            
            if die_choice == 0:
                continue
            
            die_idx = die_choice - 1
            die_value = available_dice[die_idx]
            
            # Try to add die to card
            if selected_card.add_die(die_value):
                available_dice.pop(die_idx)
                print(f"Added {die_value} to {selected_card.name}!")
                
                # Check if card is ready to activate
                if selected_card.is_ready():
                    activate = get_valid_input(f"Activate {selected_card.name}? (1=Yes, 2=Wait) ", [1, 2])
                    
                    if activate == 1:
                        result = selected_card.activate(None, enemy_obj)
                        print(f"\n>>> {result['message']}")
                        
                        # Apply effects
                        if result['effect_type'] == 'damage':
                            enemy_obj.currenthp -= result['damage_dealt']
                            print(f"{enemy_obj.name} takes {result['damage_dealt']} damage!")
                        
                        # Remove card from hand and add to discard
                        player_discard.append(player_hand.pop(card_idx))
                        
                        if enemy_obj.currenthp <= 0:
                            print(f"\n🎉 {enemy_obj.name} has been defeated! 🎉")
                            return True  # Player wins
            else:
                print(Back.WHITE + Fore.RED + Style.BRIGHT + f"\nCannot add die {die_value} to {selected_card.name}!" + Style.RESET_ALL)
        
        if enemy_obj.currenthp <= 0:
            break
        
        # === ENEMY TURN ===
        print(f"\n>>> {enemy_obj.name.upper()}'S TURN <<<")
        
        # Draw back to hand size
        cards_to_draw = enemy_hand_size - len(enemy_hand)
        if cards_to_draw > 0:
            draw_cards(enemy_deck, enemy_discard, enemy_hand, cards_to_draw)
        
        # Reset enemy card states
        for card in enemy_hand:
            card.reset_turn()
        
        # Enemy rolls dice
        enemy_dice = []
        for _ in range(enemy_dice_count):
            enemy_dice.append(random.randint(1, 6))
        print(f"{enemy_obj.name} rolls {enemy_dice_count} dice...")
        
        # Simple enemy AI - fill cards and activate when ready
        for die in enemy_dice[:]:
            if not enemy_hand:
                break
            
            for card in enemy_hand[:]:
                if card.add_die(die):
                    enemy_dice.remove(die)
                    print(f"{enemy_obj.name} uses {die} on {card.name}")
                    
                    if card.is_ready():
                        result = card.activate(enemy_obj, None)
                        print(f"{enemy_obj.name}'s {result['message']}")
                        
                        # Apply effects to player
                        if result['effect_type'] == 'damage':
                            player_current_hp -= result['damage_dealt']
                            print(f"You take {result['damage_dealt']} damage!")
                        
                        # Discard used card
                        enemy_discard.append(enemy_hand.pop(enemy_hand.index(card)))
                    break
        
        if player_current_hp <= 0:
            print(f"\n💀 You have been defeated... 💀")
            return False  # Player loses
    
    return player_current_hp > 0

"""
Regions:
1) Plains
2) Tundra
3) Forest
4) Ruins
5) Slopes
5) Pit
"""



hand=[]
discard=[]
enemy_hand=[]


# Get a working combat loop next


while play != 0:
    play_choice = get_valid_input("You stoke the \n1) Descend\n2) Quit\n", [1, 2])
    
    if play_choice == 2:
        play = "quit"
        break
    if play != "quit":
        print("A strange force draws you deeper into the dungeon...")
        print("...")
        print("...")
        opp = dummy  # Choose opponent (can expand this later)
        opp.currenthp = opp.max_hp
        
        # Give enemy a simple deck
        # enemy_deck = [create_sword(), create_dagger(), create_hammer()]

        enemy_deck=[]
        enemy_discard = []
        
        print(f"Something approaches... {opp.name} appears from the darkness!")
        
        # Start combat
        victory = combat_loop(deck, discard, hand_size, dice_count,
                            opp, enemy_deck, enemy_discard, 2, 2,
                            currenthp, charname)
        
        if not victory:
            print("\nGAME OVER")
            play = 0





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