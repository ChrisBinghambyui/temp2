import math
import random
import builtins
import shutil
import textwrap
import time
from colorama import init, Fore, Back, Style
import time
import sys

def typingPrint(text, delay=None, typing_speed=0.02):
  if delay is None:
    delay = PRINT_DELAY_SECONDS

  wrapped_text = _word_wrap_for_terminal(text)

  # Apply speed multiplier
  adjusted_typing_speed = typing_speed * SPEED_MULTIPLIER
  adjusted_delay = delay * SPEED_MULTIPLIER

  for character in wrapped_text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(adjusted_typing_speed)
  sys.stdout.write('\n')
  sys.stdout.flush()
  time.sleep(max(0, float(adjusted_delay)))


PRINT_DELAY_SECONDS = 0.5
SPEED_MULTIPLIER = 1.0  # Global speed multiplier for text printing


def set_speed_multiplier(speed_choice):
    """Set global speed multiplier based on player choice.
    1=instant (0x), 2=fast (0.5x), 3=normal (1x), 4=slow (2x)"""
    global SPEED_MULTIPLIER
    speed_map = {1: 0.0, 2: 0.5, 3: 1.0, 4: 2.0}
    SPEED_MULTIPLIER = speed_map.get(speed_choice, 1.0)


def _word_wrap_for_terminal(text):
  terminal_width = max(20, shutil.get_terminal_size((100, 20)).columns - 1)
  lines = str(text).split("\n")
  wrapped_lines = []

  for line in lines:
    if not line.strip():
      wrapped_lines.append("")
      continue
    wrapped_lines.append(
      textwrap.fill(
        line,
        width=terminal_width,
        break_long_words=False,
        break_on_hyphens=False,
      )
    )

  return "\n".join(wrapped_lines)


def print(*args, **kwargs):
  delay_seconds = kwargs.pop("delay", PRINT_DELAY_SECONDS)
  sep = kwargs.pop("sep", " ")
  typing_speed = kwargs.pop("typing_speed", 0.05)  # Character delay in seconds

  if args:
    joined_message = sep.join(str(arg) for arg in args)
    wrapped_message = _word_wrap_for_terminal(joined_message)
    
    # Print character by character with typing animation
    for character in wrapped_message:
      sys.stdout.write(character)
      sys.stdout.flush()
      time.sleep(typing_speed)
    
    # Add final newline
    sys.stdout.write('\n')
    sys.stdout.flush()
  else:
    builtins.print(**kwargs)

  # Add delay between print statements
  time.sleep(max(0, float(delay_seconds)))


def pause(seconds):
  time.sleep(max(0, float(seconds)))

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

"""
Biome keys:
plains = 1
tundra = 2
forest = 3
ruins = 4
slopes = 5
pit = 6
"""



class CARD:

    def __init__(self, name, description, id, rarity):
        self.name = name
        self.description = description
        self.id = id
        self.rarity = rarity
        
        """Rarities:
        Common 1, Uncommon 2, Rare 3, Heroic 4, Legendary 5, Celestial 6"""

"""
first two digits: card family

next one digit: upgrade tier

next 3 digits: limit (if any) than the limit. 000 if no limit, 1XX if yes, 200 if no limit and reusable, 222 if once per combat

next 2 digits: die requirements (01 is any, 02 is evens, 03 is odds, 7? accepts only the second digit)

next 2 digits: damage (if any), AX is die value * Z (A2 would be double die value), E is die value plus second value (E5 would be die value plus 5, E0 is just die value) 

next 2 digits: if triggering bonus effects are contingent on a certain number. 00 is no. 1 then a digit means just that digit (15 means only on 5's). 2 then a digit means that digit is the max, 3 then a digit means that digit is the minimum. 41 is odds, 42 is evens.

next 6 digits: status effects (00 is nothing. First digit is the code for the status to apply, second digit is how many to apply (X for die value, Y for half die value , A for die value + 1, B for same + 2, etc). 1 for poison (1Z means trigger poison), 2 for burn, 3 for lock, 4 for freeze, 5 for bleed, 6 for blind, 7 is for shield, 8 is for heal, 9 is for sacrifice. Z is for unique effects, HAS TO BE FIRST, the other 5 digits will be the unique identifier for what it does)
"""

afflict = CARD(name="Afflict", description="Apply 2 Poison, Apply 1 Blind", id="010000710000126100", rarity=2)
afflictx = CARD(name="Afflict x", description="Apply 2 Poison, Apply 2 Blind", id="011000710000126200", rarity=10)
afflictxx = CARD(name="Afflict X", description="Apply 3 Poison, Apply 2 Blind", id="01-2-000-71-00-00-136200", rarity=10)
afflicty = CARD(name="Afflict y", description="Apply 3 Poison, Apply 1 Blind", id="01-3-000-71-00-00-136100", rarity=10)
afflictyy = CARD(name="Afflict Y", description="Apply 4 Poison, Apply 2 Blind, Apply 1 Lock", id="01-4-000-71-00-00-143162", rarity=10)
afflictxy = CARD(name="Afflict XY", description="Apply 5 Poison, Apply 3 Blind, Apply 2 Lock", id="01-5-000-71-00-00-153263", rarity=10)

annihilation = CARD(name="Annihilation", description="Deal 20 damage, Apply 2 Bleed, Apply 2 Poison", id="02-0-130-01-25-00-125300", rarity=6)
annihilationx = CARD(name="Annihilation x", description="Deal 20 damage, Apply 2 Bleed, Apply 2 Poison", id="02-1-128-01-25-00-125400", rarity=10)
annihilationxx = CARD(name="Annihilation X", description="Deal 22 damage, Apply 3 Bleed, Apply 3 Poison", id="02-2-125-01-28-00-135500", rarity=10)
annihilationy = CARD(name="Annihilation y", description="Deal 22 damage, Apply 3 Bleed, Apply 3 Poison", id="02-3-130-01-28-00-135300", rarity=10)
annihilationyy = CARD(name="Annihilation Y", description="Deal 25 damage, Apply 4 Bleed, Apply 4 Poison", id="02-4-128-01-32-00-145400", rarity=10)
annihilationxy = CARD(name="Annihilation XY", description="Deal 30 damage, Apply 4 Bleed, Apply 4 Poison", id="02-5-122-01-30-00-145400", rarity=10)

apocalypse = CARD(name="Apocalypse", description="Deal 30 damage, Apply 2 Burn", id="03-0-135-01-30-00-220000", rarity=6)
apocalypsex = CARD(name="Apocalypse x", description="Deal 30 damage, Apply 2 Burn", id="03-1-132-01-30-00-220000", rarity=10)
apocalypsexx = CARD(name="Apocalypse X", description="Deal 33 damage, Apply 2 Burn", id="03-2-130-01-33-00-220000", rarity=10)
apocalypsey = CARD(name="Apocalypse y", description="Deal 32 damage, Apply 2 Burn", id="03-3-135-01-32-00-220000", rarity=10)
apocalypseyy = CARD(name="Apocalypse Y", description="Deal 35 damage, Apply 3 Burn", id="03-4-132-01-35-00-230000", rarity=10)
apocalypsexy = CARD(name="Apocalypse XY", description="Deal 35 damage, Apply 3 Burn", id="03-5-130-01-35-00-230000", rarity=10)

bash = CARD(name="Bash", description="Remove all Shield from self, Deal damage equal to double the Shield removed", id="04-0-000-01-00-00-Z00001", rarity=2)
bashx = CARD(name="Bash x", description="Deal damage equal to double current shield, then remove half of current shield (rounded down)", id="04-1-000-01-00-00-Z00002", rarity=10)
bashxx = CARD(name="Bash X", description="Deal damage equal to double current shield, then remove half of current shield (rounded up), Gain 2 Shield", id="04-2-000-01-00-00-Z00003", rarity=10)
bashy = CARD(name="Bash y", description="Deal damage equal to double current shield, then remove half of current shield (rounded up)", id="04-3-000-01-00-00-Z00004", rarity=10)
bashyy = CARD(name="Bash Y", description="Deal damage equal to triple current shield, then remove all shield", id="04-4-000-01-00-00-Z00005", rarity=10)
bashxy = CARD(name="Bash XY", description="Deal damage equal to triple current shield, then remove half of current shield (rounded down), Gain 3 Shield", id="04-5-000-01-00-00-Z00006", rarity=10)

bellow = CARD(name="Bellow", description="Deal damage equal to die value, On 6: Apply 1 Frozen", id="05-0-000-01-E0-16-410000", rarity=1)
bellowx = CARD(name="Bellow x", description="Deal damage equal to die value, On 6: Apply 1 Frozen and 1 Poison", id="05-1-000-01-E0-16-11411Z", rarity=10)
bellowxx = CARD(name="Bellow X", description="Deal damage equal to die value, On 6: Apply 2 Frozen + 1 Poison + trigger poison", id="05-2-000-01-E0-16-11421Z", rarity=10)
bellowy = CARD(name="Bellow y", description="Deal damage equal to die value, On 5-6: Apply 1 Frozen", id="05-3-000-01-E0-35-410000", rarity=10)
bellowyy = CARD(name="Bellow Y", description="Deal damage equal to die value + 2, On 5-6: Apply 2 Frozen", id="05-4-200-01-E2-35-420000", rarity=10)
bellowxy = CARD(name="Bellow XY", description="Deal damage equal to die value + 2, On 5-6: Apply 3 Frozen and 3 Poison + trigger poison", id="05-5-200-01-E2-35-13431Z", rarity=10)

bite = CARD(name="Bite", description="Deal 3 damage", id="06-0-000-01-03-00-000000", rarity=1)
bitex = CARD(name="Bite x", description="Deal damage equal to die value", id="06-1-000-01-E0-00-000000", rarity=10)
bitexx = CARD(name="Bite X", description="Deal damage equal to die value + 2", id="06-2-000-01-E2-00-000000", rarity=10)
bitey = CARD(name="Bite y", description="Deal 4 damage", id="06-3-200-01-04-00-000000", rarity=10)
biteyy = CARD(name="Bite Y", description="Deal 5 damage and heal 1", id="06-4-200-01-05-00-810000", rarity=10)
bitexy = CARD(name="Bite XY", description="Deal damage equal to die value + 4, Heal 2 HP", id="06-5-200-01-E4-00-820000", rarity=10)

bloodpact = CARD(name="Blood Pact", description="Deal 12 damage, Sacrifice 3 HP, Heal 4 HP", id="07-0-115-01-12-00-938400", rarity=4)
bloodpactx = CARD(name="Blood Pact x", description="Deal 12 damage, Heal 5 HP, Sacrifice 3 HP", id="07-1-113-01-12-00-958300", rarity=10)
bloodpactxx = CARD(name="Blood Pact X", description="Deal 15 damage, Heal 6 HP, Sacrifice 3 HP", id="07-2-110-01-15-00-968300", rarity=10)
bloodpacty = CARD(name="Blood Pact y", description="Deal 14 damage, Sacrifice 4 HP, Heal 6 HP", id="07-3-115-01-14-00-948600", rarity=10)
bloodpactyy = CARD(name="Blood Pact Y", description="Deal 18 damage, Sacrifice 5 HP, Heal 8 HP", id="07-4-113-01-18-00-958800", rarity=10)
bloodpactxy = CARD(name="Blood Pact XY", description="Deal 20 damage, Heal 12 HP, Sacrifice 8 HP", id="07-5-108-01-20-00-8C9800", rarity=10)

bloodprice = CARD(name="Blood Price", description="Sacrifice HP equal to die value, Deal double the sacrificed HP as damage", id="08-0-000-01-A2-00-9X0000", rarity=4)
bloodpricex = CARD(name="Blood Price x", description="Sacrifice HP equal to die value, Deal triple the sacrificed HP as damage", id="08-1-000-01-A3-00-9X0000", rarity=10)
bloodpricexx = CARD(name="Blood Price X", description="Sacrifice HP equal to die value, Deal triple the sacrificed HP as damage, Gain 2 Shield", id="08-2-000-01-A3-00-729X00", rarity=10)
bloodpricey = CARD(name="Blood Price y", description="Sacrifice HP equal to HALF the die value (rounded up), Deal double the sacrificed HP as damage", id="08-3-000-01-A2-00-9Y0000", rarity=10)
bloodpriceyy = CARD(name="Blood Price Y", description="Sacrifice HP equal to half the die value (rounded down), Deal triple the sacrificed HP as damage", id="08-4-000-01-A3-00-9Z0000", rarity=10)
bloodpricexy = CARD(name="Blood Price XY", description="Sacrifice HP equal to half the die value (rounded down), Deal quadruple the sacrificed HP as damage, Gain 3 Shield", id="08-5-000-01-A4-00-739Z00", rarity=10)

bloodritual = CARD(name="Blood Ritual", description="Sacrifice 5 HP, Deal 15 damage, Apply 2 Poison", id="09-0-000-71-15-00-951200", rarity=4)
bloodritualx = CARD(name="Blood Ritual x", description="Sacrifice 4 HP, Deal 15 damage, Apply 3 Poison", id="09-1-000-71-15-00-941300", rarity=10)
bloodritualxx = CARD(name="Blood Ritual X", description="Sacrifice 3 HP, Deal 18 damage, Apply 4 Poison, Apply 1 Blind", id="09-2-000-71-18-00-931416", rarity=10)
bloodritualy = CARD(name="Blood Ritual y", description="Sacrifice 6 HP, Deal 18 damage, Apply 2 Poison", id="09-3-000-71-18-00-961215", rarity=10)
bloodritualyy = CARD(name="Blood Ritual Y", description="Sacrifice 7 HP, Deal 22 damage, Apply 3 Poison, Apply 1 Bleed", id="09-4-000-71-22-00-973115", rarity=10)
bloodritualxy = CARD(name="Blood Ritual XY", description="Sacrifice 5 HP, Deal 25 damage, Apply 5 Poison, Apply 2 Blind, Apply 2 Bleed", id="09-5-000-71-25-00-955626", rarity=10)

bouldertoss = CARD(name="Boulder Toss", description="Deal 10 damage, Apply 1 Lock", id="10-0-115-01-10-00-310000", rarity=3)
bouldertossx = CARD(name="Boulder Toss x", description="Deal 11 damage, Apply 1 Lock", id="10-1-200-34-11-00-310000", rarity=10)
bouldertossy = CARD(name="Boulder Toss y", description="Deal 12 damage, Apply 2 Lock", id="10-3-200-35-12-00-320000", rarity=10)
bouldertossyy = CARD(name="Boulder Toss Y", description="Deal 14 damage, Apply 3 Lock", id="10-4-200-34-14-00-330000", rarity=10)
bouldertossxy = CARD(name="Boulder Toss XY", description="Deal 16 damage, Apply 4 Lock, Apply 1 Frozen", id="10-5-200-33-16-00-344100", rarity=10)

chainlightning = CARD(name="Chain Lightning", description="Deal triple die value damage", id="11-0-102-03-A3-00-000000", rarity=3)
chainlightningx = CARD(name="Chain Lightning x", description="Deal triple die value damage, Apply 1 Blind", id="11-1-000-03-A3-00-610000", rarity=10)
chainlightningxx = CARD(name="Chain Lightning X", description="Deal quadruple die value damage, Apply 1 Blind", id="11-2-000-03-A4-00-610000", rarity=10)
chainlightningy = CARD(name="Chain Lightning y", description="Deal quadruple die value damage", id="11-3-102-03-A4-00-000000", rarity=10)
chainlightningyy = CARD(name="Chain Lightning Y", description="Deal quadruple die value damage, Apply 1 Blind", id="11-4-102-03-A4-00-610000", rarity=10)
chainlightningxy = CARD(name="Chain Lightning XY", description="Deal quadruple die value damage, Apply 2 Blind", id="11-5-000-03-A4-00-620000", rarity=10)

chains = CARD(name="Chains", description="Deal 6 damage, Apply 2 Lock", id="12-0-200-33-06-00-320000", rarity=2)
chainsx = CARD(name="Chains x", description="Deal 7 damage, Apply 2 Lock", id="12-1-200-33-07-00-320000", rarity=10)
chainsxx = CARD(name="Chains X", description="Deal 8 damage, Apply 3 Lock", id="12-2-200-33-08-00-330000", rarity=10)
chainsy = CARD(name="Chains y", description="Deal 8 damage, Apply 3 Lock", id="12-3-200-34-08-00-330000", rarity=10)
chainsyy = CARD(name="Chains Y", description="Deal 10 damage, Apply 4 Lock", id="12-4-200-33-10-00-340000", rarity=10)
chainsxy = CARD(name="Chains XY", description="Deal 12 damage, Apply 5 Lock, Apply 2 Blind", id="12-5-200-32-12-00-355260", rarity=10)

charge = CARD(name="Charge", description="Deal 8 damage, Gain 3 Shield (activates when limit reaches 0)", id="13-0-115-01-08-00-730000", rarity=2)
chargex = CARD(name="Charge x", description="Deal 8 damage, Gain 3 Shield", id="13-1-113-01-08-00-730000", rarity=10)
chargexx = CARD(name="Charge X", description="Deal 10 damage, Gain 10 Shield", id="13-2-120-01-10-00-7A0000", rarity=10)
chargey = CARD(name="Charge y", description="Deal 8 damage, Gain 8 Shield", id="13-3-118-01-08-00-780000", rarity=10)
chargeyy = CARD(name="Charge Y", description="Deal 12 damage, Gain 6 Shield", id="13-4-115-01-12-00-760000", rarity=10)
chargexy = CARD(name="Charge XY", description="Deal 15 damage, Gain 12 Shield, Apply 1 Lock", id="13-5-112-01-15-00-7C3100", rarity=10)

chomp = CARD(name="Chomp", description="Deal 10 damage", id="14-0-110-01-10-00-000000", rarity=2)
chompx = CARD(name="Chomp x", description="Deal 10 damage", id="14-1-108-01-10-00-000000", rarity=10)
chompxx = CARD(name="Chomp X", description="Deal 14 damage, Heal 3 HP", id="14-2-110-01-14-00-830000", rarity=10)
chompy = CARD(name="Chomp y", description="Deal 12 damage", id="14-3-112-01-12-00-000000", rarity=10)
chompyy = CARD(name="Chomp Y", description="Deal 18 damage, Heal 4 HP", id="14-4-108-01-18-00-840000", rarity=10)
chompxy = CARD(name="Chomp XY", description="Deal 20 damage, Heal 5 HP", id="14-5-115-01-20-00-850000", rarity=10)

clawswipe = CARD(name="Claw Swipe", description="Deal damage equal to die value + 3, On 6: Apply 1 Bleed", id="15-0-200-01-E3-16-510000", rarity=2)
clawswipex = CARD(name="Claw Swipe x", description="Deal damage equal to die value + 4, On 6: Apply 1 Bleed", id="15-1-200-01-E4-16-510000", rarity=10)
clawswipexx = CARD(name="Claw Swipe X", description="Deal damage equal to die value + 5, On 5-6: Apply 2 Bleed", id="15-2-200-01-E5-35-520000", rarity=10)
clawswipey = CARD(name="Claw Swipe y", description="Deal damage equal to die value + 3, On 5-6: Apply 2 Bleed", id="15-3-200-01-E3-35-520000", rarity=10)
clawswipeyy = CARD(name="Claw Swipe Y", description="Deal damage equal to die value + 4, On 4-6: Apply 3 Bleed", id="15-4-200-01-E4-34-530000", rarity=10)
clawswipexy = CARD(name="Claw Swipe XY", description="Deal damage equal to die value + 6, On 4-6: Apply 4 Bleed", id="15-5-200-01-E6-34-540000", rarity=10)

control = CARD(name="Control", description="Sacrifice 2 HP, draw a new card, and roll a new die", id="16-0-000-71-00-00-Z00013", rarity=3)
controlx = CARD(name="Control x", description="Sacrifice 1 HP, draw a new card, and roll a new die", id="16-1-000-71-00-00-Z00014", rarity=10)
controlxx = CARD(name="Control X", description="Draw a new card, and roll a new die", id="16-2-000-71-00-00-Z00015", rarity=10)
controly = CARD(name="Control y", description="Sacrifice 2 HP, draw 2 new cards, and roll a new die", id="16-3-000-71-00-00-Z00016", rarity=10)
controlyy = CARD(name="Control Y", description="Sacrifice 3 HP, draw 2 new cards, and roll 2 new dice", id="16-4-000-71-00-00-Z00017", rarity=10)
controlxy = CARD(name="Control XY", description="Sacrifice 1 HP, draw 3 new cards, and roll 2 new dice", id="16-5-000-71-00-00-Z00018", rarity=10)

curse = CARD(name="Curse", description="Apply 2 Poison, Apply 2 Blind", id="17-0-000-71-00-00-126200", rarity=3)
cursex = CARD(name="Curse x", description="Apply 2 Poison, Apply 3 Blind", id="17-1-000-71-00-00-126300", rarity=10)
cursexx = CARD(name="Curse X", description="Apply 3 Poison, Apply 4 Blind, Apply 1 Lock", id="17-2-000-71-00-00-134631", rarity=10)
cursey = CARD(name="Curse y", description="Apply 3 Poison, Apply 2 Blind", id="17-3-000-71-00-00-136200", rarity=10)
curseyy = CARD(name="Curse Y", description="Apply 4 Poison, Apply 3 Blind, Apply 1 Lock", id="17-4-000-71-00-00-144331", rarity=10)
cursexy = CARD(name="Curse XY", description="Apply 5 Poison, Apply 5 Blind, Apply 2 Lock", id="17-5-000-71-00-00-155532", rarity=10)

dagger = CARD(name="Dagger", description="Deal 2 damage, Apply 1 Poison", id="18-0-000-03-02-00-110000", rarity=1)
daggerx = CARD(name="Dagger x", description="Deal 3 damage, Apply 1 Poison", id="18-1-000-01-03-00-110000", rarity=10)
daggerxx = CARD(name="Dagger X", description="Deal 4 damage, Apply 2 Poison", id="18-2-000-01-04-00-120000", rarity=10)
daggery = CARD(name="Dagger y", description="Deal 2 damage, Apply 2 Poison", id="18-3-000-03-02-00-120000", rarity=10)
daggeryy = CARD(name="Dagger Y", description="Deal 3 damage, Apply 2 Poison", id="18-4-000-03-03-00-120000", rarity=10)
daggerxy = CARD(name="Dagger XY", description="Deal 6 damage, Apply 3 Poison", id="18-5-000-01-06-00-130000", rarity=10)

darkaegis = CARD(name="Dark Aegis", description="Gain Shield equal to die value + 4, Apply 1 Poison to opponent", id="19-0-200-02-E4-00-711000", rarity=4)
darkaegisx = CARD(name="Dark Aegis x", description="Gain Shield equal to die value + 5, Apply 1 Poison to opponent", id="19-1-200-02-E5-00-711000", rarity=10)
darkaegisxx = CARD(name="Dark Aegis X", description="Gain Shield equal to die value + 6, Apply 2 Poison to opponent, Heal 1 HP", id="19-2-200-02-E6-00-712810", rarity=10)
darkaegisy = CARD(name="Dark Aegis y", description="Gain Shield equal to die value + 4, Apply 2 Poison to opponent", id="19-3-200-02-E4-00-712000", rarity=10)
darkaegisyy = CARD(name="Dark Aegis Y", description="Gain Shield equal to die value + 5, Apply 3 Poison to opponent", id="19-4-200-02-E5-00-713000", rarity=10)
darkaegisxy = CARD(name="Dark Aegis XY", description="Gain Shield equal to die value + 8, Apply 3 Poison to opponent, Heal 2 HP", id="19-5-200-02-E8-00-713820", rarity=10)

darkblessing = CARD(name="Dark Blessing", description="Heal 8 HP, Apply 2 Poison to opponent", id="20-0-118-01-00-00-812000", rarity=4)
darkblessingx = CARD(name="Dark Blessing x", description="Heal 8 HP, Apply 2 Poison to opponent", id="20-1-116-01-00-00-812000", rarity=10)
darkblessingxx = CARD(name="Dark Blessing X", description="Heal 10 HP, Apply 3 Poison to opponent, Gain 2 Shield", id="20-2-113-01-00-00-8A1372", rarity=10)
darkblessingy = CARD(name="Dark Blessing y", description="Heal 10 HP, Apply 3 Poison to opponent", id="20-3-118-01-00-00-8A3000", rarity=10)
darkblessingyy = CARD(name="Dark Blessing Y", description="Heal 12 HP, Apply 4 Poison to opponent", id="20-4-115-01-00-00-8C4000", rarity=10)
darkblessingxy = CARD(name="Dark Blessing XY", description="Heal 15 HP, Apply 5 Poison to opponent, Gain 4 Shield", id="20-5-110-01-00-00-8F5740", rarity=10)

