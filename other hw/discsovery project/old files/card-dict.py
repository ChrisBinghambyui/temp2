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