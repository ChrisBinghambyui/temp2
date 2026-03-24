import React from 'react';
import { ArrowRight } from 'lucide-react';

const ProgressionDiagram = () => {
  // Creature card data
  const creatureCards = {
    "Wolf": {
      hp: 10,
      dice: 2,
      abilities: [
        { name: "Bite", requirement: "Any", effect: "Deal 3 damage" },
        { name: "Howl", requirement: "Limit 8", effect: "Heal 2 HP" }
      ]
    },
    "Giant Locust": {
      hp: 12,
      dice: 2,
      abilities: [
        { name: "Swipe", requirement: "Limit 5", effect: "Deal 3 damage, Heal 1 HP" },
        { name: "Swipe", requirement: "Limit 5", effect: "Deal 3 damage, Heal 1 HP" }
      ]
    },
    "Naukin Outcast": {
      hp: 10,
      dice: 2,
      abilities: [
        { name: "Jab", requirement: "Any", effect: "Deal damage equal to die value" },
        { name: "Rusty Dagger", requirement: "Odd only", effect: "Deal 2 damage" }
      ]
    },
    "Dire Wolves": {
      hp: 18,
      dice: 3,
      abilities: [
        { name: "Bite x", requirement: "Any", effect: "Deal damage equal to die value" },
        { name: "Bite y", requirement: "Any", effect: "Deal 4 damage", reusable: true }
      ]
    },
    "Prowling Dellinid": {
      hp: 16,
      dice: 3,
      abilities: [
        { name: "Pounce", requirement: "Any", effect: "Deal 5 + die value damage", oncePerCombat: true },
        { name: "Swipe x", requirement: "Any", effect: "Deal 3 damage + 1 for each use this round", reusable: true }
      ]
    },
    "Juvenile Auroc": {
      hp: 20,
      dice: 3,
      abilities: [
        { name: "Fortify", requirement: "Any", effect: "Gain 3 Shield" },
        { name: "Reflecting Scales", requirement: "Any", effect: "Deal 2 damage, Apply 1 Blind" },
        { name: "Chomp", requirement: "Limit 10", effect: "Deal 10 damage (activates when limit reaches 0)" }
      ]
    },
    "Bovari Bandit": {
      hp: 30,
      dice: 3,
      abilities: [
        { name: "Shortbow x", requirement: "Odd only", effect: "Deal double die value damage" },
        { name: "Dagger x", requirement: "Any", effect: "Deal 3 damage, Apply 1 Poison" },
        { name: "Hype Up", requirement: "Limit 12", effect: "Heal 4 HP, Apply 1 Blind to self and opponent (activates when limit reaches 0)" }
      ]
    },
    "Roaming Gallox": {
      hp: 30,
      dice: 4,
      abilities: [
        { name: "Charge", requirement: "Limit 15", effect: "Deal 8 damage, Gain 3 Shield (activates when limit reaches 0)" },
        { name: "Trample", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Lock" },
        { name: "Gore", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Bleed" }
      ]
    },
    "Lone Plainsdrake": {
      hp: 30,
      dice: 4,
      abilities: [
        { name: "Reflecting Scales x", requirement: "Any", effect: "Deal 4 damage, Apply 2 Blind" },
        { name: "Reflecting Scales y", requirement: "Any", effect: "Apply 2 Blind, Gain 2 Shield" },
        { name: "Mirror Hide", requirement: "Any", effect: "Remove all negative effects from self, Apply them to opponent" },
        { name: "Chomp x", requirement: "Limit 8", effect: "Deal 10 damage (activates when limit reaches 0)" }
      ]
    },
    "Blue Dellinid": {
      hp: 12,
      dice: 2,
      abilities: [
        { name: "Pounce", requirement: "Any", effect: "Deal 5 + die value damage", oncePerCombat: true },
        { name: "Swipe x", requirement: "Any", effect: "Deal 3 damage + 1 for each use this round", reusable: true }
      ]
    },
    "Khinari Exile": {
      hp: 14,
      dice: 2,
      abilities: [
        { name: "Shortbow", requirement: "3 or below", effect: "Deal double die value damage" },
        { name: "Frosted Dagger", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Poison" }
      ]
    },
    "Territorial Whitespike": {
      hp: 16,
      dice: 2,
      abilities: [
        { name: "Gore", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Bleed" },
        { name: "Bellow", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Frozen" }
      ]
    },
    "Khinari Raider": {
      hp: 20,
      dice: 3,
      abilities: [
        { name: "Frosted Spear", requirement: "Minimum 3", effect: "Deal 3 damage", reusable: true },
        { name: "Frosted Dagger x", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Poison and 1 Frozen" },
        { name: "Ice Magic", requirement: "Exactly 2", effect: "Heal 2 HP, Remove all negative effects from self" }
      ]
    },
    "Tundra Boneguard": {
      hp: 24,
      dice: 3,
      abilities: [
        { name: "Splinter", requirement: "Any", effect: "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)" },
        { name: "Shield", requirement: "Even only", effect: "Gain Shield equal to half the die value" },
        { name: "Bash", requirement: "Any", effect: "Deal damage equal to double current shield, then remove all shield" }
      ]
    },
    "Alpha Whitespike": {
      hp: 22,
      dice: 3,
      abilities: [
        { name: "Gore x", requirement: "Any", effect: "Deal 2 + die value damage, On 6: Apply 1 Bleed" },
        { name: "Bellow y", requirement: "Any", effect: "Deal damage equal to die value, On 5-6: Apply 1 Frozen" },
        { name: "Charge", requirement: "Limit 15", effect: "Deal 8 damage, Gain 3 Shield (activates when limit reaches 0)" },
        { name: "Trample", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Lock" }
      ]
    },
    "Veteran Boneguard": {
      hp: 30,
      dice: 4,
      abilities: [
        {name: "Splinter x", requirement: "Any", effect: "Create 2 dice with half the input die value (rounded down)"},
        {name: "Shield x", requirement: "Even only", effect: "Gain shield equal to the die value" },
        {name: "Bash x", requirement: "Any", effect: "Deal damage equal to double current shield, then remove half of current shield (rounded down)"},
        {name: "Frosted Spear x", requirement: "Any", effect: "Deal 3 damage", reusable: true},
      ]
    },
    "Khinari Hunting Party": {
      hp: 30,
      dice: 4,
      abilities: [
        {name: "Splinter y", requirement: "Any", effect: "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded up)"},
        {name: "Fortify x", requirement: "Any", effect: "Gain 4 Shield and inflict 1 blind" },
        {name: "Ice Magic y", requirement: "Max 2", effect: "Heal 2 HP, Remove all negative effects from self"},
        {name: "Control", requirement: "Exactly 1", effect: "Sacrifice 2 hp, draw a new card, and roll a new die"},
        {name: "Frosted Spear x", requirement: "Any", effect: "Deal 3 damage", reusable: true},
      ]
    },
    "Hungry Frost Wyrm": {
      hp: 28,
      dice: 3,
      abilities: [
        {name: "Bite X", requirement: "Any", effect: "Deal damage equal to die value + 2" },
        {name: "Bite Y", requirement: "Any", effect: "Deal 5 damage and heal 1", reusable: true },
        { name: "Bellow y", requirement: "Any", effect: "Deal damage equal to die value, On 5-6: Apply 1 Frozen" }
      ]
    },
    "Naukin Scouts": {
      hp: 16,
      dice: 3,
      abilities: [
        { name: "Jab x", requirement: "Any", effect: "Deal 2 + die value damage" },
        { name: "Jab y", requirement: "Any", effect: "Deal damage equal to die value", reusable: true },
        { name: "Fortify", requirement: "Any", effect: "Gain 3 Shield" }
      ]
    },
    "Skittari Hunters": {
      hp: 18,
      dice: 3,
      abilities: [
        { name: "Snipe", requirement: "Limit 15", effect: "Deal 8 damage, Apply 1 Bleed (activates when limit reaches 0)" },
        { name: "Rusty Dagger x", requirement: "Odd only", effect: "Deal 3 damage" }
      ]
    },
    "Reclaimed Boneguard": {
      hp: 18,
      dice: 3,
      abilities: [
        { name: "Splinter", requirement: "Any", effect: "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)" },
        { name: "Shield", requirement: "Even only", effect: "Gain Shield equal to half the die value" },
        { name: "Bash", requirement: "Any", effect: "Remove all Shield from self, Deal damage equal to double the Shield removed" }
      ]
    },
    "Dire Bear": {
      hp: 28,
      dice: 4,
      abilities: [
        { name: "Swipe y", requirement: "Limit 5", effect: "Deal 5 damage, Heal 2 HP" },
        { name: "Bite y", requirement: "Any", effect: "Deal 4 damage", reusable: true },
        { name: "Roar", requirement: "Exactly 1", effect: "Apply 1 Lock" }
      ]
    },
    "Khinari Bladedancer": {
      hp: 22,
      dice: 4,
      abilities: [
        { name: "Splinter y", requirement: "Any", effect: "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded up)" },
        { name: "Snipe x", requirement: "Limit 15", effect: "Deal 12 damage, Apply 1 Bleed (activates when limit reaches 0)" },
        { name: "Jab y", requirement: "Any", effect: "Deal damage equal to die value", reusable: true }
      ]
    },
    "Naukin Sunstriker": {
      hp: 20,
      dice: 4,
      abilities: [
        { name: "Dagger y", requirement: "Odd only", effect: "Deal 4 damage, Apply 1 Poison" },
        { name: "Sunstrike", requirement: "Limit 4", effect: "Deal 3 damage, Apply 1 Blind" },
        { name: "Mirror Hide y", requirement: "Any", effect: "Double all negative effects on opponent" },
        { name: "Control", requirement: "Exactly 1", effect: "Sacrifice 2 hp, draw a new card, and roll a new die"}
      ]
    }
    ,
    "Verdant Shepherd": {
      hp: 40,
      dice: 4,
      abilities: [
        { name: "Maul X", requirement: "Any", effect: "Deal damage equal to die value + 6" },
        { name: "Bellow x", requirement: "Any", effect: "Deal damage equal to die value, Trigger Poison (deal damage equal to poison counters on opponent, then reduce poison counters by 1)" },
        { name: "Jade Spear", requirement: "Even only", effect: "Apply Poison equal to die value" },
        { name: "Splinter Y", requirement: "Minimum 2", effect: "Sacrifice 2 HP, Create 3 dice with half the input die value (rounded up)" }
      ]
    }
    ,
    "Barkskin Colossus": {
      hp: 50,
      dice: 4,
      abilities: [
        { name: "Splinter X", requirement: "Any", effect: "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)", reusable: true },
        { name: "Swipe X", requirement: "Any", effect: "Deal 2 damage + 2 for each use this round", reusable: true },
        { name: "Charge y", requirement: "Limit 18", effect: "Deal 8 damage, Gain 8 Shield" }
      ]
    }
    ,
    "Emerald Lich": {
      hp: 35,
      dice: 5,
      abilities: [
        { name: "Necromancy", requirement: "Limit 12", effect: "Deal 15 damage, Heal 5 HP" },
        { name: "Afflict", requirement: "Exactly 1", effect: "Apply 2 Poison, Apply 1 Blind" },
        { name: "Shield X", requirement: "Even only", effect: "Gain Shield equal to die value" },
        { name: "Life Drain x", requirement: "Odd only", effect: "Deal damage equal to die value, Heal half the damage dealt (rounded up)" }
      ]
    }
    ,
    "Brass Golem": {
      hp: 24,
      dice: 3,
      abilities: [
        { name: "Bash y", requirement: "Any", effect: "Deal damage equal to double current shield, then remove half of current shield (rounded up)" },
        { name: "Shield y", requirement: "Even only", effect: "Gain Shield equal to half the die value", reusable: true },
        { name: "Fortify", requirement: "Any", effect: "Gain 3 Shield" }
      ]
    },
    "Skittari Looters": {
      hp: 22,
      dice: 3,
      abilities: [
        { name: "Dagger x", requirement: "Any", effect: "Deal 3 damage, Apply 1 Poison" },
        { name: "Shortbow x", requirement: "Odd only", effect: "Deal double die value damage" },
        { name: "Control", requirement: "Exactly 1", effect: "Sacrifice 2 HP, draw a new card, and roll a new die" }
      ]
    },
    "Bloated Zombie": {
      hp: 26,
      dice: 3,
      abilities: [
        { name: "Bite x", requirement: "Any", effect: "Deal damage equal to die value" },
        { name: "Rupture", requirement: "Limit 10", effect: "Deal 8 damage, Apply 2 Poison" },
        { name: "Life Drain", requirement: "Odd only", effect: "Deal damage equal to die value, Heal 1 HP" }
      ]
    },
    "Iron Bulwark": {
      hp: 40,
      dice: 4,
      abilities: [
        { name: "Bash X", requirement: "Any", effect: "Deal damage equal to double current shield, then remove half of current shield (rounded up), Gain 2 Shield", reusable: true },
        { name: "Shield Y", requirement: "Even only", effect: "Gain Shield equal to die value", reusable: true },
        { name: "Fortify X", requirement: "Any", effect: "Gain 5 Shield, Apply 1 Blind" }
      ]
    },
    "Stone Drake": {
      hp: 38,
      dice: 4,
      abilities: [
        { name: "Chomp y", requirement: "Limit 12", effect: "Deal 12 damage" },
        { name: "Reflecting Scales x", requirement: "Any", effect: "Deal 4 damage, Apply 2 Blind" },
        { name: "Petrify", requirement: "On 6", effect: "Apply 2 Lock, Apply 1 Frozen" }
      ]
    },
    "Lost Myrrim": {
      hp: 36,
      dice: 4,
      abilities: [
        { name: "Spectral Strike", requirement: "Any", effect: "Deal damage equal to die value, On 5-6: Apply 1 Bleed" },
        { name: "Phase Shift", requirement: "Exactly 1", effect: "Gain 4 Shield, Remove all negative effects from self" },
        { name: "Haunting Wail", requirement: "Limit 8", effect: "Apply 2 Blind, Apply 1 Lock" }
      ]
    },
    "Fell Lich": {
      hp: 60,
      dice: 5,
      abilities: [
        { name: "Necromancy X", requirement: "Limit 15", effect: "Deal 18 damage, Heal 6 HP" },
        { name: "Afflict X", requirement: "Exactly 1", effect: "Apply 3 Poison, Apply 2 Blind" },
        { name: "Life Drain X", requirement: "Odd only", effect: "Deal damage equal to die value + 2, Heal half the damage dealt (rounded up)" },
        { name: "Soul Rend", requirement: "Minimum 4", effect: "Deal 8 damage, Apply 1 Bleed", reusable: true }
      ]
    },
    "Blighted Auroc": {
      hp: 65,
      dice: 4,
      abilities: [
        { name: "Gore X", requirement: "Any", effect: "Deal 4 + die value damage, On 6: Apply 2 Bleed" },
        { name: "Chomp X", requirement: "Limit 10", effect: "Deal 14 damage, Heal 3 HP" },
        { name: "Plague Breath", requirement: "Even only", effect: "Apply Poison equal to half die value (rounded up)" },
        { name: "Charge X", requirement: "Limit 20", effect: "Deal 10 damage, Gain 10 Shield" }
      ]
    },
    "Khinari Subjugator": {
      hp: 62,
      dice: 5,
      abilities: [
        { name: "Snipe X", requirement: "Limit 18", effect: "Deal 15 damage, Apply 2 Bleed" },
        { name: "Frosted Spear X", requirement: "Any", effect: "Deal 5 damage, On 5-6: Apply 1 Frozen", reusable: true },
        { name: "Dominate", requirement: "Exactly 1", effect: "Apply 2 Lock, Sacrifice 3 HP" },
        { name: "Splinter X", requirement: "Any", effect: "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)", reusable: true }
      ]
    },
    "Steppe Whitespike": {
      hp: 28,
      dice: 3,
      abilities: [
        { name: "Gore y", requirement: "Any", effect: "Deal 3 + die value damage, On 6: Apply 1 Bleed" },
        { name: "Bellow X", requirement: "Any", effect: "Deal damage equal to die value + 2, On 5-6: Apply 2 Frozen" },
        { name: "Trample", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Lock" }
      ]
    },
    "Caghoul Shaman": {
      hp: 26,
      dice: 4,
      abilities: [
        { name: "Lightning Bolt", requirement: "Odd only", effect: "Deal triple die value damage", oncePerCombat: true },
        { name: "Totem", requirement: "Exactly 2", effect: "Gain 5 Shield, Heal 2 HP" },
        { name: "Jab X", requirement: "Any", effect: "Deal 4 + die value damage", reusable: true }
      ]
    },
    "Naukin Outrider": {
      hp: 24,
      dice: 4,
      abilities: [
        { name: "Shortbow X", requirement: "Odd only", effect: "Deal triple die value damage" },
        { name: "Dagger Y", requirement: "Odd only", effect: "Deal 5 damage, Apply 2 Poison" },
        { name: "Evade", requirement: "Exactly 1", effect: "Gain Shield equal to 2 × the number of dice used this turn" }
      ]
    },
    "Hill Giant": {
      hp: 48,
      dice: 4,
      abilities: [
        { name: "Maul Y", requirement: "Any", effect: "Deal damage equal to die value + 8" },
        { name: "Boulder Toss", requirement: "Minimum 4", effect: "Deal 10 damage, Apply 1 Lock", reusable: true },
        { name: "Earthquake", requirement: "Limit 20", effect: "Deal 12 damage, Apply 2 Lock, Apply 1 Frozen" }
      ]
    },
    "Black Roc": {
      hp: 45,
      dice: 4,
      abilities: [
        { name: "Dive Bomb", requirement: "Minimum 5", effect: "Deal 12 damage, Apply 1 Blind" },
        { name: "Talon Strike", requirement: "Any", effect: "Deal damage equal to die value + 3, On 6: Apply 1 Bleed", reusable: true },
        { name: "Screech", requirement: "Exactly 1", effect: "Apply 2 Blind, Apply 1 Lock" }
      ]
    },
    "Whitespike Patriarch": {
      hp: 50,
      dice: 4,
      abilities: [
        { name: "Gore Y", requirement: "Any", effect: "Deal 5 + die value damage, On 5-6: Apply 2 Bleed" },
        { name: "Bellow Y", requirement: "Any", effect: "Deal damage equal to die value + 3, On 5-6: Apply 2 Frozen", reusable: true },
        { name: "Charge X", requirement: "Limit 20", effect: "Deal 10 damage, Gain 10 Shield" },
        { name: "Trample X", requirement: "Any", effect: "Deal damage equal to die value + 2, On 5-6: Apply 2 Lock" }
      ]
    },
    "Thunder Giant": {
      hp: 85,
      dice: 5,
      abilities: [
        { name: "Maul XY", requirement: "Any", effect: "Deal damage equal to die value + 12", reusable: true },
        { name: "Thunderclap", requirement: "Limit 25", effect: "Deal 18 damage, Apply 3 Blind, Apply 2 Lock" },
        { name: "Boulder Toss X", requirement: "Minimum 3", effect: "Deal 12 damage, Apply 2 Lock", reusable: true },
        { name: "Fortify Y", requirement: "Any", effect: "Gain 8 Shield, Heal 2 HP" }
      ]
    },
    "Quakewyrm": {
      hp: 83,
      dice: 5,
      abilities: [
        { name: "Chomp XY", requirement: "Limit 15", effect: "Deal 20 damage, Heal 5 HP" },
        { name: "Tremor", requirement: "Any", effect: "Deal damage equal to die value, Apply Lock equal to (die value ÷ 3, rounded down)" },
        { name: "Stone Hide", requirement: "Even only", effect: "Gain Shield equal to die value + 2", reusable: true },
        { name: "Earthshatter", requirement: "Limit 22", effect: "Deal 15 damage, Apply 3 Lock, Apply 2 Frozen" }
      ]
    },
    "Caghoul Skyshaker": {
      hp: 80,
      dice: 5,
      abilities: [
        { name: "Lightning Storm", requirement: "Limit 20", effect: "Deal 20 damage, Apply 2 Blind" },
        { name: "Chain Lightning", requirement: "Odd only", effect: "Deal quadruple die value damage" },
        { name: "Totem X", requirement: "Exactly 2", effect: "Gain 8 Shield, Heal 4 HP" },
        { name: "Wind Slash", requirement: "Any", effect: "Deal damage equal to die value + 4, On 6: Apply 2 Bleed", reusable: true }
      ]
    },
    "Condemned": {
      hp: 38,
      dice: 4,
      abilities: [
        { name: "Flail", requirement: "Any", effect: "Deal damage equal to die value, Sacrifice 1 HP" },
        { name: "Chains", requirement: "Minimum 3", effect: "Deal 6 damage, Apply 2 Lock", reusable: true },
        { name: "Desperation", requirement: "Exactly 1", effect: "Deal 10 damage, Sacrifice 5 HP" }
      ]
    },
    "Bovari Thrall": {
      hp: 40,
      dice: 4,
      abilities: [
        { name: "Gore Z", requirement: "Any", effect: "Deal 6 + die value damage, On 5-6: Apply 2 Bleed" },
        { name: "Blood Pact", requirement: "Limit 15", effect: "Deal 12 damage, Heal 4 HP, Sacrifice 3 HP" },
        { name: "Flame Strike", requirement: "Odd only", effect: "Deal double die value damage, Apply 1 Poison" }
      ]
    },
    "Hatebound Imp": {
      hp: 36,
      dice: 4,
      abilities: [
        { name: "Claw Swipe", requirement: "Any", effect: "Deal damage equal to die value + 3, On 6: Apply 1 Bleed", reusable: true },
        { name: "Curse", requirement: "Exactly 1", effect: "Apply 2 Poison, Apply 2 Blind" },
        { name: "Immolate", requirement: "Limit 10", effect: "Deal 10 damage, Apply 2 Poison, Sacrifice 2 HP" }
      ]
    },
    "Blooded Khinari": {
      hp: 62,
      dice: 5,
      abilities: [
        { name: "Snipe Y", requirement: "Limit 22", effect: "Deal 18 damage, Apply 3 Bleed, Heal 3 HP" },
        { name: "Frosted Spear Y", requirement: "Any", effect: "Deal 6 damage, On 5-6: Apply 2 Frozen", reusable: true },
        { name: "Blood Ritual", requirement: "Exactly 1", effect: "Sacrifice 5 HP, Deal 15 damage, Apply 2 Poison" },
        { name: "Splinter Y", requirement: "Any", effect: "Sacrifice 2 HP, Create 3 dice with half the input die value (rounded up)" }
      ]
    },
    "Hatebound Priest": {
      hp: 60,
      dice: 5,
      abilities: [
        { name: "Dark Blessing", requirement: "Limit 18", effect: "Heal 8 HP, Apply 2 Poison to opponent" },
        { name: "Afflict Y", requirement: "Exactly 1", effect: "Apply 4 Poison, Apply 2 Blind, Apply 1 Lock" },
        { name: "Flame Burst", requirement: "Odd only", effect: "Deal triple die value damage" },
        { name: "Life Drain Y", requirement: "Odd only", effect: "Deal damage equal to die value + 4, Heal half the damage dealt (rounded up)", reusable: true }
      ]
    },
    "Condemned Taskmaster": {
      hp: 64,
      dice: 4,
      abilities: [
        { name: "Whip Crack", requirement: "Any", effect: "Deal damage equal to die value + 5, Apply 1 Lock" },
        { name: "Chains X", requirement: "Minimum 3", effect: "Deal 8 damage, Apply 3 Lock", reusable: true },
        { name: "Torture", requirement: "Limit 20", effect: "Deal 15 damage, Apply 2 Bleed, Apply 2 Lock" },
        { name: "Bash Y", requirement: "Any", effect: "Deal damage equal to triple current shield, then remove all shield" }
      ]
    },
    "Pit Lord": {
      hp: 115,
      dice: 5,
      abilities: [
        { name: "Annihilation", requirement: "Limit 30", effect: "Deal 25 damage, Apply 3 Bleed, Apply 2 Poison" },
        { name: "Infernal Strike", requirement: "Any", effect: "Deal damage equal to die value + 8, Sacrifice 2 HP", reusable: true },
        { name: "Hellfire", requirement: "Odd only", effect: "Deal quintuple die value damage" },
        { name: "Dark Aegis", requirement: "Even only", effect: "Gain Shield equal to die value + 4, Apply 1 Poison to opponent", reusable: true }
      ]
    },
    "Blood Judge": {
      hp: 112,
      dice: 5,
      abilities: [
        { name: "Execution", requirement: "Limit 25", effect: "Deal 22 damage, Apply 4 Bleed" },
        { name: "Blood Price", requirement: "Any", effect: "Sacrifice HP equal to die value, Deal double the sacrificed HP as damage" },
        { name: "Judgement", requirement: "Exactly 6", effect: "Deal 18 damage, Heal 6 HP, Apply 2 Lock" },
        { name: "Life Drain XY", requirement: "Odd only", effect: "Deal damage equal to die value + 6, Heal the full damage dealt", reusable: true }
      ]
    },
    "Prophet of Fire": {
      hp: 110,
      dice: 6,
      abilities: [
        { name: "Apocalypse", requirement: "Limit 35", effect: "Deal 30 damage, Apply 4 Poison, Apply 3 Blind, Apply 2 Lock" },
        { name: "Meteor", requirement: "Minimum 5", effect: "Deal 15 damage, Apply 2 Bleed", reusable: true },
        { name: "Inferno", requirement: "Odd only", effect: "Deal quadruple die value damage, Apply 2 Poison" },
        { name: "Phoenix Rising", requirement: "Exactly 1", effect: "Heal 10 HP, Gain 10 Shield, Remove all negative effects from self" },
        { name: "Flame Wall", requirement: "Even only", effect: "Gain Shield equal to die value + 5, Deal 5 damage", reusable: true }
      ]
    }
  };

  const biomes = {
    plains: {
      name: "Plains",
      tiers: [
        { diff: 1, creatures: ["Wolf", "Giant Locust", "Naukin Outcast"] },
        { diff: 3, creatures: ["Dire Wolves", "Prowling Dellinid", "Juvenile Auroc"] },
        { diff: 5, creatures: ["Bovari Bandit", "Roaming Gallox", "Lone Plainsdrake"] }
      ]
    },
    plains: {
      name: "Plains",
      tiers: [
        { diff: 1, creatures: ["Wolf", "Giant Locust", "Naukin Outcast"] },
        { diff: 3, creatures: ["Dire Wolves", "Prowling Dellinid", "Juvenile Auroc"] },
        { diff: 5, creatures: ["Bovari Bandit", "Roaming Gallox", "Lone Plainsdrake"] }
      ]
    },
    tundra: {
      name: "Tundra",
      tiers: [
        { diff: 2, creatures: ["Blue Dellinid", "Khinari Exile", "Territorial Whitespike"] },
        { diff: 4, creatures: ["Khinari Raider", "Tundra Boneguard", "Alpha Whitespike"] },
        { diff: 6, creatures: ["Veteran Boneguard", "Khinari Hunting Party", "Hungry Frost Wyrm"] }
      ]
    },
    forest: {
      name: "Forest",
      tiers: [
        { diff: 3, creatures: ["Naukin Scouts", "Skittari Hunters", "Reclaimed Boneguard"] },
        { diff: 5, creatures: ["Dire Bear", "Khinari Bladedancer", "Naukin Sunstriker"] },
        { diff: 7, creatures: ["Verdant Shepherd", "Barkskin Colossus", "Emerald Lich"] }
      ]
    },
    ruins: {
      name: "Ruins",
      tiers: [
        { diff: 4, creatures: ["Brass Golem", "Skittari Looters", "Bloated Zombie"] },
        { diff: 6, creatures: ["Iron Bulwark", "Stone Drake", "Lost Myrrim"] },
        { diff: 8, creatures: ["Fell Lich", "Blighted Auroc", "Khinari Subjugator"] }
      ]
    },
    slopes: {
      name: "Slopes",
      tiers: [
        { diff: 5, creatures: ["Steppe Whitespike", "Caghoul Shaman", "Naukin Outrider"] },
        { diff: 7, creatures: ["Hill Giant", "Black Roc", "Whitespike Patriarch"] },
        { diff: 9, creatures: ["Thunder Giant", "Quakewyrm", "Caghoul Skyshaker"] }
      ]
    },
    pit: {
      name: "Pit",
      tiers: [
        { diff: 6, creatures: ["Condemned", "Bovari Thrall", "Hatebound Imp"] },
        { diff: 8, creatures: ["Blooded Khinari", "Hatebound Priest", "Condemned Taskmaster"] },
        { diff: 10, creatures: ["Pit Lord", "Blood Judge", "Prophet of Fire"] }
      ]
    }
  };

  return (
    <div className="p-6 bg-gray-900 text-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-center">Biome Progression System</h1>
      
      <div className="mb-8 p-4 bg-gray-800 rounded-lg">
        <h2 className="text-xl font-semibold mb-2">Unlock Rules:</h2>
        <ul className="list-disc list-inside space-y-1 text-sm">
          <li>Tier 1 of any biome unlocks: Next biome's Tier 1 + Same biome's Tier 2</li>
          <li>Tier 2+ of any biome only unlocks: Same biome's next tier</li>
          <li>Difficulty increases by 2 per tier within a biome</li>
          <li>Each new biome starts +1 difficulty from previous biome's start</li>
        </ul>
      </div>

      <div className="mb-8 p-4 bg-gray-800 rounded-lg border-2 border-yellow-600">
        <h2 className="text-xl font-semibold mb-2 text-yellow-400">Rewards:</h2>
        <ul className="list-disc list-inside space-y-1 text-sm">
          <li>Each creature drops <span className="font-bold text-green-400">10 × Difficulty</span> gold when defeated</li>
          <li>Each creature has a <span className="font-bold text-purple-400">1% chance</span> to drop one of their ability cards at random</li>
        </ul>
      </div>

      <div className="space-y-8">
        {Object.entries(biomes).map(([key, biome]) => (
          <div key={key} className="border-2 border-gray-700 rounded-lg p-4 bg-gray-800">
            <h2 className="text-2xl font-bold mb-4 text-blue-400">{biome.name}</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {biome.tiers.map((tier, index) => (
                <div key={index} className="bg-gray-700 p-4 rounded border-2 border-gray-600">
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="text-lg font-semibold">Tier {index + 1}</h3>
                    <span className="bg-red-600 px-3 py-1 rounded text-sm font-bold">
                      Diff: {tier.diff}
                    </span>
                  </div>
                  
                  <div className="space-y-2">
                    {tier.creatures.length > 0 ? (
                      tier.creatures.map((creature, i) => (
                        <div key={i} className="bg-gray-600 rounded">
                          <div className="p-2 text-sm font-semibold">
                            {creature}
                          </div>
                          {creatureCards[creature] && (
                            <div className="px-2 pb-2 text-xs space-y-1">
                              <div className="flex justify-between text-yellow-400">
                                <span>HP: {creatureCards[creature].hp}</span>
                                <span>Rolls: {creatureCards[creature].dice} dice</span>
                              </div>
                              {creatureCards[creature].abilities.map((ability, idx) => (
                                <div key={idx} className="bg-gray-700 p-1 rounded">
                                  <div className="font-semibold text-blue-300">
                                    {ability.name}
                                    {ability.reusable && <span className="text-green-400 ml-1">(Reusable)</span>}
                                    {ability.oncePerCombat && <span className="text-red-400 ml-1">(Once per combat)</span>}
                                  </div>
                                  <div className="text-gray-300">
                                    {ability.requirement} → {ability.effect}
                                  </div>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      ))
                    ) : (
                      <div className="text-gray-400 italic text-sm">No creatures yet</div>
                    )}
                  </div>
                  
                  {index === 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-600 text-xs text-gray-400">
                      Unlocks: {biome.name} Tier 2 + Next Biome Tier 1
                    </div>
                  )}
                  {index > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-600 text-xs text-gray-400">
                      Unlocks: {biome.name} Tier {index + 2}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProgressionDiagram;