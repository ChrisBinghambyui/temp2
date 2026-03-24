"""
Safe Town Loop - Main Gameplay Loop
This is the central loop where the player returns after each adventure.

USAGE:
------
Import this module and create a player_state dict, then call safe_town_loop():

    from safe_town_loop import safe_town_loop
    
    player_state = {
        'name': 'Adventurer',
        'current_hp': 20,
        'max_hp': 20,
        'xp': 0,
        'gold': 0,
        'difficulty': 'normal',  # 'easy', 'normal', or 'punishing'
        'deck': [card1, card2, card3],
        'level': 1,
        'current_biome': 1,
        'current_biome_tier': 1
    }
    
    final_state = safe_town_loop(player_state)

You need to have the following imported from your main game file:
- typingPrint(text, delay=None, typing_speed=0.05)
- get_valid_input(prompt, valid_options)
- run_basic_combat_loop(biome, tier, player_hp, player_max_hp, player_deck)
- _format_biome_tier_label(biome_id, tier)
"""

from colorama import Fore, Style
from Rest_loop import typingPrint
from Rest_loop import get_valid_input
from Rest_loop import run_basic_combat_loop
from Rest_loop import _format_biome_tier_label

def safe_town_loop(player_state):
    """
    Main gameplay loop for the safe town.
    
    Args:
        player_state (dict): Player state dictionary containing:
            - name: Player name
            - current_hp: Current health
            - max_hp: Maximum health
            - xp: Experience points
            - gold: Gold/currency
            - difficulty: "easy", "normal", or "punishing"
            - deck: List of cards in deck
            - level: Player level
            - current_biome: Current biome ID (1-6)
            - current_biome_tier: Current biome tier (1-3)
    
    Returns:
        dict: Final player state when quitting
    """
    
    while True:
        # Display town status
        typingPrint(
            f"\n{'='*50}\n"
            f"{player_state['name'].upper()} - ASCUS TAVERN\n"
            f"{'='*50}",
            delay=0
        )
        typingPrint(
            f"HP: {player_state['current_hp']}/{player_state['max_hp']} | "
            f"Level: {player_state['level']} | "
            f"XP: {player_state['xp']} | "
            f"Gold: {player_state['gold']}",
            delay=0
        )
        typingPrint(
            f"Difficulty: {player_state['difficulty'].upper()} | "
            f"Location: {_format_biome_tier_label(player_state['current_biome'], player_state['current_biome_tier'])}",
            delay=0
        )
        
        # Display menu
        menu_text = (
            "\nWhat would you like to do?\n"
            "1) Go on an adventure\n"
            "2) Rest and heal\n"
            "3) Check inventory\n"
            "4) Change difficulty\n"
            "5) Manage deck (coming soon)\n"
            "6) Shop (coming soon)\n"
            "7) Quit game\n"
            "\t>"
        )
        
        choice = get_valid_input(menu_text, [1, 2, 3, 4, 5, 6, 7])
        
        if choice == 1:
            # Go on adventure
            adventure_result = _run_adventure(player_state)
            if adventure_result:
                player_state = adventure_result
        
        elif choice == 2:
            # Rest and heal
            if player_state['current_hp'] < player_state['max_hp']:
                heal_amount = player_state['max_hp'] - player_state['current_hp']
                player_state['current_hp'] = player_state['max_hp']
                typingPrint(f"You rest in a cozy bed at the tavern and recover {heal_amount} HP.")
                typingPrint("You sleep peacefully and wake refreshed.")
            else:
                typingPrint("You're already at full health!")
        
        elif choice == 3:
            # Check inventory
            _display_inventory(player_state)
        
        elif choice == 4:
            # Change difficulty
            difficulty_choice = get_valid_input(
                "\nSelect difficulty:\n"
                "1) Easy (keep all loot on loss)\n"
                "2) Normal (lose 50% loot on loss)\n"
                "3) Punishing (lose all loot on loss)\n"
                "\t>",
                [1, 2, 3]
            )
            difficulties = {1: "easy", 2: "normal", 3: "punishing"}
            player_state['difficulty'] = difficulties[difficulty_choice]
            typingPrint(f"Difficulty set to {player_state['difficulty'].upper()}.")
        
        elif choice == 5:
            typingPrint("Deck management coming soon! Return later.")
        
        elif choice == 6:
            typingPrint("The shop is not yet open. Return later.")
        
        elif choice == 7:
            # Quit
            typingPrint("\nGathering your belongings, you bid farewell to Thessa and Ascus.")
            typingPrint("Perhaps you'll return someday...")
            return player_state


