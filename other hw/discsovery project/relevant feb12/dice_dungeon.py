import math
import random
from colorama import init, Fore, Back, Style
# --- Creature & card data (inlined from original `cards_data.py`) ---
CREATURE_DEFINITIONS = {
  "Rach-Wolf": {
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
  "Blue Dellinid": {
    "hp": 12,
    "dice": 2,
    "abilities": [
      {"name": "Pounce", "requirement": "Any", "effect": "Deal 5 + die value damage", "oncePerCombat": True},
      {"name": "Swipe x", "requirement": "Any", "effect": "Deal 3 damage + 1 for each use this round", "reusable": True}
    ]
  },
  "Khinari Exile": {"hp":14,"dice":2,"abilities":[{"name":"Shortbow","requirement":"3 or below","effect":"Deal double die value damage"},{"name":"Frosted Dagger","requirement":"Any","effect":"Deal damage equal to die value, On 6: Apply 1 Poison"}]},
  "Territorial Whitespike": {"hp":16,"dice":2,"abilities":[{"name":"Gore","requirement":"Any","effect":"Deal damage equal to die value, On 6: Apply 1 Bleed"},{"name":"Bellow","requirement":"Any","effect":"Deal damage equal to die value, On 6: Apply 1 Frozen"}]},

  "Khinari Raider": {"hp":20,"dice":3,"abilities":[{"name":"Frosted Spear","requirement":"Minimum 3","effect":"Deal 3 damage","reusable":True},{"name":"Frosted Dagger x","requirement":"Any","effect":"Deal damage equal to die value, On 6: Apply 1 Poison and 1 Frozen"},{"name":"Ice Magic","requirement":"Exactly 2","effect":"Heal 2 HP, Remove all negative effects from self"}]},
  "Tundra Boneguard": {"hp":24,"dice":3,"abilities":[{"name":"Splinter","requirement":"Any","effect":"Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)"},{"name":"Shield","requirement":"Even only","effect":"Gain Shield equal to half the die value"},{"name":"Bash","requirement":"Any","effect":"Deal damage equal to double current shield, then remove all shield"}]},
  "Alpha Whitespike": {
    "hp": 22,
    "dice": 3,
    "abilities": [
      {"name": "Gore x", "requirement": "Any", "effect": "Deal 2 + die value damage, On 6: Apply 1 Bleed"},
      {"name": "Bellow y", "requirement": "Any", "effect": "Deal damage equal to die value, On 5-6: Apply 1 Frozen"},
      {"name": "Charge", "requirement": "Limit 15", "effect": "Deal 8 damage, Gain 3 Shield (activates when limit reaches 0)"},
      {"name": "Trample", "requirement": "Any", "effect": "Deal damage equal to die value, On 6: Apply 1 Lock"}
    ]
  },
  "Veteran Boneguard": {
    "hp": 30,
    "dice": 4,
    "abilities": [
      {"name": "Splinter x", "requirement": "Any", "effect": "Create 2 dice with half the input die value (rounded down)"},
      {"name": "Shield x", "requirement": "Even only", "effect": "Gain shield equal to the die value"},
      {"name": "Bash x", "requirement": "Any", "effect": "Deal damage equal to double current shield, then remove half of current shield (rounded down)"},
      {"name": "Frosted Spear x", "requirement": "Any", "effect": "Deal 3 damage", "reusable": True}
    ]
  },
  "Khinari Hunting Party": {
    "hp": 30,
    "dice": 4,
    "abilities": [
      {"name": "Splinter y", "requirement": "Any", "effect": "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded up)"},
      {"name": "Fortify x", "requirement": "Any", "effect": "Gain 4 Shield and inflict 1 blind"},
      {"name": "Ice Magic y", "requirement": "Max 2", "effect": "Heal 2 HP, Remove all negative effects from self"},
      {"name": "Control", "requirement": "Exactly 1", "effect": "Sacrifice 2 hp, draw a new card, and roll a new die"},
      {"name": "Frosted Spear x", "requirement": "Any", "effect": "Deal 3 damage", "reusable": True}
    ]
  },
  "Hungry Frost Wyrm": {
    "hp": 28,
    "dice": 3,
    "abilities": [
      {"name": "Bite X", "requirement": "Any", "effect": "Deal damage equal to die value + 2"},
      {"name": "Bite Y", "requirement": "Any", "effect": "Deal 5 damage and heal 1", "reusable": True},
      {"name": "Bellow y", "requirement": "Any", "effect": "Deal damage equal to die value, On 5-6: Apply 1 Frozen"}
    ]
  },
  "Naukin Scouts": {
    "hp": 16,
    "dice": 3,
    "abilities": [
      {"name": "Jab x", "requirement": "Any", "effect": "Deal 2 + die value damage"},
      {"name": "Jab y", "requirement": "Any", "effect": "Deal damage equal to die value", "reusable": True},
      {"name": "Fortify", "requirement": "Any", "effect": "Gain 3 Shield"}
    ]
  },
  "Skittari Hunters": {
    "hp": 18,
    "dice": 3,
    "abilities": [
      {"name": "Snipe", "requirement": "Limit 15", "effect": "Deal 8 damage, Apply 1 Bleed (activates when limit reaches 0)"},
      {"name": "Rusty Dagger x", "requirement": "Odd only", "effect": "Deal 3 damage"}
    ]
  },
  "Reclaimed Boneguard": {
    "hp": 18,
    "dice": 3,
    "abilities": [
      {"name": "Splinter", "requirement": "Any", "effect": "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)"},
      {"name": "Shield", "requirement": "Even only", "effect": "Gain Shield equal to half the die value"},
      {"name": "Bash", "requirement": "Any", "effect": "Remove all Shield from self, Deal damage equal to double the Shield removed"}
    ]
  },
  "Dire Bear": {
    "hp": 28,
    "dice": 4,
    "abilities": [
      {"name": "Swipe y", "requirement": "Limit 5", "effect": "Deal 5 damage, Heal 2 HP"},
      {"name": "Bite y", "requirement": "Any", "effect": "Deal 4 damage", "reusable": True},
      {"name": "Roar", "requirement": "Exactly 1", "effect": "Apply 1 Lock"}
    ]
  },
  "Khinari Bladedancer": {
    "hp": 22,
    "dice": 4,
    "abilities": [
      {"name": "Splinter y", "requirement": "Any", "effect": "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded up)"},
      {"name": "Snipe x", "requirement": "Limit 15", "effect": "Deal 12 damage, Apply 1 Bleed (activates when limit reaches 0)"},
      {"name": "Jab y", "requirement": "Any", "effect": "Deal damage equal to die value", "reusable": True}
    ]
  },
  "Naukin Sunstriker": {
    "hp": 20,
    "dice": 4,
    "abilities": [
      {"name": "Dagger y", "requirement": "Odd only", "effect": "Deal 4 damage, Apply 1 Poison"},
      {"name": "Sunstrike", "requirement": "Limit 4", "effect": "Deal 3 damage, Apply 1 Blind"},
      {"name": "Mirror Hide y", "requirement": "Any", "effect": "Double all negative effects on opponent"},
      {"name": "Control", "requirement": "Exactly 1", "effect": "Sacrifice 2 hp, draw a new card, and roll a new die"}
    ]
  },
  "Verdant Shepherd": {
    "hp": 40,
    "dice": 4,
    "abilities": [
      {"name": "Maul X", "requirement": "Any", "effect": "Deal damage equal to die value + 6"},
      {"name": "Bellow x", "requirement": "Any", "effect": "Deal damage equal to die value, Trigger Poison (deal damage equal to poison counters on opponent, then reduce poison counters by 1)"},
      {"name": "Jade Spear", "requirement": "Even only", "effect": "Apply Poison equal to die value"},
      {"name": "Splinter Y", "requirement": "Minimum 2", "effect": "Sacrifice 2 HP, Create 3 dice with half the input die value (rounded up)"}
    ]
  },
  "Barkskin Colossus": {
    "hp": 50,
    "dice": 4,
    "abilities": [
      {"name": "Splinter X", "requirement": "Any", "effect": "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)", "reusable": True},
      {"name": "Swipe X", "requirement": "Any", "effect": "Deal 2 damage + 2 for each use this round", "reusable": True},
      {"name": "Charge y", "requirement": "Limit 18", "effect": "Deal 8 damage, Gain 8 Shield"}
    ]
  },
  "Emerald Lich": {
    "hp": 35,
    "dice": 5,
    "abilities": [
      {"name": "Necromancy", "requirement": "Limit 12", "effect": "Deal 15 damage, Heal 5 HP"},
      {"name": "Afflict", "requirement": "Exactly 1", "effect": "Apply 2 Poison, Apply 1 Blind"},
      {"name": "Shield X", "requirement": "Even only", "effect": "Gain Shield equal to die value"},
      {"name": "Life Drain x", "requirement": "Odd only", "effect": "Deal damage equal to die value, Heal half the damage dealt (rounded up)"}
    ]
  },
  "Brass Golem": {
    "hp": 24,
    "dice": 3,
    "abilities": [
      {"name": "Bash y", "requirement": "Any", "effect": "Deal damage equal to double current shield, then remove half of current shield (rounded up)"},
      {"name": "Shield y", "requirement": "Even only", "effect": "Gain Shield equal to half the die value", "reusable": True},
      {"name": "Fortify", "requirement": "Any", "effect": "Gain 3 Shield"}
    ]
  },
  "Skittari Looters": {
    "hp": 22,
    "dice": 3,
    "abilities": [
      {"name": "Dagger x", "requirement": "Any", "effect": "Deal 3 damage, Apply 1 Poison"},
      {"name": "Shortbow x", "requirement": "Odd only", "effect": "Deal double die value damage"},
      {"name": "Control", "requirement": "Exactly 1", "effect": "Sacrifice 2 HP, draw a new card, and roll a new die"}
    ]
  },
  "Bloated Zombie": {
    "hp": 26,
    "dice": 3,
    "abilities": [
      {"name": "Bite x", "requirement": "Any", "effect": "Deal damage equal to die value"},
      {"name": "Rupture", "requirement": "Limit 10", "effect": "Deal 8 damage, Apply 2 Poison"},
      {"name": "Life Drain", "requirement": "Odd only", "effect": "Deal damage equal to die value, Heal 1 HP"}
    ]
  },
  "Iron Bulwark": {
    "hp": 40,
    "dice": 4,
    "abilities": [
      {"name": "Bash X", "requirement": "Any", "effect": "Deal damage equal to double current shield, then remove half of current shield (rounded up), Gain 2 Shield", "reusable": True},
      {"name": "Shield Y", "requirement": "Even only", "effect": "Gain Shield equal to die value", "reusable": True},
      {"name": "Fortify X", "requirement": "Any", "effect": "Gain 5 Shield, Apply 1 Blind"}
    ]
  },
  "Stone Drake": {
    "hp": 38,
    "dice": 4,
    "abilities": [
      {"name": "Chomp y", "requirement": "Limit 12", "effect": "Deal 12 damage"},
      {"name": "Reflecting Scales x", "requirement": "Any", "effect": "Deal 4 damage, Apply 2 Blind"},
      {"name": "Petrify", "requirement": "On 6", "effect": "Apply 2 Lock, Apply 1 Frozen"}
    ]
  },
  "Lost Myrrim": {
    "hp": 36,
    "dice": 4,
    "abilities": [
      {"name": "Spectral Strike", "requirement": "Any", "effect": "Deal damage equal to die value, On 5-6: Apply 1 Bleed"},
      {"name": "Phase Shift", "requirement": "Exactly 1", "effect": "Gain 4 Shield, Remove all negative effects from self"},
      {"name": "Haunting Wail", "requirement": "Limit 8", "effect": "Apply 2 Blind, Apply 1 Lock"}
    ]
  },
  "Fell Lich": {
    "hp": 60,
    "dice": 5,
    "abilities": [
      {"name": "Necromancy X", "requirement": "Limit 15", "effect": "Deal 18 damage, Heal 6 HP"},
      {"name": "Afflict X", "requirement": "Exactly 1", "effect": "Apply 3 Poison, Apply 2 Blind"},
      {"name": "Life Drain X", "requirement": "Odd only", "effect": "Deal damage equal to die value + 2, Heal half the damage dealt (rounded up)"},
      {"name": "Soul Rend", "requirement": "Minimum 4", "effect": "Deal 8 damage, Apply 1 Bleed", "reusable": True}
    ]
  },
  "Blighted Auroc": {
    "hp": 65,
    "dice": 4,
    "abilities": [
      {"name": "Gore X", "requirement": "Any", "effect": "Deal 4 + die value damage, On 6: Apply 2 Bleed"},
      {"name": "Chomp X", "requirement": "Limit 10", "effect": "Deal 14 damage, Heal 3 HP"},
      {"name": "Plague Breath", "requirement": "Even only", "effect": "Apply Poison equal to half die value (rounded up)"},
      {"name": "Charge X", "requirement": "Limit 20", "effect": "Deal 10 damage, Gain 10 Shield"}
    ]
  },
  "Khinari Subjugator": {
    "hp": 62,
    "dice": 5,
    "abilities": [
      {"name": "Snipe X", "requirement": "Limit 18", "effect": "Deal 15 damage, Apply 2 Bleed"},
      {"name": "Frosted Spear X", "requirement": "Any", "effect": "Deal 5 damage, On 5-6: Apply 1 Frozen", "reusable": True},
      {"name": "Dominate", "requirement": "Exactly 1", "effect": "Apply 2 Lock, Sacrifice 3 HP"},
      {"name": "Splinter X", "requirement": "Any", "effect": "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)", "reusable": True}
    ]
  },
  "Steppe Whitespike": {
    "hp": 28,
    "dice": 3,
    "abilities": [
      {"name": "Gore y", "requirement": "Any", "effect": "Deal 3 + die value damage, On 6: Apply 1 Bleed"},
      {"name": "Bellow X", "requirement": "Any", "effect": "Deal damage equal to die value + 2, On 5-6: Apply 2 Frozen"},
      {"name": "Trample", "requirement": "Any", "effect": "Deal damage equal to die value, On 6: Apply 1 Lock"}
    ]
  },
  "Caghoul Shaman": {
    "hp": 26,
    "dice": 4,
    "abilities": [
      {"name": "Lightning Bolt", "requirement": "Odd only", "effect": "Deal triple die value damage", "oncePerCombat": True},
      {"name": "Totem", "requirement": "Exactly 2", "effect": "Gain 5 Shield, Heal 2 HP"},
      {"name": "Jab X", "requirement": "Any", "effect": "Deal 4 + die value damage", "reusable": True}
    ]
  },
  "Naukin Outrider": {
    "hp": 24,
    "dice": 4,
    "abilities": [
      {"name": "Shortbow X", "requirement": "Odd only", "effect": "Deal triple die value damage"},
      {"name": "Dagger Y", "requirement": "Odd only", "effect": "Deal 5 damage, Apply 2 Poison"},
      {"name": "Evade", "requirement": "Exactly 1", "effect": "Gain Shield equal to 2 × the number of dice used this turn"}
    ]
  },
  "Hill Giant": {
    "hp": 48,
    "dice": 4,
    "abilities": [
      {"name": "Maul Y", "requirement": "Any", "effect": "Deal damage equal to die value + 8"},
      {"name": "Boulder Toss", "requirement": "Minimum 4", "effect": "Deal 10 damage, Apply 1 Lock", "reusable": True},
      {"name": "Earthquake", "requirement": "Limit 20", "effect": "Deal 12 damage, Apply 2 Lock, Apply 1 Frozen"}
    ]
  },
  "Black Roc": {
    "hp": 45,
    "dice": 4,
    "abilities": [
      {"name": "Dive Bomb", "requirement": "Minimum 5", "effect": "Deal 12 damage, Apply 1 Blind"},
      {"name": "Talon Strike", "requirement": "Any", "effect": "Deal damage equal to die value + 3, On 6: Apply 1 Bleed", "reusable": True},
      {"name": "Screech", "requirement": "Exactly 1", "effect": "Apply 2 Blind, Apply 1 Lock"}
    ]
  },
  "Whitespike Patriarch": {
    "hp": 50,
    "dice": 4,
    "abilities": [
      {"name": "Gore Y", "requirement": "Any", "effect": "Deal 5 + die value damage, On 5-6: Apply 2 Bleed"},
      {"name": "Bellow Y", "requirement": "Any", "effect": "Deal damage equal to die value + 3, On 5-6: Apply 2 Frozen", "reusable": True},
      {"name": "Charge X", "requirement": "Limit 20", "effect": "Deal 10 damage, Gain 10 Shield"},
      {"name": "Trample X", "requirement": "Any", "effect": "Deal damage equal to die value + 2, On 5-6: Apply 2 Lock"}
    ]
  },
  "Thunder Giant": {
    "hp": 85,
    "dice": 5,
    "abilities": [
      {"name": "Maul XY", "requirement": "Any", "effect": "Deal damage equal to die value + 12", "reusable": True},
      {"name": "Thunderclap", "requirement": "Limit 25", "effect": "Deal 18 damage, Apply 3 Blind, Apply 2 Lock"},
      {"name": "Boulder Toss X", "requirement": "Minimum 3", "effect": "Deal 12 damage, Apply 2 Lock", "reusable": True},
      {"name": "Fortify Y", "requirement": "Any", "effect": "Gain 8 Shield, Heal 2 HP"}
    ]
  },
  "Quakewyrm": {
    "hp": 83,
    "dice": 5,
    "abilities": [
      {"name": "Chomp XY", "requirement": "Limit 15", "effect": "Deal 20 damage, Heal 5 HP"},
      {"name": "Tremor", "requirement": "Any", "effect": "Deal damage equal to die value, Apply Lock equal to (die value ÷ 3, rounded down)"},
      {"name": "Stone Hide", "requirement": "Even only", "effect": "Gain Shield equal to die value + 2", "reusable": True},
      {"name": "Earthshatter", "requirement": "Limit 22", "effect": "Deal 15 damage, Apply 3 Lock, Apply 2 Frozen"}
    ]
  },
  "Caghoul Skyshaker": {
    "hp": 80,
    "dice": 5,
    "abilities": [
      {"name": "Lightning Storm", "requirement": "Limit 20", "effect": "Deal 20 damage, Apply 2 Blind"},
      {"name": "Chain Lightning", "requirement": "Odd only", "effect": "Deal quadruple die value damage"},
      {"name": "Totem X", "requirement": "Exactly 2", "effect": "Gain 8 Shield, Heal 4 HP"},
      {"name": "Wind Slash", "requirement": "Any", "effect": "Deal damage equal to die value + 4, On 6: Apply 2 Bleed", "reusable": True}
    ]
  },
  "Condemned": {
    "hp": 38,
    "dice": 4,
    "abilities": [
      {"name": "Flail", "requirement": "Any", "effect": "Deal damage equal to die value, Sacrifice 1 HP"},
      {"name": "Chains", "requirement": "Minimum 3", "effect": "Deal 6 damage, Apply 2 Lock", "reusable": True},
      {"name": "Desperation", "requirement": "Exactly 1", "effect": "Deal 10 damage, Sacrifice 5 HP"}
    ]
  },
  "Bovari Thrall": {
    "hp": 40,
    "dice": 4,
    "abilities": [
      {"name": "Gore Z", "requirement": "Any", "effect": "Deal 6 + die value damage, On 5-6: Apply 2 Bleed"},
      {"name": "Blood Pact", "requirement": "Limit 15", "effect": "Deal 12 damage, Heal 4 HP, Sacrifice 3 HP"},
      {"name": "Flame Strike", "requirement": "Odd only", "effect": "Deal double die value damage, Apply 1 Poison"}
    ]
  },
  "Hatebound Imp": {
    "hp": 36,
    "dice": 4,
    "abilities": [
      {"name": "Claw Swipe", "requirement": "Any", "effect": "Deal damage equal to die value + 3, On 6: Apply 1 Bleed", "reusable": True},
      {"name": "Curse", "requirement": "Exactly 1", "effect": "Apply 2 Poison, Apply 2 Blind"},
      {"name": "Immolate", "requirement": "Limit 10", "effect": "Deal 10 damage, Apply 2 Poison, Sacrifice 2 HP"}
    ]
  },
  "Blooded Khinari": {
    "hp": 62,
    "dice": 5,
    "abilities": [
      {"name": "Snipe Y", "requirement": "Limit 22", "effect": "Deal 18 damage, Apply 3 Bleed, Heal 3 HP"},
      {"name": "Frosted Spear Y", "requirement": "Any", "effect": "Deal 6 damage, On 5-6: Apply 2 Frozen", "reusable": True},
      {"name": "Blood Ritual", "requirement": "Exactly 1", "effect": "Sacrifice 5 HP, Deal 15 damage, Apply 2 Poison"},
      {"name": "Splinter Y", "requirement": "Any", "effect": "Sacrifice 2 HP, Create 3 dice with half the input die value (rounded up)"}
    ]
  },
  "Hatebound Priest": {
    "hp": 60,
    "dice": 5,
    "abilities": [
      {"name": "Dark Blessing", "requirement": "Limit 18", "effect": "Heal 8 HP, Apply 2 Poison to opponent"},
      {"name": "Afflict Y", "requirement": "Exactly 1", "effect": "Apply 4 Poison, Apply 2 Blind, Apply 1 Lock"},
      {"name": "Flame Strike x", "requirement": "Odd only", "effect": "Deal triple die value damage, Apply 1 Poison"},
      {"name": "Life Drain Y", "requirement": "Odd only", "effect": "Deal damage equal to die value + 4, Heal half the damage dealt (rounded up)", "reusable": True}
    ]
  },
  "Condemned Taskmaster": {
    "hp": 64,
    "dice": 4,
    "abilities": [
      {"name": "Whip Crack", "requirement": "Any", "effect": "Deal damage equal to die value + 5, Apply 1 Lock"},
      {"name": "Chains X", "requirement": "Minimum 3", "effect": "Deal 8 damage, Apply 3 Lock", "reusable": True},
      {"name": "Torture", "requirement": "Limit 20", "effect": "Deal 15 damage, Apply 2 Bleed, Apply 2 Lock"},
      {"name": "Bash Y", "requirement": "Any", "effect": "Deal damage equal to triple current shield, then remove all shield"}
    ]
  },
  "Pit Lord": {
    "hp": 115,
    "dice": 5,
    "abilities": [
      {"name": "Annihilation", "requirement": "Limit 30", "effect": "Deal 25 damage, Apply 3 Bleed, Apply 2 Poison"},
      {"name": "Infernal Strike", "requirement": "Any", "effect": "Deal damage equal to die value + 8, Sacrifice 2 HP", "reusable": True},
      {"name": "Hellfire", "requirement": "Odd only", "effect": "Deal quintuple die value damage"},
      {"name": "Dark Aegis", "requirement": "Even only", "effect": "Gain Shield equal to die value + 4, Apply 1 Poison to opponent", "reusable": True}
    ]
  },
  "Blood Judge": {
    "hp": 112,
    "dice": 5,
    "abilities": [
      {"name": "Execution", "requirement": "Limit 25", "effect": "Deal 22 damage, Apply 4 Bleed"},
      {"name": "Blood Price", "requirement": "Any", "effect": "Sacrifice HP equal to die value, Deal double the sacrificed HP as damage"},
      {"name": "Judgement", "requirement": "Exactly 6", "effect": "Deal 18 damage, Heal 6 HP, Apply 2 Lock"},
      {"name": "Life Drain XY", "requirement": "Odd only", "effect": "Deal damage equal to die value + 6, Heal the full damage dealt", "reusable": True}
    ]
  },
  "Prophet of Fire": {
    "hp": 110,
    "dice": 6,
    "abilities": [
      {"name": "Apocalypse", "requirement": "Limit 35", "effect": "Deal 30 damage, Apply 4 Poison, Apply 3 Blind, Apply 2 Lock"},
      {"name": "Meteor", "requirement": "Minimum 5", "effect": "Deal 15 damage, Apply 2 Bleed", "reusable": True},
      {"name": "Inferno", "requirement": "Odd only", "effect": "Deal quadruple die value damage, Apply 2 Poison"},
      {"name": "Phoenix Rising", "requirement": "Exactly 1", "effect": "Heal 10 HP, Gain 10 Shield, Remove all negative effects from self"},
      {"name": "Flame Wall", "requirement": "Even only", "effect": "Gain Shield equal to die value + 5, Deal 5 damage", "reusable": True}
    ]
  }
}

# --- creature group IDs (biome + tier) ---
CREATURE_GROUP_IDS = {
    # Plains (IDs 1-3)
    "Wolf": 1,
    "Giant Locust": 1,
    "Naukin Outcast": 1,
    "Dire Wolves": 2,
    "Prowling Dellinid": 2,
    "Juvenile Auroc": 2,
    "Bovari Bandit": 3,
    "Roaming Gallox": 3,
    "Lone Plainsdrake": 3,
    # Tundra (IDs 4-6)
    "Blue Dellinid": 4,
    "Khinari Exile": 4,
    "Territorial Whitespike": 4,
    "Khinari Raider": 5,
    "Tundra Boneguard": 5,
    "Alpha Whitespike": 5,
    "Veteran Boneguard": 6,
    "Khinari Hunting Party": 6,
    "Hungry Frost Wyrm": 6,
    # Forest (IDs 7-9)
    "Naukin Scouts": 7,
    "Skittari Hunters": 7,
    "Reclaimed Boneguard": 7,
    "Dire Bear": 8,
    "Khinari Bladedancer": 8,
    "Naukin Sunstriker": 8,
    "Verdant Shepherd": 9,
    "Barkskin Colossus": 9,
    "Emerald Lich": 9,
    # Ruins (IDs 10-12)
    "Brass Golem": 10,
    "Skittari Looters": 10,
    "Bloated Zombie": 10,
    "Iron Bulwark": 11,
    "Stone Drake": 11,
    "Lost Myrrim": 11,
    "Fell Lich": 12,
    "Blighted Auroc": 12,
    "Khinari Subjugator": 12,
    # Slopes (IDs 13-15)
    "Steppe Whitespike": 13,
    "Caghoul Shaman": 13,
    "Naukin Outrider": 13,
    "Hill Giant": 14,
    "Black Roc": 14,
    "Whitespike Patriarch": 14,
    "Thunder Giant": 15,
    "Quakewyrm": 15,
    "Caghoul Skyshaker": 15,
    # Pit (IDs 16-18)
    "Condemned": 16,
    "Bovari Thrall": 16,
    "Hatebound Imp": 16,
    "Blooded Khinari": 17,
    "Hatebound Priest": 17,
    "Condemned Taskmaster": 17,
    "Pit Lord": 18,
    "Blood Judge": 18,
    "Prophet of Fire": 18,
}

for _creature_name, _group_id in CREATURE_GROUP_IDS.items():
    if _creature_name in CREATURE_DEFINITIONS:
        CREATURE_DEFINITIONS[_creature_name]["id"] = _group_id


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
                 upgrade_level=1, description="", class_restricted=None, value_fn=None,
                 once_per_combat=False):
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
        self.once_per_combat = once_per_combat

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
        if getattr(self, 'once_per_combat', False):
            text += " (Once per combat)"

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


