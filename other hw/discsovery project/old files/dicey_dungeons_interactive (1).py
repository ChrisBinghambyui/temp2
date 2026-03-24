#!/usr/bin/env python3
"""
DICEY DUNGEONS - Merged Best Implementation
Combines the comprehensive card system from dicey_dungeons-claude-ed.py
with the better combat loop from dice_dungeon.py
"""

import random
import sys
import math
from colorama import init, Fore, Back, Style

# ============================================================================
# CARD SYSTEM (from dicey_dungeons-claude-ed.py)
# ============================================================================

class Card:
    """A flexible card class for Dicey Dungeons-style gameplay."""
    
    def __init__(self, name, card_type='single', effect_type='damage', 
                 base_value=0, uses_dice_value=True, reusable=False, 
                 max_uses=None, cooldown=0, max_dice=1,
                 dice_restriction=None, target='enemy', 
                 status_effect=None, status_duration=0,
                 upgrade_level='base', description="", class_restricted=None, 
                 value_fn=None, once_per_combat=False, limit_value=0,
                 conditional_fn=None, special_effect=None, sacrifice_hp=0):
        
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
        self.value_fn = value_fn
        self.class_restricted = class_restricted
        self.once_per_combat = once_per_combat
        self.used_this_combat = False
        self.limit_value = limit_value
        self.current_limit = limit_value
        self.conditional_fn = conditional_fn
        self.special_effect = special_effect or {}
        self.sacrifice_hp = sacrifice_hp
        self.uses_this_turn = 0
        self.dice_slots = []
        
    def can_accept_die(self, die_value):
        """Check if this card can accept a die of this value."""
        if self.current_cooldown > 0:
            return False
        if self.once_per_combat and self.used_this_combat:
            return False
        if not self.reusable and self.uses_this_turn > 0:
            return False
        if self.max_uses and self.uses_this_turn >= self.max_uses:
            return False
        if len(self.dice_slots) >= self.max_dice:
            return False
        if self.card_type == 'limit':
            if self.current_limit - die_value < 0:
                return False
        
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
            if self.card_type == 'limit':
                self.current_limit -= die_value
            return True
        return False
    
    def is_ready(self):
        """Check if card has enough dice to activate."""
        if self.card_type == 'limit':
            return self.current_limit <= 0 and len(self.dice_slots) > 0
        elif self.card_type == 'passive':
            return True
        else:
            return len(self.dice_slots) > 0
    
    def calculate_effect(self):
        """Calculate the effect value based on dice and card properties."""
        if self.value_fn:
            return self.value_fn(self.dice_slots, self)
        
        total = self.base_value
        if self.uses_dice_value:
            total += sum(self.dice_slots)
        return total
    
    def activate(self, user, target_entity):
        """Activate the card's effect."""
        if not self.is_ready():
            return {'success': False, 'message': 'Card not ready'}
        if self.once_per_combat and self.used_this_combat:
            return {'success': False, 'message': 'Already used this combat'}
        
        result = {
            'success': True,
            'card_name': self.name,
            'dice_used': self.dice_slots.copy(),
            'effects': [],
            'value': self.calculate_effect(),
            'effect_type': self.effect_type,
            'target': self.target,
            'sacrifice_hp': self.sacrifice_hp,
            'status_effect': self.status_effect,
            'status_duration': self.status_duration
        }
        
        if self.conditional_fn:
            conditional_result = self.conditional_fn(user, target_entity, self.dice_slots)
            if conditional_result:
                result['effects'].extend(conditional_result)
                
        self.dice_slots = []
        self.uses_this_turn += 1
        if self.once_per_combat:
            self.used_this_combat = True
        if self.card_type == 'limit':
            self.current_limit = self.limit_value
        if self.cooldown > 0:
            self.current_cooldown = self.cooldown
            
        return result
    
    def reset_turn(self):
        """Reset card state for new turn."""
        self.uses_this_turn = 0
        self.dice_slots = []
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
    
    def reset_combat(self):
        """Reset card state for new combat."""
        self.reset_turn()
        self.used_this_combat = False
        self.current_limit = self.limit_value
        
    def get_display_text(self):
        """Get formatted display text for the card."""
        text = f"{self.name}"
        if self.upgrade_level != 'base':
            text += f" {self.upgrade_level}"
        slots = "□" * (self.max_dice - len(self.dice_slots)) + "■" * len(self.dice_slots)
        text += f" [{slots}]"
        if self.card_type == 'limit':
            text += f" Limit: {self.current_limit}/{self.limit_value}"
        if self.current_cooldown > 0:
            text += f" (CD: {self.current_cooldown})"
        if self.once_per_combat:
            text += " (Once per combat)" if not self.used_this_combat else " (USED)"
        return text


