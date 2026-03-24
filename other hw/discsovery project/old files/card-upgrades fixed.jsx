import React, { useState } from 'react';
import { ChevronDown, ChevronRight, ArrowRight } from 'lucide-react';

const CardUpgradeProgression = () => {
  const [expandedCards, setExpandedCards] = useState({});

  const toggleCard = (cardName) => {
    setExpandedCards(prev => ({
      ...prev,
      [cardName]: !prev[cardName]
    }));
  };

  // Card upgrade progression data - ONLY cards from the original file
  const cardProgression = {
    "Afflict": {
      base: { name: "Afflict", requirement: "Exactly 1", effect: "Apply 2 Poison, Apply 1 Blind" },
      x: { name: "Afflict x", requirement: "Exactly 1", effect: "Apply 2 Poison, Apply 2 Blind" },
      y: { name: "Afflict y", requirement: "Exactly 1", effect: "Apply 3 Poison, Apply 1 Blind" },
      X: { name: "Afflict X", requirement: "Exactly 1", effect: "Apply 3 Poison, Apply 2 Blind" },
      Y: { name: "Afflict Y", requirement: "Exactly 1", effect: "Apply 4 Poison, Apply 2 Blind, Apply 1 Lock" },
      XY: { name: "Afflict XY", requirement: "Exactly 1", effect: "Apply 5 Poison, Apply 3 Blind, Apply 2 Lock" },
    },
    "Annihilation": {
      base: { name: "Annihilation", requirement: "Limit 30", effect: "Deal 25 damage, Apply 3 Bleed, Apply 2 Poison" },
      x: { name: "Annihilation x", requirement: "Limit 28", effect: "Deal 25 damage, Apply 4 Bleed, Apply 2 Poison" },
      y: { name: "Annihilation y", requirement: "Limit 30", effect: "Deal 28 damage, Apply 3 Bleed, Apply 3 Poison" },
      X: { name: "Annihilation X", requirement: "Limit 25", effect: "Deal 28 damage, Apply 5 Bleed, Apply 3 Poison" },
      Y: { name: "Annihilation Y", requirement: "Limit 28", effect: "Deal 32 damage, Apply 4 Bleed, Apply 4 Poison" },
      XY: { name: "Annihilation XY", requirement: "Limit 22", effect: "Deal 35 damage, Apply 6 Bleed, Apply 5 Poison, Apply 2 Lock" },
    },
    "Apocalypse": {
      base: { name: "Apocalypse", requirement: "Limit 35", effect: "Deal 30 damage, Apply 4 Poison, Apply 3 Blind, Apply 2 Lock" },
      x: { name: "Apocalypse x", requirement: "Limit 32", effect: "Deal 30 damage, Apply 4 Poison, Apply 3 Blind, Apply 2 Lock" },
      y: { name: "Apocalypse y", requirement: "Limit 35", effect: "Deal 32 damage, Apply 5 Poison, Apply 3 Blind, Apply 3 Lock" },
      X: { name: "Apocalypse X", requirement: "Limit 28", effect: "Deal 33 damage, Apply 5 Poison, Apply 4 Blind, Apply 3 Lock" },
      Y: { name: "Apocalypse Y", requirement: "Limit 32", effect: "Deal 36 damage, Apply 6 Poison, Apply 4 Blind, Apply 4 Lock" },
      XY: { name: "Apocalypse XY", requirement: "Limit 25", effect: "Deal 40 damage, Apply 7 Poison, Apply 5 Blind, Apply 5 Lock, Apply 3 Bleed" },
    },
    "Bash": {
      base: { name: "Bash", requirement: "Any", effect: "Remove all Shield from self, Deal damage equal to double the Shield removed" },
      x: { name: "Bash x", requirement: "Any", effect: "Deal damage equal to double current shield, then remove half of current shield (rounded down)" },
      y: { name: "Bash y", requirement: "Any", effect: "Deal damage equal to double current shield, then remove half of current shield (rounded up)" },
      X: { name: "Bash X", requirement: "Any", effect: "Deal damage equal to double current shield, then remove half of current shield (rounded up), Gain 2 Shield", reusable: true },
      Y: { name: "Bash Y", requirement: "Any", effect: "Deal damage equal to triple current shield, then remove all shield" },
      XY: { name: "Bash XY", requirement: "Any", effect: "Deal damage equal to triple current shield, then remove half of current shield (rounded down), Gain 3 Shield", reusable: true },
    },
    "Bellow": {
      base: { name: "Bellow", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Frozen" },
      x: { name: "Bellow x", requirement: "Any", effect: "Deal damage equal to die value, Trigger Poison (deal damage equal to poison counters on opponent, then reduce poison counters by 1)" },
      y: { name: "Bellow y", requirement: "Any", effect: "Deal damage equal to die value, On 5-6: Apply 1 Frozen" },
      X: { name: "Bellow X", requirement: "Any", effect: "Deal damage equal to die value + 2, On 5-6: Apply 2 Frozen" },
      Y: { name: "Bellow Y", requirement: "Any", effect: "Deal damage equal to die value + 3, On 5-6: Apply 2 Frozen", reusable: true },
      XY: { name: "Bellow XY", requirement: "Any", effect: "Deal damage equal to die value + 4, Trigger Poison, On 5-6: Apply 3 Frozen", reusable: true },
    },
    "Bite": {
      base: { name: "Bite", requirement: "Any", effect: "Deal 3 damage" },
      x: { name: "Bite x", requirement: "Any", effect: "Deal damage equal to die value" },
      y: { name: "Bite y", requirement: "Any", effect: "Deal 4 damage", reusable: true },
      X: { name: "Bite X", requirement: "Any", effect: "Deal damage equal to die value + 2" },
      Y: { name: "Bite Y", requirement: "Any", effect: "Deal 5 damage and heal 1", reusable: true },
      XY: { name: "Bite XY", requirement: "Any", effect: "Deal damage equal to die value + 4, Heal 2 HP", reusable: true },
    },
    "Blood Pact": {
      base: { name: "Blood Pact", requirement: "Limit 15", effect: "Deal 12 damage, Heal 4 HP, Sacrifice 3 HP" },
      x: { name: "Blood Pact x", requirement: "Limit 13", effect: "Deal 12 damage, Heal 5 HP, Sacrifice 3 HP" },
      y: { name: "Blood Pact y", requirement: "Limit 15", effect: "Deal 14 damage, Heal 4 HP, Sacrifice 4 HP" },
      X: { name: "Blood Pact X", requirement: "Limit 10", effect: "Deal 15 damage, Heal 6 HP, Sacrifice 3 HP" },
      Y: { name: "Blood Pact Y", requirement: "Limit 13", effect: "Deal 18 damage, Heal 5 HP, Sacrifice 5 HP" },
      XY: { name: "Blood Pact XY", requirement: "Limit 8", effect: "Deal 20 damage, Heal 8 HP, Sacrifice 4 HP" },
    },
    "Blood Price": {
      base: { name: "Blood Price", requirement: "Any", effect: "Sacrifice HP equal to die value, Deal double the sacrificed HP as damage" },
      x: { name: "Blood Price x", requirement: "Any", effect: "Sacrifice HP equal to die value, Deal triple the sacrificed HP as damage" },
      y: { name: "Blood Price y", requirement: "Any", effect: "Sacrifice HP equal to die value + 1, Deal double the sacrificed HP as damage" },
      X: { name: "Blood Price X", requirement: "Any", effect: "Sacrifice HP equal to die value, Deal triple the sacrificed HP as damage, Gain 2 Shield" },
      Y: { name: "Blood Price Y", requirement: "Any", effect: "Sacrifice HP equal to die value + 2, Deal triple the sacrificed HP as damage" },
      XY: { name: "Blood Price XY", requirement: "Any", effect: "Sacrifice HP equal to die value + 1, Deal quadruple the sacrificed HP as damage, Gain 3 Shield" },
    
    },
    "Blood Ritual": {
      base: { name: "Blood Ritual", requirement: "Exactly 1", effect: "Sacrifice 5 HP, Deal 15 damage, Apply 2 Poison" },
      x: { name: "Blood Ritual x", requirement: "Exactly 1", effect: "Sacrifice 4 HP, Deal 15 damage, Apply 3 Poison" },
      y: { name: "Blood Ritual y", requirement: "Exactly 1", effect: "Sacrifice 6 HP, Deal 18 damage, Apply 2 Poison" },
      X: { name: "Blood Ritual X", requirement: "Exactly 1", effect: "Sacrifice 3 HP, Deal 18 damage, Apply 4 Poison, Apply 1 Blind" },
      Y: { name: "Blood Ritual Y", requirement: "Exactly 1", effect: "Sacrifice 7 HP, Deal 22 damage, Apply 3 Poison, Apply 1 Bleed" },
      XY: { name: "Blood Ritual XY", requirement: "Exactly 1", effect: "Sacrifice 5 HP, Deal 25 damage, Apply 5 Poison, Apply 2 Blind, Apply 2 Bleed" },
    },
    "Boulder Toss": {
      base: { name: "Boulder Toss", requirement: "Minimum 4", effect: "Deal 10 damage, Apply 1 Lock", reusable: true },
      x: { name: "Boulder Toss x", requirement: "Minimum 4", effect: "Deal 11 damage, Apply 1 Lock", reusable: true },
      y: { name: "Boulder Toss y", requirement: "Minimum 5", effect: "Deal 12 damage, Apply 2 Lock", reusable: true },
      Y: { name: "Boulder Toss Y", requirement: "Minimum 4", effect: "Deal 14 damage, Apply 3 Lock", reusable: true },
      XY: { name: "Boulder Toss XY", requirement: "Minimum 3", effect: "Deal 16 damage, Apply 4 Lock, Apply 1 Frozen", reusable: true },
    },
    "Chain Lightning": {
      base: { name: "Chain Lightning", requirement: "Odd only", effect: "Deal quadruple die value damage" },
      x: { name: "Chain Lightning x", requirement: "Odd only", effect: "Deal quadruple die value damage, Apply 1 Blind" },
      y: { name: "Chain Lightning y", requirement: "Odd only", effect: "Deal quintuple die value damage" },
      X: { name: "Chain Lightning X", requirement: "Odd only", effect: "Deal quintuple die value damage, Apply 2 Blind" },
      Y: { name: "Chain Lightning Y", requirement: "Odd only", effect: "Deal sextuple die value damage, Apply 1 Lock" },
      XY: { name: "Chain Lightning XY", requirement: "Odd only", effect: "Deal septuple die value damage, Apply 2 Blind, Apply 2 Lock" },
    },
    "Chains": {
      base: { name: "Chains", requirement: "Minimum 3", effect: "Deal 6 damage, Apply 2 Lock", reusable: true },
      x: { name: "Chains x", requirement: "Minimum 3", effect: "Deal 7 damage, Apply 2 Lock", reusable: true },
      y: { name: "Chains y", requirement: "Minimum 4", effect: "Deal 8 damage, Apply 3 Lock", reusable: true },
      X: { name: "Chains X", requirement: "Minimum 3", effect: "Deal 8 damage, Apply 3 Lock", reusable: true },
      Y: { name: "Chains Y", requirement: "Minimum 3", effect: "Deal 10 damage, Apply 4 Lock", reusable: true },
      XY: { name: "Chains XY", requirement: "Minimum 2", effect: "Deal 12 damage, Apply 5 Lock, Apply 2 Blind", reusable: true },
    },
    "Charge": {
      base: { name: "Charge", requirement: "Limit 15", effect: "Deal 8 damage, Gain 3 Shield (activates when limit reaches 0)" },
      x: { name: "Charge x", requirement: "Limit 13", effect: "Deal 8 damage, Gain 3 Shield" },
      y: { name: "Charge y", requirement: "Limit 18", effect: "Deal 8 damage, Gain 8 Shield" },
      X: { name: "Charge X", requirement: "Limit 20", effect: "Deal 10 damage, Gain 10 Shield" },
      Y: { name: "Charge Y", requirement: "Limit 15", effect: "Deal 12 damage, Gain 6 Shield" },
      XY: { name: "Charge XY", requirement: "Limit 12", effect: "Deal 15 damage, Gain 12 Shield, Apply 1 Lock" },
    },
    "Chomp": {
      base: { name: "Chomp", requirement: "Limit 10", effect: "Deal 10 damage (activates when limit reaches 0)" },
      y: { name: "Chomp y", requirement: "Limit 12", effect: "Deal 12 damage" },
      x: { name: "Chomp x", requirement: "Limit 8", effect: "Deal 10 damage (activates when limit reaches 0)" },
      X: { name: "Chomp X", requirement: "Limit 10", effect: "Deal 14 damage, Heal 3 HP" },
      Y: { name: "Chomp Y", requirement: "Limit 8", effect: "Deal 18 damage, Heal 4 HP" },
      XY: { name: "Chomp XY", requirement: "Limit 15", effect: "Deal 20 damage, Heal 5 HP" },
    },
    "Claw Swipe": {
      base: { name: "Claw Swipe", requirement: "Any", effect: "Deal damage equal to die value + 3, On 6: Apply 1 Bleed", reusable: true },
      x: { name: "Claw Swipe x", requirement: "Any", effect: "Deal damage equal to die value + 4, On 6: Apply 1 Bleed", reusable: true },
      y: { name: "Claw Swipe y", requirement: "Any", effect: "Deal damage equal to die value + 3, On 5-6: Apply 2 Bleed", reusable: true },
      X: { name: "Claw Swipe X", requirement: "Any", effect: "Deal damage equal to die value + 5, On 5-6: Apply 2 Bleed", reusable: true },
      Y: { name: "Claw Swipe Y", requirement: "Any", effect: "Deal damage equal to die value + 4, On 4-6: Apply 3 Bleed", reusable: true },
      XY: { name: "Claw Swipe XY", requirement: "Any", effect: "Deal damage equal to die value + 6, On 4-6: Apply 4 Bleed", reusable: true },
    },
    "Control": {
      base: { name: "Control", requirement: "Exactly 1", effect: "Sacrifice 2 HP, draw a new card, and roll a new die" },
      x: { name: "Control x", requirement: "Exactly 1", effect: "Sacrifice 1 HP, draw a new card, and roll a new die" },
      y: { name: "Control y", requirement: "Exactly 1", effect: "Sacrifice 2 HP, draw 2 new cards, and roll a new die" },
      X: { name: "Control X", requirement: "Exactly 1", effect: "Draw a new card, and roll a new die" },
      Y: { name: "Control Y", requirement: "Exactly 1", effect: "Sacrifice 3 HP, draw 2 new cards, and roll 2 new dice" },
      XY: { name: "Control XY", requirement: "Exactly 1", effect: "Sacrifice 1 HP, draw 3 new cards, and roll 2 new dice" },
    },
    "Curse": {
      base: { name: "Curse", requirement: "Exactly 1", effect: "Apply 2 Poison, Apply 2 Blind" },
      x: { name: "Curse x", requirement: "Exactly 1", effect: "Apply 2 Poison, Apply 3 Blind" },
      y: { name: "Curse y", requirement: "Exactly 1", effect: "Apply 3 Poison, Apply 2 Blind" },
      X: { name: "Curse X", requirement: "Exactly 1", effect: "Apply 3 Poison, Apply 4 Blind, Apply 1 Lock" },
      Y: { name: "Curse Y", requirement: "Exactly 1", effect: "Apply 4 Poison, Apply 3 Blind, Apply 1 Lock" },
      XY: { name: "Curse XY", requirement: "Exactly 1", effect: "Apply 5 Poison, Apply 5 Blind, Apply 2 Lock" },
    },
    "Dagger": {
      base: { name: "Dagger", requirement: "Odd only", effect: "Deal 2 damage, Apply 1 Poison" },
      x: { name: "Dagger x", requirement: "Any", effect: "Deal 3 damage, Apply 1 Poison" },
      X: { name: "Dagger X", requirement: "Odd only", effect: "Deal 4 damage, Apply 2 Poison" },
      XY: { name: "Dagger XY", requirement: "Odd only", effect: "Deal 6 damage, Apply 3 Poison" },
      y: { name: "Dagger y", requirement: "Odd only", effect: "Deal 4 damage, Apply 1 Poison" },
      Y: { name: "Dagger Y", requirement: "Odd only", effect: "Deal 5 damage, Apply 2 Poison" },
    },
    "Dark Aegis": {
      base: { name: "Dark Aegis", requirement: "Even only", effect: "Gain Shield equal to die value + 4, Apply 1 Poison to opponent", reusable: true },
      x: { name: "Dark Aegis x", requirement: "Even only", effect: "Gain Shield equal to die value + 5, Apply 1 Poison to opponent", reusable: true },
      y: { name: "Dark Aegis y", requirement: "Even only", effect: "Gain Shield equal to die value + 4, Apply 2 Poison to opponent", reusable: true },
      X: { name: "Dark Aegis X", requirement: "Even only", effect: "Gain Shield equal to die value + 6, Apply 2 Poison to opponent, Heal 1 HP", reusable: true },
      Y: { name: "Dark Aegis Y", requirement: "Even only", effect: "Gain Shield equal to die value + 5, Apply 3 Poison to opponent", reusable: true },
      XY: { name: "Dark Aegis XY", requirement: "Even only", effect: "Gain Shield equal to die value + 8, Apply 3 Poison to opponent, Heal 2 HP", reusable: true },
    },
    "Dark Blessing": {
      base: { name: "Dark Blessing", requirement: "Limit 18", effect: "Heal 8 HP, Apply 2 Poison to opponent" },
      x: { name: "Dark Blessing x", requirement: "Limit 16", effect: "Heal 8 HP, Apply 2 Poison to opponent" },
      y: { name: "Dark Blessing y", requirement: "Limit 18", effect: "Heal 10 HP, Apply 3 Poison to opponent" },
      X: { name: "Dark Blessing X", requirement: "Limit 13", effect: "Heal 10 HP, Apply 3 Poison to opponent, Gain 2 Shield" },
      Y: { name: "Dark Blessing Y", requirement: "Limit 15", effect: "Heal 12 HP, Apply 4 Poison to opponent" },
      XY: { name: "Dark Blessing XY", requirement: "Limit 10", effect: "Heal 15 HP, Apply 5 Poison to opponent, Gain 4 Shield" },
    },
    "Desperation": {
      base: { name: "Desperation", requirement: "Exactly 1", effect: "Deal 10 damage, Sacrifice 5 HP" },
      x: { name: "Desperation x", requirement: "Exactly 1", effect: "Deal 10 HP, Sacrifice 4 HP" },
      y: { name: "Desperation y", requirement: "Exactly 1", effect: "Deal 12 damage, Sacrifice 6 HP" },
      X: { name: "Desperation X", requirement: "Exactly 1", effect: "Deal 12 damage, Sacrifice 3 HP, Apply 1 Bleed" },
      Y: { name: "Desperation Y", requirement: "Exactly 1", effect: "Deal 15 damage, Sacrifice 7 HP, Apply 1 Lock" },
      XY: { name: "Desperation XY", requirement: "Exactly 1", effect: "Deal 18 damage, Sacrifice 5 HP, Apply 2 Bleed, Apply 1 Lock" },
    },
    "Dive Bomb": {
      base: { name: "Dive Bomb", requirement: "Minimum 5", effect: "Deal 12 damage, Apply 1 Blind" },
      x: { name: "Dive Bomb x", requirement: "Minimum 5", effect: "Deal 12 damage, Apply 2 Blind" },
      y: { name: "Dive Bomb y", requirement: "Minimum 6", effect: "Deal 14 damage, Apply 1 Blind" },
      X: { name: "Dive Bomb X", requirement: "Minimum 4", effect: "Deal 14 damage, Apply 3 Blind, Apply 1 Lock" },
      Y: { name: "Dive Bomb Y", requirement: "Minimum 5", effect: "Deal 16 damage, Apply 2 Blind, Apply 1 Bleed" },
      XY: { name: "Dive Bomb XY", requirement: "Minimum 3", effect: "Deal 18 damage, Apply 4 Blind, Apply 2 Lock, Apply 2 Bleed" },
    },
    "Dominate": {
      base: { name: "Dominate", requirement: "Exactly 1", effect: "Apply 2 Lock, Sacrifice 3 HP" },
      x: { name: "Dominate x", requirement: "Exactly 1", effect: "Apply 3 Lock, Sacrifice 3 HP" },
      y: { name: "Dominate y", requirement: "Exactly 1", effect: "Apply 2 Lock, Sacrifice 2 HP, Apply 1 Blind" },
      X: { name: "Dominate X", requirement: "Exactly 1", effect: "Apply 4 Lock, Sacrifice 2 HP, Apply 1 Blind" },
      Y: { name: "Dominate Y", requirement: "Exactly 1", effect: "Apply 3 Lock, Sacrifice 1 HP, Apply 2 Blind, Apply 1 Poison" },
      XY: { name: "Dominate XY", requirement: "Exactly 1", effect: "Apply 5 Lock, Sacrifice 1 HP, Apply 3 Blind, Apply 2 Poison" },
    },
    "Earthquake": {
      base: { name: "Earthquake", requirement: "Limit 20", effect: "Deal 12 damage, Apply 2 Lock, Apply 1 Frozen" },
      x: { name: "Earthquake x", requirement: "Limit 18", effect: "Deal 12 damage, Apply 2 Lock, Apply 1 Frozen" },
      y: { name: "Earthquake y", requirement: "Limit 20", effect: "Deal 14 damage, Apply 3 Lock, Apply 2 Frozen" },
      X: { name: "Earthquake X", requirement: "Limit 15", effect: "Deal 15 damage, Apply 3 Lock, Apply 2 Frozen, Destroy opponent Shield" },
      Y: { name: "Earthquake Y", requirement: "Limit 17", effect: "Deal 18 damage, Apply 4 Lock, Apply 3 Frozen" },
      XY: { name: "Earthquake XY", requirement: "Limit 12", effect: "Deal 20 damage, Apply 5 Lock, Apply 4 Frozen, Destroy opponent Shield" },
    },
    "Earthshatter": {
      base: { name: "Earthshatter", requirement: "Limit 22", effect: "Deal 15 damage, Apply 3 Lock, Apply 2 Frozen" },
      x: { name: "Earthshatter x", requirement: "Limit 20", effect: "Deal 15 damage, Apply 3 Lock, Apply 2 Frozen" },
      y: { name: "Earthshatter y", requirement: "Limit 22", effect: "Deal 18 damage, Apply 4 Lock, Apply 3 Frozen" },
      X: { name: "Earthshatter X", requirement: "Limit 17", effect: "Deal 18 damage, Apply 4 Lock, Apply 3 Frozen, Apply 1 Bleed" },
      Y: { name: "Earthshatter Y", requirement: "Limit 19", effect: "Deal 22 damage, Apply 5 Lock, Apply 4 Frozen" },
      XY: { name: "Earthshatter XY", requirement: "Limit 14", effect: "Deal 25 damage, Apply 6 Lock, Apply 5 Frozen, Apply 2 Bleed" },
    },
    "Evade": {
      base: { name: "Evade", requirement: "Exactly 1", effect: "Gain Shield equal to 2 × the number of dice used this turn" },
      x: { name: "Evade x", requirement: "Exactly 1", effect: "Gain Shield equal to 3 × the number of dice used this turn" },
      y: { name: "Evade y", requirement: "Exactly 1", effect: "Gain Shield equal to 2 × the number of dice used this turn, Heal 2 HP" },
      X: { name: "Evade X", requirement: "Exactly 1", effect: "Gain Shield equal to 4 × the number of dice used this turn, Remove 1 negative effect" },
      Y: { name: "Evade Y", requirement: "Exactly 1", effect: "Gain Shield equal to 3 × the number of dice used this turn, Heal 4 HP" },
      XY: { name: "Evade XY", requirement: "Exactly 1", effect: "Gain Shield equal to 5 × the number of dice used this turn, Heal 3 HP, Remove all negative effects" },
    },
    "Execution": {
      base: { name: "Execution", requirement: "Limit 25", effect: "Deal 22 damage, Apply 4 Bleed" },
      x: { name: "Execution x", requirement: "Limit 23", effect: "Deal 22 damage, Apply 4 Bleed" },
      y: { name: "Execution y", requirement: "Limit 25", effect: "Deal 25 damage, Apply 5 Bleed" },
      X: { name: "Execution X", requirement: "Limit 20", effect: "Deal 25 damage, Apply 5 Bleed, Apply 1 Lock" },
      Y: { name: "Execution Y", requirement: "Limit 22", effect: "Deal 28 damage, Apply 6 Bleed, Heal 2 HP" },
      XY: { name: "Execution XY", requirement: "Limit 18", effect: "Deal 32 damage, Apply 7 Bleed, Apply 2 Lock, Heal 3 HP" },
    },
    "Flail": {
      base: { name: "Flail", requirement: "Any", effect: "Deal damage equal to die value, Sacrifice 1 HP" },
      x: { name: "Flail x", requirement: "Any", effect: "Deal damage equal to die value, Sacrifice 1 HP", reusable: true },
      y: { name: "Flail y", requirement: "Any", effect: "Deal damage equal to die value + 1, Sacrifice 2 HP", reusable: true },
      X: { name: "Flail X", requirement: "Any", effect: "Deal damage equal to die value + 1, Sacrifice 1 HP, Apply 1 Bleed", reusable: true },
      Y: { name: "Flail Y", requirement: "Any", effect: "Deal damage equal to die value + 2, Sacrifice 2 HP, On 6: Apply 2 Bleed", reusable: true },
      XY: { name: "Flail XY", requirement: "Any", effect: "Deal damage equal to die value + 3, Sacrifice 1 HP, Apply 2 Bleed", reusable: true },
    },
    "Flame Burst": {
      base: { name: "Flame Burst", requirement: "Odd only", effect: "Deal triple die value damage" },
      x: { name: "Flame Burst x", requirement: "Odd only", effect: "Deal triple die value damage, Apply 1 Poison" },
      y: { name: "Flame Burst y", requirement: "Odd only", effect: "Deal quadruple die value damage" },
      X: { name: "Flame Burst X", requirement: "Odd only", effect: "Deal quadruple die value damage, Apply 2 Poison" },
      Y: { name: "Flame Burst Y", requirement: "Odd only", effect: "Deal quintuple die value damage, Apply 1 Blind" },
      XY: { name: "Flame Burst XY", requirement: "Odd only", effect: "Deal sextuple die value damage, Apply 2 Poison, Apply 2 Blind" },
    },
    "Flame Strike": {
      base: { name: "Flame Strike", requirement: "Odd only", effect: "Deal double die value damage, Apply 1 Poison" },
      x: { name: "Flame Strike x", requirement: "Odd only", effect: "Deal double die value damage, Apply 2 Poison" },
      y: { name: "Flame Strike y", requirement: "Odd only", effect: "Deal triple die value damage, Apply 1 Poison" },
      X: { name: "Flame Strike X", requirement: "Odd only", effect: "Deal triple die value damage, Apply 3 Poison, Apply 1 Blind" },
      Y: { name: "Flame Strike Y", requirement: "Odd only", effect: "Deal quadruple die value damage, Apply 2 Poison" },
      XY: { name: "Flame Strike XY", requirement: "Odd only", effect: "Deal quintuple die value damage, Apply 4 Poison, Apply 2 Blind" },
    },
    "Flame Wall": {
      base: { name: "Flame Wall", requirement: "Even only", effect: "Gain Shield equal to die value + 5, Deal 5 damage", reusable: true },
      x: { name: "Flame Wall x", requirement: "Even only", effect: "Gain Shield equal to die value + 6, Deal 5 damage", reusable: true },
      y: { name: "Flame Wall y", requirement: "Even only", effect: "Gain Shield equal to die value + 5, Deal 7 damage", reusable: true },
      X: { name: "Flame Wall X", requirement: "Even only", effect: "Gain Shield equal to die value + 8, Deal 6 damage, Apply 1 Poison", reusable: true },
      Y: { name: "Flame Wall Y", requirement: "Even only", effect: "Gain Shield equal to die value + 6, Deal 10 damage, Apply 1 Bleed", reusable: true },
      XY: { name: "Flame Wall XY", requirement: "Even only", effect: "Gain Shield equal to die value + 10, Deal 8 damage, Apply 2 Poison, Apply 1 Bleed", reusable: true },
    },
    "Fortify": {
      base: { name: "Fortify", requirement: "Any", effect: "Gain 3 Shield" },
      x: { name: "Fortify x", requirement: "Any", effect: "Gain 4 Shield and inflict 1 blind" },
      y: { name: "Fortify y", requirement: "Any", effect: "Gain 4 Shield, Remove 1 negative effect" },
      X: { name: "Fortify X", requirement: "Any", effect: "Gain 5 Shield, Apply 1 Blind" },
      Y: { name: "Fortify Y", requirement: "Any", effect: "Gain 8 Shield, Heal 2 HP" },
      XY: { name: "Fortify XY", requirement: "Any", effect: "Gain 10 Shield, Heal 3 HP, Apply 2 Blind to opponent" },
    },
    "Frosted Dagger": {
      base: { name: "Frosted Dagger", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Poison" },
      x: { name: "Frosted Dagger x", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Poison and 1 Frozen" },
      y: { name: "Frosted Dagger y", requirement: "Any", effect: "Deal damage equal to die value, On 5-6: Apply 1 Poison and 1 Frozen" },
      X: { name: "Frosted Dagger X", requirement: "Any", effect: "Deal damage equal to die value + 1, On 5-6: Apply 2 Poison and 2 Frozen" },
      Y: { name: "Frosted Dagger Y", requirement: "Any", effect: "Deal damage equal to die value + 2, On 4-6: Apply 2 Poison and 2 Frozen" },
      XY: { name: "Frosted Dagger XY", requirement: "Any", effect: "Deal damage equal to die value + 3, On 4-6: Apply 3 Poison and 3 Frozen" },
    },
    "Frosted Spear": {
      base: { name: "Frosted Spear", requirement: "Minimum 3", effect: "Deal 3 damage", reusable: true },
      x: { name: "Frosted Spear x", requirement: "Any", effect: "Deal 3 damage", reusable: true },
      y: { name: "Frosted Spear y", requirement: "Any", effect: "Deal 4 damage, On 6: Apply 1 Frozen", reusable: true },
      X: { name: "Frosted Spear X", requirement: "Any", effect: "Deal 5 damage, On 5-6: Apply 1 Frozen", reusable: true },
      Y: { name: "Frosted Spear Y", requirement: "Any", effect: "Deal 6 damage, On 5-6: Apply 2 Frozen", reusable: true },
      XY: { name: "Frosted Spear XY", requirement: "Any", effect: "Deal 8 damage, On 4-6: Apply 3 Frozen", reusable: true },
    },
    "Gore": {
      base: { name: "Gore", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Bleed" },
      x: { name: "Gore x", requirement: "Any", effect: "Deal 2 + die value damage, On 6: Apply 1 Bleed" },
      y: { name: "Gore y", requirement: "Any", effect: "Deal 3 + die value damage, On 6: Apply 1 Bleed" },
      X: { name: "Gore X", requirement: "Any", effect: "Deal 4 + die value damage, On 6: Apply 2 Bleed" },
      Y: { name: "Gore Y", requirement: "Any", effect: "Deal 5 + die value damage, On 5-6: Apply 2 Bleed" },
      XY: { name: "Gore XY", requirement: "Any", effect: "Deal 7 + die value damage, On 4-6: Apply 3 Bleed, Heal 1 HP" },
    },
    "Haunting Wail": {
      base: { name: "Haunting Wail", requirement: "Limit 8", effect: "Apply 2 Blind, Apply 1 Lock" },
      x: { name: "Haunting Wail x", requirement: "Limit 7", effect: "Apply 2 Blind, Apply 1 Lock" },
      y: { name: "Haunting Wail y", requirement: "Limit 8", effect: "Apply 3 Blind, Apply 2 Lock" },
      X: { name: "Haunting Wail X", requirement: "Limit 5", effect: "Apply 3 Blind, Apply 2 Lock, Apply 1 Poison" },
      Y: { name: "Haunting Wail Y", requirement: "Limit 6", effect: "Apply 4 Blind, Apply 3 Lock" },
      XY: { name: "Haunting Wail XY", requirement: "Limit 4", effect: "Apply 5 Blind, Apply 4 Lock, Apply 2 Poison" },
    },
    "Hellfire": {
      base: { name: "Hellfire", requirement: "Odd only", effect: "Deal quintuple die value damage" },
      x: { name: "Hellfire x", requirement: "Odd only", effect: "Deal quintuple die value damage, Apply 1 Poison" },
      y: { name: "Hellfire y", requirement: "Odd only", effect: "Deal sextuple die value damage" },
      X: { name: "Hellfire X", requirement: "Odd only", effect: "Deal sextuple die value damage, Apply 2 Poison, Apply 1 Blind" },
      Y: { name: "Hellfire Y", requirement: "Odd only", effect: "Deal septuple die value damage, Apply 1 Lock" },
      XY: { name: "Hellfire XY", requirement: "Odd only", effect: "Deal octuple die value damage, Apply 3 Poison, Apply 2 Blind, Apply 2 Lock" },
    },
    "Howl": {
      base: { name: "Howl", requirement: "Limit 8", effect: "Heal 2 HP" },
      x: { name: "Howl x", requirement: "Limit 7", effect: "Heal 2 HP" },
      y: { name: "Howl y", requirement: "Limit 8", effect: "Heal 3 HP" },
      X: { name: "Howl X", requirement: "Limit 5", effect: "Heal 3 HP, Remove 1 negative effect" },
      Y: { name: "Howl Y", requirement: "Limit 6", effect: "Heal 4 HP, Gain 2 Shield" },
      XY: { name: "Howl XY", requirement: "Limit 4", effect: "Heal 5 HP, Remove all negative effects, Gain 3 Shield" },
    },
    "Hype Up": {
      base: { name: "Hype Up", requirement: "Limit 12", effect: "Heal 4 HP, Apply 1 Blind to self and opponent (activates when limit reaches 0)" },
      x: { name: "Hype Up x", requirement: "Limit 10", effect: "Heal 4 HP, Apply 1 Blind to self and opponent" },
      y: { name: "Hype Up y", requirement: "Limit 12", effect: "Heal 5 HP, Apply 2 Blind to self and opponent" },
      X: { name: "Hype Up X", requirement: "Limit 8", effect: "Heal 5 HP, Apply 2 Blind to opponent only" },
      Y: { name: "Hype Up Y", requirement: "Limit 10", effect: "Heal 6 HP, Apply 3 Blind to self and opponent, Gain 2 Shield" },
      XY: { name: "Hype Up XY", requirement: "Limit 6", effect: "Heal 8 HP, Apply 3 Blind to opponent only, Gain 4 Shield" },
    },
    "Ice Magic": {
      base: { name: "Ice Magic", requirement: "Exactly 2", effect: "Heal 2 HP, Remove all negative effects from self" },
      x: { name: "Ice Magic x", requirement: "Exactly 2", effect: "Heal 3 HP, Remove all negative effects from self" },
      y: { name: "Ice Magic y", requirement: "Max 2", effect: "Heal 2 HP, Remove all negative effects from self" },
      X: { name: "Ice Magic X", requirement: "Max 2", effect: "Heal 4 HP, Remove all negative effects from self, Gain 2 Shield" },
      Y: { name: "Ice Magic Y", requirement: "Exactly 1", effect: "Heal 3 HP, Remove all negative effects from self, Gain 3 Shield" },
      XY: { name: "Ice Magic XY", requirement: "Max 2", effect: "Heal 5 HP, Remove all negative effects from self, Gain 5 Shield, Apply 1 Frozen to opponent" },
    },
    "Immolate": {
      base: { name: "Immolate", requirement: "Limit 10", effect: "Deal 10 damage, Apply 2 Poison, Sacrifice 2 HP" },
      x: { name: "Immolate x", requirement: "Limit 9", effect: "Deal 10 damage, Apply 2 Poison, Sacrifice 2 HP" },
      y: { name: "Immolate y", requirement: "Limit 10", effect: "Deal 12 damage, Apply 3 Poison, Sacrifice 3 HP" },
      X: { name: "Immolate X", requirement: "Limit 7", effect: "Deal 12 damage, Apply 3 Poison, Sacrifice 1 HP, Apply 1 Blind" },
      Y: { name: "Immolate Y", requirement: "Limit 8", effect: "Deal 15 damage, Apply 4 Poison, Sacrifice 4 HP" },
      XY: { name: "Immolate XY", requirement: "Limit 5", effect: "Deal 18 damage, Apply 5 Poison, Sacrifice 2 HP, Apply 2 Blind" },
    },
    "Infernal Strike": {
      base: { name: "Infernal Strike", requirement: "Any", effect: "Deal damage equal to die value + 8, Sacrifice 2 HP", reusable: true },
      x: { name: "Infernal Strike x", requirement: "Any", effect: "Deal damage equal to die value + 9, Sacrifice 2 HP", reusable: true },
      y: { name: "Infernal Strike y", requirement: "Any", effect: "Deal damage equal to die value + 10, Sacrifice 3 HP", reusable: true },
      X: { name: "Infernal Strike X", requirement: "Any", effect: "Deal damage equal to die value + 11, Sacrifice 1 HP, Apply 1 Poison", reusable: true },
      Y: { name: "Infernal Strike Y", requirement: "Any", effect: "Deal damage equal to die value + 12, Sacrifice 4 HP, Apply 1 Bleed", reusable: true },
      XY: { name: "Infernal Strike XY", requirement: "Any", effect: "Deal damage equal to die value + 14, Sacrifice 2 HP, Apply 2 Poison, Apply 1 Bleed", reusable: true },
    },
    "Inferno": {
      base: { name: "Inferno", requirement: "Odd only", effect: "Deal quadruple die value damage, Apply 2 Poison" },
      x: { name: "Inferno x", requirement: "Odd only", effect: "Deal quadruple die value damage, Apply 3 Poison" },
      y: { name: "Inferno y", requirement: "Odd only", effect: "Deal quintuple die value damage, Apply 2 Poison" },
      X: { name: "Inferno X", requirement: "Odd only", effect: "Deal quintuple die value damage, Apply 4 Poison, Apply 1 Blind" },
      Y: { name: "Inferno Y", requirement: "Odd only", effect: "Deal sextuple die value damage, Apply 3 Poison, Apply 1 Lock" },
      XY: { name: "Inferno XY", requirement: "Odd only", effect: "Deal septuple die value damage, Apply 5 Poison, Apply 2 Blind, Apply 2 Lock" },
    },
    "Jab": {
      base: { name: "Jab", requirement: "Any", effect: "Deal damage equal to die value" },
      x: { name: "Jab x", requirement: "Any", effect: "Deal 2 + die value damage" },
      y: { name: "Jab y", requirement: "Any", effect: "Deal damage equal to die value", reusable: true },
      X: { name: "Jab X", requirement: "Any", effect: "Deal 4 + die value damage", reusable: true },
      Y: { name: "Jab Y", requirement: "Any", effect: "Deal 5 + die value damage, On 6: Apply 1 Bleed", reusable: true },
      XY: { name: "Jab XY", requirement: "Any", effect: "Deal 6 + die value damage, On 5-6: Apply 2 Bleed", reusable: true },
    },
    "Jade Spear": {
      base: { name: "Jade Spear", requirement: "Even only", effect: "Apply Poison equal to die value" },
      x: { name: "Jade Spear x", requirement: "Even only", effect: "Apply Poison equal to die value, Gain 1 Shield" },
      y: { name: "Jade Spear y", requirement: "Even only", effect: "Apply Poison equal to die value + 1" },
      X: { name: "Jade Spear X", requirement: "Even only", effect: "Apply Poison equal to die value + 1, Gain 2 Shield, Apply 1 Blind" },
      Y: { name: "Jade Spear Y", requirement: "Even only", effect: "Apply Poison equal to die value + 2, Deal 3 damage" },
      XY: { name: "Jade Spear XY", requirement: "Even only", effect: "Apply Poison equal to die value + 3, Deal 5 damage, Gain 3 Shield, Apply 2 Blind" },
    },
    "Judgement": {
      base: { name: "Judgement", requirement: "Exactly 6", effect: "Deal 18 damage, Heal 6 HP, Apply 2 Lock" },
      x: { name: "Judgement x", requirement: "Exactly 6", effect: "Deal 18 damage, Heal 7 HP, Apply 2 Lock" },
      y: { name: "Judgement y", requirement: "Exactly 6", effect: "Deal 20 damage, Heal 6 HP, Apply 3 Lock" },
      X: { name: "Judgement X", requirement: "Exactly 6", effect: "Deal 22 damage, Heal 8 HP, Apply 3 Lock, Gain 3 Shield" },
      Y: { name: "Judgement Y", requirement: "Exactly 6", effect: "Deal 25 damage, Heal 7 HP, Apply 4 Lock, Apply 1 Blind" },
      XY: { name: "Judgement XY", requirement: "Exactly 6", effect: "Deal 28 damage, Heal 10 HP, Apply 5 Lock, Gain 5 Shield, Apply 2 Blind" },
    },
    "Life Drain": {
      base: { name: "Life Drain", requirement: "Odd only", effect: "Deal damage equal to die value, Heal 1 HP" },
      x: { name: "Life Drain x", requirement: "Odd only", effect: "Deal damage equal to die value, Heal half the damage dealt (rounded up)" },
      y: { name: "Life Drain y", requirement: "Odd only", effect: "Deal damage equal to die value + 1, Heal half the damage dealt (rounded up)", reusable: true },
      X: { name: "Life Drain X", requirement: "Odd only", effect: "Deal damage equal to die value + 2, Heal half the damage dealt (rounded up)" },
      Y: { name: "Life Drain Y", requirement: "Odd only", effect: "Deal damage equal to die value + 4, Heal half the damage dealt (rounded up)", reusable: true },
      XY: { name: "Life Drain XY", requirement: "Odd only", effect: "Deal damage equal to die value + 6, Heal the full damage dealt", reusable: true },
    },
    "Lightning Bolt": {
      base: { name: "Lightning Bolt", requirement: "Odd only", effect: "Deal triple die value damage", oncePerCombat: true },
      x: { name: "Lightning Bolt x", requirement: "Odd only", effect: "Deal triple die value damage, Apply 1 Blind", reusable: true },
      y: { name: "Lightning Bolt y", requirement: "Odd only", effect: "Deal quadruple die value damage", reusable: true },
      X: { name: "Lightning Bolt X", requirement: "Odd only", effect: "Deal quadruple die value damage, Apply 2 Blind, Apply 1 Lock", reusable: true },
      Y: { name: "Lightning Bolt Y", requirement: "Odd only", effect: "Deal quintuple die value damage, Apply 1 Frozen", reusable: true },
      XY: { name: "Lightning Bolt XY", requirement: "Odd only", effect: "Deal sextuple die value damage, Apply 3 Blind, Apply 2 Lock, Apply 2 Frozen", reusable: true },
    },
    "Lightning Storm": {
      base: { name: "Lightning Storm", requirement: "Limit 20", effect: "Deal 20 damage, Apply 2 Blind" },
      x: { name: "Lightning Storm x", requirement: "Limit 18", effect: "Deal 20 damage, Apply 2 Blind" },
      y: { name: "Lightning Storm y", requirement: "Limit 20", effect: "Deal 22 damage, Apply 3 Blind" },
      X: { name: "Lightning Storm X", requirement: "Limit 15", effect: "Deal 24 damage, Apply 3 Blind, Apply 2 Lock" },
      Y: { name: "Lightning Storm Y", requirement: "Limit 17", effect: "Deal 26 damage, Apply 4 Blind, Apply 1 Frozen" },
      XY: { name: "Lightning Storm XY", requirement: "Limit 12", effect: "Deal 30 damage, Apply 5 Blind, Apply 3 Lock, Apply 2 Frozen" },
    },
    "Maul": {
      base: { name: "Maul", requirement: "Any", effect: "Deal damage equal to die value + 4" },
      x: { name: "Maul x", requirement: "Any", effect: "Deal damage equal to die value + 5" },
      y: { name: "Maul y", requirement: "Any", effect: "Deal damage equal to die value + 5" },
      X: { name: "Maul X", requirement: "Any", effect: "Deal damage equal to die value + 6" },
      Y: { name: "Maul Y", requirement: "Any", effect: "Deal damage equal to die value + 8" },
      XY: { name: "Maul XY", requirement: "Any", effect: "Deal damage equal to die value + 12", reusable: true },
    },
    "Meteor": {
      base: { name: "Meteor", requirement: "Minimum 5", effect: "Deal 15 damage, Apply 2 Bleed", reusable: true },
      x: { name: "Meteor x", requirement: "Minimum 5", effect: "Deal 16 damage, Apply 2 Bleed", reusable: true },
      y: { name: "Meteor y", requirement: "Minimum 6", effect: "Deal 18 damage, Apply 3 Bleed", reusable: true },
      X: { name: "Meteor X", requirement: "Minimum 4", effect: "Deal 18 damage, Apply 3 Bleed, Apply 1 Poison", reusable: true },
      Y: { name: "Meteor Y", requirement: "Minimum 5", effect: "Deal 20 damage, Apply 4 Bleed, Apply 1 Blind", reusable: true },
      XY: { name: "Meteor XY", requirement: "Minimum 3", effect: "Deal 25 damage, Apply 5 Bleed, Apply 2 Poison, Apply 2 Blind", reusable: true },
    },
    "Mirror Hide": {
      base: { name: "Mirror Hide", requirement: "Any", effect: "Remove all negative effects from self, Apply them to opponent" },
      x: { name: "Mirror Hide x", requirement: "Any", effect: "Remove all negative effects from self, Apply them to opponent, Gain 2 Shield" },
      y: { name: "Mirror Hide y", requirement: "Any", effect: "Double all negative effects on opponent" },
      X: { name: "Mirror Hide X", requirement: "Any", effect: "Remove all negative effects from self, Double them and apply to opponent" },
      Y: { name: "Mirror Hide Y", requirement: "Any", effect: "Double all negative effects on opponent, Gain 3 Shield" },
      XY: { name: "Mirror Hide XY", requirement: "Any", effect: "Remove all negative effects from self, Triple them and apply to opponent, Gain 5 Shield" },
    },
    "Necromancy": {
      base: { name: "Necromancy", requirement: "Limit 12", effect: "Deal 15 damage, Heal 5 HP" },
      x: { name: "Necromancy x", requirement: "Limit 11", effect: "Deal 15 damage, Heal 5 HP" },
      y: { name: "Necromancy y", requirement: "Limit 12", effect: "Deal 17 damage, Heal 6 HP" },
      X: { name: "Necromancy X", requirement: "Limit 15", effect: "Deal 18 damage, Heal 6 HP" },
      Y: { name: "Necromancy Y", requirement: "Limit 10", effect: "Deal 20 damage, Heal 8 HP, Apply 1 Poison" },
      XY: { name: "Necromancy XY", requirement: "Limit 8", effect: "Deal 22 damage, Heal 10 HP, Apply 2 Poison, Gain 3 Shield" },
    },
    "Petrify": {
      base: { name: "Petrify", requirement: "On 6", effect: "Apply 2 Lock, Apply 1 Frozen" },
      x: { name: "Petrify x", requirement: "On 6", effect: "Apply 3 Lock, Apply 1 Frozen" },
      y: { name: "Petrify y", requirement: "On 6", effect: "Apply 2 Lock, Apply 2 Frozen" },
      X: { name: "Petrify X", requirement: "On 5-6", effect: "Apply 4 Lock, Apply 2 Frozen" },
      Y: { name: "Petrify Y", requirement: "On 5-6", effect: "Apply 3 Lock, Apply 3 Frozen, Apply 1 Blind" },
      XY: { name: "Petrify XY", requirement: "On 4-6", effect: "Apply 5 Lock, Apply 4 Frozen, Apply 2 Blind" },
    },
    "Phase Shift": {
      base: { name: "Phase Shift", requirement: "Exactly 1", effect: "Gain 4 Shield, Remove all negative effects from self" },
      x: { name: "Phase Shift x", requirement: "Exactly 1", effect: "Gain 5 Shield, Remove all negative effects from self" },
      y: { name: "Phase Shift y", requirement: "Exactly 1", effect: "Gain 4 Shield, Remove all negative effects from self, Heal 2 HP" },
      X: { name: "Phase Shift X", requirement: "Exactly 1", effect: "Gain 6 Shield, Remove all negative effects from self, Apply 1 Blind to opponent" },
      Y: { name: "Phase Shift Y", requirement: "Exactly 1", effect: "Gain 5 Shield, Remove all negative effects from self, Heal 4 HP" },
      XY: { name: "Phase Shift XY", requirement: "Exactly 1", effect: "Gain 8 Shield, Remove all negative effects from self, Heal 3 HP, Apply 2 Blind to opponent" },
    },
    "Phoenix Rising": {
      base: { name: "Phoenix Rising", requirement: "Exactly 1", effect: "Heal 10 HP, Gain 10 Shield, Remove all negative effects from self" },
      x: { name: "Phoenix Rising x", requirement: "Exactly 1", effect: "Heal 11 HP, Gain 10 Shield, Remove all negative effects from self" },
      y: { name: "Phoenix Rising y", requirement: "Exactly 1", effect: "Heal 10 HP, Gain 12 Shield, Remove all negative effects from self" },
      X: { name: "Phoenix Rising X", requirement: "Exactly 1", effect: "Heal 13 HP, Gain 12 Shield, Remove all negative effects from self, Apply 1 Poison to opponent" },
      Y: { name: "Phoenix Rising Y", requirement: "Exactly 1", effect: "Heal 12 HP, Gain 15 Shield, Remove all negative effects from self, Deal 5 damage" },
      XY: { name: "Phoenix Rising XY", requirement: "Exactly 1", effect: "Heal 15 HP, Gain 18 Shield, Remove all negative effects from self, Deal 8 damage, Apply 2 Poison to opponent" },
    },
    "Plague Breath": {
      base: { name: "Plague Breath", requirement: "Even only", effect: "Apply Poison equal to half die value (rounded up)" },
      x: { name: "Plague Breath x", requirement: "Even only", effect: "Apply Poison equal to half die value (rounded up), Apply 1 Blind" },
      y: { name: "Plague Breath y", requirement: "Even only", effect: "Apply Poison equal to die value" },
      X: { name: "Plague Breath X", requirement: "Even only", effect: "Apply Poison equal to die value, Apply 2 Blind" },
      Y: { name: "Plague Breath Y", requirement: "Even only", effect: "Apply Poison equal to die value + 1, Apply 1 Lock" },
      XY: { name: "Plague Breath XY", requirement: "Even only", effect: "Apply Poison equal to die value + 2, Apply 3 Blind, Apply 2 Lock" },
    },
    "Pounce": {
      base: { name: "Pounce", requirement: "Any", effect: "Deal 5 + die value damage", oncePerCombat: true },
      x: { name: "Pounce x", requirement: "Any", effect: "Deal 6 + die value damage", reusable: true },
      y: { name: "Pounce y", requirement: "Any", effect: "Deal 7 + die value damage", reusable: true },
      X: { name: "Pounce X", requirement: "Any", effect: "Deal 8 + die value damage, Apply 1 Bleed", reusable: true },
      Y: { name: "Pounce Y", requirement: "Any", effect: "Deal 9 + die value damage, Gain 2 Shield", reusable: true },
      XY: { name: "Pounce XY", requirement: "Any", effect: "Deal 12 + die value damage, Apply 2 Bleed, Gain 3 Shield", reusable: true },
    },
    "Reflecting Scales": {
      base: { name: "Reflecting Scales", requirement: "Any", effect: "Deal 2 damage, Apply 1 Blind" },
      x: { name: "Reflecting Scales x", requirement: "Any", effect: "Deal 4 damage, Apply 2 Blind" },
      y: { name: "Reflecting Scales y", requirement: "Any", effect: "Apply 2 Blind, Gain 2 Shield" },
      X: { name: "Reflecting Scales X", requirement: "Any", effect: "Deal 6 damage, Apply 3 Blind, Gain 1 Shield" },
      Y: { name: "Reflecting Scales Y", requirement: "Any", effect: "Apply 3 Blind, Gain 4 Shield, Remove 1 negative effect" },
      XY: { name: "Reflecting Scales XY", requirement: "Any", effect: "Deal 8 damage, Apply 4 Blind, Gain 5 Shield, Remove all negative effects" },
    },
    "Roar": {
      base: { name: "Roar", requirement: "Exactly 1", effect: "Apply 1 Lock" },
      x: { name: "Roar x", requirement: "Exactly 1", effect: "Apply 2 Lock" },
      y: { name: "Roar y", requirement: "Exactly 1", effect: "Apply 1 Lock, Apply 1 Blind" },
      X: { name: "Roar X", requirement: "Exactly 1", effect: "Apply 3 Lock, Apply 1 Blind" },
      Y: { name: "Roar Y", requirement: "Exactly 1", effect: "Apply 2 Lock, Apply 2 Blind, Gain 2 Shield" },
      XY: { name: "Roar XY", requirement: "Exactly 1", effect: "Apply 4 Lock, Apply 3 Blind, Gain 4 Shield" },
    },
    "Rupture": {
      base: { name: "Rupture", requirement: "Limit 10", effect: "Deal 8 damage, Apply 2 Poison" },
      x: { name: "Rupture x", requirement: "Limit 9", effect: "Deal 8 damage, Apply 2 Poison" },
      y: { name: "Rupture y", requirement: "Limit 10", effect: "Deal 10 damage, Apply 3 Poison" },
      X: { name: "Rupture X", requirement: "Limit 7", effect: "Deal 10 damage, Apply 3 Poison, Apply 1 Bleed" },
      Y: { name: "Rupture Y", requirement: "Limit 8", effect: "Deal 12 damage, Apply 4 Poison, Deal extra 2 damage per Poison on opponent" },
      XY: { name: "Rupture XY", requirement: "Limit 5", effect: "Deal 15 damage, Apply 5 Poison, Apply 2 Bleed, Deal extra 3 damage per Poison on opponent" },
    },
    "Rusty Dagger": {
      base: { name: "Rusty Dagger", requirement: "Odd only", effect: "Deal 2 damage" },
      x: { name: "Rusty Dagger x", requirement: "Odd only", effect: "Deal 3 damage" },
      y: { name: "Rusty Dagger y", requirement: "Odd only", effect: "Deal 3 damage, Apply 1 Poison" },
      X: { name: "Rusty Dagger X", requirement: "Odd only", effect: "Deal 4 damage, Apply 1 Poison" },
      Y: { name: "Rusty Dagger Y", requirement: "Odd only", effect: "Deal 4 damage, Apply 2 Poison" },
      XY: { name: "Rusty Dagger XY", requirement: "Odd only", effect: "Deal 6 damage, Apply 3 Poison, Apply 1 Bleed" },
    },
    "Screech": {
      base: { name: "Screech", requirement: "Exactly 1", effect: "Apply 2 Blind, Apply 1 Lock" },
      x: { name: "Screech x", requirement: "Exactly 1", effect: "Apply 3 Blind, Apply 1 Lock" },
      y: { name: "Screech y", requirement: "Exactly 1", effect: "Apply 2 Blind, Apply 2 Lock" },
      X: { name: "Screech X", requirement: "Exactly 1", effect: "Apply 4 Blind, Apply 2 Lock" },
      Y: { name: "Screech Y", requirement: "Exactly 1", effect: "Apply 3 Blind, Apply 3 Lock, Deal 3 damage" },
      XY: { name: "Screech XY", requirement: "Exactly 1", effect: "Apply 5 Blind, Apply 4 Lock, Deal 5 damage" },
    },
    "Shield": {
      base: { name: "Shield", requirement: "Even only", effect: "Gain Shield equal to half the die value" },
      x: { name: "Shield x", requirement: "Even only", effect: "Gain shield equal to the die value" },
      y: { name: "Shield y", requirement: "Even only", effect: "Gain Shield equal to half the die value", reusable: true },
      X: { name: "Shield X", requirement: "Even only", effect: "Gain Shield equal to die value" },
      Y: { name: "Shield Y", requirement: "Even only", effect: "Gain Shield equal to die value", reusable: true },
      XY: { name: "Shield XY", requirement: "Even only", effect: "Gain Shield equal to die value + 2, Heal 1 HP", reusable: true },
    },
    "Shortbow": {
      base: { name: "Shortbow", requirement: "3 or below", effect: "Deal double die value damage" },
      x: { name: "Shortbow x", requirement: "Odd only", effect: "Deal double die value damage" },
      X: { name: "Shortbow X", requirement: "Odd only", effect: "Deal triple die value damage" },
      y: { name: "Shortbow y", requirement: "Even only", effect: "Deal double die value damage, Apply 1 Bleed" },
      Y: { name: "Shortbow Y", requirement: "Even only", effect: "Deal double die value damage, Apply 2 Bleed" },
      XY: { name: "Shortbow XY", requirement: "Any", effect: "Deal quadruple die value damage, Apply 2 Blind, Apply 2 Bleed" },
    },
    "Snipe": {
      base: { name: "Snipe", requirement: "Limit 15", effect: "Deal 8 damage, Apply 1 Bleed (activates when limit reaches 0)" },
      x: { name: "Snipe x", requirement: "Limit 15", effect: "Deal 12 damage, Apply 1 Bleed (activates when limit reaches 0)" },
      y: { name: "Snipe y", requirement: "Limit 15", effect: "Deal 10 damage, Apply 2 Bleed" },
      X: { name: "Snipe X", requirement: "Limit 18", effect: "Deal 15 damage, Apply 2 Bleed" },
      Y: { name: "Snipe Y", requirement: "Limit 22", effect: "Deal 18 damage, Apply 3 Bleed, Heal 3 HP" },
      XY: { name: "Snipe XY", requirement: "Limit 18", effect: "Deal 22 damage, Apply 4 Bleed, Heal 4 HP, Gain 2 Shield" },
    },
    "Soul Rend": {
      base: { name: "Soul Rend", requirement: "Minimum 4", effect: "Deal 8 damage, Apply 1 Bleed", reusable: true },
      x: { name: "Soul Rend x", requirement: "Minimum 4", effect: "Deal 9 damage, Apply 1 Bleed", reusable: true },
      y: { name: "Soul Rend y", requirement: "Minimum 5", effect: "Deal 10 damage, Apply 2 Bleed", reusable: true },
      X: { name: "Soul Rend X", requirement: "Minimum 3", effect: "Deal 10 damage, Apply 2 Bleed, Heal 1 HP", reusable: true },
      Y: { name: "Soul Rend Y", requirement: "Minimum 4", effect: "Deal 12 damage, Apply 3 Bleed, Apply 1 Poison", reusable: true },
      XY: { name: "Soul Rend XY", requirement: "Minimum 2", effect: "Deal 14 damage, Apply 4 Bleed, Heal 2 HP, Apply 2 Poison", reusable: true },
    },
    "Spectral Strike": {
      base: { name: "Spectral Strike", requirement: "Any", effect: "Deal damage equal to die value, On 5-6: Apply 1 Bleed" },
      x: { name: "Spectral Strike x", requirement: "Any", effect: "Deal damage equal to die value + 1, On 5-6: Apply 1 Bleed" },
      y: { name: "Spectral Strike y", requirement: "Any", effect: "Deal damage equal to die value, On 4-6: Apply 2 Bleed" },
      X: { name: "Spectral Strike X", requirement: "Any", effect: "Deal damage equal to die value + 2, On 4-6: Apply 2 Bleed, Gain 1 Shield" },
      Y: { name: "Spectral Strike Y", requirement: "Any", effect: "Deal damage equal to die value + 1, On 3-6: Apply 3 Bleed" },
      XY: { name: "Spectral Strike XY", requirement: "Any", effect: "Deal damage equal to die value + 3, On 3-6: Apply 4 Bleed, Gain 2 Shield" },
    },
    "Splinter": {
      base: { name: "Splinter", requirement: "Any", effect: "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)" },
      x: { name: "Splinter x", requirement: "Any", effect: "Create 2 dice with half the input die value (rounded down)" },
      y: { name: "Splinter y", requirement: "Any", effect: "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded up)" },
      X: { name: "Splinter X", requirement: "Any", effect: "Sacrifice 2 HP, Create 2 dice with half the input die value (rounded down)", reusable: true },
      Y: { name: "Splinter Y", requirement: "Minimum 2", effect: "Sacrifice 2 HP, Create 3 dice with half the input die value (rounded up)" },
      XY: { name: "Splinter XY", requirement: "Any", effect: "Sacrifice 1 HP, Create 3 dice with half the input die value (rounded up)", reusable: true },
    },
    "Stone Hide": {
      base: { name: "Stone Hide", requirement: "Even only", effect: "Gain Shield equal to die value + 2", reusable: true },
      x: { name: "Stone Hide x", requirement: "Even only", effect: "Gain Shield equal to die value + 3", reusable: true },
      y: { name: "Stone Hide y", requirement: "Even only", effect: "Gain Shield equal to die value + 2, Heal 1 HP", reusable: true },
      X: { name: "Stone Hide X", requirement: "Even only", effect: "Gain Shield equal to die value + 4, Remove 1 negative effect", reusable: true },
      Y: { name: "Stone Hide Y", requirement: "Even only", effect: "Gain Shield equal to die value + 3, Heal 2 HP, Apply 1 Lock to opponent", reusable: true },
      XY: { name: "Stone Hide XY", requirement: "Even only", effect: "Gain Shield equal to die value + 6, Heal 2 HP, Remove all negative effects", reusable: true },
    },
    "Sunstrike": {
      base: { name: "Sunstrike", requirement: "Limit 4", effect: "Deal 3 damage, Apply 1 Blind" },
      x: { name: "Sunstrike x", requirement: "Limit 4", effect: "Deal 4 damage, Apply 1 Blind" },
      y: { name: "Sunstrike y", requirement: "Limit 4", effect: "Deal 3 damage, Apply 2 Blind" },
      X: { name: "Sunstrike X", requirement: "Limit 3", effect: "Deal 5 damage, Apply 2 Blind, Apply 1 Lock" },
      Y: { name: "Sunstrike Y", requirement: "Limit 3", effect: "Deal 4 damage, Apply 3 Blind, Heal 1 HP" },
      XY: { name: "Sunstrike XY", requirement: "Limit 2", effect: "Deal 7 damage, Apply 4 Blind, Apply 2 Lock, Heal 2 HP" },
    },
    "Swipe": {
      base: { name: "Swipe", requirement: "Limit 5", effect: "Deal 3 damage, Heal 1 HP" },
      x: { name: "Swipe x", requirement: "Any", effect: "Deal 3 damage + 1 for each use this round", reusable: true },
      y: { name: "Swipe y", requirement: "Limit 5", effect: "Deal 5 damage, Heal 2 HP" },
      X: { name: "Swipe X", requirement: "Any", effect: "Deal 2 damage + 2 for each use this round", reusable: true },
      Y: { name: "Swipe Y", requirement: "Limit 3", effect: "Deal 7 damage, Heal 3 HP" },
      XY: { name: "Swipe XY", requirement: "Any", effect: "Deal 3 damage + 3 for each use this round, Heal 2 HP", reusable: true },

    },
    "Talon Strike": {
      base: { name: "Talon Strike", requirement: "Any", effect: "Deal damage equal to die value + 3, On 6: Apply 1 Bleed", reusable: true },
      x: { name: "Talon Strike x", requirement: "Any", effect: "Deal damage equal to die value + 4, On 6: Apply 1 Bleed", reusable: true },
      y: { name: "Talon Strike y", requirement: "Any", effect: "Deal damage equal to die value + 3, On 5-6: Apply 2 Bleed", reusable: true },
      X: { name: "Talon Strike X", requirement: "Any", effect: "Deal damage equal to die value + 5, On 5-6: Apply 2 Bleed, Gain 1 Shield", reusable: true },
      Y: { name: "Talon Strike Y", requirement: "Any", effect: "Deal damage equal to die value + 4, On 4-6: Apply 3 Bleed", reusable: true },
      XY: { name: "Talon Strike XY", requirement: "Any", effect: "Deal damage equal to die value + 7, On 4-6: Apply 4 Bleed, Gain 2 Shield", reusable: true },
    },
    "Thunderclap": {
      base: { name: "Thunderclap", requirement: "Limit 25", effect: "Deal 18 damage, Apply 3 Blind, Apply 2 Lock" },
      x: { name: "Thunderclap x", requirement: "Limit 23", effect: "Deal 18 damage, Apply 3 Blind, Apply 2 Lock" },
      y: { name: "Thunderclap y", requirement: "Limit 25", effect: "Deal 20 damage, Apply 4 Blind, Apply 3 Lock" },
      X: { name: "Thunderclap X", requirement: "Limit 20", effect: "Deal 22 damage, Apply 4 Blind, Apply 3 Lock, Apply 1 Frozen" },
      Y: { name: "Thunderclap Y", requirement: "Limit 22", effect: "Deal 25 damage, Apply 5 Blind, Apply 4 Lock" },
      XY: { name: "Thunderclap XY", requirement: "Limit 18", effect: "Deal 28 damage, Apply 6 Blind, Apply 5 Lock, Apply 2 Frozen" },
    },
    "Torture": {
      base: { name: "Torture", requirement: "Limit 20", effect: "Deal 15 damage, Apply 2 Bleed, Apply 2 Lock" },
      x: { name: "Torture x", requirement: "Limit 18", effect: "Deal 15 damage, Apply 2 Bleed, Apply 2 Lock" },
      y: { name: "Torture y", requirement: "Limit 20", effect: "Deal 18 damage, Apply 3 Bleed, Apply 3 Lock" },
      X: { name: "Torture X", requirement: "Limit 15", effect: "Deal 18 damage, Apply 3 Bleed, Apply 3 Lock, Apply 1 Poison" },
      Y: { name: "Torture Y", requirement: "Limit 17", effect: "Deal 20 damage, Apply 4 Bleed, Apply 4 Lock" },
      XY: { name: "Torture XY", requirement: "Limit 12", effect: "Deal 25 damage, Apply 5 Bleed, Apply 5 Lock, Apply 2 Poison, Apply 2 Blind" },
    },
    "Totem": {
      base: { name: "Totem", requirement: "Exactly 2", effect: "Gain 5 Shield, Heal 2 HP" },
      x: { name: "Totem x", requirement: "Exactly 2", effect: "Gain 6 Shield, Heal 2 HP" },
      y: { name: "Totem y", requirement: "Exactly 2", effect: "Gain 5 Shield, Heal 3 HP" },
      X: { name: "Totem X", requirement: "Exactly 2", effect: "Gain 8 Shield, Heal 4 HP" },
      Y: { name: "Totem Y", requirement: "Exactly 2", effect: "Gain 7 Shield, Heal 5 HP, Remove 1 negative effect" },
      XY: { name: "Totem XY", requirement: "Exactly 2", effect: "Gain 10 Shield, Heal 6 HP, Remove all negative effects" },
    },
    "Trample": {
      base: { name: "Trample", requirement: "Any", effect: "Deal damage equal to die value, On 6: Apply 1 Lock" },
      x: { name: "Trample x", requirement: "Any", effect: "Deal damage equal to die value + 1, On 6: Apply 1 Lock" },
      y: { name: "Trample y", requirement: "Any", effect: "Deal damage equal to die value, On 5-6: Apply 2 Lock" },
      X: { name: "Trample X", requirement: "Any", effect: "Deal damage equal to die value + 2, On 5-6: Apply 2 Lock" },
      Y: { name: "Trample Y", requirement: "Any", effect: "Deal damage equal to die value + 3, On 4-6: Apply 3 Lock" },
      XY: { name: "Trample XY", requirement: "Any", effect: "Deal damage equal to die value + 4, On 4-6: Apply 4 Lock, Apply 1 Bleed" },
    },
    "Tremor": {
      base: { name: "Tremor", requirement: "Any", effect: "Deal damage equal to die value, Apply Lock equal to (die value ÷ 3, rounded down)" },
      x: { name: "Tremor x", requirement: "Any", effect: "Deal damage equal to die value + 1, Apply Lock equal to (die value ÷ 3, rounded down)" },
      y: { name: "Tremor y", requirement: "Any", effect: "Deal damage equal to die value, Apply Lock equal to (die value ÷ 2, rounded down)" },
      X: { name: "Tremor X", requirement: "Any", effect: "Deal damage equal to die value + 2, Apply Lock equal to (die value ÷ 2, rounded down)" },
      Y: { name: "Tremor Y", requirement: "Any", effect: "Deal damage equal to die value + 1, Apply Lock equal to (die value ÷ 2, rounded up)" },
      XY: { name: "Tremor XY", requirement: "Any", effect: "Deal damage equal to die value + 3, Apply Lock equal to die value" },
    },
    "Whip Crack": {
      base: { name: "Whip Crack", requirement: "Any", effect: "Deal damage equal to die value + 5, Apply 1 Lock" },
      x: { name: "Whip Crack x", requirement: "Any", effect: "Deal damage equal to die value + 6, Apply 1 Lock" },
      y: { name: "Whip Crack y", requirement: "Any", effect: "Deal damage equal to die value + 5, Apply 2 Lock" },
      X: { name: "Whip Crack X", requirement: "Any", effect: "Deal damage equal to die value + 7, Apply 2 Lock, Apply 1 Bleed" },
      Y: { name: "Whip Crack Y", requirement: "Any", effect: "Deal damage equal to die value + 6, Apply 3 Lock, Sacrifice 1 HP" },
      XY: { name: "Whip Crack XY", requirement: "Any", effect: "Deal damage equal to die value + 9, Apply 4 Lock, Apply 2 Bleed" },
    },
    "Wind Slash": {
      base: { name: "Wind Slash", requirement: "Any", effect: "Deal damage equal to die value + 4, On 6: Apply 2 Bleed", reusable: true },
      x: { name: "Wind Slash x", requirement: "Any", effect: "Deal damage equal to die value + 5, On 6: Apply 2 Bleed", reusable: true },
      y: { name: "Wind Slash y", requirement: "Any", effect: "Deal damage equal to die value + 4, On 5-6: Apply 3 Bleed", reusable: true },
      X: { name: "Wind Slash X", requirement: "Any", effect: "Deal damage equal to die value + 6, On 5-6: Apply 3 Bleed, Gain 1 Shield", reusable: true },
      Y: { name: "Wind Slash Y", requirement: "Any", effect: "Deal damage equal to die value + 5, On 4-6: Apply 4 Bleed", reusable: true },
      XY: { name: "Wind Slash XY", requirement: "Any", effect: "Deal damage equal to die value + 8, On 4-6: Apply 5 Bleed, Gain 2 Shield", reusable: true },
    },
  };

  const UpgradeCard = ({ cardName, cardData }) => {
    const isExpanded = expandedCards[cardName];
    const hasUpgrades = Object.values(cardData).some(v => v !== "[UNDEFINED]" && v !== cardData.base);

    return (
      <div className="bg-gray-800 rounded-lg border-2 border-gray-700 overflow-hidden">
        <button
          onClick={() => toggleCard(cardName)}
          className="w-full p-4 flex items-center justify-between hover:bg-gray-750 transition-colors"
        >
          <div className="flex items-center gap-3">
            {isExpanded ? <ChevronDown className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
            <h3 className="text-lg font-bold text-blue-300">{cardName}</h3>
          </div>
          {!hasUpgrades && <span className="text-xs text-gray-500 italic">No upgrades defined</span>}
        </button>

        {isExpanded && (
          <div className="p-4 pt-0 space-y-3">
            {/* Base Card */}
            <div className="bg-gray-700 rounded p-3 border-l-4 border-green-500">
              <div className="text-sm font-semibold text-green-400 mb-1">BASE</div>
              {cardData.base === "[UNDEFINED]" ? (
                <div className="text-gray-500 italic text-sm">[UNDEFINED]</div>
              ) : (
                <>
                  <div className="font-semibold text-blue-200">{cardData.base.name}</div>
                  <div className="text-xs text-gray-300 mt-1">
                    {cardData.base.requirement} → {cardData.base.effect}
                  </div>
                  {cardData.base.reusable && <span className="text-xs text-green-400"> (Reusable)</span>}
                  {cardData.base.oncePerCombat && <span className="text-xs text-red-400"> (Once per combat)</span>}
                </>
              )}
            </div>

            {/* Tier 1 Upgrades (x and y) */}
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-gray-700 rounded p-3 border-l-4 border-yellow-500">
                <div className="text-sm font-semibold text-yellow-400 mb-1">TIER 1: x variant</div>
                {cardData.x === "[UNDEFINED]" ? (
                  <div className="text-gray-500 italic text-sm">[UNDEFINED]</div>
                ) : (
                  <>
                    <div className="font-semibold text-blue-200">{cardData.x.name}</div>
                    <div className="text-xs text-gray-300 mt-1">
                      {cardData.x.requirement} → {cardData.x.effect}
                    </div>
                    {cardData.x.reusable && <span className="text-xs text-green-400"> (Reusable)</span>}
                    {cardData.x.oncePerCombat && <span className="text-xs text-red-400"> (Once per combat)</span>}
                  </>
                )}
              </div>

              <div className="bg-gray-700 rounded p-3 border-l-4 border-yellow-500">
                <div className="text-sm font-semibold text-yellow-400 mb-1">TIER 1: y variant</div>
                {cardData.y === "[UNDEFINED]" ? (
                  <div className="text-gray-500 italic text-sm">[UNDEFINED]</div>
                ) : (
                  <>
                    <div className="font-semibold text-blue-200">{cardData.y.name}</div>
                    <div className="text-xs text-gray-300 mt-1">
                      {cardData.y.requirement} → {cardData.y.effect}
                    </div>
                    {cardData.y.reusable && <span className="text-xs text-green-400"> (Reusable)</span>}
                    {cardData.y.oncePerCombat && <span className="text-xs text-red-400"> (Once per combat)</span>}
                  </>
                )}
              </div>
            </div>

            {/* Tier 2 Upgrades (X and Y) */}
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-gray-700 rounded p-3 border-l-4 border-purple-500">
                <div className="text-sm font-semibold text-purple-400 mb-1">TIER 2: X variant</div>
                {cardData.X === "[UNDEFINED]" ? (
                  <div className="text-gray-500 italic text-sm">[UNDEFINED]</div>
                ) : (
                  <>
                    <div className="font-semibold text-blue-200">{cardData.X.name}</div>
                    <div className="text-xs text-gray-300 mt-1">
                      {cardData.X.requirement} → {cardData.X.effect}
                    </div>
                    {cardData.X.reusable && <span className="text-xs text-green-400"> (Reusable)</span>}
                    {cardData.X.oncePerCombat && <span className="text-xs text-red-400"> (Once per combat)</span>}
                  </>
                )}
              </div>

              <div className="bg-gray-700 rounded p-3 border-l-4 border-purple-500">
                <div className="text-sm font-semibold text-purple-400 mb-1">TIER 2: Y variant</div>
                {cardData.Y === "[UNDEFINED]" ? (
                  <div className="text-gray-500 italic text-sm">[UNDEFINED]</div>
                ) : (
                  <>
                    <div className="font-semibold text-blue-200">{cardData.Y.name}</div>
                    <div className="text-xs text-gray-300 mt-1">
                      {cardData.Y.requirement} → {cardData.Y.effect}
                    </div>
                    {cardData.Y.reusable && <span className="text-xs text-green-400"> (Reusable)</span>}
                    {cardData.Y.oncePerCombat && <span className="text-xs text-red-400"> (Once per combat)</span>}
                  </>
                )}
              </div>
            </div>

            {/* Ultimate Upgrade (XY) */}
            <div className="bg-gray-700 rounded p-3 border-l-4 border-red-500">
              <div className="text-sm font-semibold text-red-400 mb-1">ULTIMATE: XY variant</div>
              {cardData.XY === "[UNDEFINED]" ? (
                <div className="text-gray-500 italic text-sm">[UNDEFINED]</div>
              ) : (
                <>
                  <div className="font-semibold text-blue-200">{cardData.XY.name}</div>
                  <div className="text-xs text-gray-300 mt-1">
                    {cardData.XY.requirement} → {cardData.XY.effect}
                  </div>
                  {cardData.XY.reusable && <span className="text-xs text-green-400"> (Reusable)</span>}
                  {cardData.XY.oncePerCombat && <span className="text-xs text-red-400"> (Once per combat)</span>}
                </>
              )}
            </div>
          </div>
        )}
      </div>
    );
  };

  const sortedCards = Object.keys(cardProgression).sort();

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-2 text-center bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          Card Upgrade Progression System
        </h1>
        <p className="text-center text-gray-400 mb-8">Loop Hero-inspired upgrade paths for Dicey Dungeons</p>

        <div className="mb-8 p-4 bg-gray-800 rounded-lg border-2 border-blue-700">
          <h2 className="text-xl font-semibold mb-3 text-blue-400">Upgrade Path Rules:</h2>
          <div className="space-y-2 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-green-500"></div>
              <span><strong>BASE</strong> - Starting card variant</span>
            </div>
            <div className="flex items-center gap-2">
              <ArrowRight className="w-4 h-4 text-gray-500" />
              <div className="w-4 h-4 rounded bg-yellow-500"></div>
              <span><strong>TIER 1 (x/y)</strong> - Two upgrade options from BASE</span>
            </div>
            <div className="flex items-center gap-2">
              <ArrowRight className="w-4 h-4 text-gray-500" />
              <div className="w-4 h-4 rounded bg-purple-500"></div>
              <span><strong>TIER 2 (X/Y)</strong> - Advanced upgrades from x/y variants</span>
            </div>
            <div className="flex items-center gap-2">
              <ArrowRight className="w-4 h-4 text-gray-500" />
              <div className="w-4 h-4 rounded bg-red-500"></div>
              <span><strong>ULTIMATE (XY)</strong> - Final form combining both upgrade paths</span>
            </div>
          </div>
        </div>

        <div className="mb-4 text-center text-sm text-gray-400">
          {sortedCards.length} unique card families • Click to expand
        </div>

        <div className="space-y-2">
          {sortedCards.map(cardName => (
            <UpgradeCard
              key={cardName}
              cardName={cardName}
              cardData={cardProgression[cardName]}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default CardUpgradeProgression;
