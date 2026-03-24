#!/usr/bin/env python3
"""Test script to verify card effects are working correctly."""

import sys
sys.path.insert(0, '.')

from dice_dungeon import (
    Card, Entity, Enemy, Player, create_card_from_ability, 
    apply_effect_result, get_creature, CREATURE_DEFINITIONS, CARD_PROGRESSIONS
)

def test_damage_card():
    """Test a basic damage card."""
    print("\n=== TEST 1: Damage Card ===")
    
    # Create player and enemy
    player = Entity("Player", max_hp=50)
    enemy = Entity("Enemy", max_hp=30)
    player.shield = 5
    enemy.shield = 3
    
    # Create a simple damage card: "Deal 10 damage"
    card = create_card_from_ability({
        'name': 'Jab',
        'requirement': '',
        'effect': 'Deal 8 damage'
    })
    
    print(f"Player: {player.currenthp} HP, {player.shield} Shield")
    print(f"Enemy: {enemy.currenthp} HP, {enemy.shield} Shield")
    print(f"Playing: {card.name} ({card.description})")
    
    # Apply effect with dice result
    result = {'dice_used': [3]}  # Single die showing 3
    side_effects = apply_effect_result(card, player, enemy, result)
    
    print(f"After card use:")
    print(f"Enemy: {enemy.currenthp} HP (was 30)")
    print(f"Side effects: {side_effects}")
    assert enemy.currenthp == 22, f"Expected 22 HP, got {enemy.currenthp}"
    print("✓ Damage card works!")

def test_healing_card():
    """Test a healing card."""
    print("\n=== TEST 2: Healing Card ===")
    
    player = Entity("Player", max_hp=50, currenthp=30)
    enemy = Entity("Enemy", max_hp=30)
    
    card = create_card_from_ability({
        'name': 'Fortify',
        'requirement': '',
        'effect': 'Heal 5 HP'
    })
    
    print(f"Player: {player.currenthp}/{player.max_hp} HP")
    print(f"Playing: {card.name} ({card.description})")
    
    result = {'dice_used': []}
    side_effects = apply_effect_result(card, player, enemy, result)
    
    print(f"After card use: {player.currenthp}/{player.max_hp} HP")
    assert player.currenthp == 35, f"Expected 35 HP, got {player.currenthp}"
    print("✓ Healing card works!")

def test_shield_card():
    """Test a shield gain card."""
    print("\n=== TEST 3: Shield Card ===")
    
    player = Entity("Player", max_hp=50)
    enemy = Entity("Enemy", max_hp=30)
    
    player.shield = 0
    
    card = create_card_from_ability({
        'name': 'Fortify',
        'requirement': '',
        'effect': 'Gain 3 shield'
    })
    
    print(f"Player: {player.currenthp} HP, {player.shield} Shield")
    print(f"Playing: {card.name}")
    
    result = {'dice_used': []}
    side_effects = apply_effect_result(card, player, enemy, result)
    
    print(f"After: {player.shield} Shield")
    assert player.shield == 3, f"Expected 3 shield, got {player.shield}"
    print("✓ Shield card works!")

def test_status_effect_card():
    """Test applying status effects."""
    print("\n=== TEST 4: Status Effect Card ===")
    
    player = Entity("Player", max_hp=50)
    enemy = Entity("Enemy", max_hp=30)
    
    card = create_card_from_ability({
        'name': 'Poison Strike',
        'requirement': '',
        'effect': 'Deal 5 damage, Apply 2 Poison'
    })
    
    print(f"Enemy: {enemy.currenthp} HP, {enemy.status_effects['poison'].stacks if hasattr(enemy.status_effects['poison'], 'stacks') else 0} Poison")
    print(f"Playing: {card.name}")
    
    result = {'dice_used': []}
    side_effects = apply_effect_result(card, player, enemy, result)
    
    poison = enemy.get_status_effect('poison')
    print(f"After: {enemy.currenthp} HP, {poison.stacks if poison and poison.has_stacks() else 0} Poison stacks")
    assert enemy.currenthp == 25, f"Expected 25 HP, got {enemy.currenthp}"
    assert poison.has_stacks() and poison.stacks == 2, f"Expected 2 poison, got {poison.stacks if poison else 0}"
    print("✓ Status effect card works!")

def test_dice_damage_card():
    """Test a card that uses die value for damage."""
    print("\n=== TEST 5: Dice-Based Damage Card ===")
    
    player = Entity("Player", max_hp=50)
    enemy = Entity("Enemy", max_hp=30)
    
    card = create_card_from_ability({
        'name': 'Bite',
        'requirement': '',
        'effect': 'Deal die value damage'
    })
    
    print(f"Enemy: {enemy.currenthp} HP")
    print(f"Playing: {card.name} with die value = 5")
    
    result = {'dice_used': [5]}
    side_effects = apply_effect_result(card, player, enemy, result)
    
    print(f"After: {enemy.currenthp} HP (expected 25)")
    assert enemy.currenthp == 25, f"Expected 25 HP, got {enemy.currenthp}"
    print("✓ Dice-based damage card works!")

def test_multi_effect_card():
    """Test a card with multiple effects."""
    print("\n=== TEST 6: Multi-Effect Card ===")
    
    player = Entity("Player", max_hp=50, currenthp=25)
    enemy = Entity("Enemy", max_hp=40)
    
    # This would be a real card like: "Deal 3 damage, Heal 2 HP, Apply 1 Poison"
    card = create_card_from_ability({
        'name': 'Complex Card',
        'requirement': '',
        'effect': 'Deal 3 damage, Heal 2 HP, Apply 1 Poison'
    })
    
    print(f"Player: {player.currenthp}/{player.max_hp} HP")
    print(f"Enemy: {enemy.currenthp} HP")
    print(f"Playing: {card.name}")
    
    result = {'dice_used': []}
    side_effects = apply_effect_result(card, player, enemy, result)
    
    print(f"After:")
    print(f"  Player: {player.currenthp}/{player.max_hp} HP")
    print(f"  Enemy: {enemy.currenthp} HP, {enemy.get_status_effect('poison').stacks if enemy.get_status_effect('poison').has_stacks() else 0} Poison")
    
    # The card should deal damage AND heal AND apply poison
    assert player.currenthp >= 27, f"Expected at least 27 HP, got {player.currenthp}"
    print("✓ Multi-effect card works!")

def test_creature_combat():
    """Test that creatures have proper cards and can use them."""
    print("\n=== TEST 7: Creature Card Pool ===")
    
    # Get a test creature
    wolf = get_creature("Dire Wolves")
    print(f"Creature: {wolf.name} ({wolf.currenthp}/{wolf.max_hp} HP, {len(wolf.cardpool)} cards)")
    print(f"Hand: {len(wolf.hand)} cards")
    print(f"Cards in pool: {[c.name for c in wolf.cardpool]}")
    
    assert len(wolf.cardpool) > 0, "Creature should have cards in cardpool"
    assert len(wolf.hand) > 0, "Creature should have cards in hand"
    print("✓ Creature has proper cards!")

if __name__ == '__main__':
    try:
        test_damage_card()
        test_healing_card()
        test_shield_card()
        test_status_effect_card()
        test_dice_damage_card()
        test_multi_effect_card()
        test_creature_combat()
        print("\n" + "="*50)
        print("✓ ALL TESTS PASSED!")
        print("="*50)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