# ============================================================================
# CARD CREATION FUNCTIONS (sample from first file)
# ============================================================================

def create_bite(upgrade='base'):
    """Basic attack card."""
    configs = {
        'base': {'base_value': 3, 'uses_dice_value': False, 'max_dice': 1, 'desc': 'Deal 3 damage'},
        'x': {'base_value': 0, 'uses_dice_value': True, 'max_dice': 1, 'desc': 'Deal damage equal to die value'},
        'y': {'base_value': 4, 'uses_dice_value': False, 'max_dice': 1, 'reusable': True, 'desc': 'Deal 4 damage (reusable)'},
        'X': {'base_value': 2, 'uses_dice_value': True, 'max_dice': 1, 'desc': 'Deal 2 + die value damage'},
        'Y': {'base_value': 5, 'uses_dice_value': False, 'max_dice': 1, 'reusable': True, 'desc': 'Deal 5 damage, heal 1 (reusable)'}
    }
    config = configs.get(upgrade, configs['base'])
    return Card(
        name='Bite',
        card_type='single',
        effect_type='damage',
        upgrade_level=upgrade,
        description=config['desc'],
        **{k: v for k, v in config.items() if k != 'desc'}
    )

def create_jab(upgrade='base'):
    """Quick attack card."""
    configs = {
        'base': {'base_value': 0, 'uses_dice_value': True, 'max_dice': 1, 'desc': 'Deal damage equal to die value'},
        'x': {'base_value': 2, 'uses_dice_value': True, 'max_dice': 1, 'desc': 'Deal 2 + die value damage'},
        'y': {'base_value': 0, 'uses_dice_value': True, 'max_dice': 1, 'reusable': True, 'desc': 'Deal damage equal to die value (reusable)'},
    }
    config = configs.get(upgrade, configs['base'])
    return Card(
        name='Jab',
        card_type='single',
        effect_type='damage',
        upgrade_level=upgrade,
        description=config['desc'],
        **{k: v for k, v in config.items() if k != 'desc'}
    )

def create_shield(upgrade='base'):
    """Defense card."""
    configs = {
        'base': {'base_value': 0, 'uses_dice_value': True, 'max_dice': 1, 'dice_restriction': {'only_even': True}, 
                 'desc': 'Gain shield equal to half the die value (even only)'},
        'x': {'base_value': 0, 'uses_dice_value': True, 'max_dice': 1, 'dice_restriction': {'only_even': True},
              'desc': 'Gain shield equal to the die value (even only)'},
    }
    config = configs.get(upgrade, configs['base'])
    
    def shield_value_fn(dice_slots, card):
        if upgrade == 'base':
            return sum(dice_slots) // 2
        return sum(dice_slots)
    
    return Card(
        name='Shield',
        card_type='single',
        effect_type='shield',
        target='self',
        upgrade_level=upgrade,
        description=config['desc'],
        value_fn=shield_value_fn,
        **{k: v for k, v in config.items() if k not in ['desc']}
    )

def create_fortify(upgrade='base'):
    """Defense boost card."""
    configs = {
        'base': {'base_value': 3, 'uses_dice_value': False, 'max_dice': 1, 'desc': 'Gain 3 shield'},
        'x': {'base_value': 4, 'uses_dice_value': False, 'max_dice': 1, 'desc': 'Gain 4 shield and apply 1 blind'},
    }
    config = configs.get(upgrade, configs['base'])
    return Card(
        name='Fortify',
        card_type='single',
        effect_type='shield',
        target='self',
        upgrade_level=upgrade,
        description=config['desc'],
        status_effect='blind' if upgrade == 'x' else None,
        status_duration=1 if upgrade == 'x' else 0,
        **{k: v for k, v in config.items() if k != 'desc'}
    )