def _run_adventure(player_state):
    """
    Run an adventure encounter and handle results.
    
    Args:
        player_state (dict): Current player state
    
    Returns:
        dict: Updated player state after adventure
    """
    
    # Store state before adventure
    xp_before = player_state['xp']
    gold_before = player_state['gold']
    hp_before = player_state['current_hp']
    
    # Run combat
    typingPrint(f"\nYou venture into {_format_biome_tier_label(player_state['current_biome'], player_state['current_biome_tier'])}...")
    
    encounter_result = run_basic_combat_loop(
        player_state['current_biome'],
        player_state['current_biome_tier'],
        player_hp=player_state['current_hp'],
        player_max_hp=player_state['max_hp'],
        player_deck=player_state['deck']
    )
    
    if encounter_result is None:
        typingPrint("The adventure failed to start. You return to town.")
        return player_state
    
    # Update HP from adventure
    player_state['current_hp'] = max(0, encounter_result['player_hp'])
    
    # Handle victory/defeat
    if encounter_result['result'] == 'victory':
        _handle_victory(player_state, xp_before, gold_before)
    else:
        _handle_defeat(player_state, xp_before, gold_before)
    
    return player_state


def _handle_victory(player_state, xp_before, gold_before):
    """
    Handle a successful adventure.
    Player keeps all loot regardless of difficulty.
    """
    typingPrint("\n" + Fore.GREEN + "VICTORY!" + Style.RESET_ALL)
    typingPrint("You return to Ascus, victorious!")
    
    # Generate loot (can expand this later)
    xp_gained = 100 + (player_state['current_biome_tier'] * 50)
    gold_gained = 50 + (player_state['current_biome_tier'] * 25)
    
    player_state['xp'] += xp_gained
    player_state['gold'] += gold_gained
    
    typingPrint(f"You gained {xp_gained} XP and {gold_gained} gold!")
    
    # Check for level up
    xp_for_level = 500 + (player_state['level'] * 200)
    while player_state['xp'] >= xp_for_level:
        player_state['level'] += 1
        player_state['xp'] -= xp_for_level
        player_state['max_hp'] += 5
        player_state['current_hp'] = player_state['max_hp']
        xp_for_level = 500 + (player_state['level'] * 200)
        typingPrint(f"\n" + Fore.YELLOW + f"LEVEL UP! You are now level {player_state['level']}!" + Style.RESET_ALL)


def _handle_defeat(player_state, xp_before, gold_before):
    """
    Handle a defeated adventure.
    Loot retention depends on difficulty.
    """
    typingPrint("\n" + Fore.RED + "DEFEAT!" + Style.RESET_ALL)
    typingPrint("You barely escaped with your life and return to Ascus, wounded.")
    
    # Calculate loot loss based on difficulty
    difficulty = player_state['difficulty'].lower()
    
    if difficulty == 'easy':
        # Keep everything
        xp_lost = 0
        gold_lost = 0
        typingPrint("Fortunately, easy mode lets you keep all your spoils...")
    
    elif difficulty == 'normal':
        # Lose 50%
        xp_lost = int(player_state['xp'] * 0.5)
        gold_lost = int(player_state['gold'] * 0.5)
        player_state['xp'] -= xp_lost
        player_state['gold'] -= gold_lost
        typingPrint(f"You lost {xp_lost} XP and {gold_lost} gold in the ordeal.")
    
    elif difficulty == 'punishing':
        # Lose everything
        xp_lost = player_state['xp']
        gold_lost = player_state['gold']
        player_state['xp'] = 0
        player_state['gold'] = 0
        typingPrint(f"You lost all {xp_lost} XP and {gold_lost} gold!")
    
    # Heal some HP back as player returns to town
    player_state['current_hp'] = min(
        player_state['max_hp'],
        player_state['current_hp'] + int(player_state['max_hp'] * 0.3)
    )


def _display_inventory(player_state):
    """
    Display player's inventory and stats.
    """
    typingPrint("\n" + "="*40)
    typingPrint("INVENTORY")
    typingPrint("="*40)
    typingPrint(f"Name: {player_state['name']}")
    typingPrint(f"Level: {player_state['level']}")
    typingPrint(f"HP: {player_state['current_hp']}/{player_state['max_hp']}")
    typingPrint(f"XP: {player_state['xp']}")
    typingPrint(f"Gold: {player_state['gold']}")
    typingPrint(f"Difficulty: {player_state['difficulty'].upper()}")
    typingPrint(f"Cards in deck: {len(player_state['deck'])}")
    
    if player_state['deck']:
        typingPrint("\nDeck cards:", delay=0)
        for i, card in enumerate(player_state['deck'], 1):
            card_name = card.name if hasattr(card, 'name') else str(card)
            typingPrint(f"  {i}) {card_name}", delay=0)
    
    typingPrint("="*40)