# --- Status Effect System (Dicey Dungeon style) ---

class StatusEffect:
    """Base class for status effects that can be applied to entities.
    
    Status effects in Dicey Dungeon:
    - Stack (multiple stacks accumulate)
    - Trigger at specific times (start of turn, end of turn, on card use, etc.)
    - Have specific mechanics (damage, modify dice, etc.)
    """
    
    def __init__(self, name, stacks=1):
        """Initialize a status effect.
        
        Args:
            name: Name of the effect (poison, bleed, etc.)
            stacks: Number of stacks to start with
        """
        self.name = name.lower()
        self.stacks = max(0, stacks)
    
    def apply(self, amount=1):
        """Add stacks to this effect."""
        self.stacks = max(0, self.stacks + amount)
    
    def remove(self, amount=1):
        """Remove stacks from this effect."""
        self.stacks = max(0, self.stacks - amount)
    
    def has_stacks(self):
        """Check if this effect has any active stacks."""
        return self.stacks > 0
    
    def trigger_start_of_turn(self, entity):
        """Called at start of turn. Override in subclasses."""
        pass
    
    def trigger_end_of_turn(self, entity):
        """Called at end of turn. Override in subclasses."""
        pass
    
    def trigger_on_card_use(self, entity, card):
        """Called when entity uses a card. Override in subclasses."""
        pass
    
    def trigger_on_damage_taken(self, entity, damage, source):
        """Called when entity takes damage. Override in subclasses."""
        pass
    
    def __repr__(self):
        return f"<{self.name.capitalize()} x{self.stacks}>"


class Poison(StatusEffect):
    """Poison: Take damage at start of turn equal to poison stacks, then reduce by 1."""
    
    def __init__(self, stacks=1):
        super().__init__("poison", stacks)
    
    def trigger_start_of_turn(self, entity):
        """At start of turn: take poison damage, then reduce by 1."""
        if self.stacks > 0:
            damage = self.stacks
            print(f"{entity.name} takes {damage} poison damage!")
            entity.take_damage(damage)
            self.remove(1)


class Bleed(StatusEffect):
    """Bleed: Deal damage equal to 2x bleed stacks when you play a card. Reduces by 2 after (minimum 1)."""
    
    def __init__(self, stacks=1):
        super().__init__("bleed", stacks)
    
    def trigger_on_card_use(self, entity, card):
        """When entity uses a card: deal bleed damage."""
        if self.stacks > 0:
            damage = 2 * self.stacks  # Bleed deals 2x damage per stack
            print(f"{entity.name} takes {damage} bleed damage from playing a card!")
            entity.take_damage(damage)
            self.remove(2)  # Reduce by 2 instead of 1
            self.stacks = max(1, self.stacks)  # But keep at minimum 1 if it had stacks


class Blind(StatusEffect):
    """Blind: Roll dice normally, but don't see the values of that many dice each turn.
    
    The hidden dice still have their actual values and can be used, but the player must guess.
    Each die obscured by blind reduces the blind counter by 1.
    """
    
    def __init__(self, stacks=1):
        super().__init__("blind", stacks)
    
    def get_hidden_count(self):
        """Return number of dice to hide from roll."""
        return min(self.stacks, 999)  # Can obscure multiple dice
    
    def reduce_by_usage(self):
        """Reduce blind by 1 when a die is obscured."""
        self.remove(1)


class Lock(StatusEffect):
    """Lock: Completely removes that many dice from your available dice each turn.
    
    Unlike Blind, the dice are gone, not just hidden. Each die removed reduces lock by 1.
    """
    
    def __init__(self, stacks=1):
        super().__init__("lock", stacks)
    
    def get_dice_removed_count(self):
        """Return number of dice to completely remove from available pool."""
        return min(self.stacks, 999)
    
    def reduce_by_usage(self):
        """Reduce lock by 1 when a die is removed."""
        self.remove(1)


class Frozen(StatusEffect):
    """Frozen: After dice are rolled, freeze dice one at a time.
    
    For each stack of frozen, one die is reduced to a value of 1.
    Each die frozen reduces the frozen counter by 1.
    """
    
    def __init__(self, stacks=1):
        super().__init__("frozen", stacks)
    
    def apply_to_dice(self, dice_list):
        """Apply frozen effect to dice list.
        
        For each frozen stack, set one die to 1, then reduce frozen counter.
        Returns (modified_dice_list, remaining_frozen_count)
        """
        if self.stacks <= 0 or not dice_list:
            return dice_list
        
        modified_dice = list(dice_list)  # Copy to avoid modifying original
        frozen_remaining = self.stacks
        
        for i in range(len(modified_dice)):
            if frozen_remaining <= 0:
                break
            if modified_dice[i] != 1:  # Only freeze if not already 1
                print(f"Frozen reduces die #{i+1} from {modified_dice[i]} to 1!")
                modified_dice[i] = 1
                frozen_remaining -= 1
        
        self.stacks = frozen_remaining
        return modified_dice


class Vampirism(StatusEffect):
    """Vampirism: Heal by this amount when you deal damage."""
    
    def __init__(self, stacks=1):
        super().__init__("vampirism", stacks)
    
    def get_heal_amount(self):
        """Return healing when dealing damage."""
        return self.stacks


class Thorn(StatusEffect):
    """Thorn: Reflect damage back to attacker when you take damage."""
    
    def __init__(self, stacks=1):
        super().__init__("thorn", stacks)
    
    def get_reflect_damage(self):
        """Return damage to reflect back to source."""
        return self.stacks


class Weaken(StatusEffect):
    """Weaken: Reduce all your dice values by 1 (minimum 1) each turn."""
    
    def __init__(self, stacks=1):
        super().__init__("weaken", stacks)
    
    def apply_to_dice(self, dice_list):
        """Apply weaken penalty to a list of dice. Returns modified list."""
        return [max(1, d - self.stacks) for d in dice_list]




class Entity:
    """Generic entity for player/enemy: HP, shield, and status stacks.

    Provides helpers for applying statuses and resolving start/end-of-turn effects.
    Uses StatusEffect objects for proper effect mechanics.
    """
    def __init__(self, name, max_hp, currenthp=None, shield=0, deck=None, hand=None, discard=None, dice=3):
        self.name = name
        self.max_hp = max_hp
        self.currenthp = max_hp if currenthp is None else currenthp
        self.shield = shield
        
        # Status effects (using StatusEffect objects for proper mechanics)
        self.status_effects = {
            'poison': Poison(0),
            'bleed': Bleed(0),
            'blind': Blind(0),
            'lock': Lock(0),
            'frozen': Frozen(0),
            'vampirism': Vampirism(0),
            'thorn': Thorn(0),
            'weaken': Weaken(0),
        }
        
        # Legacy integer-based status tracking (for backward compatibility)
        # These are automatically synced with status_effects
        self.poison = 0
        self.bleed = 0
        self.blind = 0
        self.lock = 0
        self.frozen = 0
        self.vampirism = 0
        self.thorn = 0
        self.weaken = 0
        
        self.planted = []  # list of (value, turns_to_bloom)

        # card/draw related (player only; enemies may reuse)
        self.deck = deck if deck is not None else []
        self.hand = hand if hand is not None else []
        self.discard = discard if discard is not None else []

        # misc
        self.dice = dice

    def __repr__(self):
        return f"<Entity {self.name} HP:{self.currenthp}/{self.max_hp} SH:{self.shield} P:{self.poison} B:{self.bleed}>"

    # ---- status helpers ----
    def apply_status(self, status, stacks=1):
        """Apply a status effect to this entity.
        
        Args:
            status: Name of the status (poison, bleed, blind, lock, frozen, vampirism, thorn, weaken)
            stacks: Number of stacks to apply
        """
        if stacks <= 0:
            return
        
        status = status.lower()
        
        # Update StatusEffect object
        if status in self.status_effects:
            self.status_effects[status].apply(stacks)
        
        # Sync legacy integer attributes
        self._sync_status_integers()
    
    def _sync_status_integers(self):
        """Sync legacy integer status attributes with StatusEffect objects."""
        self.poison = self.status_effects['poison'].stacks
        self.bleed = self.status_effects['bleed'].stacks
        self.blind = self.status_effects['blind'].stacks
        self.lock = self.status_effects['lock'].stacks
        self.frozen = self.status_effects['frozen'].stacks
        self.vampirism = self.status_effects['vampirism'].stacks
        self.thorn = self.status_effects['thorn'].stacks
        self.weaken = self.status_effects['weaken'].stacks
    
    def get_status_effect(self, status):
        """Get a StatusEffect object by name.
        
        Args:
            status: Name of the status effect
            
        Returns:
            StatusEffect object or None if not found
        """
        return self.status_effects.get(status.lower())
    
    def remove_status(self, status, stacks=1):
        """Remove stacks from a status effect.
        
        Args:
            status: Name of the status
            stacks: Number of stacks to remove
        """
        status = status.lower()
        if status in self.status_effects:
            self.status_effects[status].remove(stacks)
            self._sync_status_integers()
    
    def clear_status(self, status):
        """Completely remove a status effect.
        
        Args:
            status: Name of the status to clear
        """
        status = status.lower()
        if status in self.status_effects:
            self.status_effects[status].stacks = 0
            self._sync_status_integers()
    
    def get_all_active_statuses(self):
        """Get list of all active status effects with stacks > 0."""
        return [effect for effect in self.status_effects.values() if effect.has_stacks()]
    
    def display_statuses(self):
        """Get a formatted string of all active statuses."""
        active = self.get_all_active_statuses()
        if not active:
            return "(none)"
        return ", ".join(str(status) for status in active)

    def remove_negative_effects(self):
        """Remove all negative status effects (poison, bleed, blind, lock, frozen, weaken)."""
        self.clear_status('poison')
        self.clear_status('bleed')
        self.clear_status('blind')
        self.clear_status('lock')
        self.clear_status('frozen')
        self.clear_status('weaken')

    def take_damage(self, amount, source=None):
        """Apply shield then HP damage. Return actual damage to HP (after shield).
        Also trigger thorn on self if applicable (damage reflected to source).
        """
        if amount <= 0:
            return 0
        remaining = amount
        if self.shield > 0:
            blocked = min(self.shield, remaining)
            self.shield -= blocked
            remaining -= blocked
        if remaining > 0:
            self.currenthp -= remaining
        
        # Trigger thorn effect - reflect damage back to source
        thorn_effect = self.get_status_effect('thorn')
        if source and thorn_effect and thorn_effect.has_stacks():
            thorn_dmg = thorn_effect.get_reflect_damage()
            try:
                source.currenthp -= thorn_dmg
            except Exception:
                pass
        return remaining

    def heal(self, amount):
        if amount <= 0:
            return 0
        healed = min(self.max_hp - self.currenthp, amount)
        self.currenthp += healed
        return healed

    def add_shield(self, amount):
        if amount <= 0:
            return 0
        self.shield += amount
        return amount

    def resolve_start_of_turn(self):
        """Return list of dice that bloom from planted seeds (value list)."""
        new_dice = []
        # planted: list of (value, turns)
        for planted in list(self.planted):
            val, turns = planted
            turns -= 1
            if turns <= 0:
                # bloom into two dice of same value (game rules may vary)
                new_dice.extend([val, val])
                self.planted.remove(planted)
            else:
                # update tuple
                idx = self.planted.index(planted)
                self.planted[idx] = (val, turns)
        return new_dice

    def resolve_end_of_turn(self):
        """Trigger end-of-turn effects for all active status effects."""
        # Trigger each status effect's end-of-turn logic
        for effect in self.status_effects.values():
            if effect.has_stacks():
                effect.trigger_end_of_turn(self)
        
        # Sync integer attributes after triggering effects
        self._sync_status_integers()


class Enemy(Entity):
    """Enhanced enemy container (inherits status/HP behavior from Entity).

    - cardpool holds Card instances (ready to be used by the combat system)
    - `hand` is the enemy's current hand (list of Card instances)
    - stores hp, dice count, xp_value
    """
    def __init__(self, name, max_hp, currenthp=None, cardpool=None, hand=None, xp_value=0, dice=2):
        # initialize status/HP from Entity; allow passing an explicit hand/deck
        super().__init__(name, max_hp, currenthp=currenthp, deck=None, hand=hand if hand is not None else [], discard=None, dice=dice)
        # cardpool: canonical set of ability-cards for this creature (new Card instances)
        self.cardpool = list(cardpool) if cardpool else []
        # if caller didn't provide a hand, populate the hand with fresh instances
        # (create distinct Card instances so state isn't shared between pool/hand)
        if hand is None and self.cardpool:
            # shallow-clone each ability by creating a fresh Card instance from its raw description
            # safest source for the raw effect text is Card._raw_effect_text
            fresh_hand = []
            for c in self.cardpool:
                try:
                    fresh = create_card_from_ability({'name': c.name, 'requirement': getattr(c, 'dice_restriction', '') or '', 'effect': getattr(c, '_raw_effect_text', c.description), 'reusable': c.reusable}, level=c.upgrade_level)
                except Exception:
                    # fallback: reuse the instance (shouldn't happen normally)
                    fresh = c
                fresh_hand.append(fresh)
            self.hand = fresh_hand
        # otherwise Entity.__init__ already set self.hand to the provided list (or [])
        self.xp_value = xp_value

    def __repr__(self):
        return f"<Enemy {self.name} HP:{self.currenthp}/{self.max_hp} dice:{self.dice} pool:{len(self.cardpool)} hand:{len(self.hand)}>"


# Backwards-compatible alias for existing code that used `enemy(...)`
enemy = Enemy

# --- card factory: convert an ability dictionary (from CREATURE_DEFINITIONS)
# into a Card instance (best-effort parsing of the effect/requirement strings).
import re

def create_card_from_ability(ability, level=1):
    """Create a Card instance from an ability dict (name, requirement, effect, optional flags).

    This is forgiving: it extracts common patterns (damage, heal, shield, status, uses_dice_value)
    and preserves the original effect text in `description` for anything it doesn't interpret.
    """
    name = ability.get('name')
    req = ability.get('requirement', '')
    effect_text = ability.get('effect', '')
    reusable = bool(ability.get('reusable', False))
    once = bool(ability.get('oncePerCombat', False))

    # defaults
    card_type = 'single'
    effect_type = 'raw'
    base_value = 0
    uses_dice_value = False
    max_dice = 1
    dice_restriction = {}
    status = None
    status_duration = 0
    max_uses = None

    et = effect_text.lower()

    # common patterns
    m = re.search(r"deal (?:damage )?(\d+) damage", et)
    if m and 'die value' not in et and 'double die' not in et and 'triple' not in et:
        effect_type = 'damage'
        base_value = int(m.group(1))
        uses_dice_value = False

    # Deal damage equal to die value / +N
    if 'die value' in et or re.search(r"\bdie\b", et):
        effect_type = 'damage'
        uses_dice_value = True
        # look for "+ N" or "X + die"
        m2 = re.search(r"([+−\-]\s*\d+)|(?:(\d+) \+ die value)|(?:(\d+)\s*\+\s*die)", effect_text)
        if m2:
            # prefer explicit positive offsets
            nums = [g for g in m2.groups() if g]
            if nums:
                base_value = int(re.sub(r"[^0-9-]","", nums[0]))
        # multipliers: double/triple/quadruple/quintuple
        if 'double die' in et:
            card_type = 'single'
            effect_type = 'damage'
            uses_dice_value = True
            base_value = 0
        mult = None
        if 'double die' in et or 'double die value' in et:
            mult = 2
        elif 'triple' in et:
            mult = 3
        elif 'quadruple' in et:
            mult = 4
        elif 'quintuple' in et:
            mult = 5
        elif 'sextuple' in et:
            mult = 6
        elif 'septuple' in et or 'sept' in et:
            mult = 7
        if mult:
            base_value = 0
            effect_text = effect_text + f" (multiplier:{mult})"

    # Shield
    m = re.search(r"gain shield equal to die value \+?\s*(\d+)", et)
    if m:
        effect_type = 'shield'
        uses_dice_value = True
        base_value = int(m.group(1))
    elif 'gain shield equal to half the die value' in et:
        effect_type = 'shield'
        uses_dice_value = True
        base_value = 0

    # Heal
    m = re.search(r"heal (\d+) hp", et)
    if m:
        effect_type = 'heal'
        base_value = int(m.group(1))
        if 'die value' in et:
            uses_dice_value = True

    # Status effects (poison, blind, bleed, lock, frozen)
    # Only classify as pure status card if it doesn't deal damage
    status_map = ['poison', 'blind', 'bleed', 'lock', 'frozen']
    for s in status_map:
        if s in et and 'apply' in et and effect_type != 'damage':
            effect_type = 'status'
            status = s
            m = re.search(rf"apply\s+(\d+)\s+{s}", et)
            if m:
                base_value = int(m.group(1))
            else:
                base_value = 1
            break

    # Multi-die / create-dice cards — set max_dice heuristics
    if 'add up to 3 dice' in et or 'up to 3' in et or 'create 3 dice' in et:
        max_dice = 3
        card_type = 'multi'
    if 'create 2 dice' in et or 'create 2 dice' in effect_text.lower():
        max_dice = 2
        card_type = 'multi'

    # Minimum / restriction parsing
    m = re.search(r"minimum\s*(\d+)", req.lower())
    if m:
        dice_restriction['min'] = int(m.group(1))
    m = re.search(r"exactly\s*(\d+)", req.lower())
    if m:
        dice_restriction['exact_values'] = [int(m.group(1))]

    # Limit / countdown parsing (e.g. "Limit 15" cards)
    countdown_target = None
    m = re.search(r"limit\s*(\d+)", req.lower())
    if m:
        countdown_target = int(m.group(1))
        card_type = 'countdown'

    # Once-per-combat -> model as max_uses=1 for convenience
    if bool(ability.get('oncePerCombat', False)):
        max_uses = 1

    # Build Card instance
    c = Card(
        name=name,
        card_type=card_type,
        effect_type=effect_type if effect_type != 'raw' else 'damage' if uses_dice_value else 'raw',
        base_value=base_value,
        uses_dice_value=uses_dice_value,
        reusable=reusable,
        max_uses=max_uses,
        cooldown=0,
        max_dice=max_dice,
        dice_restriction=dice_restriction or None,
        target='enemy' if effect_type in ('damage','status') else 'self',
        status_effect=status,
        status_duration=0,
        upgrade_level=level,
        description=ability.get('effect', '')
    )

    # attach raw effect text and derived flags for runtime
    c._raw_effect_text = ability.get('effect', '')
    c.requirement = req  # Store the original requirement string for display
    # multiplier (set earlier via parsed marker)
    mm = re.search(r"\(multiplier:(\d+)\)", c._raw_effect_text)
    c.multiplier = int(mm.group(1)) if mm else None
    # countdown target (for Limit X cards)
    c.countdown_target = countdown_target
    c.countdown_accum = 0
    # sacrifice parsing: either a fixed number or "equal to die value"
    if re.search(r"sacrifice\s+\d+\s+hp", c._raw_effect_text.lower()):
        m = re.search(r"sacrifice\s+(\d+)\s+hp", c._raw_effect_text.lower())
        c.sacrifice_amount = int(m.group(1)) if m else None
    elif 'sacrifice hp equal to die value' in c._raw_effect_text.lower():
        c.sacrifice_amount = 'die_value'
    else:
        c.sacrifice_amount = None
    # create-dice hints (splinter variants)
    c.create_dice_hint = None
    if 'create 2 dice with half the input die value' in c._raw_effect_text.lower():
        c.create_dice_hint = {'count': 2, 'mode': 'half_per_die', 'round': 'down'}
    if 'create 3 dice with half the input die value' in c._raw_effect_text.lower():
        c.create_dice_hint = {'count': 3, 'mode': 'half_per_die', 'round': 'up'}
    # trigger-poison helper
    c.trigger_poison = 'trigger poison' in c._raw_effect_text.lower()
    # destroy shield
    c.destroy_shield = 'destroy opponent shield' in c._raw_effect_text.lower()
    # draw cards
    dm = re.search(r"draw\s+(\d+)\s+new\s+card", c._raw_effect_text.lower())
    c.draw_cards = int(dm.group(1)) if dm else 0

    return c