def create_charge(upgrade='base'):
    """Limit card - powerful attack."""
    configs = {
        'base': {'limit_value': 15, 'base_value': 8, 'uses_dice_value': False, 'max_dice': 99,
                 'desc': 'Deal 8 damage, gain 3 shield (limit 15)'},
        'x': {'limit_value': 12, 'base_value': 10, 'uses_dice_value': False, 'max_dice': 99,
              'desc': 'Deal 10 damage, gain 4 shield (limit 12)'},
    }
    config = configs.get(upgrade, configs['base'])
    
    def charge_effect_fn(user, target, dice_slots):
        return [
            {'type': 'damage', 'value': config['base_value']},
            {'type': 'shield', 'value': 3 if upgrade == 'base' else 4, 'target': 'self'}
        ]
    
    return Card(
        name='Charge',
        card_type='limit',
        effect_type='damage',
        upgrade_level=upgrade,
        description=config['desc'],
        conditional_fn=charge_effect_fn,
        **{k: v for k, v in config.items() if k != 'desc'}
    )

def create_life_drain(upgrade='base'):
    """Heal + damage card."""
    configs = {
        'base': {'base_value': 3, 'uses_dice_value': False, 'max_dice': 1, 'desc': 'Deal 3 damage, heal 1'},
        'x': {'base_value': 4, 'uses_dice_value': False, 'max_dice': 1, 'desc': 'Deal 4 damage, heal 2'},
    }
    config = configs.get(upgrade, configs['base'])
    
    def life_drain_effect_fn(user, target, dice_slots):
        heal_amount = 1 if upgrade == 'base' else 2
        return [
            {'type': 'damage', 'value': config['base_value']},
            {'type': 'heal', 'value': heal_amount, 'target': 'self'}
        ]
    
    return Card(
        name='Life Drain',
        card_type='single',
        effect_type='damage',
        upgrade_level=upgrade,
        description=config['desc'],
        conditional_fn=life_drain_effect_fn,
        **{k: v for k, v in config.items() if k != 'desc'}
    )

def create_gore(upgrade='base'):
    """Attack with bleed chance."""
    configs = {
        'base': {'base_value': 0, 'uses_dice_value': True, 'max_dice': 1, 'desc': 'Deal damage equal to die value, on 6: apply 1 bleed'},
        'x': {'base_value': 2, 'uses_dice_value': True, 'max_dice': 1, 'desc': 'Deal 2 + die value damage, on 6: apply 1 bleed'},
    }
    config = configs.get(upgrade, configs['base'])
    
    def gore_effect_fn(user, target, dice_slots):
        effects = []
        if dice_slots and dice_slots[0] == 6:
            effects.append({'type': 'status', 'status': 'bleed', 'duration': 1})
        return effects
    
    return Card(
        name='Gore',
        card_type='single',
        effect_type='damage',
        upgrade_level=upgrade,
        description=config['desc'],
        conditional_fn=gore_effect_fn,
        **{k: v for k, v in config.items() if k != 'desc'}
    )

def create_dagger(upgrade='base'):
    """Quick poison attack."""
    configs = {
        'base': {'base_value': 2, 'uses_dice_value': False, 'max_dice': 1, 'desc': 'Deal 2 damage'},
        'x': {'base_value': 3, 'uses_dice_value': False, 'max_dice': 1, 'desc': 'Deal 3 damage, apply 1 poison'},
    }
    config = configs.get(upgrade, configs['base'])
    return Card(
        name='Dagger',
        card_type='single',
        effect_type='damage',
        upgrade_level=upgrade,
        description=config['desc'],
        status_effect='poison' if upgrade == 'x' else None,
        status_duration=1 if upgrade == 'x' else 0,
        **{k: v for k, v in config.items() if k != 'desc'}
    )


def create_card(card_name, upgrade='base'):
    """Factory function to create cards by name."""
    card_creators = {
        'Bite': create_bite,
        'Jab': create_jab,
        'Shield': create_shield,
        'Fortify': create_fortify,
        'Charge': create_charge,
        'Life Drain': create_life_drain,
        'Gore': create_gore,
        'Dagger': create_dagger,
    }
    
    creator = card_creators.get(card_name)
    if creator:
        return creator(upgrade)
    return None


# ============================================================================
# ENTITY SYSTEM (from dice_dungeon.py with improvements)
# ============================================================================

class StatusEffect:
    """Represents a status effect on an entity."""
    def __init__(self, name, stacks=0):
        self.name = name
        self.stacks = stacks
    
    def add(self, amount):
        self.stacks += amount
    
    def remove(self, amount):
        self.stacks = max(0, self.stacks - amount)
    
    def trigger_on_card_use(self, entity, card):
        """Trigger effect when entity uses a card (e.g., bleed)."""
        if self.name == 'bleed' and self.stacks > 0:
            damage = self.stacks
            entity.currenthp -= damage
            print(f"  ⚠ Bleed deals {damage} damage to {entity.name}!")
            self.remove(1)

