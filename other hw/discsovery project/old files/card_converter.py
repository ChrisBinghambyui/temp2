"""
Automated converter for CARD_PROGRESSIONS from string-based to explicit parameter format.

Run this script to generate the new format, then copy-paste it into dice_dungeon.py
"""

import re

def parse_effect_string(effect_str, reusable_flag=False):
    """Convert an effect string into explicit parameters."""
    el = effect_str.lower()
    
    params = {
        'effect_type': 'raw',
        'base_value': 0,
        'uses_dice_value': False,
        'reusable': reusable_flag,
        'max_dice': 1,
        'description': effect_str
    }
    
    # DAMAGE patterns
    if 'deal' in el and 'damage' in el:
        params['effect_type'] = 'damage'
        
        if 'die value' in el:
            params['uses_dice_value'] = True
            # Look for "+ N" bonus
            m = re.search(r'die value \+ (\d+)', el)
            if m:
                params['base_value'] = int(m.group(1))
            # Or "N + die value"
            m = re.search(r'(\d+) \+ die value', el)
            if m:
                params['base_value'] = int(m.group(1))
        else:
            # Fixed damage
            m = re.search(r'deal (\d+) damage', el)
            if m:
                params['base_value'] = int(m.group(1))
                params['uses_dice_value'] = False
    
    # HEAL patterns  
    elif 'heal' in el and 'hp' in el:
        params['effect_type'] = 'heal'
        m = re.search(r'heal (\d+) hp', el)
        if m:
            params['base_value'] = int(m.group(1))
    
    # SHIELD patterns
    elif 'gain' in el and 'shield' in el:
        params['effect_type'] = 'shield'
        if 'die value' in el:
            params['uses_dice_value'] = True
            m = re.search(r'shield equal to die value \+ (\d+)', el)
            if m:
                params['base_value'] = int(m.group(1))
        else:
            m = re.search(r'gain (\d+) shield', el)
            if m:
                params['base_value'] = int(m.group(1))
    
    return params

def format_card_variant(variant_dict):
    """Format a single card variant as Python dict string."""
    name = variant_dict.get('name', '')
    req = variant_dict.get('requirement', 'Any')
    effect = variant_dict.get('effect', '')
    reusable = variant_dict.get('reusable', False)
    
    params = parse_effect_string(effect, reusable)
    
    lines = [
        f"      'name': \"{name}\",",
        f"      'requirement': \"{req}\",",
        f"      'effect_type': '{params['effect_type']}',",
        f"      'base_value': {params['base_value']},",
        f"      'uses_dice_value': {params['uses_dice_value']},",
        f"      'reusable': {params['reusable']},",
        f"      'max_dice': {params['max_dice']},",
        f"      'description': \"{params['description']}\"",
    ]
    
    return "{ \n" + "\n".join(lines) + "\n    }"

# Example usage - you would read the actual CARD_PROGRESSIONS and convert it
example_card = {
    'name': "Bellow",
    'requirement': "Any",
    'effect': "Deal damage equal to die value, On 6: Apply 1 Frozen"
}

print("Example conversion:")
print(format_card_variant(example_card))

print("\n" + "="*60)
print("To convert all cards, you would:")
print("1. Read the current CARD_PROGRESSIONS")
print("2. For each card family and variant, call format_card_variant()")
print("3. Rebuild the dictionary structure")
print("4. Replace in dice_dungeon.py")
print("="*60)