desperation = CARD(name="Desperation", description="Deal 10 damage, Sacrifice 5 HP", id="21-0-000-71-10-00-950000", rarity=2)
desperationx = CARD(name="Desperation x", description="Deal 10 HP, Sacrifice 4 HP", id="21-1-000-71-10-00-940000", rarity=10)
desperationxx = CARD(name="Desperation X", description="Deal 12 damage, Sacrifice 3 HP", id="21-2-000-71-12-00-930000", rarity=10)
desperationy = CARD(name="Desperation y", description="Deal 12 damage, Sacrifice 5 HP", id="21-3-102-71-12-00-950000", rarity=10)
desperationyy = CARD(name="Desperation Y", description="Deal 15 damage, Sacrifice 5 HP", id="21-4-103-71-15-00-950000", rarity=10)
desperationxy = CARD(name="Desperation XY", description="Deal 18 damage, Sacrifice 3 HP", id="21-5-103-71-18-00-930000", rarity=10)

divebomb = CARD(name="Dive Bomb", description="Deal 12 damage, Apply 1 Blind", id="22-0-000-35-12-00-610000", rarity=3)
divebombx = CARD(name="Dive Bomb x", description="Deal 12 damage, Apply 2 Blind", id="22-1-000-35-12-00-620000", rarity=10)
divebombxx = CARD(name="Dive Bomb X", description="Deal 14 damage, Apply 3 Blind, Apply 1 Lock", id="22-2-000-34-14-00-633100", rarity=10)
divebomby = CARD(name="Dive Bomb y", description="Deal 14 damage, Apply 1 Blind", id="22-3-000-36-14-00-610000", rarity=10)
divebombyy = CARD(name="Dive Bomb Y", description="Deal 16 damage, Apply 2 Blind, Apply 1 Bleed", id="22-4-000-35-16-00-625100", rarity=10)
divebombxy = CARD(name="Dive Bomb XY", description="Deal 18 damage, Apply 4 Blind, Apply 2 Lock, Apply 2 Bleed", id="22-5-000-33-18-00-643225", rarity=10)

dominate = CARD(name="Dominate", description="Apply 2 Lock, Sacrifice 3 HP", id="23-0-000-71-00-00-932000", rarity=4)
dominatex = CARD(name="Dominate x", description="Apply 3 Lock, Sacrifice 3 HP", id="23-1-000-71-00-00-933000", rarity=10)
dominatexx = CARD(name="Dominate X", description="Apply 4 Lock, Sacrifice 2 HP, Apply 1 Blind", id="23-2-000-71-00-00-942610", rarity=10)
dominatey = CARD(name="Dominate y", description="Apply 2 Lock, Sacrifice 2 HP, Apply 1 Blind", id="23-3-000-71-00-00-932161", rarity=10)
dominateyy = CARD(name="Dominate Y", description="Apply 3 Lock, Sacrifice 1 HP, Apply 2 Blind, Apply 1 Poison", id="23-4-000-71-00-00-931626", rarity=10)
dominatexy = CARD(name="Dominate XY", description="Apply 5 Lock, Sacrifice 1 HP, Apply 3 Blind, Apply 2 Poison", id="23-5-000-71-00-00-951636", rarity=10)

earthquake = CARD(name="Earthquake", description="Deal 12 damage, Apply 2 Lock, Apply 1 Frozen", id="24-0-120-01-12-00-324100", rarity=4)
earthquakex = CARD(name="Earthquake x", description="Deal 12 damage, Apply 2 Lock, Apply 1 Frozen", id="24-1-118-01-12-00-324100", rarity=10)
earthquakexx = CARD(name="Earthquake X", description="Deal 15 damage, Apply 3 Lock, Apply 2 Frozen, Destroy opponent Shield", id="24-2-115-01-15-00-Z00019", rarity=10)
earthquakey = CARD(name="Earthquake y", description="Deal 14 damage, Apply 3 Lock, Apply 2 Frozen", id="24-3-120-01-14-00-334200", rarity=10)
earthquakeyy = CARD(name="Earthquake Y", description="Deal 18 damage, Apply 4 Lock, Apply 3 Frozen", id="24-4-117-01-18-00-344300", rarity=10)
earthquakexy = CARD(name="Earthquake XY", description="Deal 20 damage, Apply 5 Lock, Apply 4 Frozen, Destroy opponent Shield", id="24-5-112-01-20-00-Z00020", rarity=10)

earthshatter = CARD(name="Earthshatter", description="Deal 15 damage, Apply 3 Lock, Apply 2 Frozen", id="25-0-122-01-15-00-334200", rarity=4)
earthshatterx = CARD(name="Earthshatter x", description="Deal 15 damage, Apply 3 Lock, Apply 2 Frozen", id="25-1-120-01-15-00-334200", rarity=10)
earthshatterxx = CARD(name="Earthshatter X", description="Deal 18 damage, Apply 4 Lock, Apply 3 Frozen, Apply 1 Bleed", id="25-2-117-01-18-00-344351", rarity=10)
earthshattery = CARD(name="Earthshatter y", description="Deal 18 damage, Apply 4 Lock, Apply 3 Frozen", id="25-3-122-01-18-00-344300", rarity=10)
earthshatteryy = CARD(name="Earthshatter Y", description="Deal 22 damage, Apply 5 Lock, Apply 4 Frozen", id="25-4-119-01-22-00-354400", rarity=10)
earthshatterxy = CARD(name="Earthshatter XY", description="Deal 25 damage, Apply 6 Lock, Apply 5 Frozen, Apply 2 Bleed", id="25-5-114-01-25-00-364552", rarity=10)

evade = CARD(name="Evade", description="Gain Shield equal to 2 × the number of dice used this turn", id="26-0-000-71-00-00-Z00021", rarity=3)
evadex = CARD(name="Evade x", description="Gain Shield equal to 3 × the number of dice used this turn", id="26-1-000-71-00-00-Z00022", rarity=10)
evadexx = CARD(name="Evade X", description="Gain Shield equal to 4 × the number of dice used this turn, Remove 1 negative effect", id="26-2-000-71-00-00-Z00023", rarity=10)
evadey = CARD(name="Evade y", description="Gain Shield equal to 2 × the number of dice used this turn, Heal 2 HP", id="26-3-000-71-00-00-Z00024", rarity=10)
evadeyy = CARD(name="Evade Y", description="Gain Shield equal to 3 × the number of dice used this turn, Heal 4 HP", id="26-4-000-71-00-00-Z00025", rarity=10)
evadexy = CARD(name="Evade XY", description="Gain Shield equal to 5 × the number of dice used this turn, Heal 3 HP, Remove all negative effects", id="26-5-000-71-00-00-Z00026", rarity=10)

execution = CARD(name="Execution", description="Deal 22 damage, Apply 4 Bleed", id="27-0-125-01-22-00-540000", rarity=5)
executionx = CARD(name="Execution x", description="Deal 22 damage, Apply 4 Bleed", id="27-1-123-01-22-00-540000", rarity=10)
executionxx = CARD(name="Execution X", description="Deal 25 damage, Apply 5 Bleed, Apply 1 Lock", id="27-2-120-01-25-00-543100", rarity=10)
executiony = CARD(name="Execution y", description="Deal 25 damage, Apply 5 Bleed", id="27-3-125-01-25-00-550000", rarity=10)
executionyy = CARD(name="Execution Y", description="Deal 28 damage, Apply 6 Bleed, Heal 2 HP", id="27-4-122-01-28-00-568200", rarity=10)
executionxy = CARD(name="Execution XY", description="Deal 32 damage, Apply 7 Bleed, Apply 2 Lock, Heal 3 HP", id="27-5-118-01-32-00-573182", rarity=10)

flail = CARD(name="Flail", description="Deal damage equal to die value, Sacrifice 1 HP", id="28-0-000-01-E0-00-910000", rarity=2)
flailx = CARD(name="Flail x", description="Deal damage equal to die value, Sacrifice 1 HP", id="28-1-200-01-E0-00-910000", rarity=10)
flailxx = CARD(name="Flail X", description="Deal damage equal to die value + 1, Sacrifice 1 HP, Apply 1 Bleed", id="28-2-200-01-E1-00-915100", rarity=10)
flaily = CARD(name="Flail y", description="Deal damage equal to die value + 1, Sacrifice 2 HP", id="28-3-200-01-E1-00-920000", rarity=10)
flailyy = CARD(name="Flail Y", description="Deal damage equal to die value + 2, Sacrifice 2 HP, On 6: Apply 2 Bleed", id="28-4-200-01-E2-16-925200", rarity=10)
flailxy = CARD(name="Flail XY", description="Deal damage equal to die value + 3, Sacrifice 1 HP, Apply 2 Bleed", id="28-5-200-01-E3-00-915200", rarity=10)

flameburst = CARD(name="Flame Burst", description="Deal double die value damage", id="29-0-000-03-A2-00-000000", rarity=3)
flameburstx = CARD(name="Flame Burst x", description="Deal double die value damage, Apply 2 Burn", id="29-1-000-03-A2-00-220000", rarity=10)
flameburstxx = CARD(name="Flame Burst X", description="Deal triple die value damage, Apply 2 Burn", id="29-2-000-03-A3-00-220000", rarity=10)
flameburstY = CARD(name="Flame Burst y", description="Deal triple die value damage", id="29-3-000-03-A3-00-000000", rarity=10)
flameburstyy = CARD(name="Flame Burst Y", description="Deal triple die value damage, Apply 1 Burn", id="29-4-000-03-A3-00-210000", rarity=10)
flameburstxy = CARD(name="Flame Burst XY", description="Deal triple die value damage, Apply 3 Burn", id="29-5-000-03-A3-00-230000", rarity=10)

flamestrike = CARD(name="Flame Strike", description="Deal double die value damage, Apply 1 Burn", id="30-0-000-03-A2-00-210000", rarity=3)
flamestrikex = CARD(name="Flame Strike x", description="Deal double die value damage, Apply 2 Burn", id="30-1-000-03-A2-00-220000", rarity=10)
flamestrikexx = CARD(name="Flame Strike X", description="Deal triple die value damage, Apply 3 Burn", id="30-2-000-03-A3-00-230000", rarity=10)
flamestrikEy = CARD(name="Flame Strike y", description="Deal triple die value damage", id="30-3-000-03-A3-00-000000", rarity=10)
flamestrikeyy = CARD(name="Flame Strike Y", description="Deal quadruple die value damage", id="30-4-000-03-A4-00-000000", rarity=10)
flamestrikexy = CARD(name="Flame Strike XY", description="Deal quadruple die value damage, Apply 3 burn", id="30-5-000-03-A4-00-230000", rarity=10)

flamewall = CARD(name="Flame Wall", description="Gain Shield equal to die value + 5, Deal 5 damage", id="31-0-200-02-E5-00-750500", rarity=4)
flamewallx = CARD(name="Flame Wall x", description="Gain Shield equal to die value + 6, Deal 5 damage", id="31-1-200-02-E6-00-750500", rarity=10)
flamewallxx = CARD(name="Flame Wall X", description="Gain Shield equal to die value + 8, Deal 6 damage, Apply 1 Burn", id="31-2-200-02-E8-00-760621", rarity=10)
flamewally = CARD(name="Flame Wall y", description="Gain Shield equal to die value + 5, Deal 7 damage", id="31-3-200-02-E5-00-750700", rarity=10)
flamewallyy = CARD(name="Flame Wall Y", description="Gain Shield equal to die value + 6, Deal 10 damage, Apply 1 Burn", id="31-4-200-02-E6-00-7A0A21", rarity=10)
flamewallxy = CARD(name="Flame Wall XY", description="Gain Shield equal to die value + 10, Deal 8 damage, Apply 2 Burn", id="31-5-200-02-EA-00-7A0822", rarity=10)

fortify = CARD(name="Fortify", description="Gain 3 Shield", id="32-0-000-01-00-00-730000", rarity=1)
fortifyx = CARD(name="Fortify x", description="Gain 4 Shield and heal 1", id="32-1-000-01-00-00-748100", rarity=10)
fortifyxx = CARD(name="Fortify X", description="Gain 5 Shield, Heal 2", id="32-2-000-01-00-00-758200", rarity=10)
fortifyy = CARD(name="Fortify y", description="Gain 6 Shield", id="32-3-000-01-00-00-760000", rarity=10)
fortifyyy = CARD(name="Fortify Y", description="Gain 8 Shield, Heal 1 HP", id="32-4-000-01-00-00-788100", rarity=10)
fortifyxy = CARD(name="Fortify XY", description="Gain 10 Shield, Heal 4 HP", id="32-5-000-01-00-00-7A8400", rarity=10)

frosteddagger = CARD(name="Frosted Dagger", description="Deal damage equal to die value, On 6: Apply 1 Poison", id="33-0-000-01-E0-16-110000", rarity=1)
frosteddaggerx = CARD(name="Frosted Dagger x", description="Deal damage equal to die value, On 6: Apply 1 Poison and 1 Frozen", id="33-1-000-01-E0-16-114100", rarity=10)
frosteddaggery = CARD(name="Frosted Dagger y", description="Deal damage equal to die value, On 5-6: Apply 1 Poison and 1 Frozen", id="33-2-000-01-E0-35-114100", rarity=10)
frosteddaggerxx = CARD(name="Frosted Dagger X", description="Deal damage equal to die value + 1, On 5-6: Apply 2 Poison and 2 Frozen", id="33-3-000-01-E1-35-124260", rarity=10)
frosteddaggeryy = CARD(name="Frosted Dagger Y", description="Deal damage equal to die value + 2, On 4-6: Apply 2 Poison and 2 Frozen", id="33-4-000-01-E2-34-124260", rarity=10)
frosteddaggerxy = CARD(name="Frosted Dagger XY", description="Deal damage equal to die value + 3, On 4-6: Apply 3 Poison and 3 Frozen", id="33-5-000-01-E3-34-134360", rarity=10)

frostedspear = CARD(name="Frosted Spear", description="Deal 3 damage", id="34-0-200-34-03-00-000000", rarity=1)
frostedspearx = CARD(name="Frosted Spear x", description="Deal 3 damage, on 6 apply 1 Frozen", id="34-1-200-33-03-16-410000", rarity=10)
frostedspearxx = CARD(name="Frosted Spear X", description="Deal 5 damage, On 5-6: Apply 1 Frozen", id="34-2-200-01-05-35-410000", rarity=10)
frostedspeary = CARD(name="Frosted Spear y", description="Deal 5 damage, On 6: Apply 1 Frozen", id="34-3-200-34-05-16-410000", rarity=10)
frostedspearYy = CARD(name="Frosted Spear Y", description="Deal 6 damage, On 5-6: Apply 2 Frozen", id="34-4-200-33-06-35-420000", rarity=10)
frostedspearxy = CARD(name="Frosted Spear XY", description="Deal 8 damage, On 4-6: Apply 3 Frozen", id="34-5-200-01-08-34-430000", rarity=10)

gore = CARD(name="Gore", description="Deal damage equal to die value, On 6: Apply 1 Bleed", id="35-0-000-01-E0-16-510000", rarity=1)
gorex = CARD(name="Gore x", description="Deal 2 + die value damage, On 6: Apply 1 Bleed", id="35-1-000-01-E2-16-510000", rarity=10)
gorexx = CARD(name="Gore X", description="Deal 4 + die value damage, On 6: Apply 2 Bleed", id="35-2-000-01-E4-16-520000", rarity=10)
gorey = CARD(name="Gore y", description="Deal 3 + die value damage, On 6: Apply 1 Bleed", id="35-3-000-01-E3-16-510000", rarity=10)
goreyy = CARD(name="Gore Y", description="Deal 5 + die value damage, On 5-6: Apply 2 Bleed", id="35-4-000-01-E5-35-520000", rarity=10)
gorexy = CARD(name="Gore XY", description="Deal 7 + die value damage, On 4-6: Apply 3 Bleed, Heal 1 HP", id="35-5-000-01-E7-34-538100", rarity=10)

hauntingwail = CARD(name="Haunting Wail", description="Apply 2 Blind, Apply 1 Lock", id="36-0-108-01-00-00-623100", rarity=3)
hauntingwailx = CARD(name="Haunting Wail x", description="Apply 2 Blind, Apply 1 Lock", id="36-1-107-01-00-00-623100", rarity=10)
hauntingwailxx = CARD(name="Haunting Wail X", description="Apply 3 Blind, Apply 2 Lock, Apply 1 Poison", id="36-2-105-01-00-00-633211", rarity=10)
hauntingwaily = CARD(name="Haunting Wail y", description="Apply 3 Blind, Apply 2 Lock", id="36-3-108-01-00-00-633200", rarity=10)
hauntingwailyy = CARD(name="Haunting Wail Y", description="Apply 4 Blind, Apply 3 Lock", id="36-4-106-01-00-00-644300", rarity=10)
hauntingwailxy = CARD(name="Haunting Wail XY", description="Apply 5 Blind, Apply 4 Lock, Apply 2 Poison", id="36-5-104-01-00-00-654421", rarity=10)

hellfire = CARD(name="Hellfire", description="Deal triple die value damage", id="37-0-103-01-A3-00-000000", rarity=4)
hellfirex = CARD(name="Hellfire x", description="Deal triple die value damage", id="37-1-104-01-A3-00-000000", rarity=10)
hellfirexx = CARD(name="Hellfire X", description="Deal quadruple die value damage", id="37-2-104-01-A4-00-000000", rarity=10)
hellfirey = CARD(name="Hellfire y", description="Deal quadruple die value damage", id="37-3-103-01-A4-00-000000", rarity=10)
hellfireyy = CARD(name="Hellfire Y", description="Deal quintuple die value damage", id="37-4-103-01-A5-00-000000", rarity=10)
hellfirexy = CARD(name="Hellfire XY", description="Deal quintuple die value damage", id="37-5-104-01-A5-00-000000", rarity=10)

howl = CARD(name="Howl", description="Heal 2 HP", id="38-0-108-01-00-00-820000", rarity=1)
howlx = CARD(name="Howl x", description="Heal 2 HP", id="38-1-107-01-00-00-820000", rarity=10)
howlxx = CARD(name="Howl X", description="Heal 3 HP, Remove 1 negative effect", id="38-2-105-01-00-00-Z00027", rarity=10)
howly = CARD(name="Howl y", description="Heal 3 HP", id="38-3-108-01-00-00-830000", rarity=10)
howlyy = CARD(name="Howl Y", description="Heal 4 HP, Gain 2 Shield", id="38-4-106-01-00-00-847200", rarity=10)
howlxy = CARD(name="Howl XY", description="Heal 5 HP, Remove all negative effects, Gain 3 Shield", id="38-5-104-01-00-00-Z00028", rarity=10)

hypeup = CARD(name="Hype Up", description="Heal 4 HP, Apply 1 Blind to self and opponent (activates when limit reaches 0)", id="39-0-112-01-00-00-Z00029", rarity=3)
hypeupx = CARD(name="Hype Up x", description="Heal 4 HP, Apply 1 Blind to self and opponent", id="39-1-110-01-00-00-Z00030", rarity=10)
hypeupxx = CARD(name="Hype Up X", description="Heal 5 HP, Apply 2 Blind to opponent only", id="39-2-108-01-00-00-Z00031", rarity=10)
hypeupy = CARD(name="Hype Up y", description="Heal 5 HP, Apply 2 Blind to self and opponent", id="39-3-112-01-00-00-Z00032", rarity=10)
hypeupyy = CARD(name="Hype Up Y", description="Heal 6 HP, Apply 3 Blind to self and opponent, Gain 2 Shield", id="39-4-110-01-00-00-Z00033", rarity=10)
hypeupxy = CARD(name="Hype Up XY", description="Heal 8 HP, Apply 3 Blind to opponent only, Gain 4 Shield", id="39-5-106-01-00-00-Z00034", rarity=10)

icemagic = CARD(name="Ice Magic", description="Heal 2 HP, Remove all negative effects from self", id="40-0-000-72-00-00-Z00035", rarity=3)
icemagicx = CARD(name="Ice Magic x", description="Heal 3 HP, Remove all negative effects from self", id="40-1-000-72-00-00-Z00036", rarity=10)
icemagicxx = CARD(name="Ice Magic X", description="Heal 4 HP, Remove all negative effects from self, Gain 2 Shield", id="40-2-102-72-00-00-Z00037", rarity=10)
icemagicy = CARD(name="Ice Magic y", description="Heal 2 HP, Remove all negative effects from self", id="40-3-102-72-00-00-Z00038", rarity=10)
icemagicyy = CARD(name="Ice Magic Y", description="Heal 3 HP, Remove all negative effects from self, Gain 3 Shield", id="40-4-102-72-00-00-Z00039", rarity=10)
icemagicxy = CARD(name="Ice Magic XY", description="Heal 5 HP, Remove all negative effects from self, Gain 5 Shield", id="40-5-103-72-00-00-Z00040", rarity=10)

immolate = CARD(name="Immolate", description="Deal 10 damage, Apply 2 Burn, Sacrifice 2 HP", id="41-0-110-01-10-00-229200", rarity=3)
immolatex = CARD(name="Immolate x", description="Deal 10 damage, Apply 2 Burn, Sacrifice 2 HP", id="41-1-109-01-10-00-229200", rarity=10)
immolatexx = CARD(name="Immolate X", description="Deal 12 damage, Apply 3 Burn, Sacrifice 1 HP", id="41-2-107-01-12-00-239100", rarity=10)
immolatey = CARD(name="Immolate y", description="Deal 12 damage, Apply 3 Burn, Sacrifice 3 HP", id="41-3-110-01-12-00-239300", rarity=10)
immolateyy = CARD(name="Immolate Y", description="Deal 15 damage, Apply 4 Burn, Sacrifice 4 HP", id="41-4-108-01-15-00-249400", rarity=10)
immolatexy = CARD(name="Immolate XY", description="Deal 18 damage, Apply 5 Burn, Sacrifice 2 HP", id="41-5-105-01-18-00-259200", rarity=10)

condemn = CARD(name="Condemn", description="Deal damage equal to die value + 8, Sacrifice 2 HP", id="42-0-200-23-E8-00-920000", rarity=4)
condemnx = CARD(name="Condemn x", description="Deal damage equal to die value + 9, Sacrifice 2 HP", id="42-1-200-23-E9-00-920000", rarity=10)
condemnxx = CARD(name="Condemn X", description="Deal damage equal to die value + 11, Sacrifice 1 HP", id="42-2-200-24-EB-00-910000", rarity=10)
condemny = CARD(name="Condemn y", description="Deal damage equal to die value + 10, Sacrifice 3 HP", id="42-3-200-23-EA-00-930000", rarity=10)
Condemnyy = CARD(name="Condemn Y", description="Deal damage equal to die value + 12, Sacrifice 4 HP", id="42-4-200-23-EC-00-940000", rarity=10)
condemnxy = CARD(name="Condemn XY", description="Deal damage equal to die value + 14, Sacrifice 2 HP", id="42-5-200-24-EE-00-920000", rarity=10)

cleansingfire = CARD(name="Inferno", description="Deal double die value damage", id="43-0-000-03-A2-00-Z00041", rarity=4)
cleansingfirex = CARD(name="Inferno x", description="Deal triple die value damage", id="43-1-000-03-A3-00-Z00042", rarity=10)
cleansingfirexx = CARD(name="Inferno X", description="Deal triple die value damage, remove all negative effects", id="43-2-000-03-A3-00-Z00043", rarity=10)
cleansingfirey = CARD(name="Inferno y", description="Deal double die value damage, remove all negative effects", id="43-3-000-03-A2-00-Z00044", rarity=10)
cleansingfireyy = CARD(name="Inferno Y", description="Deal triple die value damage, remove all negative effects", id="43-4-000-03-A3-00-Z00045", rarity=10)
cleansingfirexy = CARD(name="Inferno XY", description="Deal quadruple die value damage, remove all negative effects", id="43-5-000-03-A4-00-Z00046", rarity=10)

jab = CARD(name="Jab", description="Deal damage equal to die value", id="44-0-000-01-E0-00-000000", rarity=1)
jabx = CARD(name="Jab x", description="Deal 2 + die value damage", id="44-1-000-01-E2-00-000000", rarity=10)
jabxx = CARD(name="Jab X", description="Deal 4 + die value damage", id="44-2-200-01-E4-00-000000", rarity=10)
jaby = CARD(name="Jab y", description="Deal damage equal to die value", id="44-3-200-01-E0-00-000000", rarity=10)
jabyy = CARD(name="Jab Y", description="Deal 5 + die value damage, On 6: Apply 1 Bleed", id="44-4-200-01-E5-16-510000", rarity=10)
jabxy = CARD(name="Jab XY", description="Deal 6 + die value damage, On 5-6: Apply 2 Bleed", id="44-5-200-01-E6-35-520000", rarity=10)