class Entity:
    """Base class for player and enemy."""
    def __init__(self, name, max_hp, num_dice):
        self.name = name
        self.max_hp = max_hp
        self.currenthp = max_hp
        self.shield = 0
        self.num_dice = num_dice
        self.dice_pool = []
        self.status_effects = {}
        self.deck = []
        self.hand = []
        self.discard = []
    
    def roll_dice(self):
        """Roll dice for this turn."""
        self.dice_pool = [random.randint(1, 6) for _ in range(self.num_dice)]
        return self.dice_pool
    
    def draw_cards(self, num):
        """Draw cards from deck to hand."""
        for _ in range(num):
            if not self.deck:
                # Shuffle discard back into deck
                self.deck = self.discard[:]
                self.discard = []
                random.shuffle(self.deck)
            
            if self.deck:
                self.hand.append(self.deck.pop())
    
    def take_damage(self, amount):
        """Apply damage, accounting for shield."""
        if amount <= 0:
            return 0
        
        if self.shield > 0:
            if self.shield >= amount:
                self.shield -= amount
                print(f"  🛡 {self.name}'s shield absorbs {amount} damage! ({self.shield} shield remaining)")
                return 0
            else:
                remaining = amount - self.shield
                print(f"  🛡 {self.name}'s shield absorbs {self.shield} damage!")
                self.shield = 0
                self.currenthp -= remaining
                print(f"  💥 {self.name} takes {remaining} damage! ({self.currenthp}/{self.max_hp} HP)")
                return remaining
        else:
            self.currenthp -= amount
            print(f"  💥 {self.name} takes {amount} damage! ({self.currenthp}/{self.max_hp} HP)")
            return amount
    
    def heal(self, amount):
        """Heal HP."""
        old_hp = self.currenthp
        self.currenthp = min(self.max_hp, self.currenthp + amount)
        actual_heal = self.currenthp - old_hp
        if actual_heal > 0:
            print(f"  💚 {self.name} heals {actual_heal} HP! ({self.currenthp}/{self.max_hp} HP)")
    
    def add_shield(self, amount):
        """Add shield."""
        self.shield += amount
        print(f"  🛡 {self.name} gains {amount} shield! (Total: {self.shield})")
    
    def add_status(self, status_name, duration):
        """Add or stack a status effect."""
        if status_name not in self.status_effects:
            self.status_effects[status_name] = StatusEffect(status_name, 0)
        self.status_effects[status_name].add(duration)
        print(f"  ⚡ {self.name} receives {status_name} x{duration}!")
    
    def get_status_effect(self, name):
        """Get a status effect by name."""
        return self.status_effects.get(name)
    
    def process_turn_start(self):
        """Process status effects at turn start."""
        messages = []
        
        # Process poison
        if 'poison' in self.status_effects:
            poison = self.status_effects['poison']
            if poison.stacks > 0:
                self.currenthp -= poison.stacks
                messages.append(f"  ☠ Poison deals {poison.stacks} damage to {self.name}!")
                poison.remove(1)
        
        # Process frozen (reduces dice)
        if 'frozen' in self.status_effects:
            frozen = self.status_effects['frozen']
            if frozen.stacks > 0:
                messages.append(f"  ❄ {self.name} is frozen (dice reduced)!")
        
        return messages
    
    def process_turn_end(self):
        """Process status effects at turn end."""
        # Reset cards
        for card in self.hand + self.deck + self.discard:
            card.reset_turn()
    
    def is_alive(self):
        """Check if entity is alive."""
        return self.currenthp > 0
    
    def add_card_to_deck(self, card_name, upgrade='base'):
        """Add a card to the deck."""
        card = create_card(card_name, upgrade)
        if card:
            self.deck.append(card)
            return True
        return False


class Player(Entity):
    """Player character."""
    def __init__(self, name, max_hp=50, num_dice=3):
        super().__init__(name, max_hp, num_dice)


class Enemy(Entity):
    """Enemy character."""
    def __init__(self, name, hp=20, num_dice=2, deck_config=None):
        super().__init__(name, hp, num_dice)
        
        if deck_config:
            for card_name, upgrade in deck_config:
                self.add_card_to_deck(card_name, upgrade)


