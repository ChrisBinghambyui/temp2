# Auto-converted creature + ability data (source: `creatures - Copy.jsx`)
# Expose CREATURE_DEFINITIONS (dict) so the Python game can instantiate enemies/cards.

CREATURE_DEFINITIONS = {
  "Wolf": {
    "hp": 10,
    "dice": 2,
    "abilities": [
      {"name": "Bite", "requirement": "Any", "effect": "Deal 3 damage"},
      {"name": "Howl", "requirement": "Limit 8", "effect": "Heal 2 HP"}
    ]
  },
  "Giant Locust": {
    "hp": 12,
    "dice": 2,
    "abilities": [
      {"name": "Swipe", "requirement": "Limit 5", "effect": "Deal 3 damage, Heal 1 HP"},
      {"name": "Swipe", "requirement": "Limit 5", "effect": "Deal 3 damage, Heal 1 HP"}
    ]
  },
  "Naukin Outcast": {
    "hp": 10,
    "dice": 2,
    "abilities": [
      {"name": "Jab", "requirement": "Any", "effect": "Deal damage equal to die value"},
      {"name": "Rusty Dagger", "requirement": "Odd only", "effect": "Deal 2 damage"}
    ]
  },
  "Dire Wolves": {
    "hp": 18,
    "dice": 3,
    "abilities": [
      {"name": "Bite x", "requirement": "Any", "effect": "Deal damage equal to die value"},
      {"name": "Bite y", "requirement": "Any", "effect": "Deal 4 damage", "reusable": True}
    ]
  },
  "Prowling Dellinid": {
    "hp": 16,
    "dice": 3,
    "abilities": [
      {"name": "Pounce", "requirement": "Any", "effect": "Deal 5 + die value damage", "oncePerCombat": True},
      {"name": "Swipe x", "requirement": "Any", "effect": "Deal 3 damage + 1 for each use this round", "reusable": True}
    ]
  },
  "Juvenile Auroc": {
    "hp": 20,
    "dice": 3,
    "abilities": [
      {"name": "Fortify", "requirement": "Any", "effect": "Gain 3 Shield"},
      {"name": "Reflecting Scales", "requirement": "Any", "effect": "Deal 2 damage, Apply 1 Blind"},
      {"name": "Chomp", "requirement": "Limit 10", "effect": "Deal 10 damage (activates when limit reaches 0)"}
    ]
  },
  "Bovari Bandit": {
    "hp": 30,
    "dice": 3,
    "abilities": [
      {"name": "Shortbow x", "requirement": "Odd only", "effect": "Deal double die value damage"},
      {"name": "Dagger x", "requirement": "Any", "effect": "Deal 3 damage, Apply 1 Poison"},
      {"name": "Hype Up", "requirement": "Limit 12", "effect": "Heal 4 HP, Apply 1 Blind to self and opponent (activates when limit reaches 0)"}
    ]
  },
  "Roaming Gallox": {
    "hp": 30,
    "dice": 4,
    "abilities": [
      {"name": "Charge", "requirement": "Limit 15", "effect": "Deal 8 damage, Gain 3 Shield (activates when limit reaches 0)"},
      {"name": "Trample", "requirement": "Any", "effect": "Deal damage equal to die value, On 6: Apply 1 Lock"},
      {"name": "Gore", "requirement": "Any", "effect": "Deal damage equal to die value, On 6: Apply 1 Bleed"}
    ]
  },
  "Lone Plainsdrake": {
    "hp": 30,
    "dice": 4,
    "abilities": [
      {"name": "Reflecting Scales x", "requirement": "Any", "effect": "Deal 4 damage, Apply 2 Blind"},
      {"name": "Reflecting Scales y", "requirement": "Any", "effect": "Apply 2 Blind, Gain 2 Shield"},
      {"name": "Mirror Hide", "requirement": "Any", "effect": "Remove all negative effects from self, Apply them to opponent"},
      {"name": "Chomp x", "requirement": "Limit 8", "effect": "Deal 10 damage (activates when limit reaches 0)"}
    ]
  },
  "Blue Dellinid": {"hp":12,"dice":2,"abilities":[{"name":"Pounce","requirement":"Any","effect":"Deal 5 + die value damage","oncePerCombat":True},{"name":"Swipe x","requirement":"Any","effect":"Deal 3 damage + 1 for each use this round","reusable":True}]},
  "Khinari Exile": {"hp":14,"dice":2,"abilities":[{"name":"Shortbow","requirement":"3 or below","effect":"Deal double die value damage"},{"name":"Frosted Dagger","requirement":"Any","effect":"Deal damage equal to die value, On 6: Apply 1 Poison"}]},
  "Territorial Whitespike": {"hp":16,"dice":2,"abilities":[{"name":"Gore","requirement":"Any","effect":"Deal damage equal to die value, On 6: Apply 1 Bleed"},{"name":"Bellow","requirement":"Any","effect":"Deal damage equal to die value, On 6: Apply 1 Frozen"}]},
  "Khinari Raider": {"hp":20,"dice":3,"abilities":[{"name":"Frosted Spear","requirement":"Minimum 3","effect":"Deal 3 damage","reusable":True},{"name":"Frosted Dagger x","requirement":"Any","effect":"Deal damage equal to die value, On 6: Apply 1 Poison and 1 Frozen"},{"name":"Ice Magic","requirement":"Exactly 2","effect":"Heal 2 HP, Remove all negative effects from self"}]},
  "Tundra Boneguard": {"hp":24,"dice":3,"abilities":[{"name":"Splinter","requirement":"Any","effect":"Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)"},{"name":"Shield","requirement":"Even only","effect":"Gain Shield equal to half the die value"},{"name":"Bash","requirement":"Any","effect":"Deal damage equal to double current shield, then remove all shield"}]},
  "Alpha Whitespike": {"hp":22,"dice":3,"abilities":[{"name":"Gore x","requirement":"Any","effect":"Deal 2 + die value damage, On 6: Apply 1 Bleed"},{"name":"Bellow y","requirement":"Any","effect":"Deal damage equal to die value, On 5-6: Apply 1 Frozen"},{"name":"Charge","requirement":"Limit 15","effect":"Deal 8 damage, Gain 3 Shield (activates when limit reaches 0)"},{"name":"Trample","requirement":"Any","effect":"Deal damage equal to die value, On 6: Apply 1 Lock"}]},
  "Veteran Boneguard": {"hp":30,"dice":4,"abilities":[{"name":"Splinter x","requirement":"Any","effect":"Create 2 dice with half the input die value (rounded down)"},{"name":"Shield x","requirement":"Even only","effect":"Gain shield equal to the die value"},{"name":"Bash x","requirement":"Any","effect":"Deal damage equal to double current shield, then remove half of current shield (rounded down)"},{"name":"Frosted Spear x","requirement":"Any","effect":"Deal 3 damage","reusable":True}]},
  "Khinari Hunting Party": {"hp":30,"dice":4,"abilities":[{"name":"Splinter y","requirement":"Any","effect":"Sacrifice 2 HP, Create 2 dice with half the input die value (rounded up)"},{"name":"Fortify x","requirement":"Any","effect":"Gain 4 Shield and inflict 1 blind"},{"name":"Ice Magic y","requirement":"Max 2","effect":"Heal 2 HP, Remove all negative effects from self"},{"name":"Control","requirement":"Exactly 1","effect":"Sacrifice 2 hp, draw a new card, and roll a new die"},{"name":"Frosted Spear x","requirement":"Any","effect":"Deal 3 damage","reusable":True}]},
  "Hungry Frost Wyrm": {"hp":28,"dice":3,"abilities":[{"name":"Bite X","requirement":"Any","effect":"Deal damage equal to die value + 2"},{"name":"Bite Y","requirement":"Any","effect":"Deal 5 damage and heal 1","reusable":True},{"name":"Bellow y","requirement":"Any","effect":"Deal damage equal to die value, On 5-6: Apply 1 Frozen"}]},
  "Naukin Scouts": {"hp":16,"dice":3,"abilities":[{"name":"Jab x","requirement":"Any","effect":"Deal 2 + die value damage"},{"name":"Jab y","requirement":"Any","effect":"Deal damage equal to die value","reusable":True},{"name":"Fortify","requirement":"Any","effect":"Gain 3 Shield"}]},
  "Skittari Hunters": {"hp":18,"dice":3,"abilities":[{"name":"Snipe","requirement":"Limit 15","effect":"Deal 8 damage, Apply 1 Bleed (activates when limit reaches 0)"},{"name":"Rusty Dagger x","requirement":"Odd only","effect":"Deal 3 damage"}]},
  "Reclaimed Boneguard": {"hp":18,"dice":3,"abilities":[{"name":"Splinter","requirement":"Any","effect":"Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)"},{"name":"Shield","requirement":"Even only","effect":"Gain Shield equal to half the die value"},{"name":"Bash","requirement":"Any","effect":"Remove all Shield from self, Deal damage equal to double the Shield removed"}]},
  "Dire Bear": {"hp":28,"dice":4,"abilities":[{"name":"Swipe y","requirement":"Limit 5","effect":"Deal 5 damage, Heal 2 HP"},{"name":"Bite y","requirement":"Any","effect":"Deal 4 damage","reusable":True},{"name":"Roar","requirement":"Exactly 1","effect":"Apply 1 Lock"}]},
  "Khinari Bladedancer": {"hp":22,"dice":4,"abilities":[{"name":"Splinter y","requirement":"Any","effect":"Sacrifice 2 HP, Create 2 dice with half the input die value (rounded up)"},{"name":"Snipe x","requirement":"Limit 15","effect":"Deal 12 damage, Apply 1 Bleed (activates when limit reaches 0)"},{"name":"Jab y","requirement":"Any","effect":"Deal damage equal to die value","reusable":True}]},
  "Naukin Sunstriker": {"hp":20,"dice":4,"abilities":[{"name":"Dagger y","requirement":"Odd only","effect":"Deal 4 damage, Apply 1 Poison"},{"name":"Sunstrike","requirement":"Limit 4","effect":"Deal 3 damage, Apply 1 Blind"},{"name":"Mirror Hide y","requirement":"Any","effect":"Double all negative effects on opponent"},{"name":"Control","requirement":"Exactly 1","effect":"Sacrifice 2 hp, draw a new card, and roll a new die"}]},
  "Verdant Shepherd": {"hp":40,"dice":4,"abilities":[{"name":"Maul X","requirement":"Any","effect":"Deal damage equal to die value + 6"},{"name":"Bellow x","requirement":"Any","effect":"Deal damage equal to die value, Trigger Poison (deal damage equal to poison counters on opponent, then reduce poison counters by 1)"},{"name":"Jade Spear","requirement":"Even only","effect":"Apply Poison equal to die value"},{"name":"Splinter Y","requirement":"Minimum 2","effect":"Sacrifice 2 HP, Create 3 dice with half the input die value (rounded up)"}]},
  "Barkskin Colossus": {"hp":50,"dice":4,"abilities":[{"name":"Splinter X","requirement":"Any","effect":"Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)","reusable":True},{"name":"Swipe X","requirement":"Any","effect":"Deal 2 damage + 2 for each use this round","reusable":True},{"name":"Charge y","requirement":"Limit 18","effect":"Deal 8 damage, Gain 8 Shield"}]},
  "Emerald Lich": {"hp":35,"dice":5,"abilities":[{"name":"Necromancy","requirement":"Limit 12","effect":"Deal 15 damage, Heal 5 HP"},{"name":"Afflict","requirement":"Exactly 1","effect":"Apply 2 Poison, Apply 1 Blind"},{"name":"Shield X","requirement":"Even only","effect":"Gain Shield equal to die value"},{"name":"Life Drain x","requirement":"Odd only","effect":"Deal damage equal to die value, Heal half the damage dealt (rounded up)"}]},
  "Brass Golem": {"hp":24,"dice":3,"abilities":[{"name":"Bash y","requirement":"Any","effect":"Deal damage equal to double current shield, then remove half of current shield (rounded up)"},{"name":"Shield y","requirement":"Even only","effect":"Gain Shield equal to half the die value","reusable":True},{"name":"Fortify","requirement":"Any","effect":"Gain 3 Shield"}]},
  "Skittari Looters": {"hp":22,"dice":3,"abilities":[{"name":"Dagger x","requirement":"Any","effect":"Deal 3 damage, Apply 1 Poison"},{"name":"Shortbow x","requirement":"Odd only","effect":"Deal double die value damage"},{"name":"Control","requirement":"Exactly 1","effect":"Sacrifice 2 HP, draw a new card, and roll a new die"}]},
  "Bloated Zombie": {"hp":26,"dice":3,"abilities":[{"name":"Bite x","requirement":"Any","effect":"Deal damage equal to die value"},{"name":"Rupture","requirement":"Limit 10","effect":"Deal 8 damage, Apply 2 Poison"},{"name":"Life Drain","requirement":"Odd only","effect":"Deal damage equal to die value, Heal 1 HP"}]},
  "Iron Bulwark": {"hp":40,"dice":4,"abilities":[{"name":"Bash X","requirement":"Any","effect":"Deal damage equal to double current shield, then remove half of current shield (rounded up), Gain 2 Shield","reusable":True},{"name":"Shield Y","requirement":"Even only","effect":"Gain Shield equal to die value","reusable":True},{"name":"Fortify X","requirement":"Any","effect":"Gain 5 Shield, Apply 1 Blind"}]},
  "Stone Drake": {"hp":38,"dice":4,"abilities":[{"name":"Chomp y","requirement":"Limit 12","effect":"Deal 12 damage"},{"name":"Reflecting Scales x","requirement":"Any","effect":"Deal 4 damage, Apply 2 Blind"},{"name":"Petrify","requirement":"On 6","effect":"Apply 2 Lock, Apply 1 Frozen"}]},
  "Lost Myrrim": {"hp":36,"dice":4,"abilities":[{"name":"Spectral Strike","requirement":"Any","effect":"Deal damage equal to die value, On 5-6: Apply 1 Bleed"},{"name":"Phase Shift","requirement":"Exactly 1","effect":"Gain 4 Shield, Remove all negative effects from self"},{"name":"Haunting Wail","requirement":"Limit 8","effect":"Apply 2 Blind, Apply 1 Lock"}]},
  "Fell Lich": {"hp":60,"dice":5,"abilities":[{"name":"Necromancy X","requirement":"Limit 15","effect":"Deal 18 damage, Heal 6 HP"},{"name":"Afflict X","requirement":"Exactly 1","effect":"Apply 3 Poison, Apply 2 Blind"},{"name":"Life Drain X","requirement":"Odd only","effect":"Deal damage equal to die value + 2, Heal half the damage dealt (rounded up)"},{"name":"Soul Rend","requirement":"Minimum 4","effect":"Deal 8 damage, Apply 1 Bleed","reusable":True}]},
  "Blighted Auroc": {"hp":65,"dice":4,"abilities":[{"name":"Gore X","requirement":"Any","effect":"Deal 4 + die value damage, On 6: Apply 2 Bleed"},{"name":"Chomp X","requirement":"Limit 10","effect":"Deal 14 damage, Heal 3 HP"},{"name":"Plague Breath","requirement":"Even only","effect":"Apply Poison equal to half die value (rounded up)"},{"name":"Charge X","requirement":"Limit 20","effect":"Deal 10 damage, Gain 10 Shield"}]},
  "Khinari Subjugator": {"hp":62,"dice":5,"abilities":[{"name":"Snipe X","requirement":"Limit 18","effect":"Deal 15 damage, Apply 2 Bleed"},{"name":"Frosted Spear X","requirement":"Any","effect":"Deal 5 damage, On 5-6: Apply 1 Frozen","reusable":True},{"name":"Dominate","requirement":"Exactly 1","effect":"Apply 2 Lock, Sacrifice 3 HP"},{"name":"Splinter X","requirement":"Any","effect":"Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)","reusable":True}]},
  "Steppe Whitespike": {"hp":28,"dice":3,"abilities":[{"name":"Gore y","requirement":"Any","effect":"Deal 3 + die value damage, On 6: Apply 1 Bleed"},{"name":"Bellow X","requirement":"Any","effect":"Deal damage equal to die value + 2, On 5-6: Apply 2 Frozen"},{"name":"Trample","requirement":"Any","effect":"Deal damage equal to die value, On 6: Apply 1 Lock"}]},
  "Caghoul Shaman": {"hp":26,"dice":4,"abilities":[{"name":"Lightning Bolt","requirement":"Odd only","effect":"Deal triple die value damage","oncePerCombat":True},{"name":"Totem","requirement":"Exactly 2","effect":"Gain 5 Shield, Heal 2 HP"},{"name":"Jab X","requirement":"Any","effect":"Deal 4 + die value damage","reusable":True}]},
  "Naukin Outrider": {"hp":24,"dice":4,"abilities":[{"name":"Shortbow X","requirement":"Odd only","effect":"Deal triple die value damage"},{"name":"Dagger Y","requirement":"Odd only","effect":"Deal 5 damage, Apply 2 Poison"},{"name":"Evade","requirement":"Exactly 1","effect":"Gain Shield equal to 2 × the number of dice used this turn"}]},
  "Hill Giant": {"hp":48,"dice":4,"abilities":[{"name":"Maul Y","requirement":"Any","effect":"Deal damage equal to die value + 8"},{"name":"Boulder Toss","requirement":"Minimum 4","effect":"Deal 10 damage, Apply 1 Lock","reusable":True},{"name":"Earthquake","requirement":"Limit 20","effect":"Deal 12 damage, Apply 2 Lock, Apply 1 Frozen"}]},
  "Black Roc": {"hp":45,"dice":4,"abilities":[{"name":"Dive Bomb","requirement":"Minimum 5","effect":"Deal 12 damage, Apply 1 Blind"},{"name":"Talon Strike","requirement":"Any","effect":"Deal damage equal to die value + 3, On 6: Apply 1 Bleed","reusable":True},{"name":"Screech","requirement":"Exactly 1","effect":"Apply 2 Blind, Apply 1 Lock"}]},
  "Whitespike Patriarch": {"hp":50,"dice":4,"abilities":[{"name":"Gore Y","requirement":"Any","effect":"Deal 5 + die value damage, On 5-6: Apply 2 Bleed"},{"name":"Bellow Y","requirement":"Any","effect":"Deal damage equal to die value + 3, On 5-6: Apply 2 Frozen","reusable":True},{"name":"Charge X","requirement":"Limit 20","effect":"Deal 10 damage, Gain 10 Shield"},{"name":"Trample X","requirement":"Any","effect":"Deal damage equal to die value + 2, On 5-6: Apply 2 Lock"}]},
  "Thunder Giant": {"hp":85,"dice":5,"abilities":[{"name":"Maul XY","requirement":"Any","effect":"Deal damage equal to die value + 12","reusable":True},{"name":"Thunderclap","requirement":"Limit 25","effect":"Deal 18 damage, Apply 3 Blind, Apply 2 Lock"},{"name":"Boulder Toss X","requirement":"Minimum 3","effect":"Deal 12 damage, Apply 2 Lock","reusable":True},{"name":"Fortify Y","requirement":"Any","effect":"Gain 8 Shield, Heal 2 HP"}]},
  "Quakewyrm": {"hp":83,"dice":5,"abilities":[{"name":"Chomp XY","requirement":"Limit 15","effect":"Deal 20 damage, Heal 5 HP"},{"name":"Tremor","requirement":"Any","effect":"Deal damage equal to die value, Apply Lock equal to (die value ÷ 3, rounded down)"},{"name":"Stone Hide","requirement":"Even only","effect":"Gain Shield equal to die value + 2","reusable":True},{"name":"Earthshatter","requirement":"Limit 22","effect":"Deal 15 damage, Apply 3 Lock, Apply 2 Frozen"}]},
  "Caghoul Skyshaker": {"hp":80,"dice":5,"abilities":[{"name":"Lightning Storm","requirement":"Limit 20","effect":"Deal 20 damage, Apply 2 Blind"},{"name":"Chain Lightning","requirement":"Odd only","effect":"Deal quadruple die value damage"},{"name":"Totem X","requirement":"Exactly 2","effect":"Gain 8 Shield, Heal 4 HP"},{"name":"Wind Slash","requirement":"Any","effect":"Deal damage equal to die value + 4, On 6: Apply 2 Bleed","reusable":True}]},
  "Condemned": {"hp":38,"dice":4,"abilities":[{"name":"Flail","requirement":"Any","effect":"Deal damage equal to die value, Sacrifice 1 HP"},{"name":"Chains","requirement":"Minimum 3","effect":"Deal 6 damage, Apply 2 Lock","reusable":True},{"name":"Desperation","requirement":"Exactly 1","effect":"Deal 10 damage, Sacrifice 5 HP"}]},
  "Bovari Thrall": {"hp":40,"dice":4,"abilities":[{"name":"Gore Z","requirement":"Any","effect":"Deal 6 + die value damage, On 5-6: Apply 2 Bleed"},{"name":"Blood Pact","requirement":"Limit 15","effect":"Deal 12 damage, Heal 4 HP, Sacrifice 3 HP"},{"name":"Flame Strike","requirement":"Odd only","effect":"Deal double die value damage, Apply 1 Poison"}]},
  "Hatebound Imp": {"hp":36,"dice":4,"abilities":[{"name":"Claw Swipe","requirement":"Any","effect":"Deal damage equal to die value + 3, On 6: Apply 1 Bleed","reusable":True},{"name":"Curse","requirement":"Exactly 1","effect":"Apply 2 Poison, Apply 2 Blind"},{"name":"Immolate","requirement":"Limit 10","effect":"Deal 10 damage, Apply 2 Poison, Sacrifice 2 HP"}]},
  "Blooded Khinari": {"hp":62,"dice":5,"abilities":[{"name":"Snipe Y","requirement":"Limit 22","effect":"Deal 18 damage, Apply 3 Bleed, Heal 3 HP"},{"name":"Frosted Spear Y","requirement":"Any","effect":"Deal 6 damage, On 5-6: Apply 2 Frozen","reusable":True},{"name":"Blood Ritual","requirement":"Exactly 1","effect":"Sacrifice 5 HP, Deal 15 damage, Apply 2 Poison"},{"name":"Splinter Y","requirement":"Any","effect":"Sacrifice 2 HP, Create 3 dice with half the input die value (rounded up)"}]},
  "Hatebound Priest": {"hp":60,"dice":5,"abilities":[{"name":"Dark Blessing","requirement":"Limit 18","effect":"Heal 8 HP, Apply 2 Poison to opponent"},{"name":"Afflict Y","requirement":"Exactly 1","effect":"Apply 4 Poison, Apply 2 Blind, Apply 1 Lock"},{"name":"Flame Burst","requirement":"Odd only","effect":"Deal triple die value damage"},{"name":"Life Drain Y","requirement":"Odd only","effect":"Deal damage equal to die value + 4, Heal half the damage dealt (rounded up)","reusable":True}]},
  "Condemned Taskmaster": {"hp":64,"dice":4,"abilities":[{"name":"Whip Crack","requirement":"Any","effect":"Deal damage equal to die value + 5, Apply 1 Lock"},{"name":"Chains X","requirement":"Minimum 3","effect":"Deal 8 damage, Apply 3 Lock","reusable":True},{"name":"Torture","requirement":"Limit 20","effect":"Deal 15 damage, Apply 2 Bleed, Apply 2 Lock"},{"name":"Bash Y","requirement":"Any","effect":"Deal damage equal to triple current shield, then remove all shield"}]},
  "Pit Lord": {"hp":115,"dice":5,"abilities":[{"name":"Annihilation","requirement":"Limit 30","effect":"Deal 25 damage, Apply 3 Bleed, Apply 2 Poison"},{"name":"Infernal Strike","requirement":"Any","effect":"Deal damage equal to die value + 8, Sacrifice 2 HP","reusable":True},{"name":"Hellfire","requirement":"Odd only","effect":"Deal quintuple die value damage"},{"name":"Dark Aegis","requirement":"Even only","effect":"Gain Shield equal to die value + 4, Apply 1 Poison to opponent","reusable":True}]},
  "Blood Judge": {"hp":112,"dice":5,"abilities":[{"name":"Execution","requirement":"Limit 25","effect":"Deal 22 damage, Apply 4 Bleed"},{"name":"Blood Price","requirement":"Any","effect":"Sacrifice HP equal to die value, Deal double the sacrificed HP as damage"},{"name":"Judgement","requirement":"Exactly 6","effect":"Deal 18 damage, Heal 6 HP, Apply 2 Lock"},{"name":"Life Drain XY","requirement":"Odd only","effect":"Deal damage equal to die value + 6, Heal the full damage dealt","reusable":True}]},
  "Prophet of Fire": {"hp":110,"dice":6,"abilities":[{"name":"Apocalypse","requirement":"Limit 35","effect":"Deal 30 damage, Apply 4 Poison, Apply 3 Blind, Apply 2 Lock"},{"name":"Meteor","requirement":"Minimum 5","effect":"Deal 15 damage, Apply 2 Bleed","reusable":True},{"name":"Inferno","requirement":"Odd only","effect":"Deal quadruple die value damage, Apply 2 Poison"},{"name":"Phoenix Rising","requirement":"Exactly 1","effect":"Heal 10 HP, Gain 10 Shield, Remove all negative effects from self"},{"name":"Flame Wall","requirement":"Even only","effect":"Gain Shield equal to die value + 5, Deal 5 damage","reusable":True}]}
}

# Convenience: list of all unique card names referenced by creatures
CARD_NAMES = sorted({
    ability['name']
    for c in CREATURE_DEFINITIONS.values()
    for ability in c['abilities']
})

# Build a lightweight CARD_DEFINITIONS map so the game can look up card metadata by name.
# If a card appears multiple times with different effects (x/y/X/Y variants), the first
# occurrence is used — variants keep their full names (e.g. "Bite x").
CARD_DEFINITIONS = {}
for cdef in CREATURE_DEFINITIONS.values():
    for ability in cdef['abilities']:
        name = ability['name']
        if name in CARD_DEFINITIONS:
            continue
        CARD_DEFINITIONS[name] = {
            'requirement': ability.get('requirement', ''),
            'effect': ability.get('effect', ''),
            'reusable': bool(ability.get('reusable', False)),
            'oncePerCombat': bool(ability.get('oncePerCombat', False))
        }

if __name__ == '__main__':
    # quick sanity check
    print(f"Loaded {len(CREATURE_DEFINITIONS)} creatures with {len(CARD_NAMES)} unique card names")
    print(list(CARD_NAMES)[:30])