jadespear = CARD(name="Jade Spear", description="Apply Poison equal to die value", id="45-0-000-02-00-00-1X0000", rarity=3)
jadespearx = CARD(name="Jade Spear x", description="Apply Poison equal to die value, Gain 1 Shield", id="45-1-000-02-00-00-1X7100", rarity=10)
jadespearxx = CARD(name="Jade Spear X", description="Apply Poison equal to die value + 1, Gain 2 Shield, Apply 1 Blind", id="45-2-000-02-00-00-1A7261", rarity=10)
jadespeary = CARD(name="Jade Spear y", description="Apply Poison equal to die value + 1", id="45-3-000-02-00-00-1A0300", rarity=10)
jadespearyy = CARD(name="Jade Spear Y", description="Apply Poison equal to die value + 2, Deal 3 damage", id="45-4-000-02-00-00-1B0300", rarity=10)
jadespearxy = CARD(name="Jade Spear XY", description="Apply Poison equal to die value + 3, Deal 5 damage, Gain 3 Shield, Apply 2 Blind", id="45-5-000-02-00-00-1C730562", rarity=10)

judgement = CARD(name="Judgement", description="Deal 10 damage, Heal 6 HP, Apply  2 Lock", id="46-0-000-76-10-00-863200", rarity=5)
judgementx = CARD(name="Judgement x", description="Deal 12 damage, Heal 7 HP, Apply 2 Lock", id="46-1-000-76-12-00-873200", rarity=10)
judgementxx = CARD(name="Judgement X", description="Deal 14 damage, Heal 8 HP, Apply 3 Lock, Gain 3 Shield", id="46-2-000-76-14-00-883373", rarity=10)
judgementy = CARD(name="Judgement y", description="Deal 14 damage, Heal 6 HP, Apply 3 Lock", id="46-3-000-76-14-00-863300", rarity=10)
judgementyy = CARD(name="Judgement Y", description="Deal 18 damage, Heal 7 HP, Apply 4 Lock", id="46-4-000-76-18-00-873400", rarity=10)
judgementxy = CARD(name="Judgement XY", description="Deal 20 damage, Heal 10 HP, Apply 5 Lock, Gain 5 Shield", id="46-5-000-76-20-00-8A3575", rarity=10)

lifedrain = CARD(name="Life Drain", description="Deal damage equal to die value, Heal 1 HP", id="47-0-000-03-E0-00-810000", rarity=2)
lifedrainx = CARD(name="Life Drain x", description="Deal damage equal to die value + 2, Heal half the damage dealt (rounded up)", id="47-1-000-03-E2-00-Z00047", rarity=10)
lifedrainxx = CARD(name="Life Drain X", description="Deal damage equal to die value + 4, Heal half the damage dealt (rounded up)", id="47-2-000-03-E4-00-Z00048", rarity=10)
lifedrainy = CARD(name="Life Drain y", description="Deal damage equal to die value + 1, Heal half the damage dealt (rounded up)", id="47-3-200-03-E1-00-Z00049", rarity=10)
lifedrainyy = CARD(name="Life Drain Y", description="Deal damage equal to die value + 2, Heal half the damage dealt (rounded up)", id="47-4-200-03-E2-00-Z00050", rarity=10)
lifedrainxy = CARD(name="Life Drain XY", description="Deal damage equal to die value + 4, Heal the full damage dealt", id="47-5-200-03-E4-00-Z00051", rarity=10)

lightningbolt = CARD(name="Lightning Bolt", description="Deal triple die value damage", id="48-0-222-03-A3-00-000000", rarity=3)
lightningboltx = CARD(name="Lightning Bolt x", description="Deal triple die value damage, Apply 1 Blind", id="48-1-222-03-A3-00-610000", rarity=10)
lightningboltxx = CARD(name="Lightning Bolt X", description="Deal triple die value damage, Apply 2 Blind", id="48-2-000-03-A3-00-620000", rarity=10)
lightningbolty = CARD(name="Lightning Bolt y", description="Deal quadruple die value damage", id="48-3-222-03-A4-00-000000", rarity=10)
lightningboltyy = CARD(name="Lightning Bolt Y", description="Deal quadruple die value damage, Apply 2 Blind", id="48-4-222-03-A4-00-620000", rarity=10)
lightningboltxy = CARD(name="Lightning Bolt XY", description="Deal quadruple die value damage, Apply 3 Blind", id="48-5-200-03-A4-00-630000", rarity=10)

lightningstorm = CARD(name="Lightning Storm", description="Deal 20 damage, Apply 2 Blind", id="49-0-120-01-20-00-620000", rarity=4)
lightningstormx = CARD(name="Lightning Storm x", description="Deal 20 damage, Apply 2 Blind", id="49-1-118-01-20-00-620000", rarity=10)
lightningstormxx = CARD(name="Lightning Storm X", description="Deal 24 damage, Apply 3 Blind", id="49-2-115-01-24-00-630000", rarity=10)
lightningstormy = CARD(name="Lightning Storm y", description="Deal 22 damage, Apply 3 Blind", id="49-3-120-01-22-00-634300", rarity=10)
lightningstormyy = CARD(name="Lightning Storm Y", description="Deal 26 damage, Apply 4 Blind", id="49-4-117-01-26-00-644300", rarity=10)
lightningstormxy = CARD(name="Lightning Storm XY", description="Deal 30 damage, Apply 5 Blind", id="49-5-112-01-30-00-650000", rarity=10)

maul = CARD(name="Maul", description="Deal damage equal to die value + 4", id="50-0-000-01-E4-00-000000", rarity=2)
maulx = CARD(name="Maul x", description="Deal damage equal to die value + 4", id="50-1-200-01-E4-00-000000", rarity=10)
maulxx = CARD(name="Maul X", description="Deal damage equal to die value + 5", id="50-2-200-01-E5-00-000000", rarity=10)
mauly = CARD(name="Maul y", description="Deal damage equal to die value + 5", id="50-3-000-01-E5-00-000000", rarity=10)
maulyy = CARD(name="Maul Y", description="Deal damage equal to die value + 8", id="50-4-000-01-E8-00-000000", rarity=10)
maulxy = CARD(name="Maul XY", description="Deal damage equal to die value + 8", id="50-5-200-01-E8-00-000000", rarity=10)

meteor = CARD(name="Meteor", description="Deal 15 damage", id="51-0-000-35-15-00-000000", rarity=4)
meteorx = CARD(name="Meteor x", description="Deal 16 damage", id="51-1-200-35-16-00-000000", rarity=10)
meteorxx = CARD(name="Meteor X", description="Deal 18 damage", id="51-2-200-34-18-00-000000", rarity=10)
meteory = CARD(name="Meteor y", description="Deal 18 damage, Apply 2 Bleed", id="51-3-000-36-18-00-520000", rarity=10)
meteoryy = CARD(name="Meteor Y", description="Deal 20 damage, Apply 3 Bleed", id="51-4-000-35-20-00-530000", rarity=10)
meteorxy = CARD(name="Meteor XY", description="Deal 20 damage, Apply 4 Bleed", id="51-5-200-34-20-00-540000", rarity=10)

mirrorhide = CARD(name="Mirror Hide", description="Remove all negative effects from self", id="52-0-000-35-00-00-Z00052", rarity=3)
mirrorhidex = CARD(name="Mirror Hide x", description="Remove all negative effects from self, Apply them to opponent", id="52-1-000-35-00-00-Z00053", rarity=10)
mirrorhidexx = CARD(name="Mirror Hide X", description="Remove all negative effects from self, Apply to opponent, Gain 2 Shield", id="52-2-000-34-00-00-Z00054", rarity=10)
mirrorhidey = CARD(name="Mirror Hide y", description="Double all negative effects on opponent", id="52-3-000-35-00-00-Z00055", rarity=10)
mirrorhideyy = CARD(name="Mirror Hide Y", description="Remove all negative effects from self, Double all negative effects on opponent", id="52-4-000-35-00-00-Z00056", rarity=10)
mirrorhidexy = CARD(name="Mirror Hide XY", description="Remove all negative effects from self, Double them and apply to opponent, Gain 5 Shield", id="52-5-000-34-00-00-Z00057", rarity=10)

necromancy = CARD(name="Necromancy", description="Deal 15 damage, Heal 3 HP", id="53-0-112-01-15-00-830000", rarity=4)
necromancyx = CARD(name="Necromancy x", description="Deal 15 damage, Heal 4 HP", id="53-1-111-01-15-00-840000", rarity=10)
necromancyxx = CARD(name="Necromancy X", description="Deal 16 damage, Heal 6 HP", id="53-2-110-01-16-00-860000", rarity=10)
necromancyy = CARD(name="Necromancy y", description="Deal 17 damage, Heal 3 HP", id="53-3-112-01-17-00-830000", rarity=10)
necromancyyy = CARD(name="Necromancy Y", description="Deal 18 damage, Heal 4 HP, Apply 1 Poison", id="53-4-112-01-18-00-841100", rarity=10)
necromancyxy = CARD(name="Necromancy XY", description="Deal 20 damage, Heal 8 HP, Apply 2 Poison", id="53-5-110-01-20-00-881200", rarity=10)

petrify = CARD(name="Petrify", description="Apply 2 Lock, Apply 1 Frozen", id="54-0-000-01-00-16-324100", rarity=3)
petrifyx = CARD(name="Petrify x", description="Apply 3 Lock, Apply 1 Frozen", id="54-1-000-01-00-16-334100", rarity=10)
petrifyxx = CARD(name="Petrify X", description="Apply 4 Lock, Apply 2 Frozen", id="54-2-000-01-00-35-344200", rarity=10)
petrifyy = CARD(name="Petrify y", description="Apply 2 Lock, Apply 2 Frozen", id="54-3-000-01-00-35-324200", rarity=10)
petrifyyyy = CARD(name="Petrify Y", description="Apply 3 Lock, Apply 3 Frozen", id="54-4-000-01-00-34-334300", rarity=10)
petrifyxy = CARD(name="Petrify XY", description="Apply 5 Lock, Apply 4 Frozen", id="54-5-000-01-00-34-354400", rarity=10)

phasestep = CARD(name="Phase Shift", description="Gain 4 Shield, Remove all negative effects from self", id="55-0-000-71-00-00-Z00058", rarity=3)
phasestepx = CARD(name="Phase Shift x", description="Gain 5 Shield, Remove all negative effects from self", id="55-1-000-71-00-00-Z00059", rarity=10)
phasestepxx = CARD(name="Phase Shift X", description="Gain 6 Shield, Remove all negative effects from self", id="55-2-000-71-00-00-Z00060", rarity=10)
phasestepy = CARD(name="Phase Shift y", description="Gain 4 Shield, Remove all negative effects from self, Heal 2 HP", id="55-3-000-71-00-00-Z00061", rarity=10)
phasestepyy = CARD(name="Phase Shift Y", description="Remove all negative effects from self, for every effect removed this way, gain 1/2 shield and 1/2 health, rounded down", id="55-4-000-71-00-00-Z00062", rarity=10)
phasestepxy = CARD(name="Phase Shift XY", description="Remove all negative effects from self, For every effect removed this way, gain an equal amount of shield and heal.", id="55-5-000-71-00-00-Z00063", rarity=10)

phoenixrising = CARD(name="Phoenix Rising", description="Heal 5 HP, Remove all negative effects from self, then apply 2 burn to self", id="56-0-000-71-00-00-Z00064", rarity=4)
phoenixrisingx = CARD(name="Phoenix Rising x", description="Heal 8 HP, Remove all negative effects from self, then apply 1 burn to self and opponent", id="56-1-000-71-00-00-Z00065", rarity=10)
phoenixrisingxx = CARD(name="Phoenix Rising X", description="Heal 10 HP, Remove all negative effects from self, apply 2 burn to opp", id="56-2-000-71-00-00-Z00066", rarity=10)
phoenixrisingy = CARD(name="Phoenix Rising y", description="Heal 6 HP, Remove all negative effects from self, Deal 5 damage, then apply 2 burn to self", id="56-3-000-71-00-00-Z00067", rarity=10)
phoenixrisingyy = CARD(name="Phoenix Rising Y", description="Heal 8 HP, Remove all negative effects from self, Deal 8 damage, then apply 1 burn to self and opponent", id="56-4-000-71-00-00-Z00068", rarity=10)
phoenixrisingxy = CARD(name="Phoenix Rising XY", description="Heal 10 HP, Remove all negative effects from self, Deal 8 damage, Apply 2 burn to opp", id="56-5-000-71-00-00-Z00069", rarity=10)

plaguebreath = CARD(name="Plague Breath", description="Apply Poison equal to half die value (rounded up)", id="57-0-000-02-00-00-1Y0000", rarity=2)
plaguebreathx = CARD(name="Plague Breath x", description="Apply Poison equal to die value", id="57-1-000-02-00-00-1X0000", rarity=10)
plaguebreathxx = CARD(name="Plague Breath X", description="Apply Poison equal to die value + 1", id="57-2-000-02-00-00-1A0000", rarity=10)
plaguebreathy = CARD(name="Plague Breath y", description="Apply Poison equal to half die value (rounded up)", id="57-3-000-01-00-00-1Y0000", rarity=10)
plaguebreathyy = CARD(name="Plague Breath Y", description="Apply Poison equal to die value", id="57-4-000-01-00-00-1X0000", rarity=10)
plaguebreathxy = CARD(name="Plague Breath XY", description="Apply Poison equal to die value + 2", id="57-5-000-01-00-00-1B0000", rarity=10)

pounce = CARD(name="Pounce", description="Deal 5 + die value damage", id="58-0-222-23-E5-00-000000", rarity=2)
pouncex = CARD(name="Pounce x", description="Deal 7 + die value damage", id="58-1-222-23-E7-00-000000", rarity=10)
pouncexx = CARD(name="Pounce X", description="Deal 9 + die value damage", id="58-2-200-23-E9-00-000000", rarity=10)
pouncey = CARD(name="Pounce y", description="Deal 6 + die value damage", id="58-3-222-24-E6-00-000000", rarity=10)
pounceyy = CARD(name="Pounce Y", description="Deal 8 + die value damage", id="58-4-200-25-E8-00-000000", rarity=10)
pouncexy = CARD(name="Pounce XY", description="Deal 10 + die value damage", id="58-5-200-01-EA-00-000000", rarity=10)

reflectingscales = CARD(name="Reflecting Scales", description="Deal 2 damage, Apply 1 Blind", id="59-0-000-01-02-00-610000", rarity=1)
reflectingscalesx = CARD(name="Reflecting Scales x", description="Deal 4 damage, Apply 2 Blind", id="59-1-000-01-04-00-620000", rarity=10)
reflectingscalesxx = CARD(name="Reflecting Scales X", description="Deal 6 damage, Apply 3 Blind, Gain 1 Shield", id="59-2-000-01-06-00-637100", rarity=10)
reflectingscalesy = CARD(name="Reflecting Scales y", description="Apply 2 Blind, Gain 2 Shield", id="59-3-000-01-00-00-627200", rarity=10)
reflectingscalesyy = CARD(name="Reflecting Scales Y", description="Apply 3 Blind, Gain 4 Shield, Remove 1 negative effect", id="59-4-000-01-00-00-Z00070", rarity=10)
reflectingscalesxy = CARD(name="Reflecting Scales XY", description="Deal 8 damage, Apply 4 Blind, Gain 5 Shield, Remove all negative effects", id="59-5-000-01-08-00-Z00071", rarity=10)

roar = CARD(name="Roar", description="Apply 1 Lock", id="60-0-000-71-00-00-310000", rarity=1)
roarx = CARD(name="Roar x", description="Apply 2 Lock", id="60-1-000-71-00-00-320000", rarity=10)
roarxx = CARD(name="Roar X", description="Apply 3 Lock, Apply 1 Blind", id="60-2-000-71-00-00-336100", rarity=10)
roary = CARD(name="Roar y", description="Apply 1 Lock, Apply 1 Blind", id="60-3-000-71-00-00-316100", rarity=10)
roaryy = CARD(name="Roar Y", description="Apply 2 Lock, Apply 2 Blind", id="60-4-000-71-00-00-326200", rarity=10)
roarxy = CARD(name="Roar XY", description="Apply 4 Lock, Apply 3 Blind", id="60-5-000-71-00-00-346300", rarity=10)

rupture = CARD(name="Rupture", description="Deal 8 damage, Apply 1 Bleed", id="61-0-110-01-08-00-510000", rarity=2)
rupturex = CARD(name="Rupture x", description="Deal 8 damage, Apply 2 Bleed", id="61-1-109-01-08-00-520000", rarity=10)
rupturexx = CARD(name="Rupture X", description="Deal 10 damage, Apply 3 Bleed", id="61-2-107-01-10-00-530000", rarity=10)
rupturey = CARD(name="Rupture y", description="Deal 10 damage, Apply 1 Bleed", id="61-3-110-01-10-00-510000", rarity=10)
ruptureyy = CARD(name="Rupture Y", description="Deal 12 damage, Apply 2 Bleed", id="61-4-109-01-12-00-520000", rarity=10)
rupturexy = CARD(name="Rupture XY", description="Deal 14 damage, Apply 3 Bleed", id="61-5-107-01-14-00-530000", rarity=10)

rustydagger = CARD(name="Rusty Dagger", description="Deal 2 damage", id="62-0-000-03-02-00-000000", rarity=1)
rustydaggerx = CARD(name="Rusty Dagger x", description="Deal 3 damage, Apply 1 Poison", id="62-1-000-03-03-00-110000", rarity=10)
rustydaggerxx = CARD(name="Rusty Dagger X", description="Deal 4 damage, Apply 2 Poison", id="62-2-000-03-04-00-120000", rarity=10)
rustydaggery = CARD(name="Rusty Dagger y", description="Deal 3 damage, Apply 1 Bleed", id="62-3-000-03-03-00-510000", rarity=10)
rustydaggeryy = CARD(name="Rusty Dagger Y", description="Deal 4 damage, Apply 2 Bleed", id="62-4-000-03-04-00-520000", rarity=10)
rustydaggerxy = CARD(name="Rusty Dagger XY", description="Deal 6 damage, Apply 3 Poison, Apply 2 Bleed", id="62-5-000-03-06-00-135200", rarity=10)

screech = CARD(name="Screech", description="Apply 2 Blind, Apply 1 Lock", id="63-0-000-71-00-00-623100", rarity=2)
screechx = CARD(name="Screech x", description="Apply 3 Blind, Apply 1 Lock", id="63-1-102-71-00-00-633100", rarity=10)
screechxx = CARD(name="Screech X", description="Apply 4 Blind, Apply 2 Lock", id="63-2-103-71-00-00-643200", rarity=10)
screechy = CARD(name="Screech y", description="Apply 3 Blind, Apply 2 Lock", id="63-3-000-71-00-00-633200", rarity=10)
screechyy = CARD(name="Screech Y", description="Apply 3 Blind, Apply 3 Lock, Deal 3 damage", id="63-4-102-71-03-00-633300", rarity=10)
screechxy = CARD(name="Screech XY", description="Apply 5 Blind, Apply 4 Lock, Deal 5 damage", id="63-5-103-71-05-00-654400", rarity=10)

shield = CARD(name="Shield", description="Gain Shield equal to half the die value", id="64-0-000-02-00-00-7Y0000", rarity=1)
shieldx = CARD(name="Shield x", description="Gain shield equal to the die value", id="64-1-000-02-00-00-7X0000", rarity=10)
shieldxx = CARD(name="Shield X", description="Gain Shield equal to die value + 2", id="64-2-000-01-00-00-7B0000", rarity=10)
shieldy = CARD(name="Shield y", description="Gain Shield equal to half the die value", id="64-3-200-02-00-00-7Y0000", rarity=10)
shieldyy = CARD(name="Shield Y", description="Gain Shield equal to die value", id="64-4-200-02-00-00-7X0000", rarity=10)
shieldxy = CARD(name="Shield XY", description="Gain Shield equal to die value + 4", id="64-5-200-01-00-00-7D0000", rarity=10)

shortbow = CARD(name="Shortbow", description="Deal double die value damage", id="65-0-103-01-A2-00-000000", rarity=1)
shortbowx = CARD(name="Shortbow x", description="Deal double die value damage", id="65-1-000-03-A2-00-000000", rarity=10)
shortbowxx = CARD(name="Shortbow X", description="Deal triple die value damage", id="65-2-000-03-A3-00-000000", rarity=10)
shortbowy = CARD(name="Shortbow y", description="Deal double die value damage, Apply 1 Bleed", id="65-3-000-02-A2-00-510000", rarity=10)
shortbowyy = CARD(name="Shortbow Y", description="Deal double die value damage, Apply 2 Bleed", id="65-4-000-02-A2-00-520000", rarity=10)
shortbowxy = CARD(name="Shortbow XY", description="Deal triple die value damage, Apply 2 Bleed", id="65-5-000-01-A3-00-520000", rarity=10)

snipe = CARD(name="Snipe", description="Deal 8 damage, Apply 1 Bleed", id="66-0-115-01-08-00-510000", rarity=2)
snipex = CARD(name="Snipe x", description="Deal 12 damage, Apply 1 Bleed", id="66-1-115-01-12-00-510000", rarity=10)
snipexx = CARD(name="Snipe X", description="Deal 15 damage, Apply 3 Bleed", id="66-2-114-01-15-00-530000", rarity=10)
snipey = CARD(name="Snipe y", description="Deal 10 damage, Apply 1 Bleed", id="66-3-113-01-10-00-510000", rarity=10)
snipeyy = CARD(name="Snipe Y", description="Deal 12 damage, Apply 2 Bleed", id="66-4-110-01-12-00-520000", rarity=10)
snipexy = CARD(name="Snipe XY", description="Deal 22 damage, Apply 3 Bleed", id="66-5-118-01-22-00-530000", rarity=10)

soulrend = CARD(name="Soul Rend", description="Deal 8 damage, Apply 1 Bleed", id="67-0-200-34-08-00-510000", rarity=3)
soulrendx = CARD(name="Soul Rend x", description="Deal 9 damage, Apply 1 Bleed", id="67-1-200-33-09-00-510000", rarity=10)
soulrendxx = CARD(name="Soul Rend X", description="Deal 10 damage, Apply 2 Bleed", id="67-2-200-32-10-00-520000", rarity=10)
soulrendy = CARD(name="Soul Rend y", description="Deal 10 damage, Apply 2 Bleed", id="67-3-200-34-10-00-520000", rarity=10)
soulrendyy = CARD(name="Soul Rend Y", description="Deal 12 damage, Apply 3 Bleed", id="67-4-200-34-12-00-530000", rarity=10)
soulrendxy = CARD(name="Soul Rend XY", description="Deal 14 damage, Apply 3 Bleed", id="67-5-200-32-14-00-530000", rarity=10)

spectralstrike = CARD(name="Spectral Strike", description="Deal damage equal to die value, On 5-6: Apply 1 Bleed", id="68-0-000-01-E0-35-510000", rarity=2)
spectralstrikex = CARD(name="Spectral Strike x", description="Deal damage equal to die value + 1, On 5-6: Apply 1 Bleed", id="68-1-000-01-E1-35-510000", rarity=10)
spectralstrikexx = CARD(name="Spectral Strike X", description="Deal damage equal to die value + 2, On 4-6: Apply 2 Bleed", id="68-2-000-01-E2-34-520000", rarity=10)
spectralstrikey = CARD(name="Spectral Strike y", description="Deal damage equal to die value, On 4-6: Apply 2 Bleed", id="68-3-000-01-E0-34-520000", rarity=10)
spectralstrikeyy = CARD(name="Spectral Strike Y", description="Deal damage equal to die value + 1, On 3-6: Apply 3 Bleed", id="68-4-000-01-E1-33-530000", rarity=10)
spectralstrikexy = CARD(name="Spectral Strike XY", description="Deal damage equal to die value + 3, On 3-6: Apply 4 Bleed", id="68-5-000-01-E3-33-540000", rarity=10)

splinter = CARD(name="Splinter", description="Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)", id="69-0-000-01-00-00-Z00072", rarity=2)
splinterx = CARD(name="Splinter x", description="Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)", id="69-1-000-01-00-00-Z00073", rarity=10)
splinterxx = CARD(name="Splinter X", description="Sacrifice 1 HP, Create 2 dice with half the input die value (rounded down)", id="69-2-200-32-00-00-Z00074", rarity=10)
splintery = CARD(name="Splinter y", description="Sacrifice 2 HP, Create 2 dice with half the input die value (rounded up)", id="69-3-000-01-00-00-Z00075", rarity=10)
splinteryy = CARD(name="Splinter Y", description="Sacrifice 2 HP, Create 3 dice with half the input die value (rounded up)", id="69-4-000-32-00-00-Z00076", rarity=10)
splinterxy = CARD(name="Splinter XY", description="Sacrifice 1 HP, Create 3 dice with half the input die value (rounded up)", id="69-5-200-32-00-00-Z00077", rarity=10)