# ============================================================================
# COMBAT SYSTEM (improved from dice_dungeon.py)
# ============================================================================

def apply_card_effect(card_result, user, target):
    """Apply the effects of a card activation."""
    if not card_result.get('success'):
        return
    
    # Handle sacrifice HP
    if card_result.get('sacrifice_hp', 0) > 0:
        user.currenthp -= card_result['sacrifice_hp']
        print(f"  ❤ {user.name} sacrifices {card_result['sacrifice_hp']} HP!")
    
    # Handle main effect
    effect_type = card_result.get('effect_type')
    value = card_result.get('value', 0)
    target_type = card_result.get('target', 'enemy')
    
    actual_target = target if target_type == 'enemy' else user
    
    if effect_type == 'damage':
        actual_target.take_damage(value)
    elif effect_type == 'heal':
        actual_target.heal(value)
    elif effect_type == 'shield':
        actual_target.add_shield(value)
    
    # Handle status effects
    if card_result.get('status_effect') and card_result.get('status_duration', 0) > 0:
        target.add_status(card_result['status_effect'], card_result['status_duration'])
    
    # Handle additional effects from conditional_fn
    for effect in card_result.get('effects', []):
        effect_target = user if effect.get('target') == 'self' else target
        
        if effect['type'] == 'damage':
            effect_target.take_damage(effect['value'])
        elif effect['type'] == 'heal':
            effect_target.heal(effect['value'])
        elif effect['type'] == 'shield':
            effect_target.add_shield(effect['value'])
        elif effect['type'] == 'status':
            target.add_status(effect['status'], effect.get('duration', 1))


def combat_loop(player, enemy):
    """Main combat loop."""
    print("\n" + "=" * 70)
    print(f"⚔ COMBAT START: {player.name} vs {enemy.name}")
    print("=" * 70)
    
    turn_count = 0
    
    while player.is_alive() and enemy.is_alive():
        turn_count += 1
        print(f"\n{'='*70}")
        print(f"TURN {turn_count}")
        print(f"{'='*70}")
        
        # Process turn start effects
        player_msgs = player.process_turn_start()
        enemy_msgs = enemy.process_turn_start()
        for msg in player_msgs + enemy_msgs:
            print(msg)
        
        # Display status
        print(f"\n👤 {player.name}: {player.currenthp}/{player.max_hp} HP | {player.shield} Shield")
        print(f"👹 {enemy.name}: {enemy.currenthp}/{enemy.max_hp} HP | {enemy.shield} Shield")
        
        # Check for deaths from status effects
        if not player.is_alive():
            print(f"\n💀 {player.name} has fallen!")
            return False
        if not enemy.is_alive():
            print(f"\n🎉 {enemy.name} defeated!")
            return True
        
        # PLAYER TURN
        print(f"\n{'-'*70}")
        print("YOUR TURN")
        print(f"{'-'*70}")
        
        player.draw_cards(5)
        player.roll_dice()
        
        print(f"\n📋 Your Hand ({len(player.hand)} cards):")
        for i, card in enumerate(player.hand, 1):
            print(f"  {i}. {card.get_display_text()}")
            print(f"     {card.description}")
        
        print(f"\n🎲 Your Dice: {player.dice_pool}")
        
        # Player turn - use cards
        cards_used = 0
        while player.hand and player.dice_pool and cards_used < 3:
            # Simple AI: use first available card with first compatible die
            card_used = False
            for card in player.hand[:]:
                if card_used:
                    break
                for die in player.dice_pool[:]:
                    if card.can_accept_die(die):
                        card.add_die(die)
                        player.dice_pool.remove(die)
                        print(f"\n  ➤ Using {die} on {card.name}")
                        
                        if card.is_ready():
                            result = card.activate(player, enemy)
                            print(f"  ⚡ Activating {result['card_name']}!")
                            apply_card_effect(result, player, enemy)
                            
                            # Trigger bleed
                            bleed = player.get_status_effect('bleed')
                            if bleed and bleed.stacks > 0:
                                bleed.trigger_on_card_use(player, card)
                            
                            player.hand.remove(card)
                            player.discard.append(card)
                            cards_used += 1
                            card_used = True
                            break
                        break
            
            if not card_used:
                break
        
        # Discard remaining hand
        player.discard.extend(player.hand)
        player.hand = []
        
        # Check if enemy defeated
        if not enemy.is_alive():
            print(f"\n🎉 VICTORY! {enemy.name} defeated!")
            return True
        
        # ENEMY TURN
        print(f"\n{'-'*70}")
        print("ENEMY TURN")
        print(f"{'-'*70}")
        
        enemy.draw_cards(3)
        enemy.roll_dice()
        
        print(f"\n{enemy.name} draws cards and rolls dice...")
        
        # Enemy AI - simple random card play
        cards_used = 0
        while enemy.hand and enemy.dice_pool and cards_used < 2:
            card = random.choice(enemy.hand)
            die_used = False
            
            for die in enemy.dice_pool[:]:
                if card.can_accept_die(die):
                    card.add_die(die)
                    enemy.dice_pool.remove(die)
                    print(f"\n  {enemy.name} uses {die} on {card.name}")
                    
                    if card.is_ready():
                        result = card.activate(enemy, player)
                        print(f"  ⚡ {enemy.name} activates {result['card_name']}!")
                        apply_card_effect(result, enemy, player)
                        
                        # Trigger bleed
                        bleed = enemy.get_status_effect('bleed')
                        if bleed and bleed.stacks > 0:
                            bleed.trigger_on_card_use(enemy, card)
                        
                        enemy.hand.remove(card)
                        enemy.discard.append(card)
                        cards_used += 1
                        die_used = True
                        break
                    break
            
            if not die_used:
                break
        
        # Discard remaining hand
        enemy.discard.extend(enemy.hand)
        enemy.hand = []
        
        # Check if player defeated
        if not player.is_alive():
            print(f"\n💀 DEFEAT! {player.name} has fallen!")
            return False
        
        # Process turn end
        player.process_turn_end()
        enemy.process_turn_end()
        
        # Safety limit
        if turn_count > 30:
            print("\n⏱ Combat timeout!")
            return player.currenthp > enemy.currenthp
    
    return player.is_alive()


