poison_counter = 0
health = 10
dice = []
burn_counter = 0
lock_counter = 0
freeze_counter = 0
bleed_counter = 0

# triggers at start of turn
if poison_counter > 0:
    health -= poison_counter
    poison_counter -= 1


# triggers when card is played
if burn_counter > 0:
    health = health - (burn_counter)
    burn_counter-=1


# triggers when dice are rolled, before freeze
if lock_counter > 0:
    while lock_counter > 0 and dice > 0:
        dice.pop(0)
        lock_counter -= 1


#triggers right after lock
if freeze_counter > 0:
    while freeze_counter > 0:
        for i in dice.index():
            if dice.index(i) > 1:
                dice.index(i) = 1
        pass
    pass


# triggers at end of turn? or triggers when a card is played and burn instead triggers on dice usage, idk
if bleed_counter > 0:
    health -= bleed_counter
    bleed_counter -= 1