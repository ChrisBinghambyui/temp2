#!/usr/bin/env python3
"""Test of dice_dungeon.py import, creature initialization, and status effects."""

try:
    import dice_dungeon
    print("✓ Import successful")
    print(f"  Creatures: {len(dice_dungeon.CREATURE_DEFINITIONS)}")
    print(f"  Card families: {len(dice_dungeon.CARD_PROGRESSIONS)}")
    print(f"  Card definitions: {len(dice_dungeon.CARD_DEFINITIONS)}")
    
    # Test creature instantiation
    print("\n✓ Testing creature instantiation:")
    wolf = dice_dungeon.get_creature("Wolf")
    print(f"  Wolf: {wolf.name}, HP {wolf.max_hp}, {len(wolf.hand)} cards in hand")
    for card in wolf.hand:
        print(f"    - {card.name}")
    
    # Test status effects
    print("\n✓ Testing Status Effect System:")
    player = dice_dungeon.Entity("TestPlayer", max_hp=50, currenthp=50)
    print(f"  Player: {player.name}, HP {player.currenthp}/{player.max_hp}")
    print(f"  Active statuses: {player.display_statuses()}")
    
    # Apply some status effects
    player.apply_status('poison', 3)
    player.apply_status('bleed', 2)
    player.apply_status('blind', 1)
    print(f"\n  Applied Poison x3, Bleed x2, Blind x1")
    print(f"  Active statuses: {player.display_statuses()}")
    
    # Get specific status effect
    poison_effect = player.get_status_effect('poison')
    print(f"\n  Poison effect: {poison_effect}")
    print(f"  Poison has stacks: {poison_effect.has_stacks()}")
    
    # Test end-of-turn poison damage
    print(f"\n  Before end-of-turn: HP = {player.currenthp}, Poison stacks = {poison_effect.stacks}")
    player.resolve_end_of_turn()
    print(f"  After end-of-turn: HP = {player.currenthp}, Poison stacks = {poison_effect.stacks}")
    
    # Test removing negative effects
    print(f"\n  Active statuses before clear: {player.display_statuses()}")
    player.remove_negative_effects()
    print(f"  Active statuses after clear: {player.display_statuses()}")
    
    print("\n✓ All tests passed!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