# ============================================================================
# GAME SETUP
# ============================================================================

def create_starter_deck():
    """Create a starter deck for the player."""
    return [
        ('Bite', 'base'),
        ('Bite', 'x'),
        ('Jab', 'base'),
        ('Jab', 'y'),
        ('Fortify', 'base'),
        ('Shield', 'base'),
        ('Charge', 'base'),
        ('Life Drain', 'base'),
    ]


def create_enemy_deck(difficulty=1):
    """Create an enemy deck based on difficulty."""
    if difficulty == 1:
        return [
            ('Bite', 'base'),
            ('Gore', 'base'),
            ('Jab', 'base'),
            ('Fortify', 'base'),
        ]
    elif difficulty == 2:
        return [
            ('Bite', 'x'),
            ('Gore', 'base'),
            ('Charge', 'base'),
            ('Dagger', 'x'),
            ('Shield', 'base'),
        ]
    else:
        return [
            ('Bite', 'X'),
            ('Gore', 'x'),
            ('Charge', 'x'),
            ('Life Drain', 'x'),
            ('Shield', 'x'),
            ('Dagger', 'x'),
        ]


# ============================================================================
# INPUT UTILITIES
# ============================================================================

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


def display_hand(hand):
    """Display the player's current hand of cards."""
    print("\n=== YOUR HAND ===")
    for i, card in enumerate(hand, 1):
        print(f"{i}) {card.get_display_text()}")
        print(f"   {card.description}")
    print("=" * 50)


def display_dice(dice_list):
    """Display available dice."""
    if dice_list:
        print(f"\n🎲 Available Dice: {dice_list}")
    else:
        print("\n🎲 No dice remaining!")


# ============================================================================
# INTERACTIVE COMBAT SYSTEM
# ============================================================================

