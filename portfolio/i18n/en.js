window.I18N_LOCALES = window.I18N_LOCALES || {};
window.I18N_LOCALES.en = {
  languageName: "English",
  menu: {
    titleSubtitle: "A Dice & Card Adventure",
    begin: "Begin",
    continue: "Continue",
    importSave: "Import Save",
    languageLabel: "Language"
  },
  town: {
    defaultPlayerName: "Adventurer",
    stats: {
      hp: "HP",
      level: "Level",
      gold: "Gold",
      xp: "XP"
    },
    actions: {
      adventureName: "Adventure",
      adventureDesc: "Head into the wilderness and fight enemies",
      restName: "Rest",
      restDesc: "Sleep at the tavern and recover all HP",
      inventoryName: "Inventory & Deck",
      inventoryDesc: "Manage your cards and active deck",
      shopName: "Shop",
      shopDesc: "Buy cards from the Naukin shopkeep",
      blacksmithName: "Blacksmith",
      blacksmithDesc: "Forge 2 identical cards into an upgrade",
      trainingName: "Training",
      trainingDesc: "Improve your stats with Thessa's coaching"
    },
    gameManagement: "Game Management",
    buttons: {
      save: "Save",
      exportSave: "Export Save",
      importSave: "Import Save",
      mainMenu: "Main Menu"
    },
    meta: "{className} · {biome} Tier {tier}"
  },
  biomes: {
    1: "Plains",
    2: "Tundra",
    3: "Forest",
    4: "Ruins",
    5: "Slopes",
    6: "Pit"
  },
  charCreate: {
    title: "Create Your Adventurer",
    yourName: "Your Name",
    namePlaceholder: "Enter your name...",
    chooseClass: "Choose a Class",
    difficulty: "Difficulty",
    easy: "Easy",
    normal: "Normal",
    punishing: "Punishing",
    difficultyDescs: {
      easy: "Keep all loot when defeated",
      normal: "Lose 50% loot when defeated",
      punishing: "Lose all loot when defeated"
    },
    beginTale: "Begin the Tale",
    back: "Back"
  },
  classes: {
    Fencer: {
      name: "Fencer",
      desc: "Once per turn, you may reroll (level) dice."
    },
    Knight: {
      name: "Knight",
      desc: "Roll dice individually. Hit your limit exactly for powerful boons; exceed it and lose your turn."
    },
    Cleric: {
      name: "Cleric",
      desc: "When you roll matching dice, heal that amount. At level 2+, convert excess healing to shield."
    },
    Warlock: {
      name: "Warlock",
      desc: "When you apply status effects or shield, apply extra equal to level."
    },
    Druid: {
      name: "Druid",
      desc: "Once per turn, 'plant' a die. Next turn it blooms into additional dice."
    },
    Rogue: {
      name: "Rogue",
      desc: "Choose a lucky number for each battle. Each roll of it grants (2 × level) bonus damage."
    }
  },
  starterScreen: {
    title: "Thessa's Welcome Gift",
    story1: "Thessa places a wooden box on the counter and opens it, revealing an assortment of basic equipment.",
    story2: '"Before you head out," she says, "you should take some proper gear. I won\'t let you fight with scraps."',
    story3: '"Pick three items. Consider them a welcome gift to Ascus."',
    chooseLabel: "Choose 3 items ({count}/3 chosen)",
    takeEquipment: "Take Your Equipment",
    autoSelect: "Auto-Select 3"
  },
  prologue: {
    title: "Prologue",
    playTutorial: "Play tutorial?",
    yes: "Yes",
    no: "No",
    fight: "Fight",
    continue: "Continue",
    getUp: "GET UP?"
  },
  combat: {
    logTitle: "⚔ Combat Log",
    yourTurn: "Your Turn",
    yourDice: "Your Dice",
    hand: "Hand",
    playCard: "Play Card",
    endTurn: "End Turn",
    enemyAbilities: "Enemy Abilities",
    round: "Round",
    fight: "Fight",
    retreat: "Retreat",
    keepFighting: "Keep Fighting",
    winStreak: "Win Streak",
    legendary: "LEGENDARY",
    engage: "Engage",
    faceDoom: "⚡ Face Your Doom",
    genericEnemyFlavor: "{name} stands in your way in {biome}."
  },
  tutorial: {
    header: "TUTORIAL",
    next: "Next",
    understood: "Understood",
    firstCombat: {
      title: "Tutorial Combat",
      text: "This optional battle teaches you the combat loop. You can still use click-to-select and Play Card, or drag a die directly onto a card to play it."
    },
    deckBasics: {
      title: "Your Deck",
      text: "Cards are drawn randomly from your deck each combat round, up to your hand limit. Cards you don't play stay in your hand between turns. Used and reusable cards go to the discard pile and shuffle back in when your deck runs out."
    },
    diceBasics: {
      title: "Dice & Cards",
      text: "Each turn you roll dice (start with 2, but can train up). Pick a die, then a card (or card then die). Each card has a requirement — Any, Even, Odd, Min X, Exactly X. Use a valid die to activate the card's effect."
    },
    endTurn: {
      title: "End Your Turn",
      text: "Click End Turn when done. Unplayed cards stay in your hand. The enemy takes their turn, then a new round begins. Between fights you can retreat to town — but not mid-combat."
    }
  },
  statusHelp: {
    poison: {
      title: "Poison",
      text: "Start of turn: take {v} (equal to poison level) damage, then Poison decreases by 1."
    },
    bleed: {
      title: "Bleed",
      text: "End of turn: take {v} (equal to bleed level) damage, then Bleed decreases by 1."
    },
    burn: {
      title: "Burn",
      text: "When you play a card: take {v} damage (burn level × 2), then Burn decreases by 1."
    },
    lock: {
      title: "Lock",
      text: "When dice are rolled: lose up to {v} dice, then Lock decreases by that amount."
    },
    freeze: {
      title: "Frozen",
      text: "When dice are rolled: up to {v} dice showing above 1 are forced to 1."
    },
    blind: {
      title: "Blind",
      text: "When dice are rolled: up to {v} dice are hidden this turn."
    },
    shield: {
      title: "Shield",
      text: "Blocks incoming HP damage first. Remaining shield: {v}."
    }
  },
  cardNames: {
    "Afflict": "Afflict",
    "Annihilation": "Annihilation",
    "Apocalypse": "Apocalypse",
    "Bash": "Bash",
    "Bite": "Bite",
    "Bellow": "Bellow",
    "Blood Pact": "Blood Pact",
    "Blood Ritual": "Blood Ritual",
    "Boulder Toss": "Boulder Toss",
    "Chain Lightning": "Chain Lightning",
    "Charge": "Charge",
    "Chomp": "Chomp",
    "Claw Swipe": "Claw Swipe",
    "Cleansing Fire": "Cleansing Fire",
    "Club": "Club",
    "Control": "Control",
    "Curse": "Curse",
    "Dagger": "Dagger",
    "Dark Blessing": "Dark Blessing",
    "Dark Aegis": "Dark Aegis",
    "Desperation": "Desperation",
    "Divebomb": "Divebomb",
    "Dominate": "Dominate",
    "Earthshatter": "Earthshatter",
    "Earthquake": "Earthquake",
    "Evade": "Evade",
    "Execution": "Execution",
    "Flail": "Flail",
    "Flame Burst": "Flame Burst",
    "Flame Strike": "Flame Strike",
    "Flame Wall": "Flame Wall",
    "Fortify": "Fortify",
    "Frosted Dagger": "Frosted Dagger",
    "Frosted Spear": "Frosted Spear",
    "Gore": "Gore",
    "Haunting Wail": "Haunting Wail",
    "Hellfire": "Hellfire",
    "Howl": "Howl",
    "Ice Magic": "Ice Magic",
    "Immolate": "Immolate",
    "Jab": "Jab",
    "Jade Spear": "Jade Spear",
    "Judgement": "Judgement",
    "Life Drain": "Life Drain",
    "Lightning Bolt": "Lightning Bolt",
    "Lightning Storm": "Lightning Storm",
    "Maul": "Maul",
    "Meteor": "Meteor",
    "Mirror Hide": "Mirror Hide",
    "Necromancy": "Necromancy",
    "Petrify": "Petrify",
    "Phase Step": "Phase Step",
    "Phoenix Rising": "Phoenix Rising",
    "Plague Breath": "Plague Breath",
    "Reflecting Scales": "Reflecting Scales",
    "Roar": "Roar",
    "Rupture": "Rupture",
    "Rusty Dagger": "Rusty Dagger",
    "Screech": "Screech",
    "Shield": "Shield",
    "Shortbow": "Shortbow",
    "Snipe": "Snipe",
    "Soul Rend": "Soul Rend",
    "Spectral Strike": "Spectral Strike",
    "Splinter": "Splinter",
    "Stone Hide": "Stone Hide",
    "Sunstrike": "Sunstrike",
    "Swipe": "Swipe",
    "Talon Strike": "Talon Strike",
    "Thunderclap": "Thunderclap",
    "Torture": "Torture",
    "Totem": "Totem",
    "Trample": "Trample",
    "Tremor": "Tremor",
    "Whip Crack": "Whip Crack",
    "Wind Slash": "Wind Slash",
    "Wooden Sword": "Wooden Sword",
    "Slingshot": "Slingshot",
    "Small Stone": "Small Stone",
    "Makeshift Shield": "Makeshift Shield",
    "Bandage": "Bandage",
    "Sharpened Stick": "Sharpened Stick"
  },
  enemyFlavor: {
    // Plains
    "Wolf": "A lean, hungry wolf emerges from the tall grass. Yellow eyes track your every move.",
    "Giant Locust": "A grasshopper the size of a dog. Its jaws click rhythmically while its legs tremble with energy.",
    "Naukin Outcast": "A ratman in tattered clothes, fur matted with filth. Cast out and desperate—and therefore dangerous.",
    "Dire Wolves": "A pack that moves as one. Dire wolves are much larger than common wolves and far more cunning.",
    "Prowling Dellinid": "An enormous dark puma, long in body and low to the ground. It hunts you across the plains.",
    "Juvenile Auroc": "A young auroc, golden-scaled and long-limbed like a galloping crocodile. Young, but still lethal.",
    "Bovari Bandit": "A bovari renegade—broad and heavy, with four arms and an old grudge. This will be ugly.",
    "Roaming Gallox": "A wild gallox ox without a rider. Its aggression has no direction except straight at you.",
    "Lone Plainsdrake": "A full-grown auroc circling you. The golden scales throw light in confusing patterns.",
    // Tundra
    "Blue Dellinid": "A dellinid from the north, its dark fur shot through with pale blue that melts uncannily into snow and ice. It moves soundlessly on frozen ground.",
    "Khinari Exile": "Pale-hided and sharp-eyed, this khinari was cast out from its tundral bastion. Their fallen noble race is corrupted by ruin, but the landless are perhaps the most unpredictable of all.",
    "Territorial Whitespike": "A beast with massive curved horns and broad shoveled tusks built to dig through permafrost. It lowers its head at your approach. You stand on its territory.",
    "Khinari Raider": "Lean and cold-eyed, a khinari warrior of the raider caste—the second rung of a violent hierarchy. Their bloody gods demand sacrifice. Today, you are the offering.",
    "Tundra Boneguard": "An armored skeleton, morning star in hand, that continues to move through tundral cold with no visible purpose except violence. Its legs are crusted with frost. It does not slow down.",
    "Alpha Whitespike": "The dominant beast in an upland herd. Its horns are notched from a dozen battles. It snorts a cloud of frozen breath and stamps once—a warning of something already decided.",
    "Veteran Boneguard": "A Boneguard that has endured long enough to merit the title. Its armor is marked by countless old scars. Something keeps it moving that has nothing to do with muscle or will.",
    "Khinari Hunting Party": "Three—no, four of them emerge from the white. A khinari hunting party, organized and silent. They were looking for prey. They found you instead.",
    "Hungry Frost Wyrm": "The apex predator of the tundra: a frost wyrm, lean from a hard winter, moving with the lazy threat of something that has never truly needed to hurry.",
    // Forest
    "Naukin Scouts": "A trio of naukin scouts—ratmen in tight formation, alert and quick. Naukin are withdrawn and orderly, and they do not appreciate trespassers in their forest.",
    "Arantza Hunters": "Six-armed spiderfolk, primitive but tactical. Arantza plunder ruins and hunt old roads through this forest. They have already spotted you.",
    "Reclaimed Boneguard": "A skeleton draped in moss and root growth, the forest slowly reclaiming what the undead should never have kept. The morning star still swings with certainty.",
    "Dire Bear": "An enormous bear with a scar across its snout and ruined eyes. The forest here is old and strange, and so are the things that live in it.",
    "Khinari Bladedancer": "A khinari warrior of the bladedancer caste—lithe, elegant, and savage. They have perfected their art on everything that walks these woods.",
    "Naukin Sunstriker": "An elite naukin glide-assassin—one of the Sunstrikers, their most feared warriors. It falls from the canopy without a sound. You barely had time to see it.",
    "Verdant Shepherd": "One of the green shepherds: ancient treelives, enormous and slow of mind but terrible in wrath. It has decided this part of the forest is not for you. It is difficult to argue with a walking tree.",
    "Barkskin Colossus": "A massive creature armored in living bark, moving through the old forest as though it owns everything beneath the canopy. It probably does.",
    "Emerald Lich": "An emerald lich—an archmagus from the old world whose body has been consumed by nature's corruption. Vines pull through its ribcage. The magic smells of rot and old rain.",
    // Ruins
    "Brass Golem": "A brass automaton, still animated by the sorcery the old civilization baked into it. Arantza worship these ruins; this golem guards them.",
    "Arantza Looters": "Spiderfolk in scrap-metal armor, picking through ancient building debris. They carry weapons that don't quite fit their hands. They don't care.",
    "Bloated Zombie": "A shambling corpse, bloated and full, dragging itself through ruin corridors. Whoever it was in life is long gone.",
    "Iron Bulwark": "A golem of iron rather than brass—heavier, newer, more purposeful. It was built to protect something specific. It no longer remembers what. It guards you now.",
    "Stone Drake": "A drake of petrified scales, old enough that stone has begun growing through flesh. Its eyes still burn.",
    "Lost Myrrim": "A Myrrim—fungal folk—wandering the ruins in silence, their spore crown pulsing with faint light. The lost kind have separated from their grove. They grow strange when alone.",
    "Fell Lich": "A fell lich—once a great archmagus, now an ancient undead with too much memory and far too much power. It looks at you the way a man looks at a moth: with mild curiosity before it ends the annoyance.",
    "Blighted Auroc": "An auroc consumed by corruption, its golden scales blackened and cracked, its plague breath fouling the air around it. It should not still move. It does.",
    // Slopes
    "Cauterizer": "A thing of stitched flesh and cauterized wounds. It was made when death refused to stay dead. It was made with fire.",
    "Naukin Warmage": "A naukin conjurer dressed in scholar's tatters, fur singed and scarred. Naukin warmages are reclusive with outsiders, but their power is immense.",
    "Goat Herd": "Mountain goats that move like a single organism. They are not mindless—they coordinate, they learn, they remember. They have remembered you as a threat.",
    "Elemental Stone": "A creature of living rock and mineral will, shaping the earth to its whims. It exists in the spaces between seasons, old beyond reckoning.",
    "Tusk Rhinopede": "A massive creature—part rhino, part centipede—with tusks like chiseled stone and segments that grind and shift. It was never meant to exist. Neither were most things here.",
    "Slope Wyvern": "A wyvern of the high places, lean and scar-tissue thin. It has claimed every peak here. You are climbing its domain.",
    "Limestone Colossus": "A thing of compressed earth and calcified bone, wearing the mountain like skin. It does not fight—it crushes.",
    "Dread Basilisk": "An ancient basilisk, its gaze a thing of power, its scales a thing of legend. The slopes are its domain. You have entered the domain of something vast and patient and *old*.",
    // Pit
    "Cultist Zealot": "A creature that was once humanoid, now twisted by dark pacts. Its form writhes with shapes that shouldn't bend that way.",
    "Plaguebearer": "Something that pulses with sickness. It was diseased before it died. It was diseased before it was born. It is diseased in the ways that matter—the ways you can catch.",
    "Bone Shepherd": "A tall thin thing of elegant bone, holding a staff of more bone. It gathers the dead as a shepherd gathers sheep. You were not supposed to be here.",
    "Soul Prisoner": "A wraith bound in form, screaming silently behind eyes of void. It is in pain. It wants you to understand that pain.",
    "Primordial Dark": "Something from before the world learned to be real. It touches the air and reality bends. It touches your mind and reason bends. Do not let it touch you.",
    "Nightmare Incarnate": "Your deepest fear given teeth and claws. It knows exactly what you're afraid of. It has always known. It has been waiting forever just to show you.",
    "Oblivion Sealed": "Something that was sealed in these depths because the world feared it awake. You have opened the seal. It is stirring. It is very, very happy about that.",
    "The Price": "At the bottom of all things sits the Price. The universe demands payment. The Price is here to collect."
  },
  auto: {
    exact: {
      "Available:": "Available:",
      "In deck:": "In deck:",
      "Cost:": "Cost:",
      "Current:": "Current:",
      "Hand Size": "Hand Size",
      "Max HP": "Max HP",
      "Damage Dice": "Damage Dice",
      "Recovery": "Recovery",
      "Shield": "Shield",
      "Back": "Back",
      "Close": "Close",
      "Play Card": "Play Card",
      "End Turn": "End Turn",
      "Retreat": "Retreat",
      "Sell Cards": "Sell Cards",
      "Buy": "Buy",
      "Add to Deck": "Add to Deck",
      "Remove from Deck": "Remove from Deck",
      "Frozen": "Frozen",
      "dealt": "dealt"
    },
    patterns: [
      ["^Welcome back, (.+)!$", "Welcome back, $1!"],
      ["^Loaded save: (.+)$", "Loaded save: $1"],
      ["^You venture into (.+) Tier (\\d+)\\.\\.\\.$", "You venture into $1 Tier $2..."],
      ["^Bought (.+) for (\\d+)g\\.$", "Bought $1 for $2g."],
      ["^Sold (.+) for (\\d+)g\\.$", "Sold $1 for $2g."],
      ["^Deal (.+)$", "Deal $1"],
      ["^Apply (.+)$", "Apply $1"],
      ["^(.+) added to deck\\.$", "$1 added to deck."],
      ["^(.+) added to inventory\\.$", "$1 added to inventory."],
      ["^(.+) is defeated!$", "$1 is defeated!"],
      ["^⚡ LEGENDARY (.+) appears!$", "⚡ LEGENDARY $1 appears!"],
      ["^A (.+) appears in (.+) Tier (\\d+)!$", "A $1 appears in $2 Tier $3!"],
      ["^Loot drop! (.+) dropped (.+)!$", "Loot drop! $1 dropped $2!"],
      ["^(.+) requires (.+), but die shows (\\d+)$", "$1 requires $2, but die shows $3"],
      ["^Gain (.+)$", "Gain $1"],
      ["^Heal (.+)$", "Heal $1"]
    ],
    words: {}
  }
};