stonehide = CARD(name="Stone Hide", description="Gain Shield equal to die value + 2", id="70-0-200-02-E2-00-7B0000", rarity=3)
stonehidex = CARD(name="Stone Hide x", description="Gain Shield equal to die value + 3", id="70-1-200-02-E3-00-7C0000", rarity=10)
stonehidexx = CARD(name="Stone Hide X", description="Gain Shield equal to die value + 4, Remove 1 negative effect", id="70-2-200-02-E4-00-Z00078", rarity=10)
stonehidey = CARD(name="Stone Hide y", description="Gain Shield equal to die value + 2, Heal 1 HP", id="70-3-200-02-E2-00-7B8100", rarity=10)
stonehideyy = CARD(name="Stone Hide Y", description="Gain Shield equal to die value + 3, Heal 2 HP, Apply 1 Lock to opponent", id="70-4-200-02-E3-00-7C8231", rarity=10)
stonehidexy = CARD(name="Stone Hide XY", description="Gain Shield equal to die value + 6, Heal 2 HP, Remove all negative effects", id="70-5-200-02-E6-00-Z00079", rarity=10)

sunstrike = CARD(name="Sunstrike", description="Deal 4 damage, Apply 1 Blind", id="71-0-104-01-04-00-610000", rarity=2)
sunstrikex = CARD(name="Sunstrike x", description="Deal 6 damage, Apply 1 Blind", id="71-1-104-01-06-00-610000", rarity=10)
sunstrikexx = CARD(name="Sunstrike X", description="Deal 8 damage, Apply 2 Blind", id="71-2-104-01-08-00-620000", rarity=10)
sunstrikey = CARD(name="Sunstrike y", description="Deal 4 damage, Apply 2 Blind", id="71-3-103-01-04-00-620000", rarity=10)
sunstrikeyy = CARD(name="Sunstrike Y", description="Deal 5 damage, Apply 3 Blind", id="71-4-102-01-05-00-630000", rarity=10)
sunstrikexy = CARD(name="Sunstrike XY", description="Deal 8 damage, Apply 3 Blind", id="71-5-102-01-08-00-630000", rarity=10)

swipe = CARD(name="Swipe", description="Deal 3 damage, Heal 1 HP", id="72-0-105-01-03-00-810000", rarity=1)
swipex = CARD(name="Swipe x", description="Deal 3 damage + 1 for each use this round, Heal 1 HP", id="72-1-200-01-00-00-Z00080", rarity=10)
swipexx = CARD(name="Swipe X", description="Deal 2 damage + 2 for each use this round, Heal 1 HP", id="72-2-200-01-00-00-Z00081", rarity=10)
swipey = CARD(name="Swipe y", description="Deal 5 damage, Heal 2 HP", id="72-3-105-01-05-00-820000", rarity=10)
swipeyy = CARD(name="Swipe Y", description="Deal 7 damage, Heal 3 HP", id="72-4-103-01-07-00-830000", rarity=10)
swipexy = CARD(name="Swipe XY", description="Deal 3 damage + 3 for each use this round, Heal 3 HP", id="72-5-200-01-00-00-Z00082", rarity=10)

talonstrike = CARD(name="Talon Strike", description="Deal damage equal to die value + 3, On 6: Apply 1 Bleed", id="73-0-200-01-E3-16-510000", rarity=2)
talonstrikex = CARD(name="Talon Strike x", description="Deal damage equal to die value + 4, On 6: Apply 1 Bleed", id="73-1-200-01-E4-16-510000", rarity=10)
talonstrikexx = CARD(name="Talon Strike X", description="Deal damage equal to die value + 5, On 5-6: Apply 2 Bleed", id="73-2-200-01-E5-35-520000", rarity=10)
talonstrikey = CARD(name="Talon Strike y", description="Deal damage equal to die value + 3, On 5-6: Apply 2 Bleed", id="73-3-200-01-E3-35-520000", rarity=10)
talonstrikeyy = CARD(name="Talon Strike Y", description="Deal damage equal to die value + 4, On 4-6: Apply 3 Bleed", id="73-4-200-01-E4-34-530000", rarity=10)
talonstrikexy = CARD(name="Talon Strike XY", description="Deal damage equal to die value + 7, On 4-6: Apply 4 Bleed", id="73-5-200-01-E7-34-540000", rarity=10)

thunderclap = CARD(name="Thunderclap", description="Deal 18 damage, Apply 2 Blind", id="74-0-125-01-18-00-620000", rarity=4)
thunderclapx = CARD(name="Thunderclap x", description="Deal 18 damage, Apply 3 Blind", id="74-1-123-01-18-00-630000", rarity=10)
thunderclapxx = CARD(name="Thunderclap X", description="Deal 22 damage, Apply 4 Blind", id="74-2-120-01-22-00-640000", rarity=10)
thunderclapy = CARD(name="Thunderclap y", description="Deal 20 damage, Apply 4 Blind, Apply 1 Lock", id="74-3-125-01-20-00-644310", rarity=10)
thunderclapyy = CARD(name="Thunderclap Y", description="Deal 25 damage, Apply 4 Blind, Apply 1 Lock", id="74-4-122-01-25-00-644310", rarity=10)
thunderclapxy = CARD(name="Thunderclap XY", description="Deal 28 damage, Apply 4 Blind, Apply 2 Lock", id="74-5-118-01-28-00-644320", rarity=10)

torture = CARD(name="Torture", description="Deal 15 damage, Apply 2 Bleed, Apply 2 Lock", id="75-0-120-01-15-00-525320", rarity=4)
torturex = CARD(name="Torture x", description="Deal 15 damage, Apply 2 Bleed, Apply 2 Lock", id="75-1-118-01-15-00-525320", rarity=10)
torturexx = CARD(name="Torture X", description="Deal 18 damage, Apply 3 Bleed, Apply 3 Lock, Apply 1 Poison", id="75-2-115-01-18-00-535331", rarity=10)
torturey = CARD(name="Torture y", description="Deal 18 damage, Apply 3 Bleed, Apply 3 Lock", id="75-3-120-01-18-00-535330", rarity=10)
tortureyy = CARD(name="Torture Y", description="Deal 20 damage, Apply 4 Bleed, Apply 4 Lock", id="75-4-117-01-20-00-545440", rarity=10)
torturexy = CARD(name="Torture XY", description="Deal 25 damage, Apply 5 Bleed, Apply 5 Lock, Apply 2 Poison, Apply 2 Blind", id="75-5-112-01-25-00-555542", rarity=10)

totem = CARD(name="Totem", description="Gain 5 Shield, Heal 2 HP", id="76-0-000-72-00-00-758200", rarity=2)
totemx = CARD(name="Totem x", description="Gain 6 Shield, Heal 2 HP", id="76-1-000-72-00-00-768200", rarity=10)
totemxx = CARD(name="Totem X", description="Gain 8 Shield, Heal 4 HP", id="76-2-000-72-00-00-788400", rarity=10)
totemy = CARD(name="Totem y", description="Gain 5 Shield, Heal 3 HP", id="76-3-000-72-00-00-758300", rarity=10)
totemyy = CARD(name="Totem Y", description="Gain 7 Shield, Heal 4 HP, Remove 1 negative effect", id="76-4-000-72-00-00-Z00083", rarity=10)
totemxy = CARD(name="Totem XY", description="Gain 8 Shield, Heal 5 HP, Remove all negative effects", id="76-5-000-72-00-00-Z00084", rarity=10)

trample = CARD(name="Trample", description="Deal damage equal to die value, On 6: Apply 1 Lock", id="77-0-000-01-E0-16-310000", rarity=1)
tramplex = CARD(name="Trample x", description="Deal damage equal to die value + 1, On 6: Apply 1 Lock", id="77-1-000-01-E1-16-310000", rarity=10)
tramplexx = CARD(name="Trample X", description="Deal damage equal to die value + 2, On 5-6: Apply 2 Lock", id="77-2-000-01-E2-35-320000", rarity=10)
trampley = CARD(name="Trample y", description="Deal damage equal to die value, On 5-6: Apply 1 Lock", id="77-3-000-01-E0-35-310000", rarity=10)
trampleyy = CARD(name="Trample Y", description="Deal damage equal to die value + 1, On 4-6: Apply 2 Lock", id="77-4-000-01-E1-34-320000", rarity=10)
tramplexy = CARD(name="Trample XY", description="Deal damage equal to die value + 3, On 4-6: Apply 2 Lock", id="77-5-000-01-E3-34-320000", rarity=10)

tremor = CARD(name="Tremor", description="Deal damage equal to die value + 1", id="78-0-000-01-E1-00-000000", rarity=1)
tremorx = CARD(name="Tremor x", description="Deal damage equal to die value + 1", id="78-1-200-01-E1-00-000000", rarity=10)
tremorxx = CARD(name="Tremor X", description="Deal damage equal to die value + 2", id="78-2-200-01-E2-00-000000", rarity=10)
tremory = CARD(name="Tremor y", description="Deal damage equal to die value + 2", id="78-3-000-01-E2-00-000000", rarity=10)
tremoryy = CARD(name="Tremor Y", description="Deal damage equal to die value + 3", id="78-4-000-01-E3-00-000000", rarity=10)
tremorxy = CARD(name="Tremor XY", description="Deal damage equal to die value + 3", id="78-5-200-01-E3-00-000000", rarity=10)

whipcrack = CARD(name="Whip Crack", description="Deal damage equal to die value + 5, Apply 1 Burn", id="79-0-000-01-E5-00-210000", rarity=3)
whipcrackx = CARD(name="Whip Crack x", description="Deal damage equal to die value + 6, Apply 1 Burn", id="79-1-000-01-E6-00-210000", rarity=10)
whipcrackxx = CARD(name="Whip Crack X", description="Deal damage equal to die value + 7, Apply 2 Burn", id="79-2-000-01-E7-00-220000", rarity=10)
whipcracky = CARD(name="Whip Crack y", description="Deal damage equal to die value + 5, Apply 2 Burn", id="79-3-000-01-E5-00-220000", rarity=10)
whipcrackyy = CARD(name="Whip Crack Y", description="Deal damage equal to die value + 6, Apply 3 Burn", id="79-4-000-01-E6-00-230000", rarity=10)
whipcrackxy = CARD(name="Whip Crack XY", description="Deal damage equal to die value + 9, Apply 3 Burn", id="79-5-000-01-E9-00-230000", rarity=10)

windslash = CARD(name="Wind Slash", description="Deal damage equal to die value + 4, On 6: Apply 1 Bleed", id="80-0-200-01-E4-16-510000", rarity=2)
windslashx = CARD(name="Wind Slash x", description="Deal damage equal to die value + 5, On 6: Apply 1 Bleed", id="80-1-200-01-E5-16-510000", rarity=10)
windslashxx = CARD(name="Wind Slash X", description="Deal damage equal to die value + 6, On 5-6: Apply 1 Bleed", id="80-2-200-01-E6-35-510000", rarity=10)
windslashy = CARD(name="Wind Slash y", description="Deal damage equal to die value + 4, On 5-6: Apply 1 Bleed", id="80-3-200-01-E4-35-510000", rarity=10)
windslashyy = CARD(name="Wind Slash Y", description="Deal damage equal to die value + 5, On 4-6: Apply 2 Bleed", id="80-4-200-01-E5-34-520000", rarity=10)
windslashxy = CARD(name="Wind Slash XY", description="Deal damage equal to die value + 8, On 4-6: Apply 2 Bleed", id="80-5-200-01-E8-34-520000", rarity=10)

# Basic white boy cards
club = CARD(name='Primitive Club', description='Deal 2 damage', id='00-0-200-01-02-00-000000', rarity=10)

# Thessa's Starter Cards - Basic equipment given to new adventurers
woodensword = CARD(name='Wooden Sword', description='Deal 3 damage', id='81-0-200-01-03-00-000000', rarity=1)
slingshot = CARD(name='Slingshot', description='Deal damage equal to die value', id='82-0-200-01-E0-00-000000', rarity=1)
smallstone = CARD(name='Small Stone', description='Deal 2 damage', id='83-0-200-01-02-00-000000', rarity=1)
makeshiftshield = CARD(name='Makeshift Shield', description='Gain 2 Shield', id='84-0-200-01-00-00-720000', rarity=1)
bandage = CARD(name='Bandage', description='Heal 2 HP', id='85-0-200-01-00-00-820000', rarity=1)
sharpenedstick = CARD(name='Sharpened Stick', description='Deal 3 damage', id='86-0-200-01-03-00-000000', rarity=1)




class ENEMY:
    def __init__(self, name, intro, dice, hp, biome, biome_tier, cards=[]):
        self.name = name
        self.intro = intro
        self.intro = intro
        self.dice = dice
        self.hp = hp
        self.biome = biome
        self.biome_tier = biome_tier
        self.cards = cards

wolf = ENEMY(name='Wolf', intro=None, dice=2, hp=10, biome=1, biome_tier=1, cards=[bite, howl])
locust = ENEMY(name='Giant Locust', intro=None, dice=2, hp=12, biome=1, biome_tier=1, cards=[swipe, swipe])
naukin_outcast = ENEMY(name='Naukin Outcast', intro=None, dice=2, hp=10, biome=1, biome_tier=1, cards=[jab, rustydagger])

dire_wolves = ENEMY(name='Dire Wolves', intro=None, dice=3, hp=18, biome=1, biome_tier=2, cards=[bitex, bitey])
prowl_dellinid = ENEMY(name='Prowling Dellinid', intro=None, dice=3, hp=16, biome=1, biome_tier=2, cards=[pounce, swipex])
juv_auroc = ENEMY(name='Juvenile Auroc', intro=None, dice=3, hp=20, biome=1, biome_tier=2, cards=[fortify, reflectingscales, chomp])

bov_bandit = ENEMY(name='Bovari Bandit', intro=None, hp=30, dice=3, biome=1, biome_tier=3, cards=[shortbowx, daggerx, hypeup])
roam_gall = ENEMY(name='Roaming Gallox', intro=None, dice=4, hp=30, biome=1, biome_tier=3, cards=[charge, trample, gore])
plainsdrake = ENEMY(name='Lone Plainsdrake', intro=None, hp=30, dice=4, biome=1, biome_tier=3, cards=[reflectingscalesx, reflectingscalesy, mirrorhide, chompx])

blue_dell = ENEMY(name='Blue Dellinid', intro=None, hp=12, dice=2, biome=2, biome_tier=1, cards=[pounce, swipex])
khinari_exile = ENEMY(name='Khinari Exile', intro=None, hp=14, dice=2, biome=2, biome_tier=1, cards=[shortbow, frosteddagger])
territorial_whitespike = ENEMY(name='Territorial Whitespike', intro=None, hp=16, dice=2, biome=2, biome_tier=1, cards=[gore, bellow])

khinari_raider = ENEMY(name='Khinari Raider', intro=None, hp=20, dice=3, biome=2, biome_tier=2, cards=[frostedspear, frosteddaggerx, icemagic])
tundra_boneguard = ENEMY(name='Tundra Boneguard', intro=None, hp=24, dice=3, biome=2, biome_tier=2, cards=[splinter, shield, bash])
alpha_whitespike = ENEMY(name='Alpha Whitespike', intro=None, hp=22, dice=3, biome=2, biome_tier=2, cards=[gorex, bellowy, charge, trample])

veteran_boneguard = ENEMY(name='Veteran Boneguard', intro=None, hp=30, dice=4, biome=2, biome_tier=3, cards=[splinterx, shieldx, bashx, frostedspearx])
khinari_hunting_party = ENEMY(name='Khinari Hunting Party', intro=None, hp=30, dice=4, biome=2, biome_tier=3, cards=[splintery, fortifyx, icemagicy, control, frostedspearx])
hungry_frost_wyrm = ENEMY(name='Hungry Frost Wyrm', intro=None, hp=28, dice=3, biome=2, biome_tier=3, cards=[bitexx, biteyy, bellowy])

naukin_scouts = ENEMY(name='Naukin Scouts', intro=None, hp=16, dice=3, biome=3, biome_tier=1, cards=[jabx, jaby, fortify])
skittari_hunters = ENEMY(name='Skittari Hunters', intro=None, hp=18, dice=3, biome=3, biome_tier=1, cards=[snipe, rustydaggerx])
reclaimed_boneguard = ENEMY(name='Reclaimed Boneguard', intro=None, hp=18, dice=3, biome=3, biome_tier=1, cards=[splinter, shield, bash])

dire_bear = ENEMY(name='Dire Bear', intro=None, hp=28, dice=4, biome=3, biome_tier=2, cards=[swipey, bitey, roar])
khinari_bladedancer = ENEMY(name='Khinari Bladedancer', intro=None, hp=22, dice=4, biome=3, biome_tier=2, cards=[splintery, snipex, jaby])
naukin_sunstriker = ENEMY(name='Naukin Sunstriker', intro=None, hp=20, dice=4, biome=3, biome_tier=2, cards=[daggery, sunstrike, mirrorhidey, control])

verdant_shepherd = ENEMY(name='Verdant Shepherd', intro=None, hp=40, dice=4, biome=3, biome_tier=3, cards=[maulxx, bellowx, jadespear, splinteryy])
barkskin_colossus = ENEMY(name='Barkskin Colossus', intro=None, hp=50, dice=4, biome=3, biome_tier=3, cards=[splinterxx, swipexx, chargey])
emerald_lich = ENEMY(name='Emerald Lich', intro=None, hp=35, dice=5, biome=3, biome_tier=3, cards=[necromancy, afflict, shieldxx, lifedrainx])

brass_golem = ENEMY(name='Brass Golem', intro=None, hp=24, dice=3, biome=4, biome_tier=1, cards=[bashy, shieldy, fortify])
skittari_looters = ENEMY(name='Skittari Looters', intro=None, hp=22, dice=3, biome=4, biome_tier=1, cards=[daggerx, shortbowx, control])
bloated_zombie = ENEMY(name='Bloated Zombie', intro=None, hp=26, dice=3, biome=4, biome_tier=1, cards=[bitex, rupture, lifedrain])

iron_bulwark = ENEMY(name='Iron Bulwark', intro=None, hp=40, dice=4, biome=4, biome_tier=2, cards=[bashxx, shieldyy, fortifyxx])
stone_drake = ENEMY(name='Stone Drake', intro=None, hp=38, dice=4, biome=4, biome_tier=2, cards=[chompy, reflectingscalesx, petrify])
lost_myrrim = ENEMY(name='Lost Myrrim', intro=None, hp=36, dice=4, biome=4, biome_tier=2, cards=[spectralstrike, phasestep, hauntingwail])

fell_lich = ENEMY(name='Fell Lich', intro=None, hp=60, dice=5, biome=4, biome_tier=3, cards=[necromancyxx, afflictxx, lifedrainxx, soulrend])
blighted_auroc = ENEMY(name='Blighted Auroc', intro=None, hp=65, dice=4, biome=4, biome_tier=3, cards=[gorexx, chompxx, plaguebreath, chargexx])
khinari_subjugator = ENEMY(name='Khinari Subjugator', intro=None, hp=62, dice=5, biome=4, biome_tier=3, cards=[snipexx, frostedspearxx, dominate, splinterxx])

steppe_whitespike = ENEMY(name='Steppe Whitespike', intro=None, hp=28, dice=3, biome=5, biome_tier=1, cards=[gorey, bellowxx, trample])
caghoul_shaman = ENEMY(name='Caghoul Shaman', intro=None, hp=26, dice=4, biome=5, biome_tier=1, cards=[lightningbolt, totem, jabxx])
naukin_outrider = ENEMY(name='Naukin Outrider', intro=None, hp=24, dice=4, biome=5, biome_tier=1, cards=[shortbowxx, daggeryy, evade])

hill_giant = ENEMY(name='Hill Giant', intro=None, hp=48, dice=4, biome=5, biome_tier=2, cards=[maulyy, bouldertoss, earthquake])
black_roc = ENEMY(name='Black Roc', intro=None, hp=45, dice=4, biome=5, biome_tier=2, cards=[divebomb, talonstrike, screech])
whitespike_patriarch = ENEMY(name='Whitespike Patriarch', intro=None, hp=50, dice=4, biome=5, biome_tier=2, cards=[goreyy, bellowyy, chargexx, tramplexx])

thunder_giant = ENEMY(name='Thunder Giant', intro=None, hp=85, dice=5, biome=5, biome_tier=3, cards=[maulxy, thunderclap, bouldertossx, fortifyyy])
quakewyrm = ENEMY(name='Quakewyrm', intro=None, hp=83, dice=5, biome=5, biome_tier=3, cards=[chompxy, tremor, stonehide, earthshatter])
caghoul_skyshaker = ENEMY(name='Caghoul Skyshaker', intro=None, hp=80, dice=5, biome=5, biome_tier=3, cards=[lightningstorm, chainlightning, totemxx, windslash])

condemned = ENEMY(name='Condemned', intro=None, hp=38, dice=4, biome=6, biome_tier=1, cards=[flail, chains, desperation])
bovari_thrall = ENEMY(name='Bovari Thrall', intro=None, hp=40, dice=4, biome=6, biome_tier=1, cards=[gorexy, bloodpact, flamestrike])
hatebound_imp = ENEMY(name='Hatebound Imp', intro=None, hp=36, dice=4, biome=6, biome_tier=1, cards=[clawswipe, curse, immolate])

blooded_khinari = ENEMY(name='Blooded Khinari', intro=None, hp=62, dice=5, biome=6, biome_tier=2, cards=[snipeyy, frostedspearYy, bloodritual, splinteryy])
hatebound_priest = ENEMY(name='Hatebound Priest', intro=None, hp=60, dice=5, biome=6, biome_tier=2, cards=[darkblessing, afflictyy, flameburst, lifedrainyy])
condemned_taskmaster = ENEMY(name='Condemned Taskmaster', intro=None, hp=64, dice=4, biome=6, biome_tier=2, cards=[whipcrack, chainsxx, torture, bashyy])

pit_lord = ENEMY(name='Pit Lord', intro=None, hp=115, dice=5, biome=6, biome_tier=3, cards=[annihilation, condemn, hellfire, darkaegis])
blood_judge = ENEMY(name='Blood Judge', intro=None, hp=112, dice=5, biome=6, biome_tier=3, cards=[execution, bloodprice, judgement, lifedrainxy])
prophet_of_fire = ENEMY(name='Prophet of Fire', intro=None, hp=110, dice=6, biome=6, biome_tier=3, cards=[apocalypse, meteor, cleansingfire, phoenixrising, flamewall])


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
                typingPrint(f"Invalid choice. Please enter one of: {valid_options}")
        except ValueError:
            typingPrint("Invalid input. Please enter a number.")
    
    return choice

rolls = []

def rolldice(x):
    for i in range(x):
        y = random.randint(1, 6)
        typingPrint(Style.BRIGHT + Fore.BLACK + f"{y}" + Style.RESET_ALL)
        rolls.append(y)

typingPrint("Welcome to LOADED BONES.")

typingPrint("In Loaded Bones, you will use your magical dice to activate spellcards to ensure victory on your adventures. Try each class, refine your strategy, and triumph!")

charname = input("What is your name?\n\t>")

typingPrint("Choose your character...")
typingPrint(Style.BRIGHT + Fore.CYAN + "F E N C E R" + Style.RESET_ALL + "\nOnce per turn, may reroll a die.", delay=0) #on upgrade, can be used more times per turn
typingPrint(Style.BRIGHT + Fore.RED + "K N I G H T" + Style.RESET_ALL + "\nRoll dice individually. If your limit is exceeded, your turn immediately ends. If you match your limit exactly, you get to choose from 3 powerful boons.", delay=0) #limit starts at 9. on upgrade, the limit increases by 6.
typingPrint(Style.BRIGHT + Fore.YELLOW + "C L E R I C" + Style.RESET_ALL + "\nWhen rolling doubles, you heal by that much.", delay=0) #on level 2 and above, excess healing converts to a temporary shield.
typingPrint(Style.BRIGHT + Fore.BLUE + "W A R L O C K" + Style.RESET_ALL + "\nWhen applying status effects, apply that many plus one.", delay=0) #on upgrade, add an extra each time.
typingPrint(Style.BRIGHT + Fore.GREEN + "D R U I D" + Style.RESET_ALL + "\nOnce per turn, you may \"plant\" a die. Next turn, it will \"bloom\" with 2 dice of the same value that don't count towards your dice total.", delay=0) #On even levels, each planted die will bloom with +x (at level two, plantin a 1 will produce two 2's. At level 4, planting a 1 will produce 3's). On odd levels, planted seeds produce 1 extra die when 'blooming' (level 3 means each planted die produces 3 dice when they bloom, level 5 means 4, etc).
typingPrint(Style.BRIGHT + Fore.MAGENTA + "R O G U E" + Style.RESET_ALL + "\nYou select a lucky number at the start of each combat. Whenever that number is rolled, you deal 2 damage to your enemy.", delay=0) #on upgrade, add 2 per level. this triggers even with rerolls or dice splitting from other abilities.

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

typingPrint(f"And so begins the tale of {char_style + title + " " + charname.capitalize()}, the {charclass.lower()+Style.RESET_ALL}.")