def interactive_combat_loop(player, enemy):
    """Interactive combat loop where player makes choices."""
    print("\n" + "=" * 70)
    print(f"⚔ COMBAT START: {player.name} vs {enemy.name}")
    print("=" * 70)
    
    turn_count = 0
    
    while player.is_alive() and enemy.is_alive():
        turn_count += 1
        print(f"\n{'='*70}")
        print(f"TURN {turn_count}")
        print(f"{'='*70}")
        
        # Process turn start effects
        player_msgs = player.process_turn_start()
        enemy_msgs = enemy.process_turn_start()
        for msg in player_msgs + enemy_msgs:
            print(msg)
        
        # Display status
        print(f"\n👤 {player.name}: {player.currenthp}/{player.max_hp} HP | {player.shield} Shield")
        print(f"👹 {enemy.name}: {enemy.currenthp}/{enemy.max_hp} HP | {enemy.shield} Shield")
        
        # Check for deaths from status effects
        if not player.is_alive():
            print(f"\n💀 {player.name} has fallen!")
            return False
        if not enemy.is_alive():
            print(f"\n🎉 {enemy.name} defeated!")
            return True
        
        # PLAYER TURN
        print(f"\n{'-'*70}")
        print("YOUR TURN")
        print(f"{'-'*70}")
        
        player.draw_cards(5)
        player.roll_dice()
        
        available_dice = player.dice_pool[:]
        
        # Player action phase - interactive!
        while available_dice and player.hand:
            display_hand(player.hand)
            display_dice(available_dice)
            
            print("\nOptions:")
            print("0) End Turn")
            for i, card in enumerate(player.hand, 1):
                print(f"{i}) Add die to {card.name}")
            
            valid_options = list(range(len(player.hand) + 1))
            choice = get_valid_input("\nWhat will you do? ", valid_options)
            
            if choice == 0:
                print("Ending turn...")
                break
            
            # Player chose a card
            card_idx = choice - 1
            selected_card = player.hand[card_idx]
            
            # Show which dice can be used
            print(f"\nSelected: {selected_card.name}")
            print(f"  {selected_card.description}")
            print(f"  Slots: {selected_card.max_dice} | Filled: {len(selected_card.dice_slots)}")
            
            die_choice = get_valid_input(f"Which die to use? (1-{len(available_dice)}, 0 to cancel) ", 
                                        list(range(len(available_dice) + 1)))
            
            if die_choice == 0:
                continue
            
            die_idx = die_choice - 1
            die_value = available_dice[die_idx]
            
            # Try to add die to card
            if selected_card.can_accept_die(die_value):
                selected_card.add_die(die_value)
                available_dice.pop(die_idx)
                print(f"✓ Added {die_value} to {selected_card.name}!")
                
                # Check if card is ready to activate
                if selected_card.is_ready():
                    activate = get_valid_input(f"Activate {selected_card.name}? (1=Yes, 2=Wait) ", [1, 2])
                    
                    if activate == 1:
                        result = selected_card.activate(player, enemy)
                        print(f"\n⚡ Activating {result['card_name']}!")
                        apply_card_effect(result, player, enemy)
                        
                        # Trigger bleed
                        bleed = player.get_status_effect('bleed')
                        if bleed and bleed.stacks > 0:
                            bleed.trigger_on_card_use(player, selected_card)
                        
                        # Remove card from hand
                        player.hand.remove(selected_card)
                        player.discard.append(selected_card)
                        
                        if not enemy.is_alive():
                            print(f"\n🎉 VICTORY! {enemy.name} defeated!")
                            return True
            else:
                print(f"❌ Cannot add {die_value} to {selected_card.name} (check requirements)")
        
        # Discard remaining hand
        player.discard.extend(player.hand)
        player.hand = []
        
        # Check if enemy defeated
        if not enemy.is_alive():
            print(f"\n🎉 VICTORY! {enemy.name} defeated!")
            return True
        
        # ENEMY TURN
        print(f"\n{'-'*70}")
        print("ENEMY TURN")
        print(f"{'-'*70}")
        
        enemy.draw_cards(3)
        enemy.roll_dice()
        
        print(f"\n{enemy.name} draws cards and rolls dice...")
        
        # Enemy AI - simple random card play
        cards_used = 0
        while enemy.hand and enemy.dice_pool and cards_used < 2:
            card = random.choice(enemy.hand)
            die_used = False
            
            for die in enemy.dice_pool[:]:
                if card.can_accept_die(die):
                    card.add_die(die)
                    enemy.dice_pool.remove(die)
                    print(f"\n  {enemy.name} uses {die} on {card.name}")
                    
                    if card.is_ready():
                        result = card.activate(enemy, player)
                        print(f"  ⚡ {enemy.name} activates {result['card_name']}!")
                        apply_card_effect(result, enemy, player)
                        
                        # Trigger bleed
                        bleed = enemy.get_status_effect('bleed')
                        if bleed and bleed.stacks > 0:
                            bleed.trigger_on_card_use(enemy, card)
                        
                        enemy.hand.remove(card)
                        enemy.discard.append(card)
                        cards_used += 1
                        die_used = True
                        break
                    break
            
            if not die_used:
                break
        
        # Discard remaining hand
        enemy.discard.extend(enemy.hand)
        enemy.hand = []
        
        # Check if player defeated
        if not player.is_alive():
            print(f"\n💀 DEFEAT! {player.name} has fallen!")
            return False
        
        # Process turn end
        player.process_turn_end()
        enemy.process_turn_end()
        
        # Safety limit
        if turn_count > 30:
            print("\n⏱ Combat timeout!")
            return player.currenthp > enemy.currenthp
    
    return player.is_alive()


