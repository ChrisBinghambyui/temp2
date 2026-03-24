import math
import random
from colorama import init, Fore, Back, Style
# --- Creature & card data (inlined from original `cards_data.py`) ---
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
      {"name": "Flame Burst", "requirement": "Odd only", "effect": "Deal triple die value damage"},
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
            'poison': poison_counter(0),
            'bleed': bleed_counter(0),
            'blind': blind_counter(0),
            'lock': lock_counter(0),
            'frozen': freeze_counter(0),
            # 'vampirism': Vampirism(0),
            # 'thorn': Thorn(0),
            # 'weaken': Weaken(0),
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




poison_counter = 0
health = 10
dice = []
burn_counter = 0
lock_counter = 0
freeze_counter = 0
bleed_counter = 0
blind_counter = 0

# triggers at start of turn
if poison_counter > 0:
    health -= poison_counter
    poison_counter -= 1


# triggers when card is played
if burn_counter > 0:
    health = health - (burn_counter*2)
    burn_counter-=1


# triggers when dice are rolled, before freeze
if lock_counter > 0:
    while lock_counter > 0 and dice > 0:
        dice.pop(0)
        lock_counter -= 1


#triggers right after lock
if freeze_counter > 0:
    for i in range(len(dice)):
        if dice[i] > 1 and freeze_counter > 0:
            dice[i] = 1
            freeze_counter -= 1


# I guess this can trigger after freeze
# Find a way to have it replace the die when it's being displayed with a ? without replacing it's value
if blind_counter > 0:
    hidden_indices = []
    if blind_counter > 0 and dice:
        hide_n = min(blind_counter, len(dice))
        hidden_indices = list(range(len(dice) - hide_n, len(dice)))
        print(f"(Blind obscured {hide_n} dice - values hidden from you!)")
        blind_counter -= hide_n
    


# triggers at end of turn
if bleed_counter > 0:
    health -= bleed_counter
    bleed_counter -= 1