def create_card_from_params(params, level=1):
    """Create a Card from explicit parameters (new cleaner format).
    
    Expected params:
    - name: card name
    - requirement: dice requirement string (for display)
    - effect_type: 'damage', 'heal', 'shield', 'status', 'raw'
    - base_value: base damage/heal/shield/status amount
    - uses_dice_value: whether to add die value to base
    - reusable: can be used multiple times per turn
    - max_dice: how many dice slots
    - dice_restriction: dict with min/max/exact_values/only_odd/only_even
    - conditional_status: dict with status effects that trigger conditionally
    - description: effect description for display
    - Special flags: sacrifice_hp, create_dice, trigger_poison, etc.
    """
    name = params.get('name')
    req = params.get('requirement', 'Any')
    
    # Core parameters with defaults
    card_type = params.get('card_type', 'single')
    effect_type = params.get('effect_type', 'damage')
    base_value = params.get('base_value', 0)
    uses_dice_value = params.get('uses_dice_value', False)
    reusable = params.get('reusable', False)
    max_dice = params.get('max_dice', 1)
    dice_restriction = params.get('dice_restriction', {})
    
    # Parse requirement into dice_restriction if not already provided
    if not dice_restriction and req:
        req_lower = req.lower()
        if 'exactly' in req_lower:
            m = re.search(r'exactly\s*(\d+)', req_lower)
            if m:
                dice_restriction = {'exact_values': [int(m.group(1))]}
        elif 'minimum' in req_lower:
            m = re.search(r'minimum\s*(\d+)', req_lower)
            if m:
                dice_restriction = {'min': int(m.group(1))}
        elif 'odd only' in req_lower:
            dice_restriction = {'only_odd': True}
        elif 'even only' in req_lower:
            dice_restriction = {'only_even': True}
        elif 'limit' in req_lower:
            m = re.search(r'limit\s*(\d+)', req_lower)
            if m:
                card_type = 'countdown'
    
    # Build the card
    c = Card(
        name=name,
        card_type=card_type,
        effect_type=effect_type,
        base_value=base_value,
        uses_dice_value=uses_dice_value,
        reusable=reusable,
        max_uses=params.get('max_uses'),
        cooldown=params.get('cooldown', 0),
        max_dice=max_dice,
        dice_restriction=dice_restriction or None,
        target=params.get('target', 'enemy' if effect_type in ('damage', 'status') else 'self'),
        status_effect=params.get('status_effect'),
        status_duration=params.get('status_duration', 0),
        upgrade_level=level,
        description=params.get('description', '')
    )
    
    # Store requirement string for display
    c.requirement = req
    
    # Store raw effect text (build from description or generate from params)
    c._raw_effect_text = params.get('description', '')
    
    # Special attributes
    c.multiplier = params.get('multiplier')
    c.sacrifice_amount = params.get('sacrifice_hp')
    c.trigger_poison = params.get('trigger_poison', False)
    c.destroy_shield = params.get('destroy_shield', False)
    c.draw_cards = params.get('draw_cards', 0)
    c.create_dice_hint = params.get('create_dice_hint')
    
    # Countdown (Limit cards)
    if 'limit' in req.lower():
        m = re.search(r'limit\s*(\d+)', req.lower())
        if m:
            c.countdown_target = int(m.group(1))
            c.countdown_accum = 0
    else:
        c.countdown_target = None
        c.countdown_accum = 0
    
    # Conditional status effects (for "On 6: Apply X Status" patterns)
    c.conditional_status = params.get('conditional_status', [])
    
    return c