charname = char_style + charname + Style.RESET_ALL

difficulty = get_valid_input("Choose your difficulty:\n1) Easy\n2)Normal\n3)Punishing\n\t>", [1,2,3])

speed = get_valid_input(
    "Choose your text speed:\n"
    "1) Instant (no delays)\n"
    "2) Fast (half speed)\n"
    "3) Normal (default)\n"
    "4) Slow (double speed)\n"
    "\t>",
    [1, 2, 3, 4]
)
set_speed_multiplier(speed)

if clas == 1:
    max_player_health = 40
elif clas == 2:
    max_player_health = 42
elif clas == 3:
    max_player_health = 42
elif clas == 4:
    max_player_health = 38
elif clas == 5:
    max_player_health = 40
elif clas == 6:
    max_player_health = 38

# Track unlocked stages (1 = Plains is unlocked by default)
unlocked_stages = 1
stage_names = {1: "Plains", 2: "Caves", 3: "Mountains"}

currenthp = max_player_health

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


damage = 0

# player stats
poison_counter = 0
dice = []
cards_in_hand = []
deck = []
hand_limit = 2
dice_limit = 2
burn_counter = 0
lock_counter = 0
freeze_counter = 0
bleed_counter = 0
blind_counter = 0
shield_counter = 0

#trigger when taking damage
# if shield_counter > 0:
#     if damage > shield:
#         damage = damage - shield_counter
#         shield_counter = 0
#     elif damage < shield_counter:
#         shield_counter = shield_counter - damage
#         damage = 0
#     elif damage == shield_counter:
#         shield_counter = 0
#         damage = 0

# triggers at start of turn
# if poison_counter > 0:
#     health -= poison_counter
#     poison_counter -= 1


# triggers when card is played
# if burn_counter > 0:
#     health = health - (burn_counter*2)
#     burn_counter-=1


# triggers when dice are rolled, before freeze
# if lock_counter > 0:
#     while lock_counter > 0 and dice > 0:
#         dice.pop(0)
#         lock_counter -= 1


#triggers right after lock
# if freeze_counter > 0:
#     for i in range(len(dice)):
#         if dice[i] > 1 and freeze_counter > 0:
#             dice[i] = 1
#             freeze_counter -= 1


# I guess this can trigger after freeze
# Find a way to have it replace the die when it's being displayed with a ? without replacing it's value
# if blind_counter > 0:
#     hidden_indices = []
#     if blind_counter > 0 and dice:
#         hide_n = min(blind_counter, len(dice))
#         hidden_indices = list(range(len(dice) - hide_n, len(dice)))
#         typingPrint(f"(Blind obscured {hide_n} dice - values hidden from you!)")
#         blind_counter -= hide_n
    
play = "yeah, buddy"

# triggers at end of turn
# if bleed_counter > 0:
#     health -= bleed_counter
#     bleed_counter -= 1


class BasicCombatant:
  def __init__(
    self,
    name,
    hp,
    deck_cards,
    hand_limit_value,
    dice_limit_value,
    intro=None,
    current_hp=None,
    max_hp=None,
    class_name=None,
    player_level=1,
  ):
    self.name = name
    self.intro = intro
    resolved_max_hp = hp if max_hp is None else max_hp
    resolved_current_hp = resolved_max_hp if current_hp is None else current_hp
    self.max_hp = resolved_max_hp
    self.hp = min(resolved_current_hp, resolved_max_hp)
    self.shield = 0
    self.deck = list(deck_cards)
    random.shuffle(self.deck)
    self.discard = []
    self.cards_in_hand = []
    self.hand_limit = hand_limit_value
    self.dice_limit = dice_limit_value
    self.dice_pool = []
    self.status = {
      "poison": 0,
      "burn": 0,
      "lock": 0,
      "freeze": 0,
      "bleed": 0,
      "blind": 0,
    }
    self.hidden_die_indices = []
    self.limit_progress = {}
    self.once_per_combat_used = set()
    self.class_name = class_name
    self.player_level = max(1, int(player_level))
    self.class_state = {
      "fencer_used_turn": False,
      "druid_used_turn": False,
      "druid_planted_value": None,
      "knight_turn_total": 0,
      "knight_turn_locked": False,
      "rogue_lucky_number": None,
    }


def _class_level(actor):
  return max(1, int(getattr(actor, "player_level", 1)))


def _class_name(actor):
  raw_value = getattr(actor, "class_name", None)
  if raw_value is None:
    return ""
  return str(raw_value).strip().lower()


def _knight_roll_limit(actor):
  return 9 + ((_class_level(actor) - 1) * 6)


