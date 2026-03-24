"""Script to convert CARD_PROGRESSIONS from string-based to explicit parameters."""
import re

def parse_effect_to_params(effect_str):
    """Convert effect string to explicit parameters."""
    effect_lower = effect_str.lower()
    
    params = {
        'effect_type': 'raw',  # Default to raw, will be overridden
        'base_value': 0,
        'uses_dice_value': False,
        'reusable': False,
        'max_dice': 1,
        'conditional_status': [],
        'description': effect_str
    }
    
    # Check for damage patterns
    if 'deal' in effect_lower and 'damage' in effect_lower:
        params['effect_type'] = 'damage'
        
        # Check if uses die value
        if 'die value' in effect_lower:
            params['uses_dice_value'] = True
            
            # Look for bonus: "die value + 3"
            m = re.search(r'die value \+ (\d+)', effect_lower)
            if m:
                params['base_value'] = int(m.group(1))
            # Or "3 + die value"
            m = re.search(r'(\d+) \+ die value', effect_lower)
            if m:
                params['base_value'] = int(m.group(1))
        else:
            # Fixed damage: "Deal 25 damage"
            m = re.search(r'deal (\d+) damage', effect_lower)
            if m:
                params['base_value'] = int(m.group(1))
                params['uses_dice_value'] = False
    
    # Check for heal patterns
    if 'heal' in effect_lower and 'hp' in effect_lower:
        params['effect_type'] = 'heal'
        m = re.search(r'heal (\d+) hp', effect_lower)
        if m:
            params['base_value'] = int(m.group(1))
    
    # Check for shield patterns
    if 'gain' in effect_lower and 'shield' in effect_lower:
        params['effect_type'] = 'shield'
        m = re.search(r'gain (\d+) shield', effect_lower)
        if m:
            params['base_value'] = int(m.group(1))
    
    # Check for reusable flag
    if 'reusable' in effect_lower or re.search(r'reusable["\'\s]*:\s*true', effect_str.lower()):
        params['reusable'] = True
    
    # Parse conditional status effects (On 6:, On 5-6:)
    for status in ['poison', 'bleed', 'blind', 'lock', 'frozen']:
        # On 6: Apply X Status
        m = re.search(rf'on 6: apply (\d+) {status}', effect_lower)
        if m:
            params['conditional_status'].append({
                'status': status,
                'stacks': int(m.group(1)),
                'condition': 'on_6'
            })
            continue
        
        # On 5-6: Apply X Status  
        m = re.search(rf'on 5-6: apply (\d+) {status}', effect_lower)
        if m:
            params['conditional_status'].append({
                'status': status,
                'stacks': int(m.group(1)),
                'condition': 'on_5_6'
            })
    
    return params

def convert_card_entry(card_data):
    """Convert a card entry from old format to new format."""
    name = card_data.get('name', '')
    requirement = card_data.get('requirement', 'Any')
    effect = card_data.get('effect', '')
    reusable_flag = card_data.get('reusable', False)
    
    params = parse_effect_to_params(effect)
    params['name'] = name
    params['requirement'] = requirement
    
    # Override reusable if explicitly set in old format
    if reusable_flag:
        params['reusable'] = True
    
    return params

# Sample usage
sample = {
    'name': "Bellow",
    'requirement': "Any",
    'effect': "Deal damage equal to die value, On 6: Apply 1 Frozen"
}

converted = convert_card_entry(sample)
print("Sample conversion:")
print(f"Input: {sample}")
print(f"Output: {converted}")