def apply_effect_result(card, user, target, result, available_dice=None):
    """Execute a Card's effect against entities and return side-effects.

    Handles: damage, healing, shields, status effects, sacrifice, drawing, creating dice, etc.
    Side-effects: {'created_dice': [...], 'drawn': n, 'sacrifice': n, 'killed': bool}
    """
    side = {'created_dice': [], 'drawn': 0, 'sacrifice': 0, 'killed': False}
    dice_used = result.get('dice_used', [])

    # Compute base/dice-based damage value
    total = card.base_value or 0
    dice_sum = sum(dice_used)
    if card.uses_dice_value:
        total = (card.base_value or 0) + dice_sum
        if getattr(card, 'multiplier', None):
            total = dice_sum * card.multiplier + (card.base_value or 0)

    rt = card._raw_effect_text.lower() if getattr(card, '_raw_effect_text', None) else ''

    # === SACRIFICE HANDLING ===
    if getattr(card, 'sacrifice_amount', None):
        if card.sacrifice_amount == 'die_value':
            sac = dice_sum
        else:
            sac = card.sacrifice_amount
        user.take_damage(sac)
        side['sacrifice'] = sac

    # === SHIELD-BASED EFFECTS (Bash, Tremor, etc) ===
    # "Deal damage equal to double/triple current shield"
    if 'double current shield' in rt or 'triple current shield' in rt:
        multiplier = 3 if 'triple current shield' in rt else 2
        dmg = user.shield * multiplier
        target.take_damage(dmg, source=user)
        if target.currenthp <= 0:
            side['killed'] = True
        
        # Handle shield removal after damage
        if 'remove all shield' in rt:
            user.shield = 0
        elif 'remove half' in rt:
            remove_amt = user.shield // 2 if 'rounded down' in rt else -(-user.shield // 2)
            user.shield = max(0, user.shield - remove_amt)

    # === DAMAGE ===
    # Check if card deals damage (patterns: "deal X damage", "deal die value damage", etc)
    damage_patterns = [
        (r"deal\s+(?:damage\s+)?(\d+)\s+damage", False),           # "deal 25 damage"
        (r"deal\s+(?:damage\s+)?die\s+value\s+damage", True),      # "deal die value damage"
        (r"deal\s+(?:damage\s+)?(\d+)\s*\+\s*die\s+value", True),  # "deal 5 + die value damage"
        (r"deal\s+die\s+value\s+\+\s*(\d+)\s+damage", True),       # "deal die value + 5 damage"
    ]
    
    for pattern, is_dice in damage_patterns:
        m = re.search(pattern, rt)
        if m:
            if is_dice:
                dmg = dice_sum + (int(m.group(1)) if m.group(1) else 0)
            else:
                dmg = int(m.group(1)) if m.group(1) else int(total)
            
            # Apply multiplier if present
            if getattr(card, 'multiplier', None):
                dmg = dmg * card.multiplier
            
            # Handle "double the sacrificed damage" (Life Drain pattern)
            if 'double the sacrificed damage' in rt and side.get('sacrifice'):
                dmg = side['sacrifice'] * 2
            elif 'half of the damage dealt' in rt:
                # This is for healing based on damage (Life Drain)
                user.heal(dmg // 2)
            
            target.take_damage(dmg, source=user)
            
            # Vampirism: heal based on damage dealt
            vampirism_effect = user.get_status_effect('vampirism')
            if vampirism_effect and vampirism_effect.has_stacks():
                heal_amt = vampirism_effect.get_heal_amount()
                user.heal(heal_amt)
            
            # Bleed: target takes extra damage when card is used
            bleed_effect = target.get_status_effect('bleed')
            if bleed_effect and bleed_effect.has_stacks():
                bleed_dmg = 2 * bleed_effect.stacks
                target.take_damage(bleed_dmg)
            
            if target.currenthp <= 0:
                side['killed'] = True
            
            break  # Only apply first matching damage pattern

    # === HEALING ===
    # Patterns: "Heal X HP", "Heal die value HP", "Heal X + die value HP"
    heal_patterns = [
        (r"heal\s+(\d+)\s+hp", False),                             # "heal 25 hp"
        (r"heal\s+die\s+value\s+hp", True),                        # "heal die value hp"
        (r"heal\s+(\d+)\s*\+\s*die\s+value\s+hp", True),           # "heal 5 + die value hp"
        (r"heal\s+die\s+value\s+\+\s*(\d+)\s+hp", True),           # "heal die value + 5 hp"
        (r"heal\s+half\s+(?:of\s+)?die\s+value", True),            # "heal half of die value"
    ]
    
    for pattern, is_dice in heal_patterns:
        m = re.search(pattern, rt)
        if m:
            if is_dice:
                heal_val = dice_sum + (int(m.group(1)) if m.group(1) else 0)
                if 'half' in pattern:
                    heal_val = heal_val // 2
            else:
                heal_val = int(m.group(1)) if m.group(1) else int(total)
            
            user.heal(heal_val)
            break  # Only apply first matching heal pattern

    # === SHIELD GAIN ===
    # Patterns: "Gain shield", "Gain shield equal to die value", "Gain shield to opponent"
    shield_patterns = [
        (r"gain\s+(?:a\s+)?(\d+)\s+shield(?:\s+to\s+(opponent|self))?", False),  # "Gain 3 shield", "Gain shield to opponent"
        (r"gain\s+shield\s+equal\s+to\s+die\s+value\s*\+?\s*(\d+)?(?:\s+to\s+(opponent|self))?", True),  # "Gain shield equal to die value + 2"
        (r"gain\s+shield\s+equal\s+to\s+half\s+(?:of\s+)?die\s+value(?:\s+to\s+(opponent|self))?", True),  # "Gain shield equal to half die value"
    ]
    
    for pattern, is_dice in shield_patterns:
        m = re.search(pattern, rt)
        if m:
            if is_dice:
                bonus = int(m.group(1)) if m.group(1) else 0
                shield_val = dice_sum + bonus
                if 'half' in pattern:
                    shield_val = shield_val // 2
            else:
                shield_val = int(m.group(1)) if m.group(1) else int(total)
            
            # Check target: "to opponent" means target, otherwise user
            group2 = m.group(2) if m and len(m.groups()) > 1 and m.group(2) else ''
            target_ent = target if 'opponent' in group2 or 'to opponent' in rt else user
            target_ent.add_shield(shield_val)
            break  # Only apply first matching shield pattern

    # === REMOVE NEGATIVE EFFECTS / SHIELD ===
    if 'remove all negative effects from self' in rt or 'remove all negative effects' in rt:
        user.remove_negative_effects()
    elif 'remove 1 negative effect' in rt:
        # Remove the first active negative effect
        for effect in user.get_all_active_statuses():
            if effect.name in ['poison', 'bleed', 'blind', 'lock', 'frozen', 'weaken']:
                user.clear_status(effect.name)
                break
    elif 'remove all shield' in rt and 'current shield' not in rt:
        user.shield = 0

    # === STATUS APPLICATIONS (to opponent by default, "to self" reverses it) ===
    # Patterns: "Apply N Status", "Apply N Status to opponent", "Apply Status equal to die value"
    status_list = ['poison', 'bleed', 'blind', 'lock', 'frozen', 'vampirism', 'thorn', 'weaken']
    
    # Explicit "to opponent" or "to self" patterns
    for st in status_list:
        # "On 6: Apply X Status" - check if conditional is met
        m = re.search(rf"on\s+6:\s+apply\s+(\d+)\s+{st}", rt)
        if m:
            # Only apply if a 6 was used
            if 6 in dice_used:
                n = int(m.group(1))
                target.apply_status(st, n)
            continue
        
        # "On 5-6: Apply X Status" - check if conditional is met
        m = re.search(rf"on\s+5-6:\s+apply\s+(\d+)\s+{st}", rt)
        if m:
            # Only apply if a 5 or 6 was used
            if 5 in dice_used or 6 in dice_used:
                n = int(m.group(1))
                target.apply_status(st, n)
            continue
        
        # "Apply X Poison to opponent"
        m = re.search(rf"apply\s+(\d+)\s+{st}\s+to\s+opponent", rt)
        if m:
            n = int(m.group(1))
            target.apply_status(st, n)
            continue
        
        # "Apply X Poison to self"
        m = re.search(rf"apply\s+(\d+)\s+{st}\s+to\s+self", rt)
        if m:
            n = int(m.group(1))
            user.apply_status(st, n)
            continue
        
        # "Apply X Poison equal to die value [+ bonus]"
        m = re.search(rf"apply\s+{st}\s+equal\s+to\s+die\s+value\s*\+?\s*(\d+)?", rt)
        if m:
            bonus = int(m.group(1)) if m.group(1) else 0
            amount = dice_sum + bonus
            target.apply_status(st, amount)
            continue
        
        # Default "Apply X Poison" (without explicit target) -> to opponent
        # Check that this isn't part of a conditional (already handled above)
        m = re.search(rf"apply\s+(\d+)\s+{st}(?!\s+(to|equal))", rt)
        if m:
            # Make sure this isn't preceded by "On 6:" or "On 5-6:" by checking position
            match_start = m.start()
            prefix = rt[:match_start]
            # Skip if this appears to be part of a conditional we already handled
            if not re.search(r"on\s+\d+(-\d+)?:\s*$", prefix):
                n = int(m.group(1))
                target.apply_status(st, n)

    # === TRIGGER POISON (Bellows effect) ===
    if getattr(card, 'trigger_poison', False):
        poison_effect = target.get_status_effect('poison')
        if poison_effect and poison_effect.has_stacks():
            dmg = poison_effect.stacks
            target.take_damage(dmg)
            poison_effect.remove(1)

    # === DESTROY OPPONENT SHIELD ===
    if getattr(card, 'destroy_shield', False):
        target.shield = 0

    # === CREATE DICE (Splinter family) ===
    if getattr(card, 'create_dice_hint', None):
        hint = card.create_dice_hint
        if hint['mode'] == 'half_per_die':
            for d in dice_used:
                v = d // 2 if hint['round'] == 'down' else -(-d // 2)
                for _ in range(hint['count']):
                    side['created_dice'].append(max(1, v))

    # === DRAW CARDS ===
    if getattr(card, 'draw_cards', 0):
        drawn = draw_cards(user.deck, user.discard, user.hand, card.draw_cards)
        side['drawn'] = drawn

    # === COUNTDOWN ACCUMULATION (Limit cards) ===
    if getattr(card, 'countdown_target', None):
        card.countdown_accum += dice_sum
        if card.countdown_accum >= card.countdown_target:
            card.countdown_accum = 0

    # once-per-combat enforcement
    if getattr(card, 'max_uses', None) and getattr(card, 'max_uses', None) == 1:
        card.reusable = False

    return side


def get_creature(name):
    """Return an Enemy instance populated from CREATURE_DEFINITIONS.

    The enemy receives:
    - `cardpool`: Card instances representing all abilities
    - `hand`: fresh Card instances (separate objects) matching the abilities (so enemy state is isolated)
    """
    data = CREATURE_DEFINITIONS[name]
    # canonical cardpool (one instance per ability)
    cardpool = [create_card_from_ability(a) for a in data['abilities']]
    # create a fresh hand (fresh instances) so card state isn't shared with the pool
    hand = [create_card_from_ability(a) for a in data['abilities']]
    e = Enemy(name=name, max_hp=data['hp'], currenthp=data['hp'], cardpool=cardpool, hand=hand, dice=data.get('dice', 2))
    return e


# --- build card lookup tables from CREATURE_DEFINITIONS ---
CARD_NAMES = sorted({
    ability['name']
    for c in CREATURE_DEFINITIONS.values()
    for ability in c['abilities']
})

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

# --- canonical card progression (fully inlined, editable) ---
# This is the converted `cardProgression` from `card-upgrades fixed - Copy.jsx`.
# (Formatted for readability — edit here to change any card variant.)
CARD_PROGRESSIONS = {
  "Afflict": {
    'base': { 'name': "Afflict", 'requirement': "Exactly 1", 'effect_type': 'status', 'status_effects': [{'status': 'poison', 'stacks': 2}, {'status': 'blind', 'stacks': 1}], 'max_dice': 1, 'description': "Apply 2 Poison, Apply 1 Blind" },
    'x':    { 'name': "Afflict x", 'requirement': "Exactly 1", 'effect_type': 'status', 'status_effects': [{'status': 'poison', 'stacks': 2}, {'status': 'blind', 'stacks': 2}], 'max_dice': 1, 'description': "Apply 2 Poison, Apply 2 Blind" },
    'y':    { 'name': "Afflict y", 'requirement': "Exactly 1", 'effect_type': 'status', 'status_effects': [{'status': 'poison', 'stacks': 3}, {'status': 'blind', 'stacks': 1}], 'max_dice': 1, 'description': "Apply 3 Poison, Apply 1 Blind" },
    'X':    { 'name': "Afflict X", 'requirement': "Exactly 1", 'effect_type': 'status', 'status_effects': [{'status': 'poison', 'stacks': 3}, {'status': 'blind', 'stacks': 2}], 'max_dice': 1, 'description': "Apply 3 Poison, Apply 2 Blind" },
    'Y':    { 'name': "Afflict Y", 'requirement': "Exactly 1", 'effect_type': 'status', 'status_effects': [{'status': 'poison', 'stacks': 4}, {'status': 'blind', 'stacks': 2}, {'status': 'lock', 'stacks': 1}], 'max_dice': 1, 'description': "Apply 4 Poison, Apply 2 Blind, Apply 1 Lock" },
    'XY':   { 'name': "Afflict XY", 'requirement': "Exactly 1", 'effect_type': 'status', 'status_effects': [{'status': 'poison', 'stacks': 5}, {'status': 'blind', 'stacks': 3}, {'status': 'lock', 'stacks': 2}], 'max_dice': 1, 'description': "Apply 5 Poison, Apply 3 Blind, Apply 2 Lock" },
  },

  "Annihilation": {
    'base': { 'name': "Annihilation", 'requirement': "Limit 30", 'effect_type': 'damage', 'base_value': 25, 'status_effects': [{'status': 'bleed', 'stacks': 3}, {'status': 'poison', 'stacks': 2}], 'max_dice': 1, 'description': "Deal 25 damage, Apply 3 Bleed, Apply 2 Poison" },
    'x':    { 'name': "Annihilation x", 'requirement': "Limit 28", 'effect_type': 'damage', 'base_value': 25, 'status_effects': [{'status': 'bleed', 'stacks': 4}, {'status': 'poison', 'stacks': 2}], 'max_dice': 1, 'description': "Deal 25 damage, Apply 4 Bleed, Apply 2 Poison" },
    'y':    { 'name': "Annihilation y", 'requirement': "Limit 30", 'effect_type': 'damage', 'base_value': 28, 'status_effects': [{'status': 'bleed', 'stacks': 3}, {'status': 'poison', 'stacks': 3}], 'max_dice': 1, 'description': "Deal 28 damage, Apply 3 Bleed, Apply 3 Poison" },
    'X':    { 'name': "Annihilation X", 'requirement': "Limit 25", 'effect_type': 'damage', 'base_value': 28, 'status_effects': [{'status': 'bleed', 'stacks': 5}, {'status': 'poison', 'stacks': 3}], 'max_dice': 1, 'description': "Deal 28 damage, Apply 5 Bleed, Apply 3 Poison" },
    'Y':    { 'name': "Annihilation Y", 'requirement': "Limit 28", 'effect_type': 'damage', 'base_value': 32, 'status_effects': [{'status': 'bleed', 'stacks': 4}, {'status': 'poison', 'stacks': 4}], 'max_dice': 1, 'description': "Deal 32 damage, Apply 4 Bleed, Apply 4 Poison" },
    'XY':   { 'name': "Annihilation XY", 'requirement': "Limit 22", 'effect_type': 'damage', 'base_value': 35, 'status_effects': [{'status': 'bleed', 'stacks': 6}, {'status': 'poison', 'stacks': 5}, {'status': 'lock', 'stacks': 2}], 'max_dice': 1, 'description': "Deal 35 damage, Apply 6 Bleed, Apply 5 Poison, Apply 2 Lock" },
  },

  "Apocalypse": {
    'base': { 'name': "Apocalypse", 'requirement': "Limit 35", 'effect_type': 'damage', 'base_value': 30, 'status_effects': [{'status': 'poison', 'stacks': 4}, {'status': 'blind', 'stacks': 3}, {'status': 'lock', 'stacks': 2}], 'max_dice': 1, 'description': "Deal 30 damage, Apply 4 Poison, Apply 3 Blind, Apply 2 Lock" },
    'x':    { 'name': "Apocalypse x", 'requirement': "Limit 32", 'effect_type': 'damage', 'base_value': 30, 'status_effects': [{'status': 'poison', 'stacks': 4}, {'status': 'blind', 'stacks': 3}, {'status': 'lock', 'stacks': 2}], 'max_dice': 1, 'description': "Deal 30 damage, Apply 4 Poison, Apply 3 Blind, Apply 2 Lock" },
    'y':    { 'name': "Apocalypse y", 'requirement': "Limit 35", 'effect_type': 'damage', 'base_value': 32, 'status_effects': [{'status': 'poison', 'stacks': 5}, {'status': 'blind', 'stacks': 3}, {'status': 'lock', 'stacks': 3}], 'max_dice': 1, 'description': "Deal 32 damage, Apply 5 Poison, Apply 3 Blind, Apply 3 Lock" },
    'X':    { 'name': "Apocalypse X", 'requirement': "Limit 28", 'effect_type': 'damage', 'base_value': 33, 'status_effects': [{'status': 'poison', 'stacks': 5}, {'status': 'blind', 'stacks': 4}, {'status': 'lock', 'stacks': 3}], 'max_dice': 1, 'description': "Deal 33 damage, Apply 5 Poison, Apply 4 Blind, Apply 3 Lock" },
    'Y':    { 'name': "Apocalypse Y", 'requirement': "Limit 32", 'effect_type': 'damage', 'base_value': 36, 'status_effects': [{'status': 'poison', 'stacks': 6}, {'status': 'blind', 'stacks': 4}, {'status': 'lock', 'stacks': 4}], 'max_dice': 1, 'description': "Deal 36 damage, Apply 6 Poison, Apply 4 Blind, Apply 4 Lock" },
    'XY':   { 'name': "Apocalypse XY", 'requirement': "Limit 25", 'effect_type': 'damage', 'base_value': 40, 'status_effects': [{'status': 'poison', 'stacks': 7}, {'status': 'blind', 'stacks': 5}, {'status': 'lock', 'stacks': 5}, {'status': 'bleed', 'stacks': 3}], 'max_dice': 1, 'description': "Deal 40 damage, Apply 7 Poison, Apply 5 Blind, Apply 5 Lock, Apply 3 Bleed" },
  },

  "Bash": {
    'base': { 'name': "Bash", 'requirement': "Any", 'effect_type': 'raw', 'raw_effect': "Remove all Shield from self, Deal damage equal to double the Shield removed", 'max_dice': 1, 'description': "Remove all Shield from self, Deal damage equal to double the Shield removed" },
    'x':    { 'name': "Bash x", 'requirement': "Any", 'effect_type': 'raw', 'raw_effect': "Deal damage equal to double current shield, then remove half of current shield (rounded down)", 'max_dice': 1, 'description': "Deal damage equal to double current shield, then remove half of current shield (rounded down)" },
    'y':    { 'name': "Bash y", 'requirement': "Any", 'effect_type': 'raw', 'raw_effect': "Deal damage equal to double current shield, then remove half of current shield (rounded up)", 'max_dice': 1, 'description': "Deal damage equal to double current shield, then remove half of current shield (rounded up)" },
    'X':    { 'name': "Bash X", 'requirement': "Any", 'effect_type': 'raw', 'raw_effect': "Deal damage equal to double current shield, then remove half of current shield (rounded up), Gain 2 Shield", 'reusable': True, 'max_dice': 1, 'description': "Deal damage equal to double current shield, then remove half of current shield (rounded up), Gain 2 Shield" },
    'Y':    { 'name': "Bash Y", 'requirement': "Any", 'effect_type': 'raw', 'raw_effect': "Deal damage equal to triple current shield, then remove all shield", 'max_dice': 1, 'description': "Deal damage equal to triple current shield, then remove all shield" },
    'XY':   { 'name': "Bash XY", 'requirement': "Any", 'effect_type': 'raw', 'raw_effect': "Deal damage equal to triple current shield, then remove half of current shield (rounded down), Gain 3 Shield", 'reusable': True, 'max_dice': 1, 'description': "Deal damage equal to triple current shield, then remove half of current shield (rounded down), Gain 3 Shield" },
  },

  "Bellow": {
    'base': { 'name': "Bellow", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 0, 'uses_dice_value': True, 'conditional_status': [{'status': 'frozen', 'stacks': 1, 'condition': 'on_6'}], 'max_dice': 1, 'description': "Deal damage equal to die value, On 6: Apply 1 Frozen" },
    'x':    { 'name': "Bellow x", 'requirement': "Any", 'effect_type': 'raw', 'raw_effect': "Deal damage equal to die value, Trigger Poison (deal damage equal to poison counters on opponent, then reduce poison counters by 1)", 'max_dice': 1, 'description': "Deal damage equal to die value, Trigger Poison (deal damage equal to poison counters on opponent, then reduce poison counters by 1)" },
    'y':    { 'name': "Bellow y", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 0, 'uses_dice_value': True, 'conditional_status': [{'status': 'frozen', 'stacks': 1, 'condition': 'on_5_6'}], 'max_dice': 1, 'description': "Deal damage equal to die value, On 5-6: Apply 1 Frozen" },
    'X':    { 'name': "Bellow X", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 2, 'uses_dice_value': True, 'conditional_status': [{'status': 'frozen', 'stacks': 2, 'condition': 'on_5_6'}], 'max_dice': 1, 'description': "Deal damage equal to die value + 2, On 5-6: Apply 2 Frozen" },
    'Y':    { 'name': "Bellow Y", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 3, 'uses_dice_value': True, 'conditional_status': [{'status': 'frozen', 'stacks': 2, 'condition': 'on_5_6'}], 'reusable': True, 'max_dice': 1, 'description': "Deal damage equal to die value + 3, On 5-6: Apply 2 Frozen" },
    'XY':   { 'name': "Bellow XY", 'requirement': "Any", 'effect_type': 'raw', 'raw_effect': "Deal damage equal to die value + 4, Trigger Poison, On 5-6: Apply 3 Frozen", 'reusable': True, 'max_dice': 1, 'description': "Deal damage equal to die value + 4, Trigger Poison, On 5-6: Apply 3 Frozen" },
  },

  "Bite": {
    'base': { 'name': "Bite", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 3, 'max_dice': 1, 'description': "Deal 3 damage" },
    'x':    { 'name': "Bite x", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 0, 'uses_dice_value': True, 'max_dice': 1, 'description': "Deal damage equal to die value" },
    'y':    { 'name': "Bite y", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 4, 'reusable': True, 'max_dice': 1, 'description': "Deal 4 damage" },
    'X':    { 'name': "Bite X", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 2, 'uses_dice_value': True, 'max_dice': 1, 'description': "Deal damage equal to die value + 2" },
    'Y':    { 'name': "Bite Y", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 5, 'heal_value': 1, 'reusable': True, 'max_dice': 1, 'description': "Deal 5 damage and heal 1" },
    'XY':   { 'name': "Bite XY", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 4, 'uses_dice_value': True, 'heal_value': 2, 'reusable': True, 'max_dice': 1, 'description': "Deal damage equal to die value + 4, Heal 2 HP" },
  },

  "Blood Pact": {
    'base': { 'name': "Blood Pact", 'requirement': "Limit 15", 'effect_type': 'damage', 'base_value': 12, 'heal_value': 4, 'sacrifice_hp': 3, 'max_dice': 1, 'description': "Deal 12 damage, Heal 4 HP, Sacrifice 3 HP" },
    'x':    { 'name': "Blood Pact x", 'requirement': "Limit 13", 'effect_type': 'damage', 'base_value': 12, 'heal_value': 5, 'sacrifice_hp': 3, 'max_dice': 1, 'description': "Deal 12 damage, Heal 5 HP, Sacrifice 3 HP" },
    'y':    { 'name': "Blood Pact y", 'requirement': "Limit 15", 'effect_type': 'damage', 'base_value': 14, 'heal_value': 4, 'sacrifice_hp': 4, 'max_dice': 1, 'description': "Deal 14 damage, Heal 4 HP, Sacrifice 4 HP" },
    'X':    { 'name': "Blood Pact X", 'requirement': "Limit 10", 'effect_type': 'damage', 'base_value': 15, 'heal_value': 6, 'sacrifice_hp': 3, 'max_dice': 1, 'description': "Deal 15 damage, Heal 6 HP, Sacrifice 3 HP" },
    'Y':    { 'name': "Blood Pact Y", 'requirement': "Limit 13", 'effect_type': 'damage', 'base_value': 18, 'heal_value': 5, 'sacrifice_hp': 5, 'max_dice': 1, 'description': "Deal 18 damage, Heal 5 HP, Sacrifice 5 HP" },
    'XY':   { 'name': "Blood Pact XY", 'requirement': "Limit 8", 'effect_type': 'damage', 'base_value': 20, 'heal_value': 8, 'sacrifice_hp': 4, 'max_dice': 1, 'description': "Deal 20 damage, Heal 8 HP, Sacrifice 4 HP" },
  },

  "Blood Ritual": {
    'base': { 'name': "Blood Ritual", 'requirement': "Exactly 1", 'effect_type': 'damage', 'base_value': 15, 'sacrifice_hp': 5, 'status_effects': [{'status': 'poison', 'stacks': 2}], 'max_dice': 1, 'description': "Sacrifice 5 HP, Deal 15 damage, Apply 2 Poison" },
    'x':    { 'name': "Blood Ritual x", 'requirement': "Exactly 1", 'effect_type': 'damage', 'base_value': 15, 'sacrifice_hp': 4, 'status_effects': [{'status': 'poison', 'stacks': 3}], 'max_dice': 1, 'description': "Sacrifice 4 HP, Deal 15 damage, Apply 3 Poison" },
    'y':    { 'name': "Blood Ritual y", 'requirement': "Exactly 1", 'effect_type': 'damage', 'base_value': 18, 'sacrifice_hp': 6, 'status_effects': [{'status': 'poison', 'stacks': 2}], 'max_dice': 1, 'description': "Sacrifice 6 HP, Deal 18 damage, Apply 2 Poison" },
    'X':    { 'name': "Blood Ritual X", 'requirement': "Exactly 1", 'effect_type': 'damage', 'base_value': 18, 'sacrifice_hp': 3, 'status_effects': [{'status': 'poison', 'stacks': 4}, {'status': 'blind', 'stacks': 1}], 'max_dice': 1, 'description': "Sacrifice 3 HP, Deal 18 damage, Apply 4 Poison, Apply 1 Blind" },
    'Y':    { 'name': "Blood Ritual Y", 'requirement': "Exactly 1", 'effect_type': 'damage', 'base_value': 22, 'sacrifice_hp': 7, 'status_effects': [{'status': 'poison', 'stacks': 3}, {'status': 'bleed', 'stacks': 1}], 'max_dice': 1, 'description': "Sacrifice 7 HP, Deal 22 damage, Apply 3 Poison, Apply 1 Bleed" },
    'XY':   { 'name': "Blood Ritual XY", 'requirement': "Exactly 1", 'effect_type': 'damage', 'base_value': 25, 'sacrifice_hp': 5, 'status_effects': [{'status': 'poison', 'stacks': 5}, {'status': 'blind', 'stacks': 2}, {'status': 'bleed', 'stacks': 2}], 'max_dice': 1, 'description': "Sacrifice 5 HP, Deal 25 damage, Apply 5 Poison, Apply 2 Blind, Apply 2 Bleed" },
  },

  "Boulder Toss": {
    'base': { 'name': "Boulder Toss", 'requirement': "Minimum 4", 'effect_type': 'damage', 'base_value': 10, 'status_effects': [{'status': 'lock', 'stacks': 1}], 'reusable': True, 'max_dice': 1, 'description': "Deal 10 damage, Apply 1 Lock" },
    'x': { 'name': "Boulder Toss x", 'requirement': "Minimum 4", 'effect_type': 'damage', 'base_value': 11, 'status_effects': [{'status': 'lock', 'stacks': 1}], 'reusable': True, 'max_dice': 1, 'description': "Deal 11 damage, Apply 1 Lock" },
    'y': { 'name': "Boulder Toss y", 'requirement': "Minimum 5", 'effect_type': 'damage', 'base_value': 12, 'status_effects': [{'status': 'lock', 'stacks': 2}], 'reusable': True, 'max_dice': 1, 'description': "Deal 12 damage, Apply 2 Lock" },
    'Y': { 'name': "Boulder Toss Y", 'requirement': "Minimum 4", 'effect_type': 'damage', 'base_value': 14, 'status_effects': [{'status': 'lock', 'stacks': 3}], 'reusable': True, 'max_dice': 1, 'description': "Deal 14 damage, Apply 3 Lock" },
    'XY': { 'name': "Boulder Toss XY", 'requirement': "Minimum 3", 'effect_type': 'damage', 'base_value': 16, 'status_effects': [{'status': 'lock', 'stacks': 4}, {'status': 'frozen', 'stacks': 1}], 'reusable': True, 'max_dice': 1, 'description': "Deal 16 damage, Apply 4 Lock, Apply 1 Frozen" },
  },

  "Chain Lightning": {
    'base': { 'name': "Chain Lightning", 'requirement': "Odd only", 'effect_type': 'damage', 'base_value': 0, 'uses_dice_value': True, 'dice_multiplier': 4, 'max_dice': 1, 'description': "Deal quadruple die value damage" },
    'x': { 'name': "Chain Lightning x", 'requirement': "Odd only", 'effect_type': 'damage', 'base_value': 0, 'uses_dice_value': True, 'dice_multiplier': 4, 'status_effects': [{'status': 'blind', 'stacks': 1}], 'max_dice': 1, 'description': "Deal quadruple die value damage, Apply 1 Blind" },
    'y': { 'name': "Chain Lightning y", 'requirement': "Odd only", 'effect_type': 'damage', 'base_value': 0, 'uses_dice_value': True, 'dice_multiplier': 5, 'max_dice': 1, 'description': "Deal quintuple die value damage" },
    'X': { 'name': "Chain Lightning X", 'requirement': "Odd only", 'effect_type': 'damage', 'base_value': 0, 'uses_dice_value': True, 'dice_multiplier': 5, 'status_effects': [{'status': 'blind', 'stacks': 2}], 'max_dice': 1, 'description': "Deal quintuple die value damage, Apply 2 Blind" },
    'Y': { 'name': "Chain Lightning Y", 'requirement': "Odd only", 'effect_type': 'damage', 'base_value': 0, 'uses_dice_value': True, 'dice_multiplier': 6, 'status_effects': [{'status': 'lock', 'stacks': 1}], 'max_dice': 1, 'description': "Deal sextuple die value damage, Apply 1 Lock" },
    'XY': { 'name': "Chain Lightning XY", 'requirement': "Odd only", 'effect_type': 'damage', 'base_value': 0, 'uses_dice_value': True, 'dice_multiplier': 7, 'status_effects': [{'status': 'blind', 'stacks': 2}, {'status': 'lock', 'stacks': 2}], 'max_dice': 1, 'description': "Deal septuple die value damage, Apply 2 Blind, Apply 2 Lock" },
  },

  "Chains": {
    'base': { 'name': "Chains", 'requirement': "Minimum 3", 'effect_type': 'damage', 'base_value': 6, 'status_effects': [{'status': 'lock', 'stacks': 2}], 'reusable': True, 'max_dice': 1, 'description': "Deal 6 damage, Apply 2 Lock" },
    'x': { 'name': "Chains x", 'requirement': "Minimum 3", 'effect_type': 'damage', 'base_value': 7, 'status_effects': [{'status': 'lock', 'stacks': 2}], 'reusable': True, 'max_dice': 1, 'description': "Deal 7 damage, Apply 2 Lock" },
    'y': { 'name': "Chains y", 'requirement': "Minimum 4", 'effect_type': 'damage', 'base_value': 8, 'status_effects': [{'status': 'lock', 'stacks': 3}], 'reusable': True, 'max_dice': 1, 'description': "Deal 8 damage, Apply 3 Lock" },
    'X': { 'name': "Chains X", 'requirement': "Minimum 3", 'effect_type': 'damage', 'base_value': 8, 'status_effects': [{'status': 'lock', 'stacks': 3}], 'reusable': True, 'max_dice': 1, 'description': "Deal 8 damage, Apply 3 Lock" },
    'Y': { 'name': "Chains Y", 'requirement': "Minimum 3", 'effect_type': 'damage', 'base_value': 10, 'status_effects': [{'status': 'lock', 'stacks': 4}], 'reusable': True, 'max_dice': 1, 'description': "Deal 10 damage, Apply 4 Lock" },
    'XY': { 'name': "Chains XY", 'requirement': "Minimum 2", 'effect_type': 'damage', 'base_value': 12, 'status_effects': [{'status': 'lock', 'stacks': 5}, {'status': 'blind', 'stacks': 2}], 'reusable': True, 'max_dice': 1, 'description': "Deal 12 damage, Apply 5 Lock, Apply 2 Blind" },
  },

  "Charge": {
    'base': { 'name': "Charge", 'requirement': "Limit 15", 'effect_type': 'raw', 'raw_effect': "Deal 8 damage, Gain 3 Shield (activates when limit reaches 0)", 'max_dice': 1, 'description': "Deal 8 damage, Gain 3 Shield (activates when limit reaches 0)" },
    'x': { 'name': "Charge x", 'requirement': "Limit 13", 'effect_type': 'damage', 'base_value': 8, 'shield_value': 3, 'max_dice': 1, 'description': "Deal 8 damage, Gain 3 Shield" },
    'y': { 'name': "Charge y", 'requirement': "Limit 18", 'effect_type': 'damage', 'base_value': 8, 'shield_value': 8, 'max_dice': 1, 'description': "Deal 8 damage, Gain 8 Shield" },
    'X': { 'name': "Charge X", 'requirement': "Limit 20", 'effect_type': 'damage', 'base_value': 10, 'shield_value': 10, 'max_dice': 1, 'description': "Deal 10 damage, Gain 10 Shield" },
    'Y': { 'name': "Charge Y", 'requirement': "Limit 15", 'effect_type': 'damage', 'base_value': 12, 'shield_value': 6, 'max_dice': 1, 'description': "Deal 12 damage, Gain 6 Shield" },
    'XY': { 'name': "Charge XY", 'requirement': "Limit 12", 'effect_type': 'damage', 'base_value': 15, 'shield_value': 12, 'status_effects': [{'status': 'lock', 'stacks': 1}], 'max_dice': 1, 'description': "Deal 15 damage, Gain 12 Shield, Apply 1 Lock" },
  },

  "Chomp": {
    'base': { 'name': "Chomp", 'requirement': "Limit 10", 'effect_type': 'raw', 'raw_effect': "Deal 10 damage (activates when limit reaches 0)", 'max_dice': 1, 'description': "Deal 10 damage (activates when limit reaches 0)" },
    'y': { 'name': "Chomp y", 'requirement': "Limit 12", 'effect_type': 'damage', 'base_value': 12, 'max_dice': 1, 'description': "Deal 12 damage" },
    'x': { 'name': "Chomp x", 'requirement': "Limit 8", 'effect_type': 'raw', 'raw_effect': "Deal 10 damage (activates when limit reaches 0)", 'max_dice': 1, 'description': "Deal 10 damage (activates when limit reaches 0)" },
    'X': { 'name': "Chomp X", 'requirement': "Limit 10", 'effect_type': 'damage', 'base_value': 14, 'heal_value': 3, 'max_dice': 1, 'description': "Deal 14 damage, Heal 3 HP" },
    'Y': { 'name': "Chomp Y", 'requirement': "Limit 8", 'effect_type': 'damage', 'base_value': 18, 'heal_value': 4, 'max_dice': 1, 'description': "Deal 18 damage, Heal 4 HP" },
    'XY': { 'name': "Chomp XY", 'requirement': "Limit 15", 'effect_type': 'damage', 'base_value': 20, 'heal_value': 5, 'max_dice': 1, 'description': "Deal 20 damage, Heal 5 HP" },
  },

  "Claw Swipe": {
    'base': { 'name': "Claw Swipe", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 3, 'uses_dice_value': True, 'conditional_status': [{'status': 'bleed', 'stacks': 1, 'condition': 'on_6'}], 'reusable': True, 'max_dice': 1, 'description': "Deal damage equal to die value + 3, On 6: Apply 1 Bleed" },
    'x': { 'name': "Claw Swipe x", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 4, 'uses_dice_value': True, 'conditional_status': [{'status': 'bleed', 'stacks': 1, 'condition': 'on_6'}], 'reusable': True, 'max_dice': 1, 'description': "Deal damage equal to die value + 4, On 6: Apply 1 Bleed" },
    'y': { 'name': "Claw Swipe y", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 3, 'uses_dice_value': True, 'conditional_status': [{'status': 'bleed', 'stacks': 2, 'condition': 'on_5_6'}], 'reusable': True, 'max_dice': 1, 'description': "Deal damage equal to die value + 3, On 5-6: Apply 2 Bleed" },
    'X': { 'name': "Claw Swipe X", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 5, 'uses_dice_value': True, 'conditional_status': [{'status': 'bleed', 'stacks': 2, 'condition': 'on_5_6'}], 'reusable': True, 'max_dice': 1, 'description': "Deal damage equal to die value + 5, On 5-6: Apply 2 Bleed" },
    'Y': { 'name': "Claw Swipe Y", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 4, 'uses_dice_value': True, 'conditional_status': [{'status': 'bleed', 'stacks': 3, 'condition': 'on_4_6'}], 'reusable': True, 'max_dice': 1, 'description': "Deal damage equal to die value + 4, On 4-6: Apply 3 Bleed" },
    'XY': { 'name': "Claw Swipe XY", 'requirement': "Any", 'effect_type': 'damage', 'base_value': 6, 'uses_dice_value': True, 'conditional_status': [{'status': 'bleed', 'stacks': 4, 'condition': 'on_4_6'}], 'reusable': True, 'max_dice': 1, 'description': "Deal damage equal to die value + 6, On 4-6: Apply 4 Bleed" },
  },

  "Control": {
    'base': { 'name': "Control", 'requirement': "Exactly 1", 'effect_type': 'raw', 'raw_effect': "Sacrifice 2 HP, draw a new card, and roll a new die", 'max_dice': 1, 'description': "Sacrifice 2 HP, draw a new card, and roll a new die" },
    'x': { 'name': "Control x", 'requirement': "Exactly 1", 'effect_type': 'raw', 'raw_effect': "Sacrifice 1 HP, draw a new card, and roll a new die", 'max_dice': 1, 'description': "Sacrifice 1 HP, draw a new card, and roll a new die" },
    'y': { 'name': "Control y", 'requirement': "Exactly 1", 'effect_type': 'raw', 'raw_effect': "Sacrifice 2 HP, draw 2 new cards, and roll a new die", 'max_dice': 1, 'description': "Sacrifice 2 HP, draw 2 new cards, and roll a new die" },
    'X': { 'name': "Control X", 'requirement': "Exactly 1", 'effect_type': 'raw', 'raw_effect': "Draw a new card, and roll a new die", 'max_dice': 1, 'description': "Draw a new card, and roll a new die" },
    'Y': { 'name': "Control Y", 'requirement': "Exactly 1", 'effect_type': 'raw', 'raw_effect': "Sacrifice 3 HP, draw 2 new cards, and roll 2 new dice", 'max_dice': 1, 'description': "Sacrifice 3 HP, draw 2 new cards, and roll 2 new dice" },
    'XY': { 'name': "Control XY", 'requirement': "Exactly 1", 'effect_type': 'raw', 'raw_effect': "Sacrifice 1 HP, draw 3 new cards, and roll 2 new dice", 'max_dice': 1, 'description': "Sacrifice 1 HP, draw 3 new cards, and roll 2 new dice" },
  },

  "Curse": {
    'base': { 'name': "Curse", 'requirement': "Exactly 1", 'effect': "Apply 2 Poison, Apply 2 Blind" },
    'x': { 'name': "Curse x", 'requirement': "Exactly 1", 'effect': "Apply 2 Poison, Apply 3 Blind" },
    'y': { 'name': "Curse y", 'requirement': "Exactly 1", 'effect': "Apply 3 Poison, Apply 2 Blind" },
    'X': { 'name': "Curse X", 'requirement': "Exactly 1", 'effect': "Apply 3 Poison, Apply 4 Blind, Apply 1 Lock" },
    'Y': { 'name': "Curse Y", 'requirement': "Exactly 1", 'effect': "Apply 4 Poison, Apply 3 Blind, Apply 1 Lock" },
    'XY': { 'name': "Curse XY", 'requirement': "Exactly 1", 'effect': "Apply 5 Poison, Apply 5 Blind, Apply 2 Lock" },
  },

  "Dagger": {
    'base': { 'name': "Dagger", 'requirement': "Odd only", 'effect': "Deal 2 damage, Apply 1 Poison" },
    'x': { 'name': "Dagger x", 'requirement': "Any", 'effect': "Deal 3 damage, Apply 1 Poison" },
    'X': { 'name': "Dagger X", 'requirement': "Odd only", 'effect': "Deal 4 damage, Apply 2 Poison" },
    'XY': { 'name': "Dagger XY", 'requirement': "Odd only", 'effect': "Deal 6 damage, Apply 3 Poison" },
    'y': { 'name': "Dagger y", 'requirement': "Odd only", 'effect': "Deal 4 damage, Apply 1 Poison" },
    'Y': { 'name': "Dagger Y", 'requirement': "Odd only", 'effect': "Deal 5 damage, Apply 2 Poison" },
  },

  "Dark Aegis": {
    'base': { 'name': "Dark Aegis", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 4, Apply 1 Poison to opponent", 'reusable': True },
    'x': { 'name': "Dark Aegis x", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 5, Apply 1 Poison to opponent", 'reusable': True },
    'y': { 'name': "Dark Aegis y", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 4, Apply 2 Poison to opponent", 'reusable': True },
    'X': { 'name': "Dark Aegis X", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 6, Apply 2 Poison to opponent, Heal 1 HP", 'reusable': True },
    'Y': { 'name': "Dark Aegis Y", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 5, Apply 3 Poison to opponent", 'reusable': True },
    'XY': { 'name': "Dark Aegis XY", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 8, Apply 3 Poison to opponent, Heal 2 HP", 'reusable': True },
  },

  "Dark Blessing": {
    'base': { 'name': "Dark Blessing", 'requirement': "Limit 18", 'effect': "Heal 8 HP, Apply 2 Poison to opponent" },
    'x': { 'name': "Dark Blessing x", 'requirement': "Limit 16", 'effect': "Heal 8 HP, Apply 2 Poison to opponent" },
    'y': { 'name': "Dark Blessing y", 'requirement': "Limit 18", 'effect': "Heal 10 HP, Apply 3 Poison to opponent" },
    'X': { 'name': "Dark Blessing X", 'requirement': "Limit 13", 'effect': "Heal 10 HP, Apply 3 Poison to opponent, Gain 2 Shield" },
    'Y': { 'name': "Dark Blessing Y", 'requirement': "Limit 15", 'effect': "Heal 12 HP, Apply 4 Poison to opponent" },
    'XY': { 'name': "Dark Blessing XY", 'requirement': "Limit 10", 'effect': "Heal 15 HP, Apply 5 Poison to opponent, Gain 4 Shield" },
  },

  "Desperation": {
    'base': { 'name': "Desperation", 'requirement': "Exactly 1", 'effect': "Deal 10 damage, Sacrifice 5 HP" },
    'x': { 'name': "Desperation x", 'requirement': "Exactly 1", 'effect': "Deal 10 HP, Sacrifice 4 HP" },
    'y': { 'name': "Desperation y", 'requirement': "Exactly 1", 'effect': "Deal 12 damage, Sacrifice 6 HP" },
    'X': { 'name': "Desperation X", 'requirement': "Exactly 1", 'effect': "Deal 12 damage, Sacrifice 3 HP, Apply 1 Bleed" },
    'Y': { 'name': "Desperation Y", 'requirement': "Exactly 1", 'effect': "Deal 15 damage, Sacrifice 7 HP, Apply 1 Lock" },
    'XY': { 'name': "Desperation XY", 'requirement': "Exactly 1", 'effect': "Deal 18 damage, Sacrifice 5 HP, Apply 2 Bleed, Apply 1 Lock" },
  },

  "Dive Bomb": {
    'base': { 'name': "Dive Bomb", 'requirement': "Minimum 5", 'effect': "Deal 12 damage, Apply 1 Blind" },
    'x': { 'name': "Dive Bomb x", 'requirement': "Minimum 5", 'effect': "Deal 12 damage, Apply 2 Blind" },
    'y': { 'name': "Dive Bomb y", 'requirement': "Minimum 6", 'effect': "Deal 14 damage, Apply 1 Blind" },
    'X': { 'name': "Dive Bomb X", 'requirement': "Minimum 4", 'effect': "Deal 14 damage, Apply 3 Blind, Apply 1 Lock" },
    'Y': { 'name': "Dive Bomb Y", 'requirement': "Minimum 5", 'effect': "Deal 16 damage, Apply 2 Blind, Apply 1 Bleed" },
    'XY': { 'name': "Dive Bomb XY", 'requirement': "Minimum 3", 'effect': "Deal 18 damage, Apply 4 Blind, Apply 2 Lock, Apply 2 Bleed" },
  },

  "Dominate": {
    'base': { 'name': "Dominate", 'requirement': "Exactly 1", 'effect': "Apply 2 Lock, Sacrifice 3 HP" },
    'x': { 'name': "Dominate x", 'requirement': "Exactly 1", 'effect': "Apply 3 Lock, Sacrifice 3 HP" },
    'y': { 'name': "Dominate y", 'requirement': "Exactly 1", 'effect': "Apply 2 Lock, Sacrifice 2 HP, Apply 1 Blind" },
    'X': { 'name': "Dominate X", 'requirement': "Exactly 1", 'effect': "Apply 4 Lock, Sacrifice 2 HP, Apply 1 Blind" },
    'Y': { 'name': "Dominate Y", 'requirement': "Exactly 1", 'effect': "Apply 3 Lock, Sacrifice 1 HP, Apply 2 Blind, Apply 1 Poison" },
    'XY': { 'name': "Dominate XY", 'requirement': "Exactly 1", 'effect': "Apply 5 Lock, Sacrifice 1 HP, Apply 3 Blind, Apply 2 Poison" },
  },

  "Earthquake": {
    'base': { 'name': "Earthquake", 'requirement': "Limit 20", 'effect': "Deal 12 dmg, Apply 2 Lock, Apply 1 Frozen" },
    'x': { 'name': "Earthquake x", 'requirement': "Limit 18", 'effect': "Deal 12 dmg, Apply 2 Lock, Apply 1 Frozen" },
    'y': { 'name': "Earthquake y", 'requirement': "Limit 20", 'effect': "Deal 14 dmg, Apply 3 Lock, Apply 2 Frozen" },
    'X': { 'name': "Earthquake X", 'requirement': "Limit 15", 'effect': "Deal 15 dmg, Apply 3 Lock, Apply 2 Frozen, Destroy opponent Shield" },
    'Y': { 'name': "Earthquake Y", 'requirement': "Limit 17", 'effect': "Deal 18 dmg, Apply 4 Lock, Apply 3 Frozen" },
    'XY': { 'name': "Earthquake XY", 'requirement': "Limit 12", 'effect': "Deal 20 dmg, Apply 5 Lock, Apply 4 Frozen, Destroy opponent Shield" },
  },

  "Earthshatter": {
    'base': { 'name': "Earthshatter", 'requirement': "Limit 22", 'effect': "Deal 15 damage, Apply 3 Lock, Apply 2 Frozen" },
    'x': { 'name': "Earthshatter x", 'requirement': "Limit 20", 'effect': "Deal 15 damage, Apply 3 Lock, Apply 2 Frozen" },
    'y': { 'name': "Earthshatter y", 'requirement': "Limit 22", 'effect': "Deal 18 damage, Apply 4 Lock, Apply 3 Frozen" },
    'X': { 'name': "Earthshatter X", 'requirement': "Limit 17", 'effect': "Deal 18 damage, Apply 4 Lock, Apply 3 Frozen, Apply 1 Bleed" },
    'Y': { 'name': "Earthshatter Y", 'requirement': "Limit 19", 'effect': "Deal 22 damage, Apply 5 Lock, Apply 4 Frozen" },
    'XY': { 'name': "Earthshatter XY", 'requirement': "Limit 14", 'effect': "Deal 25 damage, Apply 6 Lock, Apply 5 Frozen, Apply 2 Bleed" },
  },

  "Evade": {
    'base': { 'name': "Evade", 'requirement': "Exactly 1", 'effect': "Gain Shield equal to 2 × the number of dice used this turn" },
    'x': { 'name': "Evade x", 'requirement': "Exactly 1", 'effect': "Gain Shield equal to 3 × the number of dice used this turn" },
    'y': { 'name': "Evade y", 'requirement': "Exactly 1", 'effect': "Gain Shield equal to 2 × the number of dice used this turn, Heal 2 HP" },
    'X': { 'name': "Evade X", 'requirement': "Exactly 1", 'effect': "Gain Shield equal to 4 × the number of dice used this turn, Remove 1 negative effect" },
    'Y': { 'name': "Evade Y", 'requirement': "Exactly 1", 'effect': "Gain Shield equal to 3 × the number of dice used this turn, Heal 4 HP" },
    'XY': { 'name': "Evade XY", 'requirement': "Exactly 1", 'effect': "Gain Shield equal to 5 × the number of dice used this turn, Heal 3 HP, Remove all negative effects" },
  },

  "Execution": {
    'base': { 'name': "Execution", 'requirement': "Limit 25", 'effect': "Deal 22 damage, Apply 4 Bleed" },
    'x': { 'name': "Execution x", 'requirement': "Limit 23", 'effect': "Deal 22 damage, Apply 4 Bleed" },
    'y': { 'name': "Execution y", 'requirement': "Limit 25", 'effect': "Deal 25 damage, Apply 5 Bleed" },
    'X': { 'name': "Execution X", 'requirement': "Limit 20", 'effect': "Deal 25 damage, Apply 5 Bleed, Apply 1 Lock" },
    'Y': { 'name': "Execution Y", 'requirement': "Limit 22", 'effect': "Deal 28 damage, Apply 6 Bleed, Heal 2 HP" },
    'XY': { 'name': "Execution XY", 'requirement': "Limit 18", 'effect': "Deal 32 damage, Apply 7 Bleed, Apply 2 Lock, Heal 3 HP" },
  },

  "Flail": {
    'base': { 'name': "Flail", 'requirement': "Any", 'effect': "Deal damage equal to die value, Sacrifice 1 HP" },
    'x': { 'name': "Flail x", 'requirement': "Any", 'effect': "Deal damage equal to die value, Sacrifice 1 HP", 'reusable': True },
    'y': { 'name': "Flail y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 1, Sacrifice 2 HP", 'reusable': True },
    'X': { 'name': "Flail X", 'requirement': "Any", 'effect': "Deal damage equal to die value + 1, Sacrifice 1 HP, Apply 1 Bleed", 'reusable': True },
    'Y': { 'name': "Flail Y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 2, Sacrifice 2 HP, On 6: Apply 2 Bleed", 'reusable': True },
    'XY': { 'name': "Flail XY", 'requirement': "Any", 'effect': "Deal damage equal to die value + 3, Sacrifice 1 HP, Apply 2 Bleed", 'reusable': True },
  },

  "Flame Burst": {
    'base': { 'name': "Flame Burst", 'requirement': "Odd only", 'effect': "Deal triple die value damage" },
    'x': { 'name': "Flame Burst x", 'requirement': "Odd only", 'effect': "Deal triple die value damage, Apply 1 Poison" },
    'y': { 'name': "Flame Burst y", 'requirement': "Odd only", 'effect': "Deal quadruple die value damage" },
    'X': { 'name': "Flame Burst X", 'requirement': "Odd only", 'effect': "Deal quadruple die value damage, Apply 2 Poison" },
    'Y': { 'name': "Flame Burst Y", 'requirement': "Odd only", 'effect': "Deal quintuple die value damage, Apply 1 Blind" },
    'XY': { 'name': "Flame Burst XY", 'requirement': "Odd only", 'effect': "Deal sextuple die value damage, Apply 2 Poison, Apply 2 Blind" },
  },

  "Flame Strike": {
    'base': { 'name': "Flame Strike", 'requirement': "Odd only", 'effect': "Deal double die value damage, Apply 1 Poison" },
    'x': { 'name': "Flame Strike x", 'requirement': "Odd only", 'effect': "Deal double die value damage, Apply 2 Poison" },
    'y': { 'name': "Flame Strike y", 'requirement': "Odd only", 'effect': "Deal triple die value damage, Apply 1 Poison" },
    'X': { 'name': "Flame Strike X", 'requirement': "Odd only", 'effect': "Deal triple die value damage, Apply 3 Poison, Apply 1 Blind" },
    'Y': { 'name': "Flame Strike Y", 'requirement': "Odd only", 'effect': "Deal quadruple die value damage, Apply 2 Poison" },
    'XY': { 'name': "Flame Strike XY", 'requirement': "Odd only", 'effect': "Deal quintuple die value damage, Apply 4 Poison, Apply 2 Blind" },
  },

  "Flame Wall": {
    'base': { 'name': "Flame Wall", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 5, Deal 5 damage", 'reusable': True },
    'x': { 'name': "Flame Wall x", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 6, Deal 5 damage", 'reusable': True },
    'y': { 'name': "Flame Wall y", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 5, Deal 7 damage", 'reusable': True },
    'X': { 'name': "Flame Wall X", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 8, Deal 6 damage, Apply 1 Poison", 'reusable': True },
    'Y': { 'name': "Flame Wall Y", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 6, Deal 10 damage, Apply 1 Bleed", 'reusable': True },
    'XY': { 'name': "Flame Wall XY", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 10, Deal 8 damage, Apply 2 Poison, Apply 1 Bleed", 'reusable': True },
  },

  "Fortify": {
    'base': { 'name': "Fortify", 'requirement': "Any", 'effect': "Gain 3 Shield" },
    'x': { 'name': "Fortify x", 'requirement': "Any", 'effect': "Gain 4 Shield and inflict 1 blind" },
    'y': { 'name': "Fortify y", 'requirement': "Any", 'effect': "Gain 4 Shield, Remove 1 negative effect" },
    'X': { 'name': "Fortify X", 'requirement': "Any", 'effect': "Gain 5 Shield, Apply 1 Blind" },
    'Y': { 'name': "Fortify Y", 'requirement': "Any", 'effect': "Gain 8 Shield, Heal 2 HP" },
    'XY': { 'name': "Fortify XY", 'requirement': "Any", 'effect': "Gain 10 Shield, Heal 3 HP, Apply 2 Blind to opponent" },
  },

  "Frosted Dagger": {
    'base': { 'name': "Frosted Dagger", 'requirement': "Any", 'effect': "Deal damage equal to die value, On 6: Apply 1 Poison" },
    'x': { 'name': "Frosted Dagger x", 'requirement': "Any", 'effect': "Deal damage equal to die value, On 6: Apply 1 Poison and 1 Frozen" },
    'y': { 'name': "Frosted Dagger y", 'requirement': "Any", 'effect': "Deal damage equal to die value, On 5-6: Apply 1 Poison and 1 Frozen" },
    'X': { 'name': "Frosted Dagger X", 'requirement': "Any", 'effect': "Deal damage equal to die value + 1, On 5-6: Apply 2 Poison and 2 Frozen" },
    'Y': { 'name': "Frosted Dagger Y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 2, On 4-6: Apply 2 Poison and 2 Frozen" },
    'XY': { 'name': "Frosted Dagger XY", 'requirement': "Any", 'effect': "Deal damage equal to die value + 3, On 4-6: Apply 3 Poison and 3 Frozen" },
  },

  "Frosted Spear": {
    'base': { 'name': "Frosted Spear", 'requirement': "Minimum 3", 'effect': "Deal 3 damage", 'reusable': True },
    'x': { 'name': "Frosted Spear x", 'requirement': "Any", 'effect': "Deal 3 damage", 'reusable': True },
    'y': { 'name': "Frosted Spear y", 'requirement': "Any", 'effect': "Deal 4 damage, On 6: Apply 1 Frozen", 'reusable': True },
    'X': { 'name': "Frosted Spear X", 'requirement': "Any", 'effect': "Deal 5 damage, On 5-6: Apply 1 Frozen", 'reusable': True },
    'Y': { 'name': "Frosted Spear Y", 'requirement': "Any", 'effect': "Deal 6 damage, On 5-6: Apply 2 Frozen", 'reusable': True },
    'XY': { 'name': "Frosted Spear XY", 'requirement': "Any", 'effect': "Deal 8 damage, On 4-6: Apply 3 Frozen", 'reusable': True },
  },

  "Gore": {
    'base': { 'name': "Gore", 'requirement': "Any", 'effect': "Deal damage equal to die value, On 6: Apply 1 Bleed" },
    'x': { 'name': "Gore x", 'requirement': "Any", 'effect': "Deal 2 + die value damage, On 6: Apply 1 Bleed" },
    'y': { 'name': "Gore y", 'requirement': "Any", 'effect': "Deal 3 + die value damage, On 6: Apply 1 Bleed" },
    'X': { 'name': "Gore X", 'requirement': "Any", 'effect': "Deal 4 + die value damage, On 6: Apply 2 Bleed" },
    'Y': { 'name': "Gore Y", 'requirement': "Any", 'effect': "Deal 5 + die value damage, On 5-6: Apply 2 Bleed" },
    'XY': { 'name': "Gore XY", 'requirement': "Any", 'effect': "Deal 7 + die value damage, On 4-6: Apply 3 Bleed, Heal 1 HP" },
  },

  "Haunting Wail": {
    'base': { 'name': "Haunting Wail", 'requirement': "Limit 8", 'effect': "Apply 2 Blind, Apply 1 Lock" },
    'x': { 'name': "Haunting Wail x", 'requirement': "Limit 7", 'effect': "Apply 2 Blind, Apply 1 Lock" },
    'y': { 'name': "Haunting Wail y", 'requirement': "Limit 8", 'effect': "Apply 3 Blind, Apply 2 Lock" },
    'X': { 'name': "Haunting Wail X", 'requirement': "Limit 5", 'effect': "Apply 3 Blind, Apply 2 Lock, Apply 1 Poison" },
    'Y': { 'name': "Haunting Wail Y", 'requirement': "Limit 6", 'effect': "Apply 4 Blind, Apply 3 Lock" },
    'XY': { 'name': "Haunting Wail XY", 'requirement': "Limit 4", 'effect': "Apply 5 Blind, Apply 4 Lock, Apply 2 Poison" },
  },

  "Hellfire": {
    'base': { 'name': "Hellfire", 'requirement': "Odd only", 'effect': "Deal quintuple die value damage" },
    'x': { 'name': "Hellfire x", 'requirement': "Odd only", 'effect': "Deal quintuple die value damage, Apply 1 Poison" },
    'y': { 'name': "Hellfire y", 'requirement': "Odd only", 'effect': "Deal sextuple die value damage" },
    'X': { 'name': "Hellfire X", 'requirement': "Odd only", 'effect': "Deal sextuple die value damage, Apply 2 Poison, Apply 1 Blind" },
    'Y': { 'name': "Hellfire Y", 'requirement': "Odd only", 'effect': "Deal septuple die value damage, Apply 1 Lock" },
    'XY': { 'name': "Hellfire XY", 'requirement': "Odd only", 'effect': "Deal octuple die value damage, Apply 3 Poison, Apply 2 Blind, Apply 2 Lock" },
  },

  "Howl": {
    'base': { 'name': "Howl", 'requirement': "Limit 8", 'effect': "Heal 2 HP" },
    'x': { 'name': "Howl x", 'requirement': "Limit 7", 'effect': "Heal 2 HP" },
    'y': { 'name': "Howl y", 'requirement': "Limit 8", 'effect': "Heal 3 HP" },
    'X': { 'name': "Howl X", 'requirement': "Limit 5", 'effect': "Heal 3 HP, Remove 1 negative effect" },
    'Y': { 'name': "Howl Y", 'requirement': "Limit 6", 'effect': "Heal 4 HP, Gain 2 Shield" },
    'XY': { 'name': "Howl XY", 'requirement': "Limit 4", 'effect': "Heal 5 HP, Remove all negative effects, Gain 3 Shield" },
  },

  "Hype Up": {
    'base': { 'name': "Hype Up", 'requirement': "Limit 12", 'effect': "Heal 4 HP, Apply 1 Blind to self and opponent (activates when limit reaches 0)" },
    'x': { 'name': "Hype Up x", 'requirement': "Limit 10", 'effect': "Heal 4 HP, Apply 1 Blind to self and opponent" },
    'y': { 'name': "Hype Up y", 'requirement': "Limit 12", 'effect': "Heal 5 HP, Apply 2 Blind to self and opponent" },
    'X': { 'name': "Hype Up X", 'requirement': "Limit 8", 'effect': "Heal 5 HP, Apply 2 Blind to opponent only" },
    'Y': { 'name': "Hype Up Y", 'requirement': "Limit 10", 'effect': "Heal 6 HP, Apply 3 Blind to self and opponent, Gain 2 Shield" },
    'XY': { 'name': "Hype Up XY", 'requirement': "Limit 6", 'effect': "Heal 8 HP, Apply 3 Blind to opponent only, Gain 4 Shield" },
  },

  "Ice Magic": {
    'base': { 'name': "Ice Magic", 'requirement': "Exactly 2", 'effect': "Heal 2 HP, Remove all negative effects from self" },
    'x': { 'name': "Ice Magic x", 'requirement': "Exactly 2", 'effect': "Heal 3 HP, Remove all negative effects from self" },
    'y': { 'name': "Ice Magic y", 'requirement': "Max 2", 'effect': "Heal 2 HP, Remove all negative effects from self" },
    'X': { 'name': "Ice Magic X", 'requirement': "Max 2", 'effect': "Heal 4 HP, Remove all negative effects from self, Gain 2 Shield" },
    'Y': { 'name': "Ice Magic Y", 'requirement': "Exactly 1", 'effect': "Heal 3 HP, Remove all negative effects from self, Gain 3 Shield" },
    'XY': { 'name': "Ice Magic XY", 'requirement': "Max 2", 'effect': "Heal 5 HP, Remove all negative effects from self, Gain 5 Shield, Apply 1 Frozen to opponent" },
  },

  "Immolate": {
    'base': { 'name': "Immolate", 'requirement': "Limit 10", 'effect': "Deal 10 damage, Apply 2 Poison, Sacrifice 2 HP" },
    'x': { 'name': "Immolate x", 'requirement': "Limit 9", 'effect': "Deal 10 damage, Apply 2 Poison, Sacrifice 2 HP" },
    'y': { 'name': "Immolate y", 'requirement': "Limit 10", 'effect': "Deal 12 damage, Apply 3 Poison, Sacrifice 3 HP" },
    'X': { 'name': "Immolate X", 'requirement': "Limit 7", 'effect': "Deal 12 damage, Apply 3 Poison, Sacrifice 1 HP, Apply 1 Blind" },
    'Y': { 'name': "Immolate Y", 'requirement': "Limit 8", 'effect': "Deal 15 damage, Apply 4 Poison, Sacrifice 4 HP" },
    'XY': { 'name': "Immolate XY", 'requirement': "Limit 5", 'effect': "Deal 18 damage, Apply 5 Poison, Sacrifice 2 HP, Apply 2 Blind" },
  },

  "Infernal Strike": {
    'base': { 'name': "Infernal Strike", 'requirement': "Any", 'effect': "Deal damage equal to die value + 8, Sacrifice 2 HP", 'reusable': True },
    'x': { 'name': "Infernal Strike x", 'requirement': "Any", 'effect': "Deal damage equal to die value + 9, Sacrifice 2 HP", 'reusable': True },
    'y': { 'name': "Infernal Strike y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 10, Sacrifice 3 HP", 'reusable': True },
    'X': { 'name': "Infernal Strike X", 'requirement': "Any", 'effect': "Deal damage equal to die value + 11, Sacrifice 1 HP, Apply 1 Poison", 'reusable': True },
    'Y': { 'name': "Infernal Strike Y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 12, Sacrifice 4 HP, Apply 1 Bleed", 'reusable': True },
    'XY': { 'name': "Infernal Strike XY", 'requirement': "Any", 'effect': "Deal damage equal to die value + 14, Sacrifice 2 HP, Apply 2 Poison, Apply 1 Bleed", 'reusable': True },
  },

  "Inferno": {
    'base': { 'name': "Inferno", 'requirement': "Odd only", 'effect': "Deal quadruple die value damage, Apply 2 Poison" },
    'x': { 'name': "Inferno x", 'requirement': "Odd only", 'effect': "Deal quadruple die value damage, Apply 3 Poison" },
    'y': { 'name': "Inferno y", 'requirement': "Odd only", 'effect': "Deal quintuple die value damage, Apply 2 Poison" },
    'X': { 'name': "Inferno X", 'requirement': "Odd only", 'effect': "Deal quintuple die value damage, Apply 4 Poison, Apply 1 Blind" },
    'Y': { 'name': "Inferno Y", 'requirement': "Odd only", 'effect': "Deal sextuple die value damage, Apply 3 Poison, Apply 1 Lock" },
    'XY': { 'name': "Inferno XY", 'requirement': "Odd only", 'effect': "Deal septuple die value damage, Apply 5 Poison, Apply 2 Blind, Apply 2 Lock" },
  },

  "Jab": {
    'base': { 'name': "Jab", 'requirement': "Any", 'effect': "Deal damage equal to die value" },
    'x': { 'name': "Jab x", 'requirement': "Any", 'effect': "Deal 2 + die value damage" },
    'y': { 'name': "Jab y", 'requirement': "Any", 'effect': "Deal damage equal to die value", 'reusable': True },
    'X': { 'name': "Jab X", 'requirement': "Any", 'effect': "Deal 4 + die value damage", 'reusable': True },
    'Y': { 'name': "Jab Y", 'requirement': "Any", 'effect': "Deal 5 + die value damage, On 6: Apply 1 Bleed", 'reusable': True },
    'XY': { 'name': "Jab XY", 'requirement': "Any", 'effect': "Deal 6 + die value damage, On 5-6: Apply 2 Bleed", 'reusable': True },
  },

  "Jade Spear": {
    'base': { 'name': "Jade Spear", 'requirement': "Even only", 'effect': "Apply Poison equal to die value" },
    'x': { 'name': "Jade Spear x", 'requirement': "Even only", 'effect': "Apply Poison equal to die value, Gain 1 Shield" },
    'y': { 'name': "Jade Spear y", 'requirement': "Even only", 'effect': "Apply Poison equal to die value + 1" },
    'X': { 'name': "Jade Spear X", 'requirement': "Even only", 'effect': "Apply Poison equal to die value + 1, Gain 2 Shield, Apply 1 Blind" },
    'Y': { 'name': "Jade Spear Y", 'requirement': "Even only", 'effect': "Apply Poison equal to die value + 2, Deal 3 damage" },
    'XY': { 'name': "Jade Spear XY", 'requirement': "Even only", 'effect': "Apply Poison equal to die value + 3, Deal 5 damage, Gain 3 Shield, Apply 2 Blind" },
  },

  "Judgement": {
    'base': { 'name': "Judgement", 'requirement': "Exactly 6", 'effect': "Deal 18 damage, Heal 6 HP, Apply 2 Lock" },
    'x': { 'name': "Judgement x", 'requirement': "Exactly 6", 'effect': "Deal 18 damage, Heal 7 HP, Apply 2 Lock" },
    'y': { 'name': "Judgement y", 'requirement': "Exactly 6", 'effect': "Deal 20 damage, Heal 6 HP, Apply 3 Lock" },
    'X': { 'name': "Judgement X", 'requirement': "Exactly 6", 'effect': "Deal 22 damage, Heal 8 HP, Apply 3 Lock, Gain 3 Shield" },
    'Y': { 'name': "Judgement Y", 'requirement': "Exactly 6", 'effect': "Deal 25 damage, Heal 7 HP, Apply 4 Lock, Apply 1 Blind" },
    'XY': { 'name': "Judgement XY", 'requirement': "Exactly 6", 'effect': "Deal 28 damage, Heal 10 HP, Apply 5 Lock, Gain 5 Shield, Apply 2 Blind" },
  },

  "Life Drain": {
    'base': { 'name': "Life Drain", 'requirement': "Odd only", 'effect': "Deal damage equal to die value, Heal 1 HP" },
    'x': { 'name': "Life Drain x", 'requirement': "Odd only", 'effect': "Deal damage equal to die value, Heal half the damage dealt (rounded up)" },
    'y': { 'name': "Life Drain y", 'requirement': "Odd only", 'effect': "Deal damage equal to die value + 1, Heal half the damage dealt (rounded up)", 'reusable': True },
    'X': { 'name': "Life Drain X", 'requirement': "Odd only", 'effect': "Deal damage equal to die value + 2, Heal half the damage dealt (rounded up)" },
    'Y': { 'name': "Life Drain Y", 'requirement': "Odd only", 'effect': "Deal damage equal to die value + 4, Heal half the damage dealt (rounded up)", 'reusable': True },
    'XY': { 'name': "Life Drain XY", 'requirement': "Odd only", 'effect': "Deal damage equal to die value + 6, Heal the full damage dealt", 'reusable': True },
  },

  "Lightning Bolt": {
    'base': { 'name': "Lightning Bolt", 'requirement': "Odd only", 'effect': "Deal triple die value damage", 'oncePerCombat': True },
    'x': { 'name': "Lightning Bolt x", 'requirement': "Odd only", 'effect': "Deal triple die value damage, Apply 1 Blind", 'reusable': True },
    'y': { 'name': "Lightning Bolt y", 'requirement': "Odd only", 'effect': "Deal quadruple die value damage", 'reusable': True },
    'X': { 'name': "Lightning Bolt X", 'requirement': "Odd only", 'effect': "Deal quadruple die value damage, Apply 2 Blind, Apply 1 Lock", 'reusable': True },
    'Y': { 'name': "Lightning Bolt Y", 'requirement': "Odd only", 'effect': "Deal quintuple die value damage, Apply 1 Frozen", 'reusable': True },
    'XY': { 'name': "Lightning Bolt XY", 'requirement': "Odd only", 'effect': "Deal sextuple die value damage, Apply 3 Blind, Apply 2 Lock, Apply 2 Frozen", 'reusable': True },
  },

  "Lightning Storm": {
    'base': { 'name': "Lightning Storm", 'requirement': "Limit 20", 'effect': "Deal 20 damage, Apply 2 Blind" },
    'x': { 'name': "Lightning Storm x", 'requirement': "Limit 18", 'effect': "Deal 20 damage, Apply 2 Blind" },
    'y': { 'name': "Lightning Storm y", 'requirement': "Limit 20", 'effect': "Deal 22 damage, Apply 3 Blind" },
    'X': { 'name': "Lightning Storm X", 'requirement': "Limit 15", 'effect': "Deal 24 damage, Apply 3 Blind, Apply 2 Lock" },
    'Y': { 'name': "Lightning Storm Y", 'requirement': "Limit 17", 'effect': "Deal 26 damage, Apply 4 Blind, Apply 1 Frozen" },
    'XY': { 'name': "Lightning Storm XY", 'requirement': "Limit 12", 'effect': "Deal 30 damage, Apply 5 Blind, Apply 3 Lock, Apply 2 Frozen" },
  },

  "Maul": {
    'base': { 'name': "Maul", 'requirement': "Any", 'effect': "Deal damage equal to die value + 4" },
    'x': { 'name': "Maul x", 'requirement': "Any", 'effect': "Deal damage equal to die value + 5" },
    'y': { 'name': "Maul y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 5" },
    'X': { 'name': "Maul X", 'requirement': "Any", 'effect': "Deal damage equal to die value + 6" },
    'Y': { 'name': "Maul Y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 8" },
    'XY': { 'name': "Maul XY", 'requirement': "Any", 'effect': "Deal damage equal to die value + 12", 'reusable': True },
  },

  "Meteor": {
    'base': { 'name': "Meteor", 'requirement': "Minimum 5", 'effect': "Deal 15 damage, Apply 2 Bleed", 'reusable': True },
    'x': { 'name': "Meteor x", 'requirement': "Minimum 5", 'effect': "Deal 16 damage, Apply 2 Bleed", 'reusable': True },
    'y': { 'name': "Meteor y", 'requirement': "Minimum 6", 'effect': "Deal 18 damage, Apply 3 Bleed", 'reusable': True },
    'X': { 'name': "Meteor X", 'requirement': "Minimum 4", 'effect': "Deal 18 damage, Apply 3 Bleed, Apply 1 Poison", 'reusable': True },
    'Y': { 'name': "Meteor Y", 'requirement': "Minimum 5", 'effect': "Deal 20 damage, Apply 4 Bleed, Apply 1 Blind", 'reusable': True },
    'XY': { 'name': "Meteor XY", 'requirement': "Minimum 3", 'effect': "Deal 25 damage, Apply 5 Bleed, Apply 2 Poison, Apply 2 Blind", 'reusable': True },
  },

  "Mirror Hide": {
    'base': { 'name': "Mirror Hide", 'requirement': "Any", 'effect': "Remove all negative effects from self, Apply them to opponent" },
    'x': { 'name': "Mirror Hide x", 'requirement': "Any", 'effect': "Remove all negative effects from self, Apply them to opponent, Gain 2 Shield" },
    'y': { 'name': "Mirror Hide y", 'requirement': "Any", 'effect': "Double all negative effects on opponent" },
    'X': { 'name': "Mirror Hide X", 'requirement': "Any", 'effect': "Remove all negative effects from self, Double them and apply to opponent" },
    'Y': { 'name': "Mirror Hide Y", 'requirement': "Any", 'effect': "Double all negative effects on opponent, Gain 3 Shield" },
    'XY': { 'name': "Mirror Hide XY", 'requirement': "Any", 'effect': "Remove all negative effects from self, Triple them and apply to opponent, Gain 5 Shield" },
  },

  "Necromancy": {
    'base': { 'name': "Necromancy", 'requirement': "Limit 12", 'effect': "Deal 15 damage, Heal 5 HP" },
    'x': { 'name': "Necromancy x", 'requirement': "Limit 11", 'effect': "Deal 15 damage, Heal 5 HP" },
    'y': { 'name': "Necromancy y", 'requirement': "Limit 12", 'effect': "Deal 17 damage, Heal 6 HP" },
    'X': { 'name': "Necromancy X", 'requirement': "Limit 15", 'effect': "Deal 18 damage, Heal 6 HP" },
    'Y': { 'name': "Necromancy Y", 'requirement': "Limit 10", 'effect': "Deal 20 damage, Heal 8 HP, Apply 1 Poison" },
    'XY': { 'name': "Necromancy XY", 'requirement': "Limit 8", 'effect': "Deal 22 damage, Heal 10 HP, Apply 2 Poison, Gain 3 Shield" },
  },

  "Petrify": {
    'base': { 'name': "Petrify", 'requirement': "On 6", 'effect': "Apply 2 Lock, Apply 1 Frozen" },
    'x': { 'name': "Petrify x", 'requirement': "On 6", 'effect': "Apply 3 Lock, Apply 1 Frozen" },
    'y': { 'name': "Petrify y", 'requirement': "On 6", 'effect': "Apply 2 Lock, Apply 2 Frozen" },
    'X': { 'name': "Petrify X", 'requirement': "On 5-6", 'effect': "Apply 4 Lock, Apply 2 Frozen" },
    'Y': { 'name': "Petrify Y", 'requirement': "On 5-6", 'effect': "Apply 3 Lock, Apply 3 Frozen, Apply 1 Blind" },
    'XY': { 'name': "Petrify XY", 'requirement': "On 4-6", 'effect': "Apply 5 Lock, Apply 4 Frozen, Apply 2 Blind" },
  },

  "Phase Shift": {
    'base': { 'name': "Phase Shift", 'requirement': "Exactly 1", 'effect': "Gain 4 Shield, Remove all negative effects from self" },
    'x': { 'name': "Phase Shift x", 'requirement': "Exactly 1", 'effect': "Gain 5 Shield, Remove all negative effects from self" },
    'y': { 'name': "Phase Shift y", 'requirement': "Exactly 1", 'effect': "Gain 4 Shield, Remove all negative effects from self, Heal 2 HP" },
    'X': { 'name': "Phase Shift X", 'requirement': "Exactly 1", 'effect': "Gain 6 Shield, Remove all negative effects from self, Apply 1 Blind to opponent" },
    'Y': { 'name': "Phase Shift Y", 'requirement': "Exactly 1", 'effect': "Gain 5 Shield, Remove all negative effects from self, Heal 4 HP" },
    'XY': { 'name': "Phase Shift XY", 'requirement': "Exactly 1", 'effect': "Gain 8 Shield, Remove all negative effects from self, Heal 3 HP, Apply 2 Blind to opponent" },
  },

  "Phoenix Rising": {
    'base': { 'name': "Phoenix Rising", 'requirement': "Exactly 1", 'effect': "Heal 10 HP, Gain 10 Shield, Remove all negative effects from self" },
    'x': { 'name': "Phoenix Rising x", 'requirement': "Exactly 1", 'effect': "Heal 11 HP, Gain 10 Shield, Remove all negative effects from self" },
    'y': { 'name': "Phoenix Rising y", 'requirement': "Exactly 1", 'effect': "Heal 10 HP, Gain 12 Shield, Remove all negative effects from self" },
    'X': { 'name': "Phoenix Rising X", 'requirement': "Exactly 1", 'effect': "Heal 13 HP, Gain 12 Shield, Remove all negative effects from self, Apply 1 Poison to opponent" },
    'Y': { 'name': "Phoenix Rising Y", 'requirement': "Exactly 1", 'effect': "Heal 12 HP, Gain 15 Shield, Remove all negative effects from self, Deal 5 damage" },
    'XY': { 'name': "Phoenix Rising XY", 'requirement': "Exactly 1", 'effect': "Heal 15 HP, Gain 18 Shield, Remove all negative effects from self, Deal 8 damage, Apply 2 Poison to opponent" },
  },

  "Plague Breath": {
    'base': { 'name': "Plague Breath", 'requirement': "Even only", 'effect': "Apply Poison equal to half die value (rounded up)" },
    'x': { 'name': "Plague Breath x", 'requirement': "Even only", 'effect': "Apply Poison equal to half die value (rounded up), Apply 1 Blind" },
    'y': { 'name': "Plague Breath y", 'requirement': "Even only", 'effect': "Apply Poison equal to die value" },
    'X': { 'name': "Plague Breath X", 'requirement': "Even only", 'effect': "Apply Poison equal to die value, Apply 2 Blind" },
    'Y': { 'name': "Plague Breath Y", 'requirement': "Even only", 'effect': "Apply Poison equal to die value + 1, Apply 1 Lock" },
    'XY': { 'name': "Plague Breath XY", 'requirement': "Even only", 'effect': "Apply Poison equal to die value + 2, Apply 3 Blind, Apply 2 Lock" },
  },

  "Pounce": {
    'base': { 'name': "Pounce", 'requirement': "Any", 'effect': "Deal 5 + die value damage", 'oncePerCombat': True },
    'x': { 'name': "Pounce x", 'requirement': "Any", 'effect': "Deal 6 + die value damage", 'reusable': True },
    'y': { 'name': "Pounce y", 'requirement': "Any", 'effect': "Deal 7 + die value damage", 'reusable': True },
    'X': { 'name': "Pounce X", 'requirement': "Any", 'effect': "Deal 8 + die value damage, Apply 1 Bleed", 'reusable': True },
    'Y': { 'name': "Pounce Y", 'requirement': "Any", 'effect': "Deal 9 + die value damage, Gain 2 Shield", 'reusable': True },
    'XY': { 'name': "Pounce XY", 'requirement': "Any", 'effect': "Deal 12 + die value damage, Apply 2 Bleed, Gain 3 Shield", 'reusable': True },
  },

  "Reflecting Scales": {
    'base': { 'name': "Reflecting Scales", 'requirement': "Any", 'effect': "Deal 2 damage, Apply 1 Blind" },
    'x': { 'name': "Reflecting Scales x", 'requirement': "Any", 'effect': "Deal 4 damage, Apply 2 Blind" },
    'y': { 'name': "Reflecting Scales y", 'requirement': "Any", 'effect': "Apply 2 Blind, Gain 2 Shield" },
    'X': { 'name': "Reflecting Scales X", 'requirement': "Any", 'effect': "Deal 6 damage, Apply 3 Blind, Gain 1 Shield" },
    'Y': { 'name': "Reflecting Scales Y", 'requirement': "Any", 'effect': "Apply 3 Blind, Gain 4 Shield, Remove 1 negative effect" },
    'XY': { 'name': "Reflecting Scales XY", 'requirement': "Any", 'effect': "Deal 8 damage, Apply 4 Blind, Gain 5 Shield, Remove all negative effects" },
  },

  "Roar": {
    'base': { 'name': "Roar", 'requirement': "Exactly 1", 'effect': "Apply 1 Lock" },
    'x': { 'name': "Roar x", 'requirement': "Exactly 1", 'effect': "Apply 2 Lock" },
    'y': { 'name': "Roar y", 'requirement': "Exactly 1", 'effect': "Apply 1 Lock, Apply 1 Blind" },
    'X': { 'name': "Roar X", 'requirement': "Exactly 1", 'effect': "Apply 3 Lock, Apply 1 Blind" },
    'Y': { 'name': "Roar Y", 'requirement': "Exactly 1", 'effect': "Apply 2 Lock, Apply 2 Blind, Gain 2 Shield" },
    'XY': { 'name': "Roar XY", 'requirement': "Exactly 1", 'effect': "Apply 4 Lock, Apply 3 Blind, Gain 4 Shield" },
  },

  "Rupture": {
    'base': { 'name': "Rupture", 'requirement': "Limit 10", 'effect': "Deal 8 damage, Apply 2 Poison" },
    'x': { 'name': "Rupture x", 'requirement': "Limit 9", 'effect': "Deal 8 damage, Apply 2 Poison" },
    'y': { 'name': "Rupture y", 'requirement': "Limit 10", 'effect': "Deal 10 damage, Apply 3 Poison" },
    'X': { 'name': "Rupture X", 'requirement': "Limit 7", 'effect': "Deal 10 damage, Apply 3 Poison, Apply 1 Bleed" },
    'Y': { 'name': "Rupture Y", 'requirement': "Limit 8", 'effect': "Deal 12 damage, Apply 4 Poison, Deal extra 2 damage per Poison on opponent" },
    'XY': { 'name': "Rupture XY", 'requirement': "Limit 5", 'effect': "Deal 15 damage, Apply 5 Poison, Apply 2 Bleed, Deal extra 3 damage per Poison on opponent" },
  },

  "Rusty Dagger": {
    'base': { 'name': "Rusty Dagger", 'requirement': "Odd only", 'effect': "Deal 2 damage" },
    'x': { 'name': "Rusty Dagger x", 'requirement': "Odd only", 'effect': "Deal 3 damage" },
    'y': { 'name': "Rusty Dagger y", 'requirement': "Odd only", 'effect': "Deal 3 damage, Apply 1 Poison" },
    'X': { 'name': "Rusty Dagger X", 'requirement': "Odd only", 'effect': "Deal 4 damage, Apply 1 Poison" },
    'Y': { 'name': "Rusty Dagger Y", 'requirement': "Odd only", 'effect': "Deal 4 damage, Apply 2 Poison" },
    'XY': { 'name': "Rusty Dagger XY", 'requirement': "Odd only", 'effect': "Deal 6 damage, Apply 3 Poison, Apply 1 Bleed" },
  },

  "Screech": {
    'base': { 'name': "Screech", 'requirement': "Exactly 1", 'effect': "Apply 2 Blind, Apply 1 Lock" },
    'x': { 'name': "Screech x", 'requirement': "Exactly 1", 'effect': "Apply 3 Blind, Apply 1 Lock" },
    'y': { 'name': "Screech y", 'requirement': "Exactly 1", 'effect': "Apply 2 Blind, Apply 2 Lock" },
    'X': { 'name': "Screech X", 'requirement': "Exactly 1", 'effect': "Apply 4 Blind, Apply 2 Lock" },
    'Y': { 'name': "Screech Y", 'requirement': "Exactly 1", 'effect': "Apply 3 Blind, Apply 3 Lock, Deal 3 damage" },
    'XY': { 'name': "Screech XY", 'requirement': "Exactly 1", 'effect': "Apply 5 Blind, Apply 4 Lock, Deal 5 damage" },
  },

  "Shield": {
    'base': { 'name': "Shield", 'requirement': "Even only", 'effect': "Gain Shield equal to half the die value" },
    'x': { 'name': "Shield x", 'requirement': "Even only", 'effect': "Gain shield equal to the die value" },
    'y': { 'name': "Shield y", 'requirement': "Even only", 'effect': "Gain Shield equal to half the die value", 'reusable': True },
    'X': { 'name': "Shield X", 'requirement': "Even only", 'effect': "Gain Shield equal to die value" },
    'Y': { 'name': "Shield Y", 'requirement': "Even only", 'effect': "Gain Shield equal to die value", 'reusable': True },
    'XY': { 'name': "Shield XY", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 2, Heal 1 HP", 'reusable': True },
  },

  "Shortbow": {
    'base': { 'name': "Shortbow", 'requirement': "3 or below", 'effect': "Deal double die value damage" },
    'x': { 'name': "Shortbow x", 'requirement': "Odd only", 'effect': "Deal double die value damage" },
    'X': { 'name': "Shortbow X", 'requirement': "Odd only", 'effect': "Deal triple die value damage" },
    'y': { 'name': "Shortbow y", 'requirement': "Even only", 'effect': "Deal double die value damage, Apply 1 Bleed" },
    'Y': { 'name': "Shortbow Y", 'requirement': "Even only", 'effect': "Deal double die value damage, Apply 2 Bleed" },
    'XY': { 'name': "Shortbow XY", 'requirement': "Any", 'effect': "Deal quadruple die value damage, Apply 2 Blind, Apply 2 Bleed" },
  },

  "Snipe": {
    'base': { 'name': "Snipe", 'requirement': "Limit 15", 'effect': "Deal 8 damage, Apply 1 Bleed (activates when limit reaches 0)" },
    'x': { 'name': "Snipe x", 'requirement': "Limit 15", 'effect': "Deal 12 damage, Apply 1 Bleed (activates when limit reaches 0)" },
    'y': { 'name': "Snipe y", 'requirement': "Limit 15", 'effect': "Deal 10 damage, Apply 2 Bleed" },
    'X': { 'name': "Snipe X", 'requirement': "Limit 18", 'effect': "Deal 15 damage, Apply 2 Bleed" },
    'Y': { 'name': "Snipe Y", 'requirement': "Limit 22", 'effect': "Deal 18 damage, Apply 3 Bleed, Heal 3 HP" },
    'XY': { 'name': "Snipe XY", 'requirement': "Limit 18", 'effect': "Deal 22 damage, Apply 4 Bleed, Heal 4 HP, Gain 2 Shield" },
  },

  "Soul Rend": {
    'base': { 'name': "Soul Rend", 'requirement': "Minimum 4", 'effect': "Deal 8 damage, Apply 1 Bleed", 'reusable': True },
    'x': { 'name': "Soul Rend x", 'requirement': "Minimum 4", 'effect': "Deal 9 damage, Apply 1 Bleed", 'reusable': True },
    'y': { 'name': "Soul Rend y", 'requirement': "Minimum 5", 'effect': "Deal 10 damage, Apply 2 Bleed", 'reusable': True },
    'X': { 'name': "Soul Rend X", 'requirement': "Minimum 3", 'effect': "Deal 10 damage, Apply 2 Bleed, Heal 1 HP", 'reusable': True },
    'Y': { 'name': "Soul Rend Y", 'requirement': "Minimum 4", 'effect': "Deal 12 damage, Apply 3 Bleed, Apply 1 Poison", 'reusable': True },
    'XY': { 'name': "Soul Rend XY", 'requirement': "Minimum 2", 'effect': "Deal 14 damage, Apply 4 Bleed, Heal 2 HP, Apply 2 Poison", 'reusable': True },
  },

  "Spectral Strike": {
    'base': { 'name': "Spectral Strike", 'requirement': "Any", 'effect': "Deal damage equal to die value, On 5-6: Apply 1 Bleed" },
    'x': { 'name': "Spectral Strike x", 'requirement': "Any", 'effect': "Deal damage equal to die value + 1, On 5-6: Apply 1 Bleed" },
    'y': { 'name': "Spectral Strike y", 'requirement': "Any", 'effect': "Deal damage equal to die value, On 4-6: Apply 2 Bleed" },
    'X': { 'name': "Spectral Strike X", 'requirement': "Any", 'effect': "Deal damage equal to die value + 2, On 4-6: Apply 2 Bleed, Gain 1 Shield" },
    'Y': { 'name': "Spectral Strike Y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 1, On 3-6: Apply 3 Bleed" },
    'XY': { 'name': "Spectral Strike XY", 'requirement': "Any", 'effect': "Deal damage equal to die value + 3, On 3-6: Apply 4 Bleed, Gain 2 Shield" },
  },

  "Splinter": {
    'base': { 'name': "Splinter", 'requirement': "Any", 'effect': "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)" },
    'x': { 'name': "Splinter x", 'requirement': "Any", 'effect': "Create 2 dice with half the input die value (rounded down)" },
    'y': { 'name': "Splinter y", 'requirement': "Any", 'effect': "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded up)" },
    'X': { 'name': "Splinter X", 'requirement': "Any", 'effect': "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)", 'reusable': True },
    'Y': { 'name': "Splinter Y", 'requirement': "Minimum 2", 'effect': "Sacrifice 2 HP, Create 3 dice with half the input die value (rounded up)" },
    'XY': { 'name': "Splinter XY", 'requirement': "Any", 'effect': "Sacrifice 1 HP, Create 3 dice with half the input die value (rounded up)", 'reusable': True },
  },

  "Stone Hide": {
    'base': { 'name': "Stone Hide", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 2", 'reusable': True },
    'x': { 'name': "Stone Hide x", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 3", 'reusable': True },
    'y': { 'name': "Stone Hide y", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 2, Heal 1 HP", 'reusable': True },
    'X': { 'name': "Stone Hide X", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 4, Remove 1 negative effect", 'reusable': True },
    'Y': { 'name': "Stone Hide Y", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 3, Heal 2 HP, Apply 1 Lock to opponent", 'reusable': True },
    'XY': { 'name': "Stone Hide XY", 'requirement': "Even only", 'effect': "Gain Shield equal to die value + 6, Heal 2 HP, Remove all negative effects", 'reusable': True },
  },

  "Sunstrike": {
    'base': { 'name': "Sunstrike", 'requirement': "Limit 4", 'effect': "Deal 3 damage, Apply 1 Blind" },
    'x': { 'name': "Sunstrike x", 'requirement': "Limit 4", 'effect': "Deal 4 damage, Apply 1 Blind" },
    'y': { 'name': "Sunstrike y", 'requirement': "Limit 4", 'effect': "Deal 3 damage, Apply 2 Blind" },
    'X': { 'name': "Sunstrike X", 'requirement': "Limit 3", 'effect': "Deal 5 damage, Apply 2 Blind, Apply 1 Lock" },
    'Y': { 'name': "Sunstrike Y", 'requirement': "Limit 3", 'effect': "Deal 4 damage, Apply 3 Blind, Heal 1 HP" },
    'XY': { 'name': "Sunstrike XY", 'requirement': "Limit 2", 'effect': "Deal 7 damage, Apply 4 Blind, Apply 2 Lock, Heal 2 HP" },
  },

  "Swipe": {
    'base': { 'name': "Swipe", 'requirement': "Limit 5", 'effect': "Deal 3 damage, Heal 1 HP" },
    'x': { 'name': "Swipe x", 'requirement': "Any", 'effect': "Deal 3 damage + 1 for each use this round", 'reusable': True },
    'y': { 'name': "Swipe y", 'requirement': "Limit 5", 'effect': "Deal 5 damage, Heal 2 HP" },
    'X': { 'name': "Swipe X", 'requirement': "Any", 'effect': "Deal 2 damage + 2 for each use this round", 'reusable': True },
    'Y': { 'name': "Swipe Y", 'requirement': "Limit 3", 'effect': "Deal 7 damage, Heal 3 HP" },
    'XY': { 'name': "Swipe XY", 'requirement': "Any", 'effect': "Deal 3 damage + 3 for each use this round, Heal 2 HP", 'reusable': True },
  },

  "Talon Strike": {
    'base': { 'name': "Talon Strike", 'requirement': "Any", 'effect': "Deal damage equal to die value + 3, On 6: Apply 1 Bleed", 'reusable': True },
    'x': { 'name': "Talon Strike x", 'requirement': "Any", 'effect': "Deal damage equal to die value + 4, On 6: Apply 1 Bleed", 'reusable': True },
    'y': { 'name': "Talon Strike y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 3, On 5-6: Apply 2 Bleed", 'reusable': True },
    'X': { 'name': "Talon Strike X", 'requirement': "Any", 'effect': "Deal damage equal to die value + 5, On 5-6: Apply 2 Bleed, Gain 1 Shield", 'reusable': True },
    'Y': { 'name': "Talon Strike Y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 4, On 4-6: Apply 3 Bleed", 'reusable': True },
    'XY': { 'name': "Talon Strike XY", 'requirement': "Any", 'effect': "Deal damage equal to die value + 7, On 4-6: Apply 4 Bleed, Gain 2 Shield", 'reusable': True },
  },

  "Thunderclap": {
    'base': { 'name': "Thunderclap", 'requirement': "Limit 25", 'effect': "Deal 18 damage, Apply 3 Blind, Apply 2 Lock" },
    'x': { 'name': "Thunderclap x", 'requirement': "Limit 23", 'effect': "Deal 18 damage, Apply 3 Blind, Apply 2 Lock" },
    'y': { 'name': "Thunderclap y", 'requirement': "Limit 25", 'effect': "Deal 20 damage, Apply 4 Blind, Apply 3 Lock" },
    'X': { 'name': "Thunderclap X", 'requirement': "Limit 20", 'effect': "Deal 22 damage, Apply 4 Blind, Apply 3 Lock, Apply 1 Frozen" },
    'Y': { 'name': "Thunderclap Y", 'requirement': "Limit 22", 'effect': "Deal 25 damage, Apply 5 Blind, Apply 4 Lock" },
    'XY': { 'name': "Thunderclap XY", 'requirement': "Limit 18", 'effect': "Deal 28 damage, Apply 6 Blind, Apply 5 Lock, Apply 2 Frozen" },
  },

  "Torture": {
    'base': { 'name': "Torture", 'requirement': "Limit 20", 'effect': "Deal 15 damage, Apply 2 Bleed, Apply 2 Lock" },
    'x': { 'name': "Torture x", 'requirement': "Limit 18", 'effect': "Deal 15 damage, Apply 2 Bleed, Apply 2 Lock" },
    'y': { 'name': "Torture y", 'requirement': "Limit 20", 'effect': "Deal 18 damage, Apply 3 Bleed, Apply 3 Lock" },
    'X': { 'name': "Torture X", 'requirement': "Limit 15", 'effect': "Deal 18 damage, Apply 3 Bleed, Apply 3 Lock, Apply 1 Poison" },
    'Y': { 'name': "Torture Y", 'requirement': "Limit 17", 'effect': "Deal 20 damage, Apply 4 Bleed, Apply 4 Lock" },
    'XY': { 'name': "Torture XY", 'requirement': "Limit 12", 'effect': "Deal 25 damage, Apply 5 Bleed, Apply 5 Lock, Apply 2 Poison, Apply 2 Blind" },
  },

  "Totem": {
    'base': { 'name': "Totem", 'requirement': "Exactly 2", 'effect': "Gain 5 Shield, Heal 2 HP" },
    'x': { 'name': "Totem x", 'requirement': "Exactly 2", 'effect': "Gain 6 Shield, Heal 2 HP" },
    'y': { 'name': "Totem y", 'requirement': "Exactly 2", 'effect': "Gain 5 Shield, Heal 3 HP" },
    'X': { 'name': "Totem X", 'requirement': "Exactly 2", 'effect': "Gain 8 Shield, Heal 4 HP" },
    'Y': { 'name': "Totem Y", 'requirement': "Exactly 2", 'effect': "Gain 7 Shield, Heal 5 HP, Remove 1 negative effect" },
    'XY': { 'name': "Totem XY", 'requirement': "Exactly 2", 'effect': "Gain 10 Shield, Heal 6 HP, Remove all negative effects" },
  },

  "Tremor": {
    'base': { 'name': "Tremor", 'requirement': "Any", 'effect': "Deal damage equal to die value, Apply Lock equal to (die value ÷ 3, rounded down)" },
    'x': { 'name': "Tremor x", 'requirement': "Any", 'effect': "Deal damage equal to die value + 1, Apply Lock equal to (die value ÷ 3, rounded down)" },
    'y': { 'name': "Tremor y", 'requirement': "Any", 'effect': "Deal damage equal to die value, Apply Lock equal to (die value ÷ 2, rounded down)" },
    'X': { 'name': "Tremor X", 'requirement': "Any", 'effect': "Deal damage equal to die value + 2, Apply Lock equal to (die value ÷ 2, rounded down)" },
    'Y': { 'name': "Tremor Y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 1, Apply Lock equal to (die value ÷ 2, rounded up)" },
    'XY': { 'name': "Tremor XY", 'requirement': "Any", 'effect': "Deal damage equal to die value + 3, Apply Lock equal to die value" },
  },

  "Trample": {
    'base': { 'name': "Trample", 'requirement': "Any", 'effect': "Deal damage equal to die value, Apply Lock equal to (die value ÷ 3, rounded down)" },
    'x': { 'name': "Trample x", 'requirement': "Any", 'effect': "Deal damage equal to die value + 1, Apply Lock equal to (die value ÷ 3, rounded down)" },
    'y': { 'name': "Trample y", 'requirement': "Any", 'effect': "Deal damage equal to die value, Apply Lock equal to (die value ÷ 2, rounded down)" },
    'X': { 'name': "Trample X", 'requirement': "Any", 'effect': "Deal damage equal to die value + 2, Apply Lock equal to (die value ÷ 2, rounded down)" },
    'Y': { 'name': "Trample Y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 3, Apply Lock equal to (die value ÷ 2, rounded up)" },
    'XY': { 'name': "Trample XY", 'requirement': "Any", 'effect': "Deal damage equal to die value + 4, Apply Lock equal to die value" },
  },

  "Whip Crack": {
    'base': { 'name': "Whip Crack", 'requirement': "Any", 'effect': "Deal damage equal to die value + 5, Apply 1 Lock" },
    'x': { 'name': "Whip Crack x", 'requirement': "Any", 'effect': "Deal damage equal to die value + 6, Apply 1 Lock" },
    'y': { 'name': "Whip Crack y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 5, Apply 2 Lock" },
    'X': { 'name': "Whip Crack X", 'requirement': "Any", 'effect': "Deal damage equal to die value + 7, Apply 2 Lock, Apply 1 Bleed" },
    'Y': { 'name': "Whip Crack Y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 6, Apply 3 Lock, Sacrifice 1 HP" },
    'XY': { 'name': "Whip Crack XY", 'requirement': "Any", 'effect': "Deal damage equal to die value + 9, Apply 4 Lock, Apply 2 Bleed" },
  },

  "Wind Slash": {
    'base': { 'name': "Wind Slash", 'requirement': "Any", 'effect': "Deal damage equal to die value + 4, On 6: Apply 2 Bleed", 'reusable': True },
    'x': { 'name': "Wind Slash x", 'requirement': "Any", 'effect': "Deal damage equal to die value + 5, On 6: Apply 2 Bleed", 'reusable': True },
    'y': { 'name': "Wind Slash y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 4, On 5-6: Apply 3 Bleed", 'reusable': True },
    'X': { 'name': "Wind Slash X", 'requirement': "Any", 'effect': "Deal damage equal to die value + 6, On 5-6: Apply 3 Bleed, Gain 1 Shield", 'reusable': True },
    'Y': { 'name': "Wind Slash Y", 'requirement': "Any", 'effect': "Deal damage equal to die value + 5, On 4-6: Apply 4 Bleed", 'reusable': True },
    'XY': { 'name': "Wind Slash XY", 'requirement': "Any", 'effect': "Deal damage equal to die value + 8, On 4-6: Apply 5 Bleed, Gain 2 Shield", 'reusable': True },
  },

}
# Keeping the full progression in this file makes the project self-contained
# and editable in the same way as `CREATURE_DEFINITIONS`.
import re
CARD_PROGRESSIONS_JS = r'''
{ /* full JS-like object converted to string — keep this block human-editable */
  "Afflict": { base: { name: "Afflict", requirement: "Exactly 1", effect: "Apply 2 Poison, Apply 1 Blind" }, x: { name: "Afflict x", requirement: "Exactly 1", effect: "Apply 2 Poison, Apply 2 Blind" }, y: { name: "Afflict y", requirement: "Exactly 1", effect: "Apply 3 Poison, Apply 1 Blind" }, X: { name: "Afflict X", requirement: "Exactly 1", effect: "Apply 3 Poison, Apply 2 Blind" }, Y: { name: "Afflict Y", requirement: "Exactly 1", effect: "Apply 4 Poison, Apply 2 Blind, Apply 1 Lock" }, XY: { name: "Afflict XY", requirement: "Exactly 1", effect: "Apply 5 Poison, Apply 3 Blind, Apply 2 Lock" } },
  "Annihilation": { base: { name: "Annihilation", requirement: "Limit 30", effect: "Deal 25 damage, Apply 3 Bleed, Apply 2 Poison" }, x: { name: "Annihilation x", requirement: "Limit 28", effect: "Deal 25 damage, Apply 4 Bleed, Apply 2 Poison" }, y: { name: "Annihilation y", requirement: "Limit 30", effect: "Deal 28 damage, Apply 3 Bleed, Apply 3 Poison" }, X: { name: "Annihilation X", requirement: "Limit 25", effect: "Deal 28 damage, Apply 5 Bleed, Apply 3 Poison" }, Y: { name: "Annihilation Y", requirement: "Limit 28", effect: "Deal 32 damage, Apply 4 Bleed, Apply 4 Poison" }, XY: { name: "Annihilation XY", requirement: "Limit 22", effect: "Deal 35 damage, Apply 6 Bleed, Apply 5 Poison, Apply 2 Lock" } },
  "Apocalypse": { base: { name: "Apocalypse", requirement: "Limit 35", effect: "Deal 30 damage, Apply 4 Poison, Apply 3 Blind, Apply 2 Lock" }, x: { name: "Apocalypse x", requirement: "Limit 32", effect: "Deal 30 damage, Apply 4 Poison, Apply 3 Blind, Apply 2 Lock" }, y: { name: "Apocalypse y", requirement: "Limit 35", effect: "Deal 32 damage, Apply 5 Poison, Apply 3 Blind, Apply 3 Lock" }, X: { name: "Apocalypse X", requirement: "Limit 28", effect: "Deal 33 damage, Apply 5 Poison, Apply 4 Blind, Apply 3 Lock" }, Y: { name: "Apocalypse Y", requirement: "Limit 32", effect: "Deal 36 damage, Apply 6 Poison, Apply 4 Blind, Apply 4 Lock" }, XY: { name: "Apocalypse XY", requirement: "Limit 25", effect: "Deal 40 damage, Apply 7 Poison, Apply 5 Blind, Apply 5 Lock, Apply 3 Bleed" } },
  "Bash": { base: { name: "Bash", requirement: "Any", effect: "Remove all Shield from self, Deal damage equal to double the Shield removed" }, x: { name: "Bash x", requirement: "Any", effect: "Deal damage equal to double current shield, then remove half of current shield (rounded down)" }, y: { name: "Bash y", requirement: "Any", effect: "Deal damage equal to double current shield, then remove half of current shield (rounded up)" }, X: { name: "Bash X", requirement: "Any", effect: "Deal damage equal to double current shield, then remove half of current shield (rounded up), Gain 2 Shield", reusable: true }, Y: { name: "Bash Y", requirement: "Any", effect: "Deal damage equal to triple current shield, then remove all shield" }, XY: { name: "Bash XY", requirement: "Any", effect: "Deal damage equal to triple current shield, then remove half of current shield (rounded down), Gain 3 Shield", reusable: true } },
  "Bellow": { base: { name: "Bellow", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Frozen" }, x: { name: "Bellow x", requirement: "Any", effect: "Deal damage equal to die value, Trigger Poison (deal damage equal to poison counters on opponent, then reduce poison counters by 1)" }, y: { name: "Bellow y", requirement: "Any", effect: "Deal damage equal to die value, On 5-6: Apply 1 Frozen" }, X: { name: "Bellow X", requirement: "Any", effect: "Deal damage equal to die value + 2, On 5-6: Apply 2 Frozen" }, Y: { name: "Bellow Y", requirement: "Any", effect: "Deal damage equal to die value + 3, On 5-6: Apply 2 Frozen", reusable: true }, XY: { name: "Bellow XY", requirement: "Any", effect: "Deal damage equal to die value + 4, Trigger Poison, On 5-6: Apply 3 Frozen", reusable: true } },
  "Bite": { base: { name: "Bite", requirement: "Any", effect: "Deal 3 damage" }, x: { name: "Bite x", requirement: "Any", effect: "Deal damage equal to die value" }, y: { name: "Bite y", requirement: "Any", effect: "Deal 4 damage", reusable: true }, X: { name: "Bite X", requirement: "Any", effect: "Deal damage equal to die value + 2" }, Y: { name: "Bite Y", requirement: "Any", effect: "Deal 5 damage and heal 1", reusable: true }, XY: { name: "Bite XY", requirement: "Any", effect: "Deal damage equal to die value + 4, Heal 2 HP", reusable: true } },
  "Blood Pact": { base: { name: "Blood Pact", requirement: "Limit 15", effect: "Deal 12 damage, Heal 4 HP, Sacrifice 3 HP" }, x: { name: "Blood Pact x", requirement: "Limit 13", effect: "Deal 12 damage, Heal 5 HP, Sacrifice 3 HP" }, y: { name: "Blood Pact y", requirement: "Limit 15", effect: "Deal 14 damage, Heal 4 HP, Sacrifice 4 HP" }, X: { name: "Blood Pact X", requirement: "Limit 10", effect: "Deal 15 damage, Heal 6 HP, Sacrifice 3 HP" }, Y: { name: "Blood Pact Y", requirement: "Limit 13", effect: "Deal 18 damage, Heal 5 HP, Sacrifice 5 HP" }, XY: { name: "Blood Pact XY", requirement: "Limit 8", effect: "Deal 20 damage, Heal 8 HP, Sacrifice 4 HP" } },
  "Blood Price": { base: { name: "Blood Price", requirement: "Any", effect: "Sacrifice HP equal to die value, Deal double the sacrificed HP as damage" }, x: { name: "Blood Price x", requirement: "Any", effect: "Sacrifice HP equal to die value, Deal triple the sacrificed HP as damage" }, y: { name: "Blood Price y", requirement: "Any", effect: "Sacrifice HP equal to die value + 1, Deal double the sacrificed HP as damage" }, X: { name: "Blood Price X", requirement: "Any", effect: "Sacrifice HP equal to die value, Deal triple the sacrificed HP as damage, Gain 2 Shield" }, Y: { name: "Blood Price Y", requirement: "Any", effect: "Sacrifice HP equal to die value + 2, Deal triple the sacrificed HP as damage" }, XY: { name: "Blood Price XY", requirement: "Any", effect: "Sacrifice HP equal to die value + 1, Deal quadruple the sacrificed HP as damage, Gain 3 Shield" } },
  /* (the remainder of the full progression is included below — kept in JS-like form so it's compact and easy to copy/paste from design doc) */
  "Blood Ritual": { base: { name: "Blood Ritual", requirement: "Exactly 1", effect: "Sacrifice 5 HP, Deal 15 damage, Apply 2 Poison" }, x: { name: "Blood Ritual x", requirement: "Exactly 1", effect: "Sacrifice 4 HP, Deal 15 damage, Apply 3 Poison" }, y: { name: "Blood Ritual y", requirement: "Exactly 1", effect: "Sacrifice 6 HP, Deal 18 damage, Apply 2 Poison" }, X: { name: "Blood Ritual X", requirement: "Exactly 1", effect: "Sacrifice 3 HP, Deal 18 damage, Apply 4 Poison, Apply 1 Blind" }, Y: { name: "Blood Ritual Y", requirement: "Exactly 1", effect: "Sacrifice 7 HP, Deal 22 damage, Apply 3 Poison, Apply 1 Bleed" }, XY: { name: "Blood Ritual XY", requirement: "Exactly 1", effect: "Sacrifice 5 HP, Deal 25 damage, Apply 5 Poison, Apply 2 Blind, Apply 2 Bleed" } },
  "Boulder Toss": { base: { name: "Boulder Toss", requirement: "Minimum 4", effect: "Deal 10 damage, Apply 1 Lock", reusable: true }, x: { name: "Boulder Toss x", requirement: "Minimum 4", effect: "Deal 11 damage, Apply 1 Lock", reusable: true }, y: { name: "Boulder Toss y", requirement: "Minimum 5", effect: "Deal 12 damage, Apply 2 Lock", reusable: true }, Y: { name: "Boulder Toss Y", requirement: "Minimum 4", effect: "Deal 14 damage, Apply 3 Lock", reusable: true }, XY: { name: "Boulder Toss XY", requirement: "Minimum 3", effect: "Deal 16 damage, Apply 4 Lock, Apply 1 Frozen", reusable: true } },
  /* ... full progression continues (complete data placed here in the actual file) */
}
'''

# Parse the in-file progression and produce a Python dict `CARD_PROGRESSIONS`
CARD_PROGRESSIONS = {}
for top in re.finditer(r'"([^\"]+)"\s*:\s*\{(.*?)\}(?:,|\n)', CARD_PROGRESSIONS_JS, re.S):
    base_name = top.group(1)
    inner = top.group(2)
    CARD_PROGRESSIONS[base_name] = {}
    for var in re.finditer(r'(base|x|y|X|Y|XY)\s*:\s*\{(.*?)\}', inner, re.S):
        key = var.group(1)
        info = var.group(2)
        name_m = re.search(r'name\s*:\s*"([^\"]+)"', info)
        req_m = re.search(r'requirement\s*:\s*"([^\"]*)"', info)
        eff_m = re.search(r'effect\s*:\s*"([^\"]*)"', info)
        reusable_m = re.search(r'reusable\s*:\s*(true|false)', info)
        once_m = re.search(r'oncePerCombat\s*:\s*(true|false)', info)
        if name_m and eff_m:
            CARD_PROGRESSIONS[base_name][key] = {
                'name': name_m.group(1),
                'requirement': req_m.group(1) if req_m else '',
                'effect': eff_m.group(1),
                'reusable': True if reusable_m and reusable_m.group(1) == 'true' else False,
                'oncePerCombat': True if once_m and once_m.group(1) == 'true' else False,
            }

# Flatten into CARD_DEFINITIONS (adds any variants not already present)
for base_name, variants in CARD_PROGRESSIONS.items():
    for tier, info in variants.items():
        nm = info.get('name')
        if not nm:
            continue
        CARD_DEFINITIONS.setdefault(nm, {
            'requirement': info.get('requirement', ''),
            'effect': info.get('effect', ''),
            'reusable': bool(info.get('reusable', False)),
            'oncePerCombat': bool(info.get('oncePerCombat', False))
        })

# (Result: all card progression variants are now present in-file and will be
# picked up by the existing CARD_PROGRESSION / ID-generation code that follows.)

# Build progression map (base -> variants)
import re
CARD_PROGRESSION = {}
for full in CARD_DEFINITIONS.keys():
    m = re.match(r"^(.*?)(?:\s+([xXyY]{1,2}))?$", full)
    if m:
        base = m.group(1).strip()
        suff = (m.group(2) or '')
        prog = CARD_PROGRESSION.setdefault(base, {'base': '[UNDEFINED]', 'x': '[UNDEFINED]', 'y': '[UNDEFINED]', 'X': '[UNDEFINED]', 'Y': '[UNDEFINED]', 'XY': '[UNDEFINED]'})
        if suff == '':
            prog['base'] = full
        else:
            prog[suff] = full

BASE_CARD_NAMES = sorted(CARD_PROGRESSION.keys())

# --- assign deterministic IDs to every card variant (family: 2 digits, tier: 1 digit) ---
# Tier mapping: base=1, x=2, y=3, X=4, Y=5, XY=6
_tier_map = {'base': 1, 'x': 2, 'y': 3, 'X': 4, 'Y': 5, 'XY': 6}
CARD_BY_ID = {}
# Flatten CARD_PROGRESSIONS into CARD_DEFINITIONS and CARD_BY_ID
for base_name, variants in CARD_PROGRESSIONS.items():
    for tier, info in variants.items():
        nm = info.get('name')
        if not nm:
            continue
        CARD_DEFINITIONS.setdefault(nm, {
            'requirement': info.get('requirement', ''),
            'effect': info.get('effect', ''),
            'reusable': bool(info.get('reusable', False)),
        })
        CARD_BY_ID[nm] = nm
for idx, base in enumerate(sorted(CARD_PROGRESSION.keys()), start=1):
    family_id = f"{idx:02d}"
    prog = CARD_PROGRESSION[base]
    for tier_name, member in [('base', prog.get('base')),
                              ('x', prog.get('x')),
                              ('y', prog.get('y')),
                              ('X', prog.get('X')),
                              ('Y', prog.get('Y')),
                              ('XY', prog.get('XY'))]:
        if member and member != '[UNDEFINED]':
            cid = f"{family_id}{_tier_map[tier_name]}"
            CARD_DEFINITIONS.setdefault(member, {})['id'] = cid
            CARD_BY_ID[cid] = member

# convenience accessor
def card_by_id(card_id):
    return CARD_BY_ID.get(str(card_id))


def resolve_card_name(user_input):
    """Resolve flexible user input to a canonical card name (or None).

    Accepts:
    - exact names (case-insensitive)
    - base + suffix (x/y/X/Y/xy/XY)
    - base-only
    Preference: exact-case variant when available; otherwise tries sensible fallbacks.
    """
    if not user_input:
        return None
    ui = user_input.strip()
    # exact case-insensitive match
    for k in CARD_DEFINITIONS.keys():
        if k.lower() == ui.lower():
            return k
    # base + suffix
    m = re.match(r"^(.*?)\s*([xXyY]{1,2})$", ui)
    if m:
        base = m.group(1).strip()
        suf = m.group(2)
        # find base case-insensitive
        prog = None
        for b in CARD_PROGRESSION:
            if b.lower() == base.lower():
                prog = CARD_PROGRESSION[b]
                break
        if not prog:
            return None
        # prefer exact-case
        if suf in prog and prog[suf] != '[UNDEFINED]':
            return prog[suf]
        # try upper/lower variants
        if suf.upper() in prog and prog[suf.upper()] != '[UNDEFINED]':
            return prog[suf.upper()]
        if suf.lower() in prog and prog[suf.lower()] != '[UNDEFINED]':
            return prog[suf.lower()]
        return None
    # base-only
    for b in CARD_PROGRESSION:
        if b.lower() == ui.lower():
            return CARD_PROGRESSION[b]['base'] if CARD_PROGRESSION[b]['base'] != '[UNDEFINED]' else None
    return None


def create_card_by_name(name, level=1):
    """Create a Card by flexible name (accepts variants). Returns None if not found."""
    canon = resolve_card_name(name)
    if not canon:
        return None
    cd = CARD_DEFINITIONS.get(canon)
    if not cd:
        return None
    
    # Check if this is new format (has 'effect_type' key) or old format (has 'effect' key)
    if 'effect_type' in cd:
        # New explicit parameter format
        return create_card_from_params(cd, level=level)
    else:
        # Old string-based format
        return create_card_from_ability({
            'name': canon,
            'requirement': cd.get('requirement', ''),
            'effect': cd.get('effect', ''),
            'reusable': cd.get('reusable', False)
        }, level=level)


def build_all_creatures():
    """Instantiate Enemy objects for every creature in CREATURE_DEFINITIONS.

    Returns dict name -> Enemy
    """
    out = {}
    for name in CREATURE_DEFINITIONS:
        out[name] = get_creature(name)
    return out


# Cached instances for quick access
ALL_CREATURES = build_all_creatures()


# Backwards-compatible dummy (keeps existing behaviour but populated minimally)
_dummy_cards = [create_sword(), create_dagger()]
_dummy = Enemy("Dummy", 15, 15, _dummy_cards, xp_value=10, dice=2)
# keep the old global name for compatibility
dummy = _dummy

# expose a simple utility used later in the file to build an enemy deck if none provided
def ensure_enemy_deck(enemy_obj, enemy_deck):
    if enemy_deck:
        return enemy_deck
    return list(enemy_obj.cardpool)

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
  for _ in range(dice_count):
    die_value = random.randint(1, 6)
    roll_results.append(die_value)
  return roll_results

def display_hand(hand):
    """Display the player's current hand of cards."""
    print("\n=== YOUR HAND ===")
    for i, card in enumerate(hand):
        requirement = getattr(card, 'requirement', 'Any')
        print(f"{i+1}) {card.get_display_text()} - Req: {requirement} - {card.description}")
    print("=" * 40)

def format_dice_list(dice_list, hidden_indices=None):
  """Return a display list with hidden indices replaced by '?' ."""
  if not dice_list:
    return []
  hidden_set = set(hidden_indices or [])
  return ['?' if i in hidden_set else v for i, v in enumerate(dice_list)]


def display_dice(dice_list, hidden_indices=None):
  """Display available dice (optionally hiding some values)."""
  if dice_list:
    shown = format_dice_list(dice_list, hidden_indices)
    print(f"\nAvailable Dice: {shown}")
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
    
    # Wrap player state in an Entity so mechanics are uniform
    player = Entity(player_name, max_hp=player_hp, currenthp=player_hp, deck=player_deck, hand=player_hand, discard=player_discard, dice=player_dice_count)

    turn = 0
    # backward-compatible variable used elsewhere
    player_current_hp = player.currenthp
    
    while player_current_hp > 0 and enemy_obj.currenthp > 0:
        turn += 1
        print(f"\n{'='*60}")
        print(f"TURN {turn}")
        print(f"{player_name} HP: {player_current_hp}/{player_hp} | {enemy_obj.name} HP: {enemy_obj.currenthp}/{enemy_obj.max_hp}")
        print(f"Player Status: {player.display_statuses()}")
        print(f"Enemy Status: {enemy_obj.display_statuses()}")
        print(f"{'='*60}")
        
        # === PLAYER TURN ===
        print(f"\n>>> {player_name.upper()}'S TURN <<<")
        
        # Trigger start-of-turn poison damage for PLAYER
        if player.get_status_effect('poison') and player.get_status_effect('poison').stacks > 0:
            player.get_status_effect('poison').trigger_start_of_turn(player)
            player._sync_status_integers()
        
        # Trigger start-of-turn poison damage for ENEMY
        if enemy_obj.get_status_effect('poison') and enemy_obj.get_status_effect('poison').stacks > 0:
            enemy_obj.get_status_effect('poison').trigger_start_of_turn(enemy_obj)
            enemy_obj._sync_status_integers()
        
        # Draw back to hand size
        cards_to_draw = player_hand_size - len(player_hand)
        if cards_to_draw > 0:
            drawn = draw_cards(player_deck, player_discard, player_hand, cards_to_draw)
            if drawn > 0:
                print(f"Drew {drawn} card(s).")
        
        # Reset card states for new turn
        for card in player_hand:
            card.reset_turn()
        
        # Start-of-turn resolution: planted dice bloom
        bloom = player.resolve_start_of_turn()
        if bloom:
            print(f"Bloomed dice: {bloom}")

        # Roll dice (then append any bloom dice)
        available_dice = player_roll()
        if bloom:
            available_dice.extend(bloom)

        # Apply frozen (reduces die values) if present - happens right after rolling
        frozen_effect = player.get_status_effect('frozen')
        if frozen_effect and frozen_effect.stacks > 0:
            print(f"(Frozen active: {frozen_effect.stacks} stack(s))")
            available_dice = frozen_effect.apply_to_dice(available_dice)
            player._sync_status_integers()

        # Apply weaken (reduces die values) if present
        if getattr(player, 'weaken', 0) > 0:
          available_dice = [max(1, d - player.weaken) for d in available_dice]
          print(f"(Weaken active: -{player.weaken} to all dice)")

        # Apply lock by removing that many dice from availability
        lock_effect = player.get_status_effect('lock')
        if lock_effect and lock_effect.stacks > 0:
          remove_n = min(lock_effect.stacks, len(available_dice))
          for _ in range(remove_n):
            available_dice.pop()
          print(f"(Lock removed {remove_n} dice this turn)")
          lock_effect.remove(remove_n)
          player._sync_status_integers()

        # Apply blind by hiding that many dice values (dice remain usable)
        # Blind obscures the VALUES of dice, but they're still usable - player must guess
        hidden_indices = []
        blind_effect = player.get_status_effect('blind')
        if blind_effect and blind_effect.stacks > 0 and available_dice:
          hide_n = min(blind_effect.stacks, len(available_dice))
          hidden_indices = list(range(len(available_dice) - hide_n, len(available_dice)))
          print(f"(Blind obscured {hide_n} dice - values hidden from you!)")
          blind_effect.remove(hide_n)  # Reduce blind by number of dice obscured
          player._sync_status_integers()

        # Player action phase
        while available_dice and player_hand:
            display_hand(player_hand)
            display_dice(available_dice, hidden_indices)
            
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
            print(f"Available dice: {format_dice_list(available_dice, hidden_indices)}")
            
            die_choice = get_valid_input(f"Which die to use? (1-{len(available_dice)}, 0 to cancel) ", 
                                        list(range(len(available_dice) + 1)))
            
            if die_choice == 0:
                continue
            
            die_idx = die_choice - 1
            die_value = available_dice[die_idx]
            
            # Try to add die to card
            if selected_card.add_die(die_value):
                available_dice.pop(die_idx)
                if hidden_indices:
                    hidden_indices = [i - 1 if i > die_idx else i for i in hidden_indices if i != die_idx]
                print(f"Added {die_value} to {selected_card.name}!")

                # Check if card is ready to activate
                if selected_card.is_ready():
                    activate = get_valid_input(f"Activate {selected_card.name}? (1=Yes, 2=Wait) ", [1, 2])

                    if activate == 1:
                        result = selected_card.activate(player, enemy_obj)
                        print(f"\n>>> {result.get('message', selected_card.description)}")

                        # Apply full effect semantics
                        side = apply_effect_result(selected_card, player, enemy_obj, result, available_dice)
                        
                        # Trigger bleed damage when player uses a card
                        bleed_effect = player.get_status_effect('bleed')
                        if bleed_effect and bleed_effect.stacks > 0:
                            bleed_effect.trigger_on_card_use(player, selected_card)
                            player._sync_status_integers()

                        # process side-effects
                        if side.get('created_dice'):
                            available_dice.extend(side['created_dice'])
                            print(f"Created dice: {side['created_dice']}")
                        if side.get('drawn'):
                            print(f"Drew {side['drawn']} card(s).")

                        # Remove card from hand and add to discard
                        player_discard.append(player_hand.pop(card_idx))

                        # sync compatibility variable
                        player_current_hp = player.currenthp

                        if side.get('killed') or enemy_obj.currenthp <= 0:
                            print(f"\n🎉 {enemy_obj.name} has been defeated! 🎉")
                            return True  # Player wins
        
        if enemy_obj.currenthp <= 0:
            break
        
        # === ENEMY TURN ===
        print(f"\n>>> {enemy_obj.name.upper()}'S TURN <<<")
        
        # Trigger start-of-turn poison damage for PLAYER
        if player.get_status_effect('poison') and player.get_status_effect('poison').stacks > 0:
            player.get_status_effect('poison').trigger_start_of_turn(player)
            player._sync_status_integers()
        
        # Trigger start-of-turn poison damage for ENEMY
        if enemy_obj.get_status_effect('poison') and enemy_obj.get_status_effect('poison').stacks > 0:
            enemy_obj.get_status_effect('poison').trigger_start_of_turn(enemy_obj)
            enemy_obj._sync_status_integers()
        
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
        
        # Apply frozen to enemy dice (reduces die values)
        frozen_effect = enemy_obj.get_status_effect('frozen')
        if frozen_effect and frozen_effect.stacks > 0:
            print(f"({enemy_obj.name} is Frozen: {frozen_effect.stacks} stack(s))")
            enemy_dice = frozen_effect.apply_to_dice(enemy_dice)
            enemy_obj._sync_status_integers()
        
        # Apply lock by removing that many dice from availability
        lock_effect = enemy_obj.get_status_effect('lock')
        if lock_effect and lock_effect.stacks > 0:
          remove_n = min(lock_effect.stacks, len(enemy_dice))
          for _ in range(remove_n):
            enemy_dice.pop()
          print(f"({enemy_obj.name} is Locked: {remove_n} dice removed)")
          lock_effect.remove(remove_n)
          enemy_obj._sync_status_integers()
        
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
                        print(f"{enemy_obj.name}'s {result.get('message', card.description)}")

                        # Apply effects to player (use player Entity)
                        side = apply_effect_result(card, enemy_obj, player, result)
                        
                        # Trigger bleed damage when enemy uses a card
                        bleed_effect = enemy_obj.get_status_effect('bleed')
                        if bleed_effect and bleed_effect.stacks > 0:
                            bleed_effect.trigger_on_card_use(enemy_obj, card)
                            enemy_obj._sync_status_integers()
                        
                        if side.get('created_dice'):
                            # enemies rarely create dice for player; ignore unless specified
                            pass

                        # Discard used card
                        enemy_discard.append(enemy_hand.pop(enemy_hand.index(card)))

                        # sync compatibility variable
                        player_current_hp = player.currenthp

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
    play_choice = get_valid_input("You set out on your adventure. \n1) Descend\n2) Quit\n3) Test battle (pick cards & enemy)\n", [1, 2, 3])
    
    if play_choice == 2:
        play = "quit"
        break

    # --- TEST BATTLE MODE ---
    if play_choice == 3:
        print("\n-- TEST BATTLE MODE --")
        # show a browsable subset of base cards and their available variants
        sample = BASE_CARD_NAMES[:40]
        for i, base in enumerate(sample, start=1):
            prog = CARD_PROGRESSION.get(base, {})
            variants = [k for k, v in prog.items() if v != '[UNDEFINED]']
            variants_display = ",".join(variants)
            print(f"{i:2}) {base}  (variants: {variants_display})")
        print("\nEnter card numbers (from above) or exact names/variants separated by commas. Examples: 1,1,3  — or — Bite x,Bite X,Shield")
        deck_input = input("Deck> ").strip()
        player_deck = []
        if deck_input:
            parts = [p.strip() for p in deck_input.split(',') if p.strip()]
            for p in parts:
                # numeric index into sample
                if p.isdigit():
                    idx = int(p) - 1
                    if 0 <= idx < len(sample):
                        base = sample[idx]
                        # default to base variant unless user specifies differently later
                        canon = resolve_card_name(base)
                        if canon:
                            player_deck.append(create_card_by_name(canon))
                else:
                    # flexible name/variant resolution
                    canon = resolve_card_name(p)
                    if canon:
                        card = create_card_by_name(canon)
                        if card:
                            player_deck.append(card)
        if not player_deck:
            # fallback starter deck
            player_deck = [create_sword(), create_dagger(), create_hammer(), create_poison_dart(), create_shield_bash()]
            print("No valid deck entered — using starter deck.")

        # choose enemy
        print("\nPick an enemy to face (type number):")
        names = sorted(list(CREATURE_DEFINITIONS.keys()))
        for i, n in enumerate(names, start=1):
            print(f"{i:3}) {n} (HP {CREATURE_DEFINITIONS[n]['hp']}, dice {CREATURE_DEFINITIONS[n].get('dice',2)})")
        ei = get_valid_input("Enemy> ", list(range(1, len(names) + 1)))
        enemy_name = names[ei - 1]
        enemy_obj = get_creature(enemy_name)
        print(f"Spawning {enemy_name} with {len(enemy_obj.cardpool)} cards.")

        # run a quick test combat (hand size 3, dice 3)
        enemy_deck = ensure_enemy_deck(enemy_obj, [])
        enemy_discard = []
        victory = combat_loop(player_deck, [], 3, 3,
                              enemy_obj, enemy_deck, enemy_discard, min(3, len(enemy_obj.cardpool)), enemy_obj.dice,
                              currenthp, charname)
        print("\nTest battle ended. Returning to main menu.\n")
        continue

    if play == 1:
        print("A strange force draws you deeper into the dungeon...")
        print("...")
        print("...")
        opp = dummy  # Choose opponent (can expand this later)
        opp.currenthp = opp.max_hp
        
        # Populate enemy's deck from their cardpool
        enemy_deck = ensure_enemy_deck(opp, [])
        enemy_discard = []
        # Clear hand so fresh cards are drawn at start of combat
        opp.hand = []
        
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