# ============================================================================
# MAIN GAME
# ============================================================================

def main():
    """Main game loop with character creation."""
    print("=" * 70)
    print(" " * 25 + "DICEY DUNGEONS")
    print(" " * 20 + "Interactive Edition")
    print("=" * 70)
    
    # Character creation
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
        num_dice = 2
        char_style = Style.BRIGHT + Fore.CYAN
    if clas == 2:
        charclass = "Knight"
        title = "Ser"
        num_dice = 2
        char_style = Style.BRIGHT + Fore.RED
    if clas == 3:
        charclass = "Cleric"
        title = "Vicar"
        num_dice = 2
        char_style = Style.BRIGHT + Fore.YELLOW
    if clas == 4:
        charclass = "Warlock"
        title = "Pactist"
        num_dice = 2
        char_style = Style.BRIGHT + Fore.BLUE
    if clas == 5:
        charclass = "Druid"
        title = "Warden"
        num_dice = 2
        char_style = Style.BRIGHT + Fore.GREEN
    if clas == 6:
        charclass = "Rogue"
        title = "Shade"
        num_dice = 2
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
    
    # Create player
    player = Player(charname.capitalize(), max_hp=hp, num_dice=num_dice)
    starter_deck = create_starter_deck()
    for card_name, upgrade in starter_deck:
        player.add_card_to_deck(card_name, upgrade)
    
    print(f"\n✓ Character created!")
    print(f"  Name: {player.name}")
    print(f"  Class: {charclass}")
    print(f"  HP: {player.max_hp}")
    print(f"  Dice: {player.num_dice}")
    print(f"  Deck: {len(player.deck)} cards")
    
    # Shuffle deck
    random.shuffle(player.deck)
    
    # Game loop
    playing = True
    while playing and player.is_alive():
        print("\n" + "=" * 70)
        print("ADVENTURE")
        print("=" * 70)
        print("1) Fight an enemy")
        print("2) Quit")
        
        choice = get_valid_input("\nWhat will you do? ", [1, 2])
        
        if choice == 2:
            print("\nThanks for playing!")
            playing = False
            break
        
        # Create enemy based on difficulty
        print("\nChoose difficulty:")
        print("1) Easy")
        print("2) Medium")
        print("3) Hard")
        
        difficulty = get_valid_input("Difficulty> ", [1, 2, 3])
        
        enemy_configs = {
            1: ("Goblin Scout", 25, 2, create_enemy_deck(1)),
            2: ("Goblin Warrior", 35, 3, create_enemy_deck(2)),
            3: ("Goblin Champion", 45, 3, create_enemy_deck(3))
        }
        
        enemy_name, enemy_hp, enemy_dice, enemy_deck_config = enemy_configs[difficulty]
        enemy = Enemy(enemy_name, hp=enemy_hp, num_dice=enemy_dice, deck_config=enemy_deck_config)
        random.shuffle(enemy.deck)
        
        print(f"\n🎯 A {enemy.name} appears!")
        print(f"  HP: {enemy.max_hp} | Dice: {enemy.num_dice} | Cards: {len(enemy.deck)}")
        
        # Run combat
        victory = interactive_combat_loop(player, enemy)
        
        # End combat
        if victory:
            print("\n🏆 VICTORY!")
            # Heal player a bit between fights
            player.currenthp = min(player.max_hp, player.currenthp + 10)
            print(f"You rest and recover 10 HP. Current HP: {player.currenthp}/{player.max_hp}")
        else:
            print("\n💀 DEFEAT!")
            playing = False
    
    # Game over
    print("\n" + "=" * 70)
    if player.is_alive():
        print("Thanks for playing!")
    else:
        print("GAME OVER")
    print("=" * 70)


if __name__ == "__main__":
    main()