def _cleric_heal_scaler(actor):
  # Kept intentionally moderate to preserve progression without runaway healing.
  return 1 + ((_class_level(actor) - 1) // 2)


def _apply_class_passive_on_roll(actor, opposing_actor):
  class_name = _class_name(actor)
  if class_name == "cleric" and actor.dice_pool:
    counts = {}
    for die_value in actor.dice_pool:
      counts[die_value] = counts.get(die_value, 0) + 1

    total_heal = 0
    heal_scale = _cleric_heal_scaler(actor)
    for die_value, count in counts.items():
      if count >= 2:
        pair_units = count - 1
        total_heal += pair_units * die_value * heal_scale

    if total_heal > 0:
      hp_before = actor.hp
      actor.hp = min(actor.max_hp, actor.hp + total_heal)
      healed_amount = actor.hp - hp_before
      if healed_amount > 0:
        typingPrint(f"Cleric passive: heals {healed_amount} HP from matched dice.")
      else:
        # At level 2+, overflow converts to temporary shield.
        if _class_level(actor) >= 2:
          actor.shield += total_heal
          typingPrint(f"Cleric passive: healing overflow grants {total_heal} temporary shield.")

  if class_name == "rogue" and actor.dice_pool and opposing_actor is not None:
    lucky_number = actor.class_state.get("rogue_lucky_number")
    if lucky_number in [1, 2, 3, 4, 5, 6]:
      hit_count = actor.dice_pool.count(lucky_number)
      if hit_count > 0:
        damage_per_hit = 2 * _class_level(actor)
        total_damage = damage_per_hit * hit_count
        dealt = _apply_shielded_damage(opposing_actor, total_damage)
        typingPrint(
          f"Rogue passive: lucky number {lucky_number} hit {hit_count} time(s), dealing {dealt} damage."
        )


def _apply_druid_bloom_if_ready(actor):
  if _class_name(actor) != "druid":
    return

  planted_value = actor.class_state.get("druid_planted_value")
  if planted_value is None:
    return

  level_value = _class_level(actor)
  value_bonus = level_value // 2
  bloom_value = min(6, planted_value + value_bonus)
  extra_dice = (level_value - 1) // 2
  bloom_count = 2 + extra_dice
  actor.dice_pool.extend([bloom_value] * bloom_count)
  actor.class_state["druid_planted_value"] = None
  typingPrint(f"Druid bloom: your planted die blooms into {bloom_count} die/dice of value {bloom_value}.")


def _class_ability_label(actor):
  class_name = _class_name(actor)
  if class_name == "fencer":
    return "Fencer Card (Free): Reroll one die (once per turn)"
  if class_name == "druid":
    return "Druid Card (Free): Plant one die for next-turn bloom (once per turn)"
  if class_name == "knight":
    current_total = actor.class_state.get("knight_turn_total", 0)
    roll_limit = _knight_roll_limit(actor)
    remaining = max(0, roll_limit - current_total)
    return f"Knight Card (Free): Roll one die toward limit ({current_total}/{roll_limit}, rem {remaining})"
  if class_name == "cleric":
    return "Cleric Passive Card: Matched dice heal you after rolling"
  if class_name == "rogue":
    lucky_number = actor.class_state.get("rogue_lucky_number")
    if lucky_number in [1, 2, 3, 4, 5, 6]:
      return f"Rogue Passive Card: Lucky number {lucky_number} deals bonus damage"
    return "Rogue Passive Card: Select a lucky number before combat"
  return None


def _class_ability_usable(actor):
  class_name = _class_name(actor)
  if class_name == "fencer":
    return (not actor.class_state.get("fencer_used_turn", False)) and bool(actor.dice_pool)
  if class_name == "druid":
    return (not actor.class_state.get("druid_used_turn", False)) and bool(actor.dice_pool)
  if class_name == "knight":
    if actor.class_state.get("knight_turn_locked", False):
      return False
    current_total = actor.class_state.get("knight_turn_total", 0)
    return current_total < _knight_roll_limit(actor)
  return False


def _resolve_knight_jackpot(actor, opposing_actor, auto_player=False):
  level_value = _class_level(actor)
  if auto_player:
    dealt = _apply_shielded_damage(opposing_actor, 4 * level_value)
    typingPrint(f"Knight jackpot: auto-picks Smite and deals {dealt} damage.")
    return

  typingPrint("Knight jackpot! Choose a boon:")
  typingPrint(f"1) Heal {3 * level_value} HP")
  typingPrint(f"2) Smite for {4 * level_value} damage")
  typingPrint("3) Gain one die showing 6")
  boon_choice = get_valid_input("\t>", [1, 2, 3])
  if boon_choice == 1:
    hp_before = actor.hp
    actor.hp = min(actor.max_hp, actor.hp + (3 * level_value))
    typingPrint(f"Knight boon: healed {actor.hp - hp_before} HP.")
  elif boon_choice == 2:
    dealt = _apply_shielded_damage(opposing_actor, 4 * level_value)
    typingPrint(f"Knight boon: dealt {dealt} damage.")
  else:
    actor.dice_pool.append(6)
    typingPrint("Knight boon: gained one die showing 6.")


def _use_class_ability(actor, opposing_actor, auto_player=False):
  class_name = _class_name(actor)
  if class_name == "fencer":
    if not _class_ability_usable(actor):
      return False, "Fencer ability unavailable right now."
    if auto_player:
      die_index = actor.dice_pool.index(min(actor.dice_pool))
    else:
      chosen_text = input("Choose die index to reroll: ").strip()
      if not chosen_text.isdigit():
        return False, "Invalid die choice for reroll."
      die_index = int(chosen_text) - 1
      if die_index < 0 or die_index >= len(actor.dice_pool):
        return False, "Die choice out of range for reroll."

    old_value = actor.dice_pool[die_index]
    new_value = random.randint(1, 6)
    actor.dice_pool[die_index] = new_value
    actor.class_state["fencer_used_turn"] = True
    return True, f"Fencer reroll: {old_value} -> {new_value}."

  if class_name == "druid":
    if not _class_ability_usable(actor):
      return False, "Druid ability unavailable right now."
    if auto_player:
      die_index = actor.dice_pool.index(min(actor.dice_pool))
    else:
      chosen_text = input("Choose die index to plant: ").strip()
      if not chosen_text.isdigit():
        return False, "Invalid die choice for planting."
      die_index = int(chosen_text) - 1
      if die_index < 0 or die_index >= len(actor.dice_pool):
        return False, "Die choice out of range for planting."

    planted_value = actor.dice_pool.pop(die_index)
    actor.class_state["druid_planted_value"] = planted_value
    actor.class_state["druid_used_turn"] = True
    return True, f"Druid plant: stored {planted_value}. It will bloom next turn."

  if class_name == "knight":
    if not _class_ability_usable(actor):
      return False, "Knight roll is unavailable right now."

    new_die = random.randint(1, 6)
    actor.class_state["knight_turn_total"] += new_die
    roll_limit = _knight_roll_limit(actor)
    total_value = actor.class_state["knight_turn_total"]

    if total_value > roll_limit:
      actor.dice_pool = []
      actor.class_state["knight_turn_locked"] = True
      return True, f"Knight bust! Rolled {new_die}, exceeded {roll_limit}, and all unspent dice vanish. Turn ends."

    actor.dice_pool.append(new_die)
    if total_value == roll_limit:
      _resolve_knight_jackpot(actor, opposing_actor, auto_player=auto_player)
      actor.class_state["knight_turn_locked"] = True
      return True, f"Knight roll: {new_die}. Jackpot! Total {total_value}/{roll_limit}."

    return True, f"Knight roll: {new_die}. Total {total_value}/{roll_limit}."

  return False, "No active class ability."


def _get_enemies_for_biome(biome_id):
  biome_enemies = []
  for value in globals().values():
    if isinstance(value, ENEMY) and value.biome == biome_id:
      biome_enemies.append(value)
  return biome_enemies


BIOME_NAMES = {
  1: "Plains",
  2: "Tundra",
  3: "Forest",
  4: "Ruins",
  5: "Slops",
  6: "Pit",
}


def _format_biome_label(biome_id):
  biome_name = BIOME_NAMES.get(biome_id, "Unknown")
  return f"Biome {biome_id}: {biome_name}"


def _format_biome_tier_label(biome_id, biome_tier):
  return f"{_format_biome_label(biome_id)} | Tier {biome_tier}"


def _get_enemies_for_biome_tier(biome_id, biome_tier):
  biome_tier_enemies = []
  for value in globals().values():
    if isinstance(value, ENEMY) and value.biome == biome_id and value.biome_tier == biome_tier:
      biome_tier_enemies.append(value)
  return biome_tier_enemies


def _spawn_enemy_for_biome(biome_id, biome_tier=None):
  if biome_tier is None:
    possible_enemies = _get_enemies_for_biome(biome_id)
  else:
    possible_enemies = _get_enemies_for_biome_tier(biome_id, biome_tier)

  if not possible_enemies:
    return None

  chosen_enemy = random.choice(possible_enemies)
  return BasicCombatant(
    name=chosen_enemy.name,
    hp=chosen_enemy.hp,
    deck_cards=chosen_enemy.cards,
    hand_limit_value=3,
    dice_limit_value=chosen_enemy.dice,
    intro=chosen_enemy.intro,
  )


def _card_name_suffix(card_name):
  if card_name.endswith(" XY"):
    return card_name[:-3], "XY"
  if card_name.endswith(" x"):
    return card_name[:-2], "x"
  if card_name.endswith(" y"):
    return card_name[:-2], "y"
  if card_name.endswith(" X"):
    return card_name[:-2], "X"
  if card_name.endswith(" Y"):
    return card_name[:-2], "Y"
  return card_name, ""


def _get_all_cards_by_name():
  cards_by_name = {}
  for value in globals().values():
    if isinstance(value, CARD):
      cards_by_name[value.name] = value
  return cards_by_name


def _upgrade_card_one_step(card_obj, cards_by_name):
  base_name, suffix = _card_name_suffix(card_obj.name)

  if suffix == "":
    candidates = [
      cards_by_name.get(f"{base_name} x"),
      cards_by_name.get(f"{base_name} y"),
    ]
    candidates = [candidate for candidate in candidates if candidate is not None]
    if candidates:
      return random.choice(candidates)
    return card_obj

  if suffix == "x":
    return cards_by_name.get(f"{base_name} X", card_obj)
  if suffix == "y":
    return cards_by_name.get(f"{base_name} Y", card_obj)
  if suffix in ["X", "Y"]:
    return cards_by_name.get(f"{base_name} XY", card_obj)

  return card_obj


def _spawn_legendary_enemy_for_biome_tier(biome_id, biome_tier):
  candidates = _get_enemies_for_biome_tier(biome_id, biome_tier)
  if not candidates:
    return None, None

  chosen_enemy = random.choice(candidates)
  legendary_cards = list(chosen_enemy.cards)
  cards_by_name = _get_all_cards_by_name()

  upgradable_indices = []
  for card_index, card_obj in enumerate(legendary_cards):
    upgraded_card = _upgrade_card_one_step(card_obj, cards_by_name)
    if upgraded_card is not card_obj:
      upgradable_indices.append((card_index, upgraded_card))

  upgrade_text = "No card could be upgraded."
  if upgradable_indices:
    chosen_index, upgraded_card = random.choice(upgradable_indices)
    old_card = legendary_cards[chosen_index]
    legendary_cards[chosen_index] = upgraded_card
    upgrade_text = f"{old_card.name} -> {upgraded_card.name}"

  legendary_hp = math.ceil(chosen_enemy.hp * 1.5)
  legendary_actor = BasicCombatant(
    name=f"LEGENDARY {chosen_enemy.name}",
    hp=legendary_hp,
    deck_cards=legendary_cards,
    hand_limit_value=3,
    dice_limit_value=chosen_enemy.dice,
    intro=chosen_enemy.intro,
  )
  return legendary_actor, upgrade_text


def _draw_up_to_hand_limit(actor):
  while len(actor.cards_in_hand) < actor.hand_limit:
    if not actor.deck:
      if not actor.discard:
        break
      actor.deck = actor.discard
      actor.discard = []
      random.shuffle(actor.deck)
    actor.cards_in_hand.append(actor.deck.pop())


def _roll_dice_pool(actor):
  actor.dice_pool = [random.randint(1, 6) for _ in range(max(0, actor.dice_limit))]
  actor.hidden_die_indices = []


def _apply_shielded_damage(target, amount):
  if amount <= 0:
    return 0
  remaining = amount
  if target.shield > 0:
    blocked = min(target.shield, remaining)
    target.shield -= blocked
    remaining -= blocked
  if remaining > 0:
    target.hp -= remaining
  return remaining


def _trigger_start_of_turn(actor):
  if actor.status["poison"] > 0:
    actor.hp -= actor.status["poison"]
    actor.status["poison"] -= 1


def _trigger_on_card_played(actor):
  if actor.status["burn"] > 0:
    actor.hp -= actor.status["burn"] * 2
    actor.status["burn"] -= 1


def _trigger_on_dice_rolled(actor, opposing_actor=None, hide_output_for_blind=False):
  if actor.status["lock"] > 0:
    locks_to_apply = min(actor.status["lock"], len(actor.dice_pool))
    for _ in range(locks_to_apply):
      actor.dice_pool.pop(0)
    actor.status["lock"] -= locks_to_apply

  if actor.status["freeze"] > 0:
    for die_index in range(len(actor.dice_pool)):
      if actor.dice_pool[die_index] > 1 and actor.status["freeze"] > 0:
        actor.dice_pool[die_index] = 1
        actor.status["freeze"] -= 1

  if actor.status["blind"] > 0 and actor.dice_pool:
    hidden_count = min(actor.status["blind"], len(actor.dice_pool))
    actor.hidden_die_indices = list(range(len(actor.dice_pool) - hidden_count, len(actor.dice_pool)))
    actor.status["blind"] -= hidden_count
    if hide_output_for_blind:
      typingPrint(f"{actor.name} is blinded: {hidden_count} die/dice value(s) are obscured.")

  _apply_class_passive_on_roll(actor, opposing_actor)


def _trigger_end_of_turn(actor):
  if actor.status["bleed"] > 0:
    actor.hp -= actor.status["bleed"]
    actor.status["bleed"] -= 1


def _reset_combat_state(actor):
  actor.shield = 0
  actor.hidden_die_indices = []
  actor.limit_progress = {}
  actor.once_per_combat_used = set()
  for status_name in actor.status:
    actor.status[status_name] = 0


def _sanitize_card_id(card_id_value):
  return str(card_id_value).replace("-", "")


def _parse_card_id(card_id_value):
  cleaned = _sanitize_card_id(card_id_value)
  if len(cleaned) < 18:
    return None
  cleaned = cleaned[:18]
  return {
    "family": cleaned[0:2],
    "tier": cleaned[2:3],
    "limit": cleaned[3:6],
    "die_req": cleaned[6:8],
    "damage": cleaned[8:10],
    "trigger": cleaned[10:12],
    "status": cleaned[12:18],
  }


def _check_die_requirement(requirement_code, die_value):
  if requirement_code == "01":
    return True
  if requirement_code == "02":
    return die_value % 2 == 0
  if requirement_code == "03":
    return die_value % 2 == 1

  if requirement_code and requirement_code[0] == "7" and requirement_code[1].isdigit():
    return die_value == int(requirement_code[1])
  if requirement_code and requirement_code[0] == "3" and requirement_code[1].isdigit():
    return die_value >= int(requirement_code[1])
  if requirement_code and requirement_code[0] == "2" and requirement_code[1].isdigit():
    return die_value <= int(requirement_code[1])

  return True


def _check_trigger_condition(trigger_code, die_value):
  if trigger_code == "00":
    return True
  if trigger_code == "41":
    return die_value % 2 == 1
  if trigger_code == "42":
    return die_value % 2 == 0
  if trigger_code[0] == "1" and trigger_code[1].isdigit():
    return die_value == int(trigger_code[1])
  if trigger_code[0] == "2" and trigger_code[1].isdigit():
    return die_value <= int(trigger_code[1])
  if trigger_code[0] == "3" and trigger_code[1].isdigit():
    return die_value >= int(trigger_code[1])
  return False


def _amount_from_token(amount_token, die_value):
  if amount_token == "0":
    return 0
  if amount_token.isdigit():
    return int(amount_token)
  if amount_token == "X":
    return die_value
  if amount_token == "Y":
    return math.ceil(die_value / 2)
  if amount_token == "Z":
    return math.floor(die_value / 2)
  if amount_token in "ABCDEF":
    return die_value + (ord(amount_token) - ord("A") + 1)
  return 0


def _evaluate_damage(damage_code, die_value):
  if damage_code == "00":
    return 0
  if damage_code[0] == "E" and damage_code[1].isdigit():
    return die_value + int(damage_code[1])
  if damage_code[0] == "A" and damage_code[1].isdigit():
    return die_value * int(damage_code[1])
  if damage_code.isdigit():
    return int(damage_code)
  return 0


def _apply_status_pairs(source, target, status_block, die_value, trigger_condition_met):
  if not trigger_condition_met:
    return

  for pair_start in range(0, 6, 2):
    pair = status_block[pair_start:pair_start + 2]
    if pair == "00":
      continue

    status_code = pair[0]
    amount_token = pair[1]

    if status_code == "Z":
      continue

    if status_code == "1" and amount_token == "Z":
      poison_value = max(0, target.status["poison"])
      _apply_shielded_damage(target, poison_value)
      if target.status["poison"] > 0:
        target.status["poison"] -= 1
      continue

    amount_value = _amount_from_token(amount_token, die_value)
    if amount_value <= 0:
      continue

    if _class_name(source) == "warlock" and status_code in ["1", "2", "3", "4", "5", "6"]:
      amount_value += _class_level(source)

    if status_code == "1":
      target.status["poison"] += amount_value
    elif status_code == "2":
      target.status["burn"] += amount_value
    elif status_code == "3":
      target.status["lock"] += amount_value
    elif status_code == "4":
      target.status["freeze"] += amount_value
    elif status_code == "5":
      target.status["bleed"] += amount_value
    elif status_code == "6":
      target.status["blind"] += amount_value
    elif status_code == "7":
      source.shield += amount_value
    elif status_code == "8":
      source.hp = min(source.max_hp, source.hp + amount_value)
    elif status_code == "9":
      source.hp -= amount_value


def _card_key(card_obj):
  return f"{card_obj.name}::{card_obj.id}"


def _get_limit_value(limit_code):
  if len(limit_code) != 3:
    return 0
  if limit_code[0] == "1":
    return int(limit_code[1:3])
  return 0


def _is_reusable_limit(limit_code):
  return len(limit_code) == 3 and limit_code[0] == "2"


def _is_once_per_combat(limit_code):
  return limit_code == "222"


def _format_card_limit_display(actor, card_obj):
  card_info = _parse_card_id(card_obj.id)
  if card_info is None:
    return ""

  limit_value = _get_limit_value(card_info["limit"])
  if limit_value <= 0:
    return ""

  card_identifier = _card_key(card_obj)
  current_progress = actor.limit_progress.get(card_identifier, 0)
  return f" | Charge {current_progress}/{limit_value}"


def _resolve_card_use(source, target, card_obj, die_value):
  card_info = _parse_card_id(card_obj.id)
  if card_info is None:
    return False, "Card ID format invalid.", False

  if not _check_die_requirement(card_info["die_req"], die_value):
    return False, "Selected die does not meet card requirement.", False

  card_identifier = _card_key(card_obj)
  limit_code = card_info["limit"]

  if _is_once_per_combat(limit_code) and card_identifier in source.once_per_combat_used:
    return False, "Card is once-per-combat and already used.", False

  limit_value = _get_limit_value(limit_code)
  effect_triggers_now = True
  if limit_value > 0:
    if card_identifier not in source.limit_progress:
      source.limit_progress[card_identifier] = 0
    source.limit_progress[card_identifier] += die_value
    if source.limit_progress[card_identifier] < limit_value:
      effect_triggers_now = False
    else:
      source.limit_progress[card_identifier] = 0

  if _is_once_per_combat(limit_code):
    source.once_per_combat_used.add(card_identifier)

  _trigger_on_card_played(source)

  if not effect_triggers_now:
    progress_text = f"{source.name} charges {card_obj.name} ({source.limit_progress.get(card_identifier, 0)}/{limit_value})."
    return True, progress_text, True

  trigger_condition_met = _check_trigger_condition(card_info["trigger"], die_value)

  damage_value = _evaluate_damage(card_info["damage"], die_value)
  hp_damage_done = _apply_shielded_damage(target, damage_value)

  _apply_status_pairs(
    source=source,
    target=target,
    status_block=card_info["status"],
    die_value=die_value,
    trigger_condition_met=trigger_condition_met,
  )

  reusable_flag = _is_reusable_limit(limit_code)
  action_text = f"\n{source.name} uses {card_obj.name} with a {die_value} for {hp_damage_done} HP damage."
  return True, action_text, reusable_flag


def _build_die_ascii_lines(die_value):
  if die_value == "?":
    return [
      "+-------+",
      "|       |",
      "|   ?   |",
      "|       |",
      "+-------+",
    ]

  pip_positions = {
    1: [(1, 1)],
    2: [(0, 0), (2, 2)],
    3: [(0, 0), (1, 1), (2, 2)],
    4: [(0, 0), (0, 2), (2, 0), (2, 2)],
    5: [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
    6: [(0, 0), (1, 0), (2, 0), (0, 2), (1, 2), (2, 2)],
  }

  if die_value not in pip_positions:
    return [
      "+-------+",
      "|       |",
      f"|  {str(die_value).center(3)}  |",
      "|       |",
      "+-------+",
    ]

  grid = [[" " for _ in range(3)] for _ in range(3)]
  for row_index, col_index in pip_positions[die_value]:
    grid[row_index][col_index] = "*"

  return [
    "+-------+",
    f"| {grid[0][0]}   {grid[0][2]} |",
    f"| {grid[1][0]} {grid[1][1]} {grid[1][2]} |",
    f"| {grid[2][0]}   {grid[2][2]} |",
    "+-------+",
  ]


def _display_dice_for_player(player_actor):
  if not player_actor.dice_pool:
    typingPrint("Dice: (none)")
    return

  die_blocks = []
  labels = []
  for index, value in enumerate(player_actor.dice_pool, start=1):
    if (index - 1) in player_actor.hidden_die_indices:
      die_blocks.append(_build_die_ascii_lines("?"))
    else:
      die_blocks.append(_build_die_ascii_lines(value))
    labels.append(f"   ({index})   ")

  typingPrint("Dice:")
  for line_index in range(5):
    typingPrint("  ".join(block[line_index] for block in die_blocks), delay=0)
  typingPrint("  ".join(labels), delay = 0)


def _display_dice_pool_ascii(dice_pool, header="Dice:"):
  if not dice_pool:
    typingPrint(f"{header} (none)")
    return

  die_blocks = [_build_die_ascii_lines(die_value) for die_value in dice_pool]
  labels = [f"   ({index})   " for index in range(1, len(dice_pool) + 1)]

  typingPrint(header)
  for line_index in range(5):
    typingPrint("  ".join(block[line_index] for block in die_blocks), delay=0)
  typingPrint("  ".join(labels), delay=0)


def _player_take_turn(player_actor, enemy_actor, auto_player=False):
  _trigger_start_of_turn(player_actor)
  if player_actor.hp <= 0:
    return

  player_actor.class_state["fencer_used_turn"] = False
  player_actor.class_state["druid_used_turn"] = False
  player_actor.class_state["knight_turn_total"] = 0
  player_actor.class_state["knight_turn_locked"] = False

  _draw_up_to_hand_limit(player_actor)
  if _class_name(player_actor) == "knight":
    player_actor.dice_pool = []
    player_actor.hidden_die_indices = []
  else:
    _roll_dice_pool(player_actor)
    _apply_druid_bloom_if_ready(player_actor)
  _trigger_on_dice_rolled(player_actor, opposing_actor=enemy_actor, hide_output_for_blind=True)

  while enemy_actor.hp > 0 and player_actor.hp > 0:
    if _class_name(player_actor) == "knight" and player_actor.class_state.get("knight_turn_locked", False):
      break

    ability_label = _class_ability_label(player_actor)
    ability_is_usable = _class_ability_usable(player_actor)
    has_card_play = bool(player_actor.dice_pool and player_actor.cards_in_hand)
    if not has_card_play and not ability_is_usable:
      break

    if auto_player:
      if _class_ability_usable(player_actor):
        played_ability, ability_text = _use_class_ability(player_actor, enemy_actor, auto_player=True)
        if played_ability:
          typingPrint(ability_text)
          continue

      usable_move = None
      for card_index, hand_card in enumerate(player_actor.cards_in_hand):
        parsed = _parse_card_id(hand_card.id)
        if parsed is None:
          continue
        for die_index, die_value in enumerate(player_actor.dice_pool):
          if _check_die_requirement(parsed["die_req"], die_value):
            usable_move = (card_index, die_index)
            break
        if usable_move is not None:
          break
      if usable_move is None:
        break
      chosen_card_index, chosen_die_index = usable_move
    else:
      typingPrint(f"\n{player_actor.name} HP:{player_actor.hp}/{player_actor.max_hp} SH:{player_actor.shield}")
      typingPrint(f"{enemy_actor.name} HP:{enemy_actor.hp}/{enemy_actor.max_hp} SH:{enemy_actor.shield}")
      _display_dice_for_player(player_actor)
      if ability_label is not None:
        if ability_is_usable:
          typingPrint(f"0) {ability_label}")
        else:
          typingPrint(f"0) {ability_label} [not ready]")
      for card_index, hand_card in enumerate(player_actor.cards_in_hand, start=1):
        limit_text = _format_card_limit_display(player_actor, hand_card)
        typingPrint(f"{card_index}) {hand_card.name} | {hand_card.description}{limit_text}")

      chosen_card_text = input("Choose card number to play (or press Enter to end turn): ").strip()
      if chosen_card_text == "":
        break
      if not chosen_card_text.isdigit():
        typingPrint("Invalid card choice.")
        continue

      if chosen_card_text == "0":
        played_ability, ability_text = _use_class_ability(player_actor, enemy_actor, auto_player=False)
        typingPrint(ability_text)
        if _class_name(player_actor) == "fencer" and played_ability:
          _trigger_on_dice_rolled(player_actor, opposing_actor=enemy_actor, hide_output_for_blind=True)
        if _class_name(player_actor) == "knight" and player_actor.class_state.get("knight_turn_locked", False):
          break
        continue

      chosen_card_index = int(chosen_card_text) - 1
      if chosen_card_index < 0 or chosen_card_index >= len(player_actor.cards_in_hand):
        typingPrint("Card choice out of range.")
        continue

      chosen_die_text = input("Choose die index to spend: ").strip()
      if not chosen_die_text.isdigit():
        typingPrint("Invalid die choice.")
        continue
      chosen_die_index = int(chosen_die_text) - 1
      if chosen_die_index < 0 or chosen_die_index >= len(player_actor.dice_pool):
        typingPrint("Die choice out of range.")
        continue

    chosen_card = player_actor.cards_in_hand[chosen_card_index]
    spent_die = player_actor.dice_pool.pop(chosen_die_index)
    played, action_result, keep_in_hand = _resolve_card_use(player_actor, enemy_actor, chosen_card, spent_die)
    typingPrint(action_result)

    if played and not keep_in_hand:
      moved_card = player_actor.cards_in_hand.pop(chosen_card_index)
      player_actor.discard.append(moved_card)

  _trigger_end_of_turn(player_actor)


def _enemy_take_turn(enemy_actor, player_actor):
  _trigger_start_of_turn(enemy_actor)
  if enemy_actor.hp <= 0:
    return

  _draw_up_to_hand_limit(enemy_actor)
  _roll_dice_pool(enemy_actor)
  _trigger_on_dice_rolled(enemy_actor, opposing_actor=player_actor, hide_output_for_blind=False)

  while enemy_actor.dice_pool and enemy_actor.cards_in_hand and player_actor.hp > 0 and enemy_actor.hp > 0:
    selected_move = None
    for card_index, hand_card in enumerate(enemy_actor.cards_in_hand):
      parsed = _parse_card_id(hand_card.id)
      if parsed is None:
        continue
      for die_index, die_value in enumerate(enemy_actor.dice_pool):
        if _check_die_requirement(parsed["die_req"], die_value):
          selected_move = (card_index, die_index)
          break
      if selected_move is not None:
        break

    if selected_move is None:
      break

    card_index, die_index = selected_move
    enemy_card = enemy_actor.cards_in_hand[card_index]
    spent_die = enemy_actor.dice_pool.pop(die_index)
    played, action_result, keep_in_hand = _resolve_card_use(enemy_actor, player_actor, enemy_card, spent_die)
    typingPrint(action_result)

    if played and not keep_in_hand:
      moved_card = enemy_actor.cards_in_hand.pop(card_index)
      enemy_actor.discard.append(moved_card)

  _trigger_end_of_turn(enemy_actor)


def run_basic_combat_loop(
  current_biome,
  current_biome_tier=1,
  player_hp=None,
  player_max_hp=None,
  player_deck=None,
  auto_player=False,
  legendary_enemy=False,
  player_hand_limit=None,
  player_start_shield=0,
  player_class=None,
  player_level=1,
  rogue_lucky_number=None,
):
  """
  Basic combat loop:
  - Randomly chooses an enemy valid for the current biome and biome tier.
  - Player goes first: draw to hand limit and roll to dice limit.
  - Cards are activated by spending dice and resolving effects via card ID data.
  - Enemy then does the same, but with hand size capped at 3.
  - Status effect triggers fire at their relevant timings.
  - Combat ends when enemy dies or player HP drops to 0 (retreat).
  """
  if current_biome_tier not in [1, 2, 3]:
    typingPrint("Invalid biome tier. Please choose 1, 2, or 3.")
    return None

  legendary_upgrade_text = None
  if legendary_enemy:
    enemy_actor, legendary_upgrade_text = _spawn_legendary_enemy_for_biome_tier(current_biome, current_biome_tier)
  else:
    enemy_actor = _spawn_enemy_for_biome(current_biome, current_biome_tier)

  if enemy_actor is None:
    typingPrint(f"No enemy found for biome {current_biome}, tier {current_biome_tier}.")
    return None

  starting_hp = currenthp if player_hp is None else player_hp
  if player_max_hp is None:
    player_max_hp = max_player_health if "max_player_health" in globals() else starting_hp
  starting_hp = min(starting_hp, player_max_hp)

  if player_deck is None:
    player_deck = deck

  resolved_hand_limit = hand_limit if player_hand_limit is None else player_hand_limit

  player_actor = BasicCombatant(
    name=charname,
    hp=player_max_hp,
    deck_cards=player_deck,
    hand_limit_value=resolved_hand_limit,
    dice_limit_value=dice_limit,
    current_hp=starting_hp,
    class_name=player_class,
    player_level=player_level,
  )
  player_actor.shield = max(0, int(player_start_shield))
  if _class_name(player_actor) == "rogue":
    if auto_player:
      player_actor.class_state["rogue_lucky_number"] = rogue_lucky_number if rogue_lucky_number in [1, 2, 3, 4, 5, 6] else 3
    else:
      chosen_lucky = rogue_lucky_number
      if chosen_lucky not in [1, 2, 3, 4, 5, 6]:
        typingPrint("Choose your lucky number for this combat:")
        chosen_lucky = get_valid_input("\t>", [1, 2, 3, 4, 5, 6])
      player_actor.class_state["rogue_lucky_number"] = chosen_lucky
      typingPrint(f"Rogue passive set: lucky number {chosen_lucky}.")

  if legendary_enemy:
    typingPrint(f"\nA Legendary {enemy_actor.name} appears at the end of your journey!")
    typingPrint(f"Legendary bonus: HP x1.5 (rounded up), upgraded card: {legendary_upgrade_text}")
  else:
    typingPrint("")
    if enemy_actor.intro:
      typingPrint(enemy_actor.intro)
    else:
      typingPrint(f"A wild {enemy_actor.name} appears in {_format_biome_tier_label(current_biome, current_biome_tier)}!")

  if player_actor.shield > 0:
    typingPrint(f"Training bonus: You start this battle with {player_actor.shield} shield.")

  round_number = 1
  while player_actor.hp > 0 and enemy_actor.hp > 0:
    typingPrint(f"\n--- Round {round_number} ---")
    _player_take_turn(player_actor, enemy_actor, auto_player=auto_player)
    if enemy_actor.hp <= 0:
      break

    _enemy_take_turn(enemy_actor, player_actor)
    round_number += 1

  if enemy_actor.hp <= 0:
    _reset_combat_state(player_actor)
    _reset_combat_state(enemy_actor)
    typingPrint(f"{enemy_actor.name} is defeated!")
    return {
      "result": "victory",
      "player_hp": player_actor.hp,
      "enemy": enemy_actor.name,
      "enemy_cards": list(enemy_actor.cards),
      "rounds": round_number,
    }

  _reset_combat_state(player_actor)
  _reset_combat_state(enemy_actor)
  typingPrint("You were reduced to 0 HP or less and are forced to retreat.")
  return {
    "result": "retreat",
    "player_hp": player_actor.hp,
    "enemy": enemy_actor.name,
    "enemy_cards": list(enemy_actor.cards),
    "rounds": round_number,
  }


def _handle_enemy_card_drop(encounter_result, player_deck=None, player_inventory=None):
  """10% chance to loot one random card from the defeated enemy."""
  if encounter_result.get("result") != "victory":
    return

  enemy_cards = encounter_result.get("enemy_cards") or []
  if not enemy_cards:
    return

  if random.random() >= 0.10:
    return

  dropped_card = random.choice(enemy_cards)
  typingPrint(f"\nLoot drop! {encounter_result.get('enemy', 'The enemy')} dropped {dropped_card.name}.")
  typingPrint("What do you want to do with this card?")
  typingPrint("1) Send to inventory")
  typingPrint("2) Add to deck now")

  loot_choice = get_valid_input("\t>", [1, 2])

  if player_inventory is not None:
    player_inventory.append(dropped_card)

  if loot_choice == 1:
    typingPrint(f"{dropped_card.name} was sent to your inventory.")
    return

  if player_deck is not None:
    player_deck.append(dropped_card)
  typingPrint(f"{dropped_card.name} was added to your deck.")

def adventuring_loop(
  current_biome,
  current_biome_tier,
  max_player_health,
  player_deck=None,
  player_inventory=None,
  player_hand_limit=None,
  player_start_shield=0,
  player_class=None,
  player_level=1,
):
  current_player_health = max_player_health
  win_streak = 0
  total_gold_earned = 0
  total_xp_earned = 0
  unlocked_destinations = {(current_biome, current_biome_tier)}
  legendary_unlocks_claimed = set()

  def try_unlock(destination_list, biome_value, tier_value):
    if biome_value < 1 or biome_value > 6:
      return
    if tier_value < 1 or tier_value > 3:
      return
    destination = (biome_value, tier_value)
    if destination not in unlocked_destinations:
      unlocked_destinations.add(destination)
      destination_list.append(destination)

  def unlocks_for_legendary_defeat(biome_value, tier_value):
    if biome_value == 1 and tier_value == 1:
      return [(2, 1), (1, 2)]
    if biome_value == 1 and tier_value == 2:
      return [(1, 3)]
    return []

  # Choose destination at the start of the adventure
  sorted_unlocked = sorted(unlocked_destinations, key=lambda item: (item[0], item[1]))
  typingPrint("\nChoose your destination:")
  for option_index, (biome_value, tier_value) in enumerate(sorted_unlocked, start=1):
    typingPrint(f"{option_index}) {_format_biome_tier_label(biome_value, tier_value)}")

  selected_index = get_valid_input("\t>", list(range(1, len(sorted_unlocked) + 1)))
  selected_biome, selected_tier = sorted_unlocked[selected_index - 1]
  
  typingPrint(f"\nYou venture into {_format_biome_tier_label(selected_biome, selected_tier)}...")

  # Main combat loop - stay in the selected biome/tier
  while current_player_health > 0:
    # Run combat encounter
    encounter_result = run_basic_combat_loop(
      selected_biome,
      selected_tier,
      player_hp=current_player_health,
      player_max_hp=max_player_health,
      player_deck=player_deck,
      player_hand_limit=player_hand_limit,
      player_start_shield=player_start_shield,
      player_class=player_class,
      player_level=player_level,
    )
    if encounter_result is None:
      return None

    current_player_health = encounter_result["player_hp"]

    # Check if player was defeated
    if encounter_result["result"] != "victory":
      # Player was defeated in combat
      return {
        "result": "retreat",
        "player_hp": current_player_health,
        "rounds": win_streak,
        "total_xp": total_xp_earned,
        "total_gold": total_gold_earned,
      }

    # Player won this battle
    win_streak += 1

    # 10% chance to loot a random card from the defeated enemy.
    _handle_enemy_card_drop(
      encounter_result,
      player_deck=player_deck,
      player_inventory=player_inventory,
    )
    
    # Calculate rewards with multiplier for persistence
    # Base rewards scale with biome tier
    base_xp = 50 + (selected_tier * 30)
    base_gold = 25 + (selected_tier * 15)
    
    # Multiplier increases by 8% per consecutive win, capping at 2.0x
    # Win 1: 1.0x, Win 2: 1.08x, Win 3: 1.16x, Win 5: 1.32x, Win 10: 1.72x
    multiplier = min(1.0 + (win_streak - 1) * 0.08, 2.0)
    
    xp_earned = int(base_xp * multiplier)
    gold_earned = int(base_gold * multiplier)
    
    total_xp_earned += xp_earned
    total_gold_earned += gold_earned
    
    typingPrint(f"Victory! You earned {xp_earned} XP and {gold_earned} gold (x{multiplier:.2f} multiplier).")

    # Check for legendary boss encounter
    if win_streak == 10:
      typingPrint("\n=== MINI BOSS ENCOUNTER ===")
      legendary_result = run_basic_combat_loop(
        selected_biome,
        selected_tier,
        player_hp=current_player_health,
        player_max_hp=max_player_health,
        legendary_enemy=True,
        player_deck=player_deck,
        player_hand_limit=player_hand_limit,
        player_start_shield=player_start_shield,
        player_class=player_class,
        player_level=player_level,
      )
      if legendary_result is None:
        return None
      current_player_health = legendary_result["player_hp"]
      
      if legendary_result["result"] == "victory":
        # 10% chance to loot a random card from the defeated legendary enemy.
        _handle_enemy_card_drop(
          legendary_result,
          player_deck=player_deck,
          player_inventory=player_inventory,
        )

        # Player beat the legendary boss!
        # Legendary boss gives bonus rewards
        legendary_xp = int((100 + selected_tier * 50) * 2.0)  # Always 2x multiplier for legendary
        legendary_gold = int((50 + selected_tier * 25) * 2.0)
        total_xp_earned += legendary_xp
        total_gold_earned += legendary_gold
        typingPrint(f"Legendary Victory! You earned {legendary_xp} XP and {legendary_gold} gold!")
        
        legendary_key = (selected_biome, selected_tier)
        if legendary_key not in legendary_unlocks_claimed:
          legendary_unlocks_claimed.add(legendary_key)
          newly_unlocked = []
          for biome_value, tier_value in unlocks_for_legendary_defeat(selected_biome, selected_tier):
            try_unlock(newly_unlocked, biome_value, tier_value)

          if newly_unlocked:
            unlock_text = ", ".join(
              _format_biome_tier_label(biome_value, tier_value) for biome_value, tier_value in newly_unlocked
            )
            typingPrint(f"Unlocked: {unlock_text}")
        
        typingPrint(f"\nYou've conquered this area! Total earnings: {total_xp_earned} XP, {total_gold_earned} gold.")
        typingPrint("Returning to town...")
        return {
          "result": "victory",
          "player_hp": current_player_health,
          "rounds": win_streak,
          "total_xp": total_xp_earned,
          "total_gold": total_gold_earned,
        }
      else:
        # Player was defeated by legendary boss
        return {
          "result": "retreat",
          "player_hp": current_player_health,
          "rounds": win_streak,
          "total_xp": total_xp_earned,
          "total_gold": total_gold_earned,
        }

    # After winning a regular battle, offer choice to continue or retreat
    typingPrint(f"\nYou've won {win_streak} battles in a row.")
    typingPrint(f"Total earnings so far: {total_xp_earned} XP, {total_gold_earned} gold.")
    next_multiplier = min(1.0 + win_streak * 0.08, 2.0)
    typingPrint(f"Next battle multiplier: x{next_multiplier:.2f}")
    typingPrint("What do you want to do?")
    typingPrint("1) Continue fighting")
    typingPrint("2) Retreat to town")
    
    choice = get_valid_input("\t>", [1, 2])
    
    if choice == 2:
      typingPrint(f"\nYou decide to retreat to town with {total_xp_earned} XP and {total_gold_earned} gold.")
      return {
        "result": "retreat",
        "player_hp": current_player_health,
        "rounds": win_streak,
        "total_xp": total_xp_earned,
        "total_gold": total_gold_earned,
      }
    
    # Player chose to continue, loop continues

  # This should only be reached if HP drops to 0 between battles somehow
  return {
    "result": "retreat",
    "player_hp": current_player_health,
    "rounds": win_streak,
    "total_xp": total_xp_earned,
    "total_gold": total_gold_earned,
  }

shop = 0
# For purchasing cards

blacksmith = 0
# For upgrading cards

RARITY_LABELS = {
  1: "Common",
  2: "Uncommon",
  3: "Rare",
  4: "Heroic",
  5: "Legendary",
  6: "Celestial",
}

SHOP_PRICE_RANGES = {
  1: (15, 20),
  2: (30, 40),
  3: (70, 90),
  4: (125, 150),
  5: (200, 250),
  6: (350, 500),
}


def _is_base_level_card(card_obj):
  if not isinstance(card_obj, CARD):
    return False
  _, suffix = _card_name_suffix(card_obj.name)
  return suffix == "" and 1 <= card_obj.rarity <= 6


def _get_shop_card_pools_by_rarity():
  pools = {rarity: [] for rarity in range(1, 7)}
  for value in globals().values():
    if _is_base_level_card(value):
      pools[value.rarity].append(value)
  return pools


def _roll_shop_rarity(pools):
  weighted_table = [
    (1, 0.50),
    (2, 0.25),
    (3, 0.15),
    (4, 0.05),
    (5, 0.03),
    (6, 0.02),
  ]

  # Retry a few times so we still respect weighted rolls if a rarity pool is empty.
  for _ in range(12):
    roll = random.random()
    cumulative = 0.0
    for rarity, chance in weighted_table:
      cumulative += chance
      if roll <= cumulative:
        if pools.get(rarity):
          return rarity
        break

  available_rarities = [rarity for rarity, cards in pools.items() if cards]
  return random.choice(available_rarities) if available_rarities else None


def _generate_shop_offers(offer_count=6):
  pools = _get_shop_card_pools_by_rarity()
  sale_active = random.random() < 0.05
  selected_card_ids = set()
  offers = []

  for _ in range(offer_count):
    rarity = _roll_shop_rarity(pools)
    if rarity is None:
      break

    rarity_pool = pools[rarity]
    available_pool = [card for card in rarity_pool if card.id not in selected_card_ids]
    if not available_pool:
      available_pool = rarity_pool

    if not available_pool:
      continue

    chosen_card = random.choice(available_pool)
    selected_card_ids.add(chosen_card.id)

    low_price, high_price = SHOP_PRICE_RANGES[rarity]
    base_price = random.randint(low_price, high_price)
    final_price = math.ceil(base_price * 0.5) if sale_active else base_price

    offers.append(
      {
        "card": chosen_card,
        "rarity": rarity,
        "base_price": base_price,
        "price": final_price,
        "purchased": False,
      }
    )

  return offers, sale_active


def _run_shop(player_state):
  offers, sale_active = _generate_shop_offers(offer_count=6)

  typingPrint("\nYou step into the naukin card shop.")
  if sale_active:
    typingPrint("The shopkeep rings a bell: \"Sale day! Everything is 50% off!\"")

  if not offers:
    typingPrint("The shelves are oddly empty today. Come back later.")
    return

  while True:
    typingPrint("\n=== SHOP INVENTORY ===", delay=0)
    typingPrint(f"Gold: {player_state['gold']}", delay=0)

    for index, offer in enumerate(offers, start=1):
      card = offer["card"]
      rarity_name = RARITY_LABELS[offer["rarity"]]

      if offer["purchased"]:
        price_text = "SOLD"
      elif sale_active:
        price_text = f"{offer['base_price']} -> {offer['price']} gold"
      else:
        price_text = f"{offer['price']} gold"

      typingPrint(
        f"{index}) {card.name} [{rarity_name}] - {price_text}",
        delay=0,
      )

    valid_options = [0] + list(range(1, len(offers) + 1))
    selection = get_valid_input(
      "Choose a card to buy, or 0 to leave the shop:\n\t>",
      valid_options,
    )

    if selection == 0:
      typingPrint("You leave the shop.")
      return

    chosen_offer = offers[selection - 1]
    if chosen_offer["purchased"]:
      typingPrint("That card has already been sold.")
      continue

    price = chosen_offer["price"]
    if player_state["gold"] < price:
      typingPrint("You do not have enough gold for that card.")
      continue

    player_state["gold"] -= price
    player_state["inventory"].append(chosen_offer["card"])
    chosen_offer["purchased"] = True
    typingPrint(f"Purchased {chosen_offer['card'].name} for {price} gold.")
    typingPrint(f"Gold remaining: {player_state['gold']}")


def _card_upgrade_tier(card_obj):
  _, suffix = _card_name_suffix(card_obj.name)
  if suffix == "":
    return 1
  if suffix in ["x", "y"]:
    return 2
  if suffix in ["X", "Y"]:
    return 3
  return 4


def _blacksmith_upgrade_candidates(card_obj, cards_by_name):
  base_name, suffix = _card_name_suffix(card_obj.name)
  if suffix == "":
    options = [
      cards_by_name.get(f"{base_name} x"),
      cards_by_name.get(f"{base_name} y"),
    ]
    return [option for option in options if option is not None]
  if suffix == "x":
    upgraded = cards_by_name.get(f"{base_name} X")
    return [upgraded] if upgraded is not None else []
  if suffix == "y":
    upgraded = cards_by_name.get(f"{base_name} Y")
    return [upgraded] if upgraded is not None else []
  if suffix in ["X", "Y"]:
    upgraded = cards_by_name.get(f"{base_name} XY")
    return [upgraded] if upgraded is not None else []
  return []


def _run_blacksmith(player_state):
  cards_by_name = _get_all_cards_by_name()
  owned_cards = player_state["inventory"]

  while True:
    # Count cards by name
    card_counts = {}
    for card in owned_cards:
      card_counts[card.name] = card_counts.get(card.name, 0) + 1

    # Find cards with at least 2 copies that can be upgraded
    upgradeable_cards = {}
    for card_name, count in card_counts.items():
      if count >= 2:
        sample_card = next(c for c in owned_cards if c.name == card_name)
        candidates = _blacksmith_upgrade_candidates(sample_card, cards_by_name)
        if candidates:
          upgradeable_cards[card_name] = (sample_card, candidates)

    if not upgradeable_cards:
      typingPrint("You need 2 identical copies of an upgradable card to forge.")
      return

    typingPrint("\nThe naukin blacksmith grunts and gestures at the anvil.")
    typingPrint(f"Gold: {player_state['gold']}", delay=0)
    typingPrint("Choose a card to forge (2 identical copies + gold -> 1 upgraded card, 0 to leave):", delay=0)

    valid_choices = [0]
    card_list = []
    for index, (card_name, (sample_card, _)) in enumerate(sorted(upgradeable_cards.items()), start=1):
      tier_value = _card_upgrade_tier(sample_card)
      forge_cost = 50 * (2 ** tier_value)
      count = card_counts[card_name]
      typingPrint(f"{index}) {card_name} (x{count}) - Tier {tier_value} - Cost: {forge_cost}g", delay=0)
      card_list.append(card_name)
      valid_choices.append(index)

    choice = get_valid_input("\t>", valid_choices)
    if choice == 0:
      typingPrint("You step away from the forge.")
      return

    chosen_card_name = card_list[choice - 1]
    sample_card, candidates = upgradeable_cards[chosen_card_name]
    
    target_tier = _card_upgrade_tier(sample_card)
    forge_cost = 50 * (2 ** target_tier)
    
    if player_state["gold"] < forge_cost:
      typingPrint(f"Forging this card costs {forge_cost} gold. You don't have enough.")
      continue

    upgraded_card = candidates[0]
    if len(candidates) > 1:
      typingPrint("Choose the upgrade path:", delay=0)
      for option_index, option_card in enumerate(candidates, start=1):
        typingPrint(f"{option_index}) {option_card.name}", delay=0)
      path_choice = get_valid_input("\t>", list(range(1, len(candidates) + 1)))
      upgraded_card = candidates[path_choice - 1]

    # Remove 2 copies of the card and add 1 upgraded version
    player_state["gold"] -= forge_cost
    removed_count = 0
    for i in range(len(owned_cards) - 1, -1, -1):
      if owned_cards[i].name == chosen_card_name and removed_count < 2:
        owned_cards.pop(i)
        removed_count += 1

    owned_cards.append(upgraded_card)
    removed_from_deck = _sync_deck_to_inventory(player_state)

    typingPrint(
      f"Forge complete: sacrificed 2x {chosen_card_name} and forged 1x {upgraded_card.name}."
    )
    if removed_from_deck > 0:
      typingPrint("Some deck cards were removed because they are no longer owned.")
    typingPrint(f"Gold remaining: {player_state['gold']}")


TRAINING_BASE_COSTS = {
  "hand": 180,
  "max_hp": 220,
  "recovery": 160,
  "shield": 190,
}


def _initialize_training_state(player_state):
  player_state.setdefault("training_hand_level", 0)
  player_state.setdefault("training_hp_level", 0)
  player_state.setdefault("training_recovery_level", 0)
  player_state.setdefault("training_shield_level", 0)


def _training_cost(base_cost, level):
  return math.ceil(base_cost * (1.4 ** level))


def _training_values(player_state):
  hand_bonus = int(player_state.get("training_hand_level", 0))
  hp_bonus = int(player_state.get("training_hp_level", 0)) * 5
  recovery_percent = int(player_state.get("training_recovery_level", 0)) * 5
  starting_shield = int(player_state.get("training_shield_level", 0))
  return {
    "hand_bonus": hand_bonus,
    "hp_bonus": hp_bonus,
    "recovery_percent": recovery_percent,
    "starting_shield": starting_shield,
  }


def _run_training(player_state):
  _initialize_training_state(player_state)

  while True:
    values = _training_values(player_state)
    hand_cost = _training_cost(TRAINING_BASE_COSTS["hand"], player_state["training_hand_level"])
    hp_cost = _training_cost(TRAINING_BASE_COSTS["max_hp"], player_state["training_hp_level"])
    recovery_cost = _training_cost(TRAINING_BASE_COSTS["recovery"], player_state["training_recovery_level"])
    shield_cost = _training_cost(TRAINING_BASE_COSTS["shield"], player_state["training_shield_level"])

    typingPrint("\nThessa wipes her hands and looks you over.")
    typingPrint(f"Gold: {player_state['gold']}", delay=0)
    typingPrint("\nTraining options:", delay=0)
    typingPrint(f"1) Hand size +1 (current bonus: +{values['hand_bonus']}) - {hand_cost} gold", delay=0)
    typingPrint(f"2) Max HP +5 (current bonus: +{values['hp_bonus']}) - {hp_cost} gold", delay=0)
    typingPrint(
      f"3) Between-battle recovery +5% (current: {values['recovery_percent']}%) - {recovery_cost} gold",
      delay=0,
    )
    typingPrint(
      f"4) Starting shield +1 (current bonus: +{values['starting_shield']}) - {shield_cost} gold",
      delay=0,
    )
    typingPrint("0) Leave training", delay=0)

    training_choice = get_valid_input("\t>", [0, 1, 2, 3, 4])
    if training_choice == 0:
      typingPrint("You thank Thessa and step away from training.")
      return

    if training_choice == 1:
      if player_state["gold"] < hand_cost:
        typingPrint("Thessa shakes her head. \"You don't have enough gold for that session.\"")
        continue
      player_state["gold"] -= hand_cost
      player_state["training_hand_level"] += 1
      typingPrint("Your drills pay off. You can now hold one more card in hand each battle.")

    elif training_choice == 2:
      if player_state["gold"] < hp_cost:
        typingPrint("Thessa shakes her head. \"You don't have enough gold for that session.\"")
        continue
      player_state["gold"] -= hp_cost
      player_state["training_hp_level"] += 1
      player_state["max_hp"] += 5
      player_state["current_hp"] = min(player_state["max_hp"], player_state["current_hp"] + 5)
      typingPrint("The regimen is brutal, but your body hardens. Max HP increased by 5.")

    elif training_choice == 3:
      if player_state["gold"] < recovery_cost:
        typingPrint("Thessa shakes her head. \"You don't have enough gold for that session.\"")
        continue
      player_state["gold"] -= recovery_cost
      player_state["training_recovery_level"] += 1
      new_recovery = _training_values(player_state)["recovery_percent"]
      typingPrint(f"You learn better breathing and recovery habits. Between-battle recovery is now {new_recovery}%.")

    elif training_choice == 4:
      if player_state["gold"] < shield_cost:
        typingPrint("Thessa shakes her head. \"You don't have enough gold for that session.\"")
        continue
      player_state["gold"] -= shield_cost
      player_state["training_shield_level"] += 1
      new_shield = _training_values(player_state)["starting_shield"]
      typingPrint(f"Your defensive stance improves. You now start battles with {new_shield} shield.")

# ==================== THESSA'S STARTER CARDS ====================

def _offer_thessa_starter_cards(player_state):
    """Thessa offers the player 6 basic cards to choose 3 from before their first adventure."""
    starter_cards = [woodensword, slingshot, smallstone, makeshiftshield, bandage, sharpenedstick]
    
    typingPrint("\nThessa places a wooden box on the counter and opens it, revealing various basic equipment.")
    typingPrint('"Before you head out there," she says, "you should take some proper gear. Can\'t have you fighting with just scraps."')
    typingPrint('"Pick any three. Consider them a welcome gift to Ascus."\n')
    
    # Display all available cards
    typingPrint("Available equipment:")
    for i, card in enumerate(starter_cards, 1):
        typingPrint(f"  {i}) {card.name} - {card.description}")
    
    chosen_cards = []
    available_indices = list(range(len(starter_cards)))
    
    while len(chosen_cards) < 3:
        typingPrint(f"\nYou've chosen {len(chosen_cards)}/3 items.")
        choice_input = input(f"Choose item {len(chosen_cards) + 1} (1-{len(starter_cards)}): ").strip()
        
        try:
            choice = int(choice_input)
            if 1 <= choice <= len(starter_cards):
                choice_idx = choice - 1
                if choice_idx in available_indices:
                    chosen_card = starter_cards[choice_idx]
                    chosen_cards.append(chosen_card)
                    available_indices.remove(choice_idx)
                    typingPrint(f"You take the {chosen_card.name}.")
                else:
                    typingPrint("You've already taken that item. Choose another.")
            else:
                typingPrint(f"Please enter a number between 1 and {len(starter_cards)}.")
        except ValueError:
            typingPrint("Invalid input. Please enter a number.")
    
    # Add chosen cards to inventory and deck
    for card in chosen_cards:
        player_state["inventory"].append(card)
        player_state["deck"].append(card)
    
    typingPrint(f"\nYou carefully pack away your new equipment: {', '.join(c.name for c in chosen_cards)}.")
    typingPrint('Thessa nods approvingly. "Those should serve you well out there. Now, about that adventure..."')
    player_state["thessa_starter_cards_given"] = True

# ==================== SAFE TOWN LOOP ====================
# Main gameplay loop for the safe town where player returns after adventures

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
            - inventory: List of all owned cards
            - deck: List of cards in deck
            - level: Player level
            - current_biome: Current biome ID (1-6)
            - current_biome_tier: Current biome tier (1-3)
    
    Returns:
        dict: Final player state when quitting
    """
    player_state.setdefault("shop_unlocked", False)
    player_state.setdefault("blacksmith_unlocked", False)
    player_state.setdefault("speed", 3)  # Default to normal speed
    player_state["level"] = max(1, int(player_state.get("level", 1)))
    _initialize_training_state(player_state)
    _initialize_inventory_state(player_state)
    
    # Apply saved speed setting
    set_speed_multiplier(player_state.get("speed", 3))
    
    # Offer Thessa's starter cards on first visit
    if not player_state.get("thessa_starter_cards_given", False):
        _offer_thessa_starter_cards(player_state)
    
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

      menu_text = (
        "\nWhat would you like to do?\n"
        "1) Go on an adventure\n"
        "2) Rest and heal\n"
        "3) Inventory and deck\n"
        "4) Change difficulty\n"
        "5) Change text speed\n"
        "6) Shop\n"
        "7) Blacksmith\n"
        "8) Training\n"
        "9) Quit game\n"
        "\t>"
      )

      choice = get_valid_input(menu_text, [1, 2, 3, 4, 5, 6, 7, 8, 9])

      if choice == 1:
        if not player_state['deck']:
          typingPrint("Your active deck is empty. Add cards from Inventory and deck first.")
          continue
        adventure_result = _run_adventure(player_state)
        if adventure_result:
          player_state = adventure_result

      elif choice == 2:
        if player_state['current_hp'] < player_state['max_hp']:
          heal_amount = player_state['max_hp'] - player_state['current_hp']
          player_state['current_hp'] = player_state['max_hp']
          typingPrint(f"You rest in a cozy bed at the tavern and recover {heal_amount} HP.")
          typingPrint("You sleep peacefully and wake refreshed.")
        else:
          typingPrint("You're already at full health!")

      elif choice == 3:
        _manage_inventory_and_deck(player_state)

      elif choice == 4:
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
        speed_choice = get_valid_input(
          "\nSelect text speed:\n"
          "1) Instant (no delays)\n"
          "2) Fast (half speed)\n"
          "3) Normal (default)\n"
          "4) Slow (double speed)\n"
          "\t>",
          [1, 2, 3, 4]
        )
        set_speed_multiplier(speed_choice)
        player_state['speed'] = speed_choice
        speed_names = {1: "Instant", 2: "Fast", 3: "Normal", 4: "Slow"}
        typingPrint(f"Text speed set to {speed_names[speed_choice]}.")

      elif choice == 6:
        if not player_state.get("shop_unlocked", False):
          typingPrint("The naukin shopkeep eyes you suspiciously. It would probably be best to return later.")
        else:
          _run_shop(player_state)

      elif choice == 7:
        if not player_state.get("blacksmith_unlocked", False):
          typingPrint("The naukin blacksmith spots your approach and hurriedly closes up shop. It would probably be best to return later.")
        else:
          _run_blacksmith(player_state)

      elif choice == 8:
        _run_training(player_state)

      elif choice == 9:
        typingPrint("\nGathering your belongings, you bid farewell to Thessa and Ascus.")
        typingPrint("Perhaps you'll return someday...")
        return player_state


def _initialize_inventory_state(player_state):
    if not isinstance(player_state.get("deck"), list):
      player_state["deck"] = []

    if not isinstance(player_state.get("inventory"), list):
      player_state["inventory"] = list(player_state["deck"])

    missing_deck_cards = _sync_deck_to_inventory(player_state)
    if missing_deck_cards > 0 and not player_state["deck"] and player_state["inventory"]:
      # Keep a playable deck for migrated states where ownership data was incomplete.
      player_state["deck"].append(player_state["inventory"][0])


def _card_count_map(cards):
    counts = {}
    for card in cards:
      counts[card.name] = counts.get(card.name, 0) + 1
    return counts


def _sync_deck_to_inventory(player_state):
    inventory_counts = _card_count_map(player_state["inventory"])
    deck_counts = {}
    kept_deck = []
    removed_count = 0

    for card in player_state["deck"]:
      in_deck = deck_counts.get(card.name, 0)
      max_owned = inventory_counts.get(card.name, 0)
      if in_deck < max_owned:
        kept_deck.append(card)
        deck_counts[card.name] = in_deck + 1
      else:
        removed_count += 1

    player_state["deck"] = kept_deck
    return removed_count


def _manage_inventory_and_deck(player_state):
    while True:
      inventory_counts = _card_count_map(player_state["inventory"])
      deck_counts = _card_count_map(player_state["deck"])

      typingPrint("\n" + "="*50)
      typingPrint("INVENTORY AND DECK")
      typingPrint("="*50)
      typingPrint(f"Owned cards: {len(player_state['inventory'])}")
      typingPrint(f"Deck cards: {len(player_state['deck'])}")

      choice = get_valid_input(
        "\n1) View active deck\n"
        "2) View owned inventory\n"
        "3) Add card to deck\n"
        "4) Remove card from deck\n"
        "0) Back\n"
        "\t>",
        [0, 1, 2, 3, 4],
      )

      if choice == 0:
        return

      if choice == 1:
        if not player_state["deck"]:
          typingPrint("Your active deck is empty.")
          continue
        typingPrint("\nActive deck:", delay=0)
        for index, card in enumerate(player_state["deck"], start=1):
          typingPrint(f"{index}) {card.name}", delay=0)
        continue

      if choice == 2:
        if not player_state["inventory"]:
          typingPrint("You do not own any cards yet.")
          continue
        typingPrint("\nOwned cards:", delay=0)
        for card_name in sorted(inventory_counts):
          owned = inventory_counts[card_name]
          in_deck = deck_counts.get(card_name, 0)
          available = owned - in_deck
          typingPrint(
            f"{card_name} | Owned: {owned} | In deck: {in_deck} | Available: {available}",
            delay=0,
          )
        continue

      if choice == 3:
        add_options = []
        for card_name in sorted(inventory_counts):
          available = inventory_counts[card_name] - deck_counts.get(card_name, 0)
          if available > 0:
            sample_card = next(card for card in player_state["inventory"] if card.name == card_name)
            add_options.append((card_name, sample_card, available))

        if not add_options:
          typingPrint("No owned cards are available to add to your deck.")
          continue

        typingPrint("\nChoose a card to add to your deck (0 to cancel):", delay=0)
        valid_choices = [0]
        for index, (card_name, _, available) in enumerate(add_options, start=1):
          typingPrint(f"{index}) {card_name} (available: {available})", delay=0)
          valid_choices.append(index)

        add_choice = get_valid_input("\t>", valid_choices)
        if add_choice == 0:
          continue

        chosen_name, chosen_card, _ = add_options[add_choice - 1]
        player_state["deck"].append(chosen_card)
        typingPrint(f"Added {chosen_name} to your active deck.")
        continue

      if choice == 4:
        if not player_state["deck"]:
          typingPrint("Your active deck is already empty.")
          continue

        typingPrint("\nChoose a deck card to remove (0 to cancel):", delay=0)
        valid_choices = [0]
        for index, card in enumerate(player_state["deck"], start=1):
          typingPrint(f"{index}) {card.name}", delay=0)
          valid_choices.append(index)

        remove_choice = get_valid_input("\t>", valid_choices)
        if remove_choice == 0:
          continue

        removed_card = player_state["deck"].pop(remove_choice - 1)
        typingPrint(f"Removed {removed_card.name} from your active deck.")


def _display_inventory(player_state):
    """
    Backward-compatible wrapper.
    """
    _manage_inventory_and_deck(player_state)


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
    
    # Get training bonuses
    training_values = _training_values(player_state)
    
    # Run multi-battle adventuring loop
    adventure_result = adventuring_loop(
        player_state['current_biome'],
        player_state['current_biome_tier'],
        player_state['max_hp'],
        player_deck=player_state['deck'],
        player_inventory=player_state['inventory'],
        player_hand_limit=hand_limit + training_values['hand_bonus'],
        player_start_shield=training_values['starting_shield'],
      player_class=player_state.get('class', charclass),
      player_level=max(1, player_state.get('level', 1)),
    )
    
    if adventure_result is None:
        typingPrint("The adventure failed to start. You return to town.")
        return player_state
    
    # Update HP from adventure
    player_state['current_hp'] = max(0, adventure_result['player_hp'])
    
    # Apply training recovery if player survived
    recovery_percent = training_values['recovery_percent']
    if recovery_percent > 0 and player_state['current_hp'] > 0:
      recovery_amount = math.ceil(player_state['max_hp'] * (recovery_percent / 100))
      hp_before_recovery = player_state['current_hp']
      player_state['current_hp'] = min(player_state['max_hp'], player_state['current_hp'] + recovery_amount)
      actual_heal = player_state['current_hp'] - hp_before_recovery
      if actual_heal > 0:
        typingPrint(f"Training bonus: you recover {actual_heal} HP after returning to town.")
    
    # Handle victory/defeat with rewards from adventure
    if adventure_result['result'] == 'victory':
        _handle_adventure_victory(player_state, adventure_result)
    else:
        _handle_adventure_defeat(player_state, adventure_result)
    
    return player_state


def _xp_needed_for_next_level(current_level):
    """
    Calibrated for current adventure rewards (tier scaling + streak multipliers).
    Growth is mildly quadratic: faster than linear, slower than exponential.
    """
    normalized_level = max(1, int(current_level))
    step = normalized_level - 1
    return 220 + (120 * step) + (22 * step * step)


def _handle_adventure_victory(player_state, adventure_result):
    """
    Handle a successful multi-battle adventure.
    Player keeps all loot regardless of difficulty.
    """
    typingPrint("\n" + Fore.GREEN + "ADVENTURE COMPLETE!" + Style.RESET_ALL)
    typingPrint("You return to Ascus, victorious!")
    
    # Use rewards from adventure
    xp_gained = adventure_result.get('total_xp', 0)
    gold_gained = adventure_result.get('total_gold', 0)
    
    player_state['xp'] += xp_gained
    player_state['gold'] += gold_gained
    
    typingPrint(f"Total rewards: {xp_gained} XP and {gold_gained} gold over {adventure_result['rounds']} battles!")
    
    # Check for level up (only after XP is secured in town)
    xp_for_level = _xp_needed_for_next_level(player_state['level'])
    while player_state['xp'] >= xp_for_level:
        player_state['level'] += 1
        player_state['xp'] -= xp_for_level
        player_state['max_hp'] += 5
        player_state['current_hp'] = player_state['max_hp']
        xp_for_level = _xp_needed_for_next_level(player_state['level'])
        typingPrint(f"\n" + Fore.YELLOW + f"LEVEL UP! You are now level {player_state['level']}!" + Style.RESET_ALL)

    if (
      not player_state.get("shop_unlocked", False)
      and player_state.get("current_biome") == 1
      and player_state.get("current_biome_tier") == 1
    ):
      player_state["shop_unlocked"] = True
      typingPrint("The shopkeep looks you up and down, sighs, and opens the door to let you in.")

    blacksmith_unlock_milestones = {(1, 3), (2, 2), (3, 1)}
    if (
      not player_state.get("blacksmith_unlocked", False)
      and (player_state.get("current_biome"), player_state.get("current_biome_tier")) in blacksmith_unlock_milestones
    ):
      player_state["blacksmith_unlocked"] = True
      typingPrint("A heavy voice calls out from a nearby forge: \"You look ready for real steel. Come see me.\"")


def _handle_adventure_defeat(player_state, adventure_result):
    """
    Handle a failed or retreated adventure.
    Reward retention depends on difficulty setting.
    """
    typingPrint("\n" + Fore.RED + "RETREAT!" + Style.RESET_ALL)
    
    xp_earned = adventure_result.get('total_xp', 0)
    gold_earned = adventure_result.get('total_gold', 0)
    
    if player_state['current_hp'] <= 0:
        typingPrint("You were defeated and forced to retreat!")
    else:
        typingPrint("You retreated to town before completing the area.")
    
    # Apply difficulty-based penalties
    if player_state['difficulty'] == 'easy':
        # Keep all loot
        player_state['xp'] += xp_earned
        player_state['gold'] += gold_earned
        typingPrint(f"You keep all your earnings: {xp_earned} XP and {gold_earned} gold.")
    elif player_state['difficulty'] == 'normal':
        # Lose 50% of loot
        xp_kept = xp_earned // 2
        gold_kept = gold_earned // 2
        player_state['xp'] += xp_kept
        player_state['gold'] += gold_kept
        typingPrint(f"You lost half your earnings in the retreat.")
        typingPrint(f"Kept: {xp_kept} XP and {gold_kept} gold (lost {xp_earned - xp_kept} XP and {gold_earned - gold_kept} gold).")
    else:  # punishing
        # Lose all loot
        typingPrint(f"You lost all your earnings in the retreat: {xp_earned} XP and {gold_earned} gold.")
    
    # Check for level up after secured XP is applied in town
    xp_for_level = _xp_needed_for_next_level(player_state['level'])
    while player_state['xp'] >= xp_for_level:
      player_state['level'] += 1
      player_state['xp'] -= xp_for_level
      player_state['max_hp'] += 5
      if player_state['current_hp'] > 0:
        player_state['current_hp'] = player_state['max_hp']
      xp_for_level = _xp_needed_for_next_level(player_state['level'])
      typingPrint(f"\n" + Fore.YELLOW + f"LEVEL UP! You are now level {player_state['level']}!" + Style.RESET_ALL)

    if (
      not player_state.get("shop_unlocked", False)
      and player_state.get("current_biome") == 1
      and player_state.get("current_biome_tier") == 1
    ):
      player_state["shop_unlocked"] = True
      typingPrint("The shopkeep looks you up and down, sighs, and opens the door to let you in.")

    blacksmith_unlock_milestones = {(1, 3), (2, 2), (3, 1)}
    if (
      not player_state.get("blacksmith_unlocked", False)
      and (player_state.get("current_biome"), player_state.get("current_biome_tier")) in blacksmith_unlock_milestones
    ):
      player_state["blacksmith_unlocked"] = True
      typingPrint("A heavy voice calls out from a nearby forge: \"You look ready for real steel. Come see me.\"")


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


def run_tutorial(seed=7):
  """
  Tiny, self-contained player-controlled tutorial combat:
  - Uses 3 example cards.
  - Fights one simple enemy.
  - Shows step-based tutorial tips while preserving player control.
  """
  random.seed(seed)

  player_name = "Player"
  player_hp = 20

  enemy = {
    "name": "Strange Pirate",
    "hp": 20,
    "attack_min": 5,
    "attack_max": 10,
  }

  cards = [
    {"name": "Strike", "cost": 1, "damage": 5, "heal": 0},
    {"name": "Heavy Blow", "cost": 2, "damage": 8, "heal": 0},
    {"name": "First Aid", "cost": 1, "damage": 0, "heal": 3},
  ]

  deck = cards * 3
  random.shuffle(deck)
  hand = []

  max_hand = 3
  max_dice = 2
  round_number = 1
  max_player_hp = player_hp

  shown_roll_tip = False
  shown_slot_tip = False
  shown_activate_tip = False

  typingPrint("\n=== Tutorial Combat ===")
  typingPrint(f"{player_name} HP: {player_hp} | {enemy['name']} HP: {enemy['hp']}")

  while player_hp > 0 and enemy["hp"] > 0:
    typingPrint(f"\n--- Round {round_number} ---")

    while len(hand) < max_hand and deck:
      hand.append(deck.pop())

    if hand:
      typingPrint("Your hand:")
      for index, card in enumerate(hand, start=1):
        typingPrint(
          f"  {index}) {card['name']} "
          f"(cost {card['cost']}, dmg {card['damage']}, heal {card['heal']})"
        )

    if not shown_roll_tip:
      typingPrint(
        Fore.CYAN
        + "[Tutorial] Step 1: Rolling Dice\n"
        + "You roll dice at the start of your turn.\n"
        + "Each die can power one card if its value meets the card cost."
        + Style.RESET_ALL
      )
      shown_roll_tip = True

    dice_pool = [random.randint(1, 6) for _ in range(max_dice)]
    _display_dice_pool_ascii(dice_pool, header="You roll:")

    while hand and dice_pool and enemy["hp"] > 0:
      if not shown_slot_tip:
        typingPrint(
          Fore.CYAN
          + "[Tutorial] Step 2: Slotting Dice into Cards\n"
          + "Choose a card, then choose which die to spend on it.\n"
          + "A die can only be slotted if the die value is at least equal to the card cost."
          + Style.RESET_ALL
        )
        shown_slot_tip = True

      typingPrint("\nChoose a card to play (0 to end your turn):")
      for index, card in enumerate(hand, start=1):
        typingPrint(
          f"  {index}) {card['name']} "
          f"(cost {card['cost']}, dmg {card['damage']}, heal {card['heal']})"
        )
      chosen_card_input = get_valid_input(
        "\t>",
        list(range(0, len(hand) + 1)),
      )

      if chosen_card_input == 0:
        typingPrint("You end your turn.")
        break

      chosen_card_index = chosen_card_input - 1
      chosen_card = hand[chosen_card_index]

      _display_dice_pool_ascii(dice_pool, header="Available dice:")
      chosen_die_input = get_valid_input(
        "Choose a die to slot:\n\t>",
        list(range(1, len(dice_pool) + 1)),
      )
      chosen_die_index = chosen_die_input - 1
      chosen_die_value = dice_pool[chosen_die_index]

      if chosen_die_value < chosen_card["cost"]:
        typingPrint("That die is too low for this card. Pick another card.")
        continue

      if not shown_activate_tip:
        typingPrint(
          Fore.CYAN
          + "[Tutorial] Step 3: Activating Card Effects\n"
          + "After a valid die is slotted, the card effect triggers immediately."
          + Style.RESET_ALL
        )
        shown_activate_tip = True

      spent_die = dice_pool.pop(chosen_die_index)
      enemy["hp"] -= chosen_card["damage"]
      player_hp = min(max_player_hp, player_hp + chosen_card["heal"])

      typingPrint(
        f"Played {chosen_card['name']} (cost {chosen_card['cost']}, used die {spent_die}) -> "
        f"Enemy -{chosen_card['damage']} HP, You +{chosen_card['heal']} HP"
      )

      hand.pop(chosen_card_index)

      if enemy["hp"] > 0:
        typingPrint(f"Current HP -> {player_name}: {player_hp} | {enemy['name']}: {enemy['hp']}")

    if enemy["hp"] <= 0:
      typingPrint(f"{enemy['name']} is defeated!")
      break

    enemy_damage = random.randint(enemy["attack_min"], enemy["attack_max"])
    player_hp -= enemy_damage
    typingPrint(f"{enemy['name']} attacks for {enemy_damage} damage.")

    typingPrint(f"End round -> {player_name}: {max(0, player_hp)} HP | {enemy['name']}: {max(0, enemy['hp'])} HP")
    round_number += 1

  result = "victory" if enemy["hp"] <= 0 else "defeat"
  typingPrint(f"\nResult: {result.upper()} in {round_number} round(s).")
  return result

def _debug_prompt_int(prompt_text, default_value, minimum_value=1, maximum_value=None):
  raw = input(f"{prompt_text} [{default_value}]\n\t>").strip()
  if raw == "":
    return default_value
  if not raw.isdigit():
    typingPrint("Invalid number. Keeping previous value.")
    return default_value

  parsed = int(raw)
  if parsed < minimum_value:
    typingPrint(f"Value must be at least {minimum_value}. Keeping previous value.")
    return default_value
  if maximum_value is not None and parsed > maximum_value:
    typingPrint(f"Value must be at most {maximum_value}. Keeping previous value.")
    return default_value
  return parsed


def _build_debug_card_family_lookup():
  family_lookup = {}
  for value in globals().values():
    if not isinstance(value, CARD):
      continue

    cleaned_id = _sanitize_card_id(value.id)
    if len(cleaned_id) < 3 or not cleaned_id[:3].isdigit():
      continue

    family_code = cleaned_id[:2]
    tier_code = int(cleaned_id[2])
    base_name, _ = _card_name_suffix(value.name)

    if family_code not in family_lookup:
      family_lookup[family_code] = {
        "name": base_name,
        "tiers": {},
      }

    if tier_code not in family_lookup[family_code]["tiers"]:
      family_lookup[family_code]["tiers"][tier_code] = value

    if tier_code == 0:
      family_lookup[family_code]["name"] = base_name

  return family_lookup


def _resolve_debug_family_code(user_text, family_lookup):
  cleaned = user_text.strip().lower()
  if not cleaned:
    return None

  if cleaned.isdigit():
    numeric = int(cleaned)
    if 0 <= numeric <= 80:
      candidate = f"{numeric:02d}"
      if candidate in family_lookup:
        return candidate

  for family_code, family_data in family_lookup.items():
    if family_data["name"].lower() == cleaned:
      return family_code

  return None


def _resolve_debug_tier_code(user_text):
  tier_aliases = {
    "0": 0,
    "base": 0,
    "1": 1,
    "x": 1,
    "2": 2,
    "x+": 2,
    "xx": 2,
    "x2": 2,
    "3": 3,
    "y": 3,
    "4": 4,
    "y+": 4,
    "yy": 4,
    "y2": 4,
    "5": 5,
    "xy": 5,
  }
  return tier_aliases.get(user_text.strip().lower())


def _debug_fill_deck_by_family_tier(current_deck):
  family_lookup = _build_debug_card_family_lookup()
  if not family_lookup:
    typingPrint("No card families available.")
    return current_deck

  typingPrint("\nDeck fill mode: choose family by name or code (00-80), then tier by name/code (0-5).")
  typingPrint("Tier names: 0=base, 1=x, 2=X, 3=y, 4=Y, 5=XY")

  while True:
    family_input = input("Family (or 'done' to finish)\n\t>").strip()
    if family_input.lower() in ["done", "q", "quit", "exit"]:
      break

    family_code = _resolve_debug_family_code(family_input, family_lookup)
    if family_code is None:
      typingPrint("Unknown family. Try a valid name or code from 00 to 80.")
      continue

    family_data = family_lookup[family_code]
    typingPrint(f"Selected family {family_code} - {family_data['name']}")
    available_tiers = sorted(family_data["tiers"].keys())
    typingPrint(f"Available tiers: {available_tiers}")

    tier_input = input("Tier (name or code 0-5)\n\t>").strip()
    tier_code = _resolve_debug_tier_code(tier_input)
    if tier_code is None:
      typingPrint("Invalid tier input.")
      continue
    if tier_code not in family_data["tiers"]:
      typingPrint(f"Tier {tier_code} is not defined for this family.")
      continue

    copies = _debug_prompt_int("How many copies to add", 1, minimum_value=1, maximum_value=20)
    chosen_card = family_data["tiers"][tier_code]
    for _ in range(copies):
      current_deck.append(chosen_card)
    typingPrint(f"Added {copies}x {chosen_card.name}.")

  typingPrint(f"Deck now has {len(current_deck)} card(s).")
  return current_deck


def run_debug_battle_lab():
  global max_player_health, currenthp, hand_limit, dice_limit, play

  typingPrint("\n=== DEBUG BATTLE LAB ===")
  typingPrint("Run infinite test battles and tweak stats between fights.\n")

  debug_max_hp = max_player_health
  debug_current_hp = currenthp
  debug_hand_limit = hand_limit
  debug_dice_limit = dice_limit
  debug_biome = 1
  debug_biome_tier = 1
  debug_player_deck = list(deck) if deck else [club, rustydagger]

  while True:
    typingPrint("\nCurrent debug settings:")
    typingPrint(
      f"HP: {debug_current_hp}/{debug_max_hp} | Dice: {debug_dice_limit} | Hand: {debug_hand_limit} | "
      f"{_format_biome_tier_label(debug_biome, debug_biome_tier)} | Deck: {len(debug_player_deck)} cards"
    )

    choice = get_valid_input(
      "\n1) Start test battle\n2) Set max HP\n3) Set current HP\n4) Set dice limit\n5) Set hand limit\n6) Set biome\n7) Set biome tier\n8) Fill deck (family+tier)\n9) Reset HP to max\n10) Quit debug mode\n\t>",
      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    )

    if choice == 1:
      max_player_health = debug_max_hp
      currenthp = debug_current_hp
      hand_limit = debug_hand_limit
      dice_limit = debug_dice_limit

      encounter_result = run_basic_combat_loop(
        debug_biome,
        debug_biome_tier,
        player_hp=debug_current_hp,
        player_max_hp=debug_max_hp,
        player_deck=debug_player_deck,
      )

      if encounter_result is None:
        typingPrint("Battle could not start with current settings.")
        continue

      debug_current_hp = max(0, encounter_result["player_hp"])
      typingPrint(
        f"Battle result: {encounter_result['result']} | "
        f"Ending HP: {debug_current_hp}/{debug_max_hp}"
      )

      if debug_current_hp <= 0:
        typingPrint("You were defeated. Resetting current HP to max for the next test.")
        debug_current_hp = debug_max_hp

    elif choice == 2:
      debug_max_hp = _debug_prompt_int("Set max HP", debug_max_hp, minimum_value=1)
      debug_current_hp = min(debug_current_hp, debug_max_hp)
    elif choice == 3:
      debug_current_hp = _debug_prompt_int("Set current HP", debug_current_hp, minimum_value=1, maximum_value=debug_max_hp)
    elif choice == 4:
      debug_dice_limit = _debug_prompt_int("Set dice limit", debug_dice_limit, minimum_value=1, maximum_value=10)
    elif choice == 5:
      debug_hand_limit = _debug_prompt_int("Set hand limit", debug_hand_limit, minimum_value=1, maximum_value=10)
    elif choice == 6:
      debug_biome = _debug_prompt_int("Set biome", debug_biome, minimum_value=1, maximum_value=6)
    elif choice == 7:
      debug_biome_tier = _debug_prompt_int("Set biome tier", debug_biome_tier, minimum_value=1, maximum_value=3)
    elif choice == 8:
      debug_player_deck = []
      debug_player_deck = _debug_fill_deck_by_family_tier(debug_player_deck)
      if not debug_player_deck:
        debug_player_deck = [club, rustydagger]
        typingPrint("Deck was empty; restored fallback deck.")
    elif choice == 9:
      debug_current_hp = debug_max_hp
      typingPrint(f"Current HP reset to {debug_current_hp}/{debug_max_hp}.")
    else:
      play = "quit"
      typingPrint("Exiting debug mode.")
      return


if charname.lower() == "debug":
  run_debug_battle_lab()







while play!="quit":
  x=get_valid_input("Play the tutorial?\n1) Yes\n2) No\n\t>", [1, 2])
  if x == 1:
    typingPrint("The sea air blows around you as you watch the waves break against your ship. You hoped to make it to your destination without any storms, but it seems luck is not on your side. The sea churns and grows violent as you sail under the rolling black clouds. You've never seen clouds quite so dark. If you weren't on the open ocean, you'd think it was smoke.\n", delay=0.75)
    typingPrint("The deck lurches, as though colliding with a rock, but as the captain orders the sailors about, you take a peek over the side and find nothing that could have caused the movement, just the shadows of marine life zipping around the beleagered boat. But they're too fast. A loud splash sounds, and you whip around to see a silhouette behind you. A sailor you've never met stands, sword drawn, dripping wet. It opens it's mouth, letting out a low whistle, before raising its blade and charging you.\n", delay=0.75)
    result = run_tutorial()
    if result == "victory":
        typingPrint("You stand over the defeated pirate. The strange man looks up at you, then begins to... melt. He dissappears, seeping into the cracks in the boards of the ship, leaving you alone. Truly alone, because as you look around, you can find none of the other sailors manning the ship. The storm has calmed, but the clouds still fill the sky. The sea is eerily still. Then you feel something. A terrible rumbling, growing all around you. The ship explodes beneath your feet, and you are sent sailing into the air. You manage to get a look at a massive creature, a sea serpent of some kind, emerging from where you were just standing, before you collide with the water and everything goes black", delay=0.75)
    elif result == "defeat":
        typingPrint("You lie on your back, defeated. You try to inch away from the strange pirate, but with the rail behind you and his blade before you, you have nowhere to go. A rumbling sounds all around the ship, and the pirate finally takes it's unearthly dark eyes off you as it looks around frantically. You take the chance to scramble to the side and put some distance between you and your foe. You grab a stry chunk of wood as a primitive defensive club, but when you turn around you witness the pirate diving off the side of the ship. You rush to the side to see where he went, but despite searching for a few minutes you see nothing. You turn around and are faced with something infinitely worse. A massive sea serpent, 300, no 400 feet tall at least, looms above your ship, huge glowing blue eyes focused unblinking at you. Your head begins to swim, and you collapse against the rail for support. The eyes seem to grow in both size and intensity, and soon you can see nothing else. You try to turn, but are unable to escape the blue light. Soon, your mind collapses, and the world flees from you.", delay=0.75)
  typingPrint("...")
  typingPrint("...")
  typingPrint("...")
  typingPrint("...")
  typingPrint("You remember the smell of the sea...", delay=0.75)
  typingPrint("...")
  typingPrint("...")
  typingPrint("You remember the swaying of the ship...", delay=0.75)
  typingPrint("...")
  typingPrint("...")
  typingPrint("You remember..."+Style.BRIGHT+Fore.CYAN+ "lightning...", delay=0.75)
  typingPrint(Style.RESET_ALL + "...")
  typingPrint(Style.DIM+Fore.CYAN+"Wind...", delay=0.75)
  typingPrint(Style.RESET_ALL + "...")
  typingPrint("And then the icy grip of the sea...", delay=0.75)
  typingPrint("...")
  typingPrint("...")
  typingPrint("...")
  typingPrint("...")
  x=input(Style.BRIGHT + Fore.RED + "GET UP?" + Style.RESET_ALL + "\n\t>")
  typingPrint("As life slowly awakens in your head, you feel coarse sand beneath you and the gentle nudging of waves against your leg. Your first attempt to move your arms fails you, but after a few moments you're able to place them underneath you ans shakily stand. You see the wide golden expanse of plains ahead.\n", delay=0.75)
  typingPrint("You brush off some of the sand and turn to see what's left of the crash. However...\n", delay=0.75)
  typingPrint("You are not on a seaside beach or some lonely island.\n", delay=0.75)
  typingPrint("Before you is a lake. A large lake, to be sure, but you scan the bredth of it easily without squinting.\n", delay=0.75)
  typingPrint("The only connections this lake has are a small creek trickling in from the north, and a slow, shallow stream exiting it to the west.\n", delay=0.75)
  typingPrint("Certainly confusing, but you have more things to worry about now. Some of the ship you were on seems to have made it to this strange lakeside alongside you, but you see no evidence of other survivors. You spend the rest of the day collecting debris and searching wreckage. You manage to scrounge together some remnants of what was probably the sail, and set up a simple shelter for the night.\n", delay=0.75)
  typingPrint("The night, thankfully, passes quickly. As you make your way outside in the morning, you see small tracks left by some evening passerby, not far from your makeshift tent. Just the thought of something else alive makes you realize how hungry you are. Maybe you can find some animal to eat, or, if you're lucky, a tavern. You slide a small metal shard into your pocket to use as a knife, and break off an unrotted piece of wood as a primitive club.\n")
  typingPrint("By midday, you are travelling through those beautiful golden stalks. This looks like farmland. Hopefully it's farmer is nearby. You hear a rustling to your side, and turn to investigate. You'd hoped to find help, but your luck has betrayed you once again.\n")
  poison_counter = 0
  dice = []
  cards_in_hand = []
  deck = [club, rustydagger]
  hand_limit = 2
  dice_limit = 2
  burn_counter = 0
  lock_counter = 0
  freeze_counter = 0
  bleed_counter = 0
  blind_counter = 0
  shield_counter = 0
  current_biome = 1
  current_biome_tier = 1
  current_player_health = max_player_health

  player_xp = 0
  player_gold = 0
  player_level = 1

  player_state = {
    "name": charname,
    "class": charclass,
    "current_hp": current_player_health,
    "max_hp": max_player_health,
    "xp": player_xp,
    "gold": player_gold,
    "difficulty": "normal",  # Can be "easy", "normal", or "punishing"
    "speed": speed,  # Text speed: 1=instant, 2=fast, 3=normal, 4=slow
    "inventory": list(deck),
    "deck": deck,
    "level": player_level,
    "current_biome": current_biome,
    "current_biome_tier": current_biome_tier
  }

  result_data = adventuring_loop(1, 1, max_player_health, player_class=charclass, player_level=player_level)
  #  Create the 'safe zone
  first_time = 0
  while play != "quit":
    if first_time == False:
      # Check if player was defeated (forced retreat with 0 HP)
      if result_data and result_data.get("result") == "retreat" and result_data.get("player_hp", 0) <= 0:
        first_time = True
        typingPrint("You stagger to relative safety before collapsing on the ground. That last fight got you good. Luckily, you had some straps leftover from the sail that you use to make a makeshift bandage.\n", delay=0.75)
        typingPrint("As you finish wrapping, you think you hear the sound of carriage wheels. You must be getting delirious. Regardless, you limp towards the sound, hoping beyond hope to find some sort of aid.\n", delay=0.75)
        typingPrint("You stumble out onto a worn dirt road. Slowly getting further and further is a wagon. You weakly croak, wave your arms, but you seem unable to get the attention of the wagon driver.\n", delay=0.75)
        typingPrint("With all your remaining strength you let out a shout, but the effort leaves you nearly breathless, and you fall to your knees. As your vision fades. You can see the wagon slow, and a silhouette hop off and rush towards you.\n", delay=0.75)
        typingPrint("What seems to be either only a few moments later, or a dew decades, you are able to again open your eyes. You are lying in a bed, in a room faintly lit by torchlight. You try to sit up, but wince in pain.\n", delay=0.75)
        typingPrint("Your wounds are bandaged. A strange salve is on a scratch on your arm. It has an unpleasant smell, but you can't feel any pain from it. As you pat yourself down, inspecting your wrappings, a voice clears from the corner of the room.\n", delay=0.75)
        typingPrint('"You took quite the beating, stranger," says the voice. It is somehow both very deep, yet still soft. A silhouette forms and steps into the light, and you are finally able to get a good look at your savior.\n', delay=0.75)
        typingPrint("You recognize them as a bovari, one of the ox-folk. The bovari stands about as tall as you, but her horns curl up another foot. Her impressive arms split at the elbows, ending in four powerful hands, the two left ones holding small vials.\n", delay=0.75)
        typingPrint('"Not many travellers pass through here," she says, wiping away the salve from your arm before applying a new coat. "We can\'t let the few that do make it croak on us, can we?"\n', delay=0.75)
        typingPrint(f'As she works, you ask for her name. "Thessa", she says. "What\'s yours?" "{charname}," you reply. "Don\'t know where you were headed, but you\'ve made it to Ascus." She says this like it\'s supposed to mean something to you, but you\'ve never heard the name before.\n', delay=0.75)
        typingPrint('After a few moments tending to your wounds, she helps you up. The salve is working miracles, as you\'re able to make it out the door and down the stairs without much help.\n', delay=0.75)
        typingPrint("You're in a modest tavern, filled with ratmen. The Naukin are a reclusive people, and they validate that stereotype, eyeing you and hushing their conversations as you enter the room.\n", delay=0.75)
        typingPrint('Thessa leads you to the bar counter and helps you into a seat, before going behind and fixing a few drinks. "Don\'t mind them, they\'re always wary of outsiders." She slides you a drink, before getting to work on another for another customer.\n', delay=0.75)
        typingPrint("You down the drink, a warm, earthy beverage that fills your stomach. \"What do I owe you?\", you ask, sheepishly patting youreself down for a coinpurse you both know isn't there.\n", delay=0.75)
        typingPrint("The woman laughs. \"A stack of clean dishes is a good start\", she says, gesturing to the kitchen.\n", delay=0.75)
      # Check if player successfully completed first adventure (beat legendary enemy)
      elif result_data and result_data.get("result") == "victory":
        first_time = True
        typingPrint("You pat yourself down, surprised you made it out with as few scratches as you did. Looking around, you spot a faint trail of smoke in the distance, almost like from a chimney. You decide to head towards it.\n", delay=0.75)
        typingPrint("After about another hour of hiking through wheat fields, yyou can finally see a small village in the distance. A few houses and other buildings are loosely scattered around a sturdy-looking tavern, and the scent of fresh bread drifts towards your nose.\n", delay=0.75)
        typingPrint("As you enter the village, the citizens grow quiet, and you can feel all eyes on you. The denizens seem to be mostly Naukin, rat-folk known for being extremely reclusive and secluded by nature.\n", delay=0.75)
        typingPrint("The tavern greets you with mostly the same reaction, with one notable excepetion: a large friendly Bovari bartender. The ox-folk warmly gestures you over, greeting you with a drink ready before you even sit down.\n", delay=0.75)
        typingPrint('"Welcome to Ascus, traveller," says the bartender. "My name is Thessa. We don\'t get many visitors here, so don\'t mind the strange looks. Took them a couple years to get used to me," she chuckles.\n', delay=0.75)
        typingPrint('"What can I do you for?", Thessa asks, her four hands cleaning the counter and pouring drinks with remarkable dexterity.')
        typingPrint("You sip a drink and feel it warm your chest. You patch your wounds, and ask for a room. \"How long will you be staying?\", the barkeep asks.")
        typingPrint("You look at your ragged clothes and bandaged hands. There's no cities you can reach, and you'd be too poor to make it if you could.")
        typingPrint("You'll be stuck here for a while. Might as well make some coin adventuring.")
      # Check if player voluntarily retreated (retreat with HP > 0)
      elif result_data and result_data.get("result") == "retreat" and result_data.get("player_hp", 0) > 0:
        first_time = True
        typingPrint("You make your way back through the wilderness, following the path you took earlier. After some time, you spot smoke rising from a chimney in the distance.\n", delay=0.75)
        typingPrint("You arrive at a small village nestled among wheat fields. The buildings are modest but sturdy, clustered around a welcoming tavern.\n", delay=0.75)
        typingPrint("As you enter the village, you notice the inhabitants - mostly Naukin, the reclusive rat-folk - eye you curiously. They're not used to outsiders.\n", delay=0.75)
        typingPrint("The tavern offers a warm respite. Behind the bar, a large Bovari with impressive horns and four arms greets you with a friendly wave.\n", delay=0.75)
        typingPrint('"Welcome to Ascus, traveller!" she says cheerfully. "Name\'s Thessa. Don\'t mind the locals - they warm up eventually. Took me a couple years," she chuckles, sliding you a drink.\n', delay=0.75)
        typingPrint("You accept the drink gratefully and settle in. This seems like as good a base as any for your adventures.")
      safe_town_loop(player_state)