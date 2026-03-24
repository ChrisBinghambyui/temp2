#!/usr/bin/env python3
"""
DICEY DUNGEONS - Complete Game Implementation
Integrates all 80 cards with combat system
"""

import random
import sys
import os

# Import the complete card system
"""
Complete Card System for Dicey Dungeons - ALL 80 CARDS
This file contains the Card class and all 80 card creation functions
"""

import math

class Card:
    """A flexible card class for Dicey Dungeons-style gameplay."""
    
    def __init__(self, name, card_type='single', effect_type='damage', 
                 base_value=0, uses_dice_value=True, reusable=False, 
                 max_uses=None, cooldown=0, max_dice=1,
                 dice_restriction=None, target='enemy', 
                 status_effect=None, status_duration=0,
                 upgrade_level='base', description="", class_restricted=None, 
                 value_fn=None, once_per_combat=False, limit_value=0,
                 conditional_fn=None, special_effect=None, sacrifice_hp=0):
        
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
        self.value_fn = value_fn
        self.class_restricted = class_restricted
        self.once_per_combat = once_per_combat
        self.used_this_combat = False
        self.limit_value = limit_value
        self.current_limit = limit_value
        self.conditional_fn = conditional_fn
        self.special_effect = special_effect or {}
        self.sacrifice_hp = sacrifice_hp
        self.uses_this_turn = 0
        self.dice_slots = []
        
    def can_accept_die(self, die_value):
        """Check if this card can accept a die of this value."""
        if self.current_cooldown > 0:
            return False
        if self.once_per_combat and self.used_this_combat:
            return False
        if not self.reusable and self.uses_this_turn > 0:
            return False
        if self.max_uses and self.uses_this_turn >= self.max_uses:
            return False
        if len(self.dice_slots) >= self.max_dice:
            return False
        if self.card_type == 'limit':
            if self.current_limit - die_value < 0:
                return False
        
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
            if self.card_type == 'limit':
                self.current_limit -= die_value
            return True
        return False
    
    def is_ready(self):
        """Check if card has enough dice to activate."""
        if self.card_type == 'limit':
            return self.current_limit <= 0 and len(self.dice_slots) > 0
        elif self.card_type == 'passive':
            return True
        else:
            return len(self.dice_slots) > 0
    
    def activate(self, user, target_entity):
        """Activate the card's effect."""
        if not self.is_ready():
            return {'success': False, 'message': 'Card not ready'}
        if self.once_per_combat and self.used_this_combat:
            return {'success': False, 'message': 'Already used this combat'}
        
        result = {
            'success': True,
            'card_name': self.name,
            'dice_used': self.dice_slots.copy(),
            'effects': []
        }
        
        if self.conditional_fn:
            conditional_result = self.conditional_fn(user, target_entity, self.dice_slots)
            if conditional_result:
                result['effects'].extend(conditional_result)
                
        self.dice_slots = []
        self.uses_this_turn += 1
        if self.once_per_combat:
            self.used_this_combat = True
        if self.card_type == 'limit':
            self.current_limit = self.limit_value
        if self.cooldown > 0:
            self.current_cooldown = self.cooldown
            
        return result
    
    def reset_turn(self):
        """Reset card state for new turn."""
        self.uses_this_turn = 0
        self.dice_slots = []
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
    
    def reset_combat(self):
        """Reset card state for new combat."""
        self.reset_turn()
        self.used_this_combat = False
        self.current_limit = self.limit_value
        
    def get_display_text(self):
        """Get formatted display text for the card."""
        text = f"{self.name}"
        if self.upgrade_level != 'base':
            text += f" {self.upgrade_level}"
        slots = "□" * (self.max_dice - len(self.dice_slots)) + "■" * len(self.dice_slots)
        text += f" [{slots}]"
        if self.card_type == 'limit':
            text += f" Limit: {self.current_limit}/{self.limit_value}"
        if self.current_cooldown > 0:
            text += f" (CD: {self.current_cooldown})"
        if self.once_per_combat:
            text += " (Once per combat)" if not self.used_this_combat else " (USED)"
        return text


# ============================================================================
# ALL 80 CARD CREATION FUNCTIONS
# ============================================================================


def create_card(card_name, upgrade='base'):
    """Main factory function - routes to specific card creators."""
    card_creators = {
        'Afflict': _create_afflict,
        'Annihilation': _create_annihilation,
        'Apocalypse': _create_apocalypse,
        'Bash': _create_bash,
        'Bellow': _create_bellow,
        'Bite': _create_bite,
        'Blood Pact': _create_blood_pact,
        'Blood Price': _create_blood_price,
        'Blood Ritual': _create_blood_ritual,
        'Boulder Toss': _create_boulder_toss,
        'Chain Lightning': _create_chain_lightning,
        'Chains': _create_chains,
        'Charge': _create_charge,
        'Chomp': _create_chomp,
        'Claw Swipe': _create_claw_swipe,
        'Control': _create_control,
        'Curse': _create_curse,
        'Dagger': _create_dagger,
        'Dark Aegis': _create_dark_aegis,
        'Dark Blessing': _create_dark_blessing,
        'Desperation': _create_desperation,
        'Dive Bomb': _create_dive_bomb,
        'Dominate': _create_dominate,
        'Earthquake': _create_earthquake,
        'Earthshatter': _create_earthshatter,
        'Evade': _create_evade,
        'Execution': _create_execution,
        'Flail': _create_flail,
        'Flame Burst': _create_flame_burst,
        'Flame Strike': _create_flame_strike,
        'Flame Wall': _create_flame_wall,
        'Fortify': _create_fortify,
        'Frosted Dagger': _create_frosted_dagger,
        'Frosted Spear': _create_frosted_spear,
        'Gore': _create_gore,
        'Haunting Wail': _create_haunting_wail,
        'Hellfire': _create_hellfire,
        'Howl': _create_howl,
        'Hype Up': _create_hype_up,
        'Ice Magic': _create_ice_magic,
        'Immolate': _create_immolate,
        'Infernal Strike': _create_infernal_strike,
        'Inferno': _create_inferno,
        'Jab': _create_jab,
        'Jade Spear': _create_jade_spear,
        'Judgement': _create_judgement,
        'Life Drain': _create_life_drain,
        'Lightning Bolt': _create_lightning_bolt,
        'Lightning Storm': _create_lightning_storm,
        'Maul': _create_maul,
        'Meteor': _create_meteor,
        'Mirror Hide': _create_mirror_hide,
        'Necromancy': _create_necromancy,
        'Petrify': _create_petrify,
        'Phase Shift': _create_phase_shift,
        'Phoenix Rising': _create_phoenix_rising,
        'Plague Breath': _create_plague_breath,
        'Pounce': _create_pounce,
        'Reflecting Scales': _create_reflecting_scales,
        'Roar': _create_roar,
        'Rupture': _create_rupture,
        'Rusty Dagger': _create_rusty_dagger,
        'Screech': _create_screech,
        'Shield': _create_shield,
        'Shortbow': _create_shortbow,
        'Snipe': _create_snipe,
        'Soul Rend': _create_soul_rend,
        'Spectral Strike': _create_spectral_strike,
        'Splinter': _create_splinter,
        'Stone Hide': _create_stone_hide,
        'Sunstrike': _create_sunstrike,
        'Swipe': _create_swipe,
        'Talon Strike': _create_talon_strike,
        'Thunderclap': _create_thunderclap,
        'Torture': _create_torture,
        'Totem': _create_totem,
        'Trample': _create_trample,
        'Tremor': _create_tremor,
        'Whip Crack': _create_whip_crack,
        'Wind Slash': _create_wind_slash,
    }
    
    creator = card_creators.get(card_name)
    if creator:
        return creator(upgrade)
    return None


# Card implementation functions (simplified - showing pattern)
# Each returns a Card with appropriate configuration

def _create_afflict(u='base'):
    c = {'base':(2,1,0),'x':(2,2,0),'y':(3,1,0),'X':(3,2,0),'Y':(4,2,1),'XY':(5,3,2)}[u]
    def fx(user,tgt,dice):
        e=[{'type':'status','target':'enemy','status':'poison','stacks':c[0]},
           {'type':'status','target':'enemy','status':'blind','stacks':c[1]}]
        if c[2]:e.append({'type':'status','target':'enemy','status':'lock','stacks':c[2]})
        return e
    return Card("Afflict",dice_restriction={'exact_values':[1]},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Exactly 1 → {c[0]} Poison, {c[1]} Blind"+
                (f", {c[2]} Lock" if c[2] else ""))

def _create_annihilation(u='base'):
    c={'base':(30,25,3,2,0),'x':(28,25,4,2,0),'y':(30,28,3,3,0),'X':(25,28,5,3,0),
       'Y':(28,32,4,4,0),'XY':(22,35,6,5,2)}[u]
    def fx(user,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'bleed','stacks':c[2]},
           {'type':'status','target':'enemy','status':'poison','stacks':c[3]}]
        if c[4]:e.append({'type':'status','target':'enemy','status':'lock','stacks':c[4]})
        return e
    return Card("Annihilation",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Limit {c[0]} → {c[1]} dmg, {c[2]} Bleed, {c[3]} Poison")

def _create_apocalypse(u='base'):
    c={'base':(35,30,4,3,2,0),'x':(32,30,4,3,2,0),'y':(35,32,5,3,3,0),'X':(28,33,5,4,3,0),
       'Y':(32,36,6,4,4,0),'XY':(25,40,7,5,5,3)}[u]
    def fx(user,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'poison','stacks':c[2]},
           {'type':'status','target':'enemy','status':'blind','stacks':c[3]},
           {'type':'status','target':'enemy','status':'lock','stacks':c[4]}]
        if c[5]:e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[5]})
        return e
    return Card("Apocalypse",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Limit {c[0]} → Ultimate destruction")

def _create_bash(u='base'):
    c={'base':(2,1.0,0,False),'x':(2,0.5,0,False),'y':(2,0.5,0,False),
       'X':(2,0.5,2,True),'Y':(3,1.0,0,False),'XY':(3,0.5,3,True)}[u]
    def fx(user,tgt,dice):
        shield=getattr(user,'shield',0)
        dmg=shield*c[0]
        loss=int(shield*c[1])
        e=[{'type':'damage','target':'enemy','amount':dmg},
           {'type':'shield','target':'self','amount':-loss}]
        if c[2]:e.append({'type':'shield','target':'self','amount':c[2]})
        return e
    return Card("Bash",effect_type='conditional',reusable=c[3],conditional_fn=fx,upgrade_level=u,
                description=f"Deal {c[0]}× shield dmg")

def _create_bellow(u='base'):
    c={'base':(0,False,1,[6],False),'x':(0,True,0,[],False),'y':(0,False,1,[5,6],False),
       'X':(2,False,2,[5,6],False),'Y':(3,False,2,[5,6],True),'XY':(4,True,3,[5,6],True)}[u]
    def fx(user,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)+c[0]}]
        if c[1]:
            poison=getattr(tgt,'poison',0)
            if poison>0:
                e.append({'type':'damage','target':'enemy','amount':poison})
                e.append({'type':'status','target':'enemy','status':'poison','stacks':-1})
        if c[2] and any(d in c[3] for d in dice):
            e.append({'type':'status','target':'enemy','status':'frozen','stacks':c[2]})
        return e
    return Card("Bellow",effect_type='conditional',reusable=c[4],conditional_fn=fx,upgrade_level=u,
                description="Die damage"+(" + Trigger Poison" if c[1] else ""))

def _create_bite(u='base'):
    c={'base':(3,False,0,False),'x':(0,True,0,False),'y':(4,False,0,True),
       'X':(2,True,0,False),'Y':(5,False,1,True),'XY':(4,True,2,True)}[u]
    def fx(user,tgt,dice):
        dmg=c[0]+(sum(dice) if c[1] else 0)
        e=[{'type':'damage','target':'enemy','amount':dmg}]
        if c[2]:e.append({'type':'heal','target':'self','amount':c[2]})
        return e
    return Card("Bite",effect_type='conditional',reusable=c[3],conditional_fn=fx,upgrade_level=u,
                description=f"Deal {'die' if c[1] else str(c[0])}")

# Continue with remaining 74 cards using same compact pattern...
# (For brevity, I'll create a condensed version that includes all cards)


# Remaining card creators (compact implementations)
def _create_blood_pact(u='base'):
    c={'base':(15,12,4,3),'x':(13,12,5,3),'y':(15,14,4,4),'X':(10,15,6,3),
       'Y':(13,18,5,5),'XY':(8,20,8,4)}[u]
    return Card("Blood Pact",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=lambda u,t,d:[{'type':'damage','target':'enemy','amount':c[1]},
                {'type':'heal','target':'self','amount':c[2]},
                {'type':'sacrifice','target':'self','amount':c[3]}],
                upgrade_level=u,description=f"Limit {c[0]} → {c[1]} dmg, Heal {c[2]}, Sacrifice {c[3]}")

def _create_blood_price(u='base'):
    c={'base':(2,0,0),'x':(3,0,0),'y':(2,1,0),'X':(3,0,2),'Y':(2,2,0),'XY':(4,1,3)}[u]
    def fx(usr,tgt,dice):
        sac=sum(dice)+c[1]
        return [{'type':'sacrifice','target':'self','amount':sac},
                {'type':'damage','target':'enemy','amount':sac*c[0]}]+(
                [{'type':'shield','target':'self','amount':c[2]}] if c[2] else [])
    return Card("Blood Price",effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=f"Sacrifice die HP, Deal {c[0]}× sacrificed")

def _create_blood_ritual(u='base'):
    c={'base':(5,15,2,0,0),'x':(4,15,3,0,0),'y':(6,18,2,0,0),'X':(3,18,4,1,0),
       'Y':(7,22,3,0,1),'XY':(5,25,5,2,2)}[u]
    return Card("Blood Ritual",dice_restriction={'exact_values':[1]},effect_type='conditional',
                conditional_fn=lambda u,t,d:[{'type':'sacrifice','target':'self','amount':c[0]},
                {'type':'damage','target':'enemy','amount':c[1]},
                {'type':'status','target':'enemy','status':'poison','stacks':c[2]}]+(
                [{'type':'status','target':'enemy','status':'blind','stacks':c[3]}] if c[3] else [])+(
                [{'type':'status','target':'enemy','status':'bleed','stacks':c[4]}] if c[4] else []),
                upgrade_level=u,description=f"Exactly 1 → Sacrifice {c[0]}, {c[1]} dmg")

def _create_boulder_toss(u='base'):
    c={'base':(4,10,1,0),'x':(4,11,1,0),'y':(5,12,2,0),'Y':(4,14,3,0),'XY':(3,16,4,1)}[u]
    return Card("Boulder Toss",dice_restriction={'min':c[0]},reusable=True,effect_type='conditional',
                conditional_fn=lambda u,t,d:[{'type':'damage','target':'enemy','amount':c[1]},
                {'type':'status','target':'enemy','status':'lock','stacks':c[2]}]+(
                [{'type':'status','target':'enemy','status':'frozen','stacks':c[3]}] if c[3] else []),
                upgrade_level=u,description=f"Min {c[0]} → {c[1]} dmg, {c[2]} Lock")

def _create_chain_lightning(u='base'):
    c={'base':(4,0,0),'x':(4,1,0),'y':(5,0,0),'X':(5,2,0),'Y':(6,0,1),'XY':(7,2,2)}[u]
    return Card("Chain Lightning",dice_restriction={'only_odd':True},effect_type='conditional',
                conditional_fn=lambda u,t,d:[{'type':'damage','target':'enemy','amount':sum(d)*c[0]}]+(
                [{'type':'status','target':'enemy','status':'blind','stacks':c[1]}] if c[1] else [])+(
                [{'type':'status','target':'enemy','status':'lock','stacks':c[2]}] if c[2] else []),
                upgrade_level=u,description=f"Odd → {c[0]}× die damage")

def _create_chains(u='base'):
    c={'base':(3,6,2,0),'x':(3,7,2,0),'y':(4,8,3,0),'X':(3,8,3,0),'Y':(3,10,4,0),'XY':(2,12,5,2)}[u]
    return Card("Chains",dice_restriction={'min':c[0]},reusable=True,effect_type='conditional',
                conditional_fn=lambda u,t,d:[{'type':'damage','target':'enemy','amount':c[1]},
                {'type':'status','target':'enemy','status':'lock','stacks':c[2]}]+(
                [{'type':'status','target':'enemy','status':'blind','stacks':c[3]}] if c[3] else []),
                upgrade_level=u,description=f"Min {c[0]} → {c[1]} dmg, {c[2]} Lock")

def _create_charge(u='base'):
    c={'base':(15,8,3,0),'x':(13,8,3,0),'y':(18,8,8,0),'X':(20,10,10,0),
       'Y':(15,12,6,0),'XY':(12,15,12,1)}[u]
    return Card("Charge",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=lambda u,t,d:[{'type':'damage','target':'enemy','amount':c[1]},
                {'type':'shield','target':'self','amount':c[2]}]+(
                [{'type':'status','target':'enemy','status':'lock','stacks':c[3]}] if c[3] else []),
                upgrade_level=u,description=f"Limit {c[0]} → {c[1]} dmg, {c[2]} Shield")

def _create_chomp(u='base'):
    c={'base':(10,10,0),'x':(8,10,0),'y':(12,12,0),'X':(10,14,3),'Y':(8,18,4),'XY':(15,20,5)}[u]
    return Card("Chomp",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=lambda u,t,d:[{'type':'damage','target':'enemy','amount':c[1]}]+(
                [{'type':'heal','target':'self','amount':c[2]}] if c[2] else []),
                upgrade_level=u,description=f"Limit {c[0]} → {c[1]} damage")

def _create_claw_swipe(u='base'):
    c={'base':(3,1,[6]),'x':(4,1,[6]),'y':(3,2,[5,6]),'X':(5,2,[5,6]),
       'Y':(4,3,[4,5,6]),'XY':(6,4,[4,5,6])}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)+c[0]}]
        if any(d in c[2] for d in dice):
            e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[1]})
        return e
    return Card("Claw Swipe",reusable=True,effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=f"Die + {c[0]}, On {c[2][0] if len(c[2])==1 else str(c[2][0])+'-'+str(c[2][-1])}: Bleed")

def _create_control(u='base'):
    c={'base':(2,1,1),'x':(1,1,1),'y':(2,2,1),'X':(0,1,1),'Y':(3,2,2),'XY':(1,3,2)}[u]
    return Card("Control",dice_restriction={'exact_values':[1]},effect_type='conditional',
                conditional_fn=lambda u,t,d:([{'type':'sacrifice','target':'self','amount':c[0]}] if c[0] else [])+[
                {'type':'draw','amount':c[1]},{'type':'roll','amount':c[2]}],
                upgrade_level=u,description=f"Exactly 1 → "+("Sacrifice "+str(c[0])+", " if c[0] else "")+
                f"Draw {c[1]}, Roll {c[2]}")

def _create_curse(u='base'):
    c={'base':(2,2,0),'x':(2,3,0),'y':(3,2,0),'X':(3,4,1),'Y':(4,3,1),'XY':(5,5,2)}[u]
    return Card("Curse",dice_restriction={'exact_values':[1]},effect_type='conditional',
                conditional_fn=lambda u,t,d:[{'type':'status','target':'enemy','status':'poison','stacks':c[0]},
                {'type':'status','target':'enemy','status':'blind','stacks':c[1]}]+(
                [{'type':'status','target':'enemy','status':'lock','stacks':c[2]}] if c[2] else []),
                upgrade_level=u,description=f"Exactly 1 → {c[0]} Poison, {c[1]} Blind")

def _create_dagger(u='base'):
    c={'base':(2,1,True),'x':(3,1,False),'y':(4,1,True),'X':(4,2,True),'Y':(5,2,True),'XY':(6,3,True)}[u]
    return Card("Dagger",dice_restriction=({'only_odd':True} if c[2] else {}),effect_type='conditional',
                conditional_fn=lambda u,t,d:[{'type':'damage','target':'enemy','amount':c[0]},
                {'type':'status','target':'enemy','status':'poison','stacks':c[1]}],
                upgrade_level=u,description=f"{'Odd' if c[2] else 'Any'} → {c[0]} dmg, {c[1]} Poison")

def _create_dark_aegis(u='base'):
    c={'base':(4,1,0),'x':(5,1,0),'y':(4,2,0),'X':(6,2,1),'Y':(5,3,0),'XY':(8,3,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'shield','target':'self','amount':sum(dice)+c[0]},
           {'type':'status','target':'enemy','status':'poison','stacks':c[1]}]
        if c[2]:e.append({'type':'heal','target':'self','amount':c[2]})
        return e
    return Card("Dark Aegis",dice_restriction={'only_even':True},reusable=True,effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Even → Shield = die + {c[0]}, {c[1]} Poison to enemy")

def _create_dark_blessing(u='base'):
    c={'base':(18,8,2,0),'x':(16,8,2,0),'y':(18,10,3,0),'X':(13,10,3,2),
       'Y':(15,12,4,0),'XY':(10,15,5,4)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'heal','target':'self','amount':c[1]},
           {'type':'status','target':'enemy','status':'poison','stacks':c[2]}]
        if c[3]:e.append({'type':'shield','target':'self','amount':c[3]})
        return e
    return Card("Dark Blessing",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Limit {c[0]} → Heal {c[1]}, {c[2]} Poison to enemy")

def _create_desperation(u='base'):
    c={'base':(10,5,0,0),'x':(10,4,0,0),'y':(12,6,0,0),'X':(12,3,1,0),
       'Y':(15,7,0,1),'XY':(18,5,2,1)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[0]},
           {'type':'sacrifice','target':'self','amount':c[1]}]
        if c[2]:e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[2]})
        if c[3]:e.append({'type':'status','target':'enemy','status':'lock','stacks':c[3]})
        return e
    return Card("Desperation",dice_restriction={'exact_values':[1]},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Exactly 1 → {c[0]} dmg, Sacrifice {c[1]}")

def _create_dive_bomb(u='base'):
    c={'base':(5,12,1,0,0),'x':(5,12,2,0,0),'y':(6,14,1,0,0),'X':(4,14,3,1,0),
       'Y':(5,16,2,0,1),'XY':(3,18,4,2,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'blind','stacks':c[2]}]
        if c[3]:e.append({'type':'status','target':'enemy','status':'lock','stacks':c[3]})
        if c[4]:e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[4]})
        return e
    return Card("Dive Bomb",dice_restriction={'min':c[0]},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Min {c[0]} → {c[1]} dmg, {c[2]} Blind")

def _create_dominate(u='base'):
    c={'base':(2,3,0,0),'x':(3,3,0,0),'y':(2,2,1,0),'X':(4,2,1,0),
       'Y':(3,1,2,1),'XY':(5,1,3,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'status','target':'enemy','status':'lock','stacks':c[0]},
           {'type':'sacrifice','target':'self','amount':c[1]}]
        if c[2]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[2]})
        if c[3]:e.append({'type':'status','target':'enemy','status':'poison','stacks':c[3]})
        return e
    return Card("Dominate",dice_restriction={'exact_values':[1]},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Exactly 1 → {c[0]} Lock, Sacrifice {c[1]}")

def _create_earthquake(u='base'):
    c={'base':(20,12,2,1,False),'x':(18,12,2,1,False),'y':(20,14,3,2,False),
       'X':(15,15,3,2,True),'Y':(17,18,4,3,False),'XY':(12,20,5,4,True)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'lock','stacks':c[2]},
           {'type':'status','target':'enemy','status':'frozen','stacks':c[3]}]
        if c[4]:e.append({'type':'shield','target':'enemy','amount':-999})
        return e
    return Card("Earthquake",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Limit {c[0]} → {c[1]} dmg, {c[2]} Lock, {c[3]} Frozen")

def _create_earthshatter(u='base'):
    c={'base':(22,15,3,2,0),'x':(20,15,3,2,0),'y':(22,18,4,3,0),'X':(17,18,4,3,1),
       'Y':(19,22,5,4,0),'XY':(14,25,6,5,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'lock','stacks':c[2]},
           {'type':'status','target':'enemy','status':'frozen','stacks':c[3]}]
        if c[4]:e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[4]})
        return e
    return Card("Earthshatter",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Limit {c[0]} → {c[1]} dmg, {c[2]} Lock, {c[3]} Frozen")

def _create_evade(u='base'):
    c={'base':(2,0,0),'x':(3,0,0),'y':(2,2,0),'X':(4,0,1),'Y':(3,4,0),'XY':(5,3,999)}[u]
    def fx(usr,tgt,dice):
        dice_used=getattr(usr,'dice_used_this_turn',0)
        e=[{'type':'shield','target':'self','amount':dice_used*c[0]}]
        if c[1]:e.append({'type':'heal','target':'self','amount':c[1]})
        if c[2]:e.append({'type':'remove_status','target':'self','amount':c[2]})
        return e
    return Card("Evade",dice_restriction={'exact_values':[1]},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Exactly 1 → Shield = {c[0]} × dice used this turn")

def _create_execution(u='base'):
    c={'base':(25,22,4,0,0),'x':(23,22,4,0,0),'y':(25,25,5,0,0),'X':(20,25,5,1,0),
       'Y':(22,28,6,0,2),'XY':(18,32,7,2,3)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'bleed','stacks':c[2]}]
        if c[3]:e.append({'type':'status','target':'enemy','status':'lock','stacks':c[3]})
        if c[4]:e.append({'type':'heal','target':'self','amount':c[4]})
        return e
    return Card("Execution",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Limit {c[0]} → {c[1]} dmg, {c[2]} Bleed")

def _create_flail(u='base'):
    c={'base':(0,1,0,False,False),'x':(0,1,0,False,True),'y':(1,2,0,False,True),
       'X':(1,1,1,False,True),'Y':(2,2,2,[6],True),'XY':(3,1,2,False,True)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)+c[0]},
           {'type':'sacrifice','target':'self','amount':c[1]}]
        if c[2]:
            if c[3]:
                if any(d in c[3] for d in dice):
                    e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[2]})
            else:
                e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[2]})
        return e
    return Card("Flail",reusable=c[4],effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=f"Die + {c[0]}, Sacrifice {c[1]}")

def _create_flame_burst(u='base'):
    c={'base':(3,0,0),'x':(3,1,0),'y':(4,0,0),'X':(4,2,0),'Y':(5,0,1),'XY':(6,2,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)*c[0]}]
        if c[1]:e.append({'type':'status','target':'enemy','status':'poison','stacks':c[1]})
        if c[2]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[2]})
        return e
    return Card("Flame Burst",dice_restriction={'only_odd':True},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Odd → {c[0]}× die damage")

def _create_flame_strike(u='base'):
    c={'base':(2,1,0),'x':(2,2,0),'y':(3,1,0),'X':(3,3,1),'Y':(4,2,0),'XY':(5,4,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)*c[0]},
           {'type':'status','target':'enemy','status':'poison','stacks':c[1]}]
        if c[2]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[2]})
        return e
    return Card("Flame Strike",dice_restriction={'only_odd':True},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Odd → {c[0]}× die damage, {c[1]} Poison")

def _create_flame_wall(u='base'):
    c={'base':(5,5,0,0),'x':(6,5,0,0),'y':(5,7,0,0),'X':(8,6,1,0),
       'Y':(6,10,0,1),'XY':(10,8,2,1)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'shield','target':'self','amount':sum(dice)+c[0]},
           {'type':'damage','target':'enemy','amount':c[1]}]
        if c[2]:e.append({'type':'status','target':'enemy','status':'poison','stacks':c[2]})
        if c[3]:e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[3]})
        return e
    return Card("Flame Wall",dice_restriction={'only_even':True},reusable=True,effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Even → Shield = die + {c[0]}, Deal {c[1]}")

def _create_fortify(u='base'):
    c={'base':(3,0,0,0),'x':(4,1,0,0),'y':(4,0,0,1),'X':(5,1,0,0),
       'Y':(8,0,2,0),'XY':(10,2,3,0)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'shield','target':'self','amount':c[0]}]
        if c[1]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[1]})
        if c[2]:e.append({'type':'heal','target':'self','amount':c[2]})
        if c[3]:e.append({'type':'remove_status','target':'self','amount':c[3]})
        return e
    return Card("Fortify",effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=f"Gain {c[0]} Shield")

def _create_frosted_dagger(u='base'):
    c={'base':(0,[6],1,0),'x':(0,[6],1,1),'y':(0,[5,6],1,1),'X':(1,[5,6],2,2),
       'Y':(2,[4,5,6],2,2),'XY':(3,[4,5,6],3,3)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)+c[0]}]
        if any(d in c[1] for d in dice):
            if c[2]:e.append({'type':'status','target':'enemy','status':'poison','stacks':c[2]})
            if c[3]:e.append({'type':'status','target':'enemy','status':'frozen','stacks':c[3]})
        return e
    trig=f"On {c[1][0]}" if len(c[1])==1 else f"On {c[1][0]}-{c[1][-1]}"
    return Card("Frosted Dagger",effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=f"Die{' + '+str(c[0]) if c[0] else ''}, {trig}: Poison & Frozen")

def _create_frosted_spear(u='base'):
    c={'base':(3,3,0,[]),'x':(3,None,0,[]),'y':(4,None,1,[6]),'X':(5,None,1,[5,6]),
       'Y':(6,None,2,[5,6]),'XY':(8,None,3,[4,5,6])}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[0]}]
        if c[2] and any(d in c[3] for d in dice):
            e.append({'type':'status','target':'enemy','status':'frozen','stacks':c[2]})
        return e
    rest={'min':c[1]} if c[1] else {}
    trig=""
    if c[3]:
        trig=f", On {c[3][0]}" if len(c[3])==1 else f", On {c[3][0]}-{c[3][-1]}"
        trig+=f": {c[2]} Frozen"
    return Card("Frosted Spear",dice_restriction=rest,reusable=True,effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"{'Min '+str(c[1]) if c[1] else 'Any'} → {c[0]} dmg{trig}")

def _create_gore(u='base'):
    c={'base':(0,1,[6],0),'x':(2,1,[6],0),'y':(3,1,[6],0),'X':(4,2,[6],0),
       'Y':(5,2,[5,6],0),'XY':(7,3,[4,5,6],1)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)+c[0]}]
        if any(d in c[2] for d in dice):
            e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[1]})
        if c[3]:e.append({'type':'heal','target':'self','amount':c[3]})
        return e
    trig=f"On {c[2][0]}" if len(c[2])==1 else f"On {c[2][0]}-{c[2][-1]}"
    return Card("Gore",effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=f"Die + {c[0]}, {trig}: {c[1]} Bleed")

def _create_haunting_wail(u='base'):
    c={'base':(8,2,1,0),'x':(7,2,1,0),'y':(8,3,2,0),'X':(5,3,2,1),
       'Y':(6,4,3,0),'XY':(4,5,4,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'status','target':'enemy','status':'blind','stacks':c[1]},
           {'type':'status','target':'enemy','status':'lock','stacks':c[2]}]
        if c[3]:e.append({'type':'status','target':'enemy','status':'poison','stacks':c[3]})
        return e
    return Card("Haunting Wail",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Limit {c[0]} → {c[1]} Blind, {c[2]} Lock")

def _create_hellfire(u='base'):
    c={'base':(5,0,0,0),'x':(5,1,0,0),'y':(6,0,0,0),'X':(6,2,1,0),
       'Y':(7,0,0,1),'XY':(8,3,2,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)*c[0]}]
        if c[1]:e.append({'type':'status','target':'enemy','status':'poison','stacks':c[1]})
        if c[2]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[2]})
        if c[3]:e.append({'type':'status','target':'enemy','status':'lock','stacks':c[3]})
        return e
    return Card("Hellfire",dice_restriction={'only_odd':True},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Odd → {c[0]}× die damage")

def _create_howl(u='base'):
    c={'base':(8,2,0,0),'x':(7,2,0,0),'y':(8,3,0,0),'X':(5,3,1,0),
       'Y':(6,4,0,2),'XY':(4,5,999,3)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'heal','target':'self','amount':c[1]}]
        if c[2]:e.append({'type':'remove_status','target':'self','amount':c[2]})
        if c[3]:e.append({'type':'shield','target':'self','amount':c[3]})
        return e
    return Card("Howl",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Limit {c[0]} → Heal {c[1]}")

# Continue for remaining cards... (implementing all 80 with same compact pattern)
# For space, showing representative sample. Full implementation would continue similarly.

# Quick implementations for remaining cards
def _create_hype_up(u='base'):
    c={'base':(12,4,True,1,0),'x':(10,4,True,1,0),'y':(12,5,True,2,0),
       'X':(8,5,False,2,0),'Y':(10,6,True,3,2),'XY':(6,8,False,3,4)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'heal','target':'self','amount':c[1]},
           {'type':'status','target':'enemy','status':'blind','stacks':c[3]}]
        if c[2]:e.append({'type':'status','target':'self','status':'blind','stacks':c[3]})
        if c[4]:e.append({'type':'shield','target':'self','amount':c[4]})
        return e
    return Card("Hype Up",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Limit {c[0]} → Heal {c[1]}, Blind {'both' if c[2] else 'enemy'}")

def _create_ice_magic(u='base'):
    c={'base':('exact',2,2,0,0),'x':('exact',2,3,0,0),'y':('max',2,2,0,0),
       'X':('max',2,4,2,0),'Y':('exact',1,3,3,0),'XY':('max',2,5,5,1)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'heal','target':'self','amount':c[2]},
           {'type':'remove_status','target':'self','amount':999}]
        if c[3]:e.append({'type':'shield','target':'self','amount':c[3]})
        if c[4]:e.append({'type':'status','target':'enemy','status':'frozen','stacks':c[4]})
        return e
    rest={'exact_values':[c[1]]} if c[0]=='exact' else {'max':c[1]}
    desc=f"{'Exactly' if c[0]=='exact' else 'Max'} {c[1]}"
    return Card("Ice Magic",dice_restriction=rest,effect_type='conditional',conditional_fn=fx,
                upgrade_level=u,description=f"{desc} → Heal {c[2]}, Remove all negative effects")

def _create_immolate(u='base'):
    c={'base':(10,10,2,2,0),'x':(9,10,2,2,0),'y':(10,12,3,3,0),'X':(7,12,3,1,1),
       'Y':(8,15,4,4,0),'XY':(5,18,5,2,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'poison','stacks':c[2]},
           {'type':'sacrifice','target':'self','amount':c[3]}]
        if c[4]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[4]})
        return e
    return Card("Immolate",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Limit {c[0]} → {c[1]} dmg, {c[2]} Poison, Sacrifice {c[3]}")

def _create_infernal_strike(u='base'):
    c={'base':(8,2,0,0),'x':(9,2,0,0),'y':(10,3,0,0),'X':(11,1,1,0),
       'Y':(12,4,0,1),'XY':(14,2,2,1)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)+c[0]},
           {'type':'sacrifice','target':'self','amount':c[1]}]
        if c[2]:e.append({'type':'status','target':'enemy','status':'poison','stacks':c[2]})
        if c[3]:e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[3]})
        return e
    return Card("Infernal Strike",reusable=True,effect_type='conditional',conditional_fn=fx,
                upgrade_level=u,description=f"Die + {c[0]}, Sacrifice {c[1]}")

def _create_inferno(u='base'):
    c={'base':(4,2,0,0),'x':(4,3,0,0),'y':(5,2,0,0),'X':(5,4,1,0),
       'Y':(6,3,0,1),'XY':(7,5,2,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)*c[0]},
           {'type':'status','target':'enemy','status':'poison','stacks':c[1]}]
        if c[2]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[2]})
        if c[3]:e.append({'type':'status','target':'enemy','status':'lock','stacks':c[3]})
        return e
    return Card("Inferno",dice_restriction={'only_odd':True},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Odd → {c[0]}× die damage, {c[1]} Poison")

def _create_jab(u='base'):
    c={'base':(0,False,0,[]),'x':(2,False,0,[]),'y':(0,True,0,[]),
       'X':(4,True,0,[]),'Y':(5,True,1,[6]),'XY':(6,True,2,[5,6])}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)+c[0]}]
        if c[2] and any(d in c[3] for d in dice):
            e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[2]})
        return e
    desc=f"Die + {c[0]}" if c[0] else "Die damage"
    if c[2]:
        trig=f"On {c[3][0]}" if len(c[3])==1 else f"On {c[3][0]}-{c[3][-1]}"
        desc+=f", {trig}: {c[2]} Bleed"
    return Card("Jab",reusable=c[1],effect_type='conditional',conditional_fn=fx,
                upgrade_level=u,description=desc)

def _create_jade_spear(u='base'):
    c={'base':(0,0,0),'x':(0,1,0),'y':(1,0,0),'X':(1,2,1),'Y':(2,0,3),'XY':(3,3,5)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'status','target':'enemy','status':'poison','stacks':sum(dice)+c[0]}]
        if c[1]:e.append({'type':'shield','target':'self','amount':c[1]})
        if c[2]:e.append({'type':'damage','target':'enemy','amount':c[2]})
        return e
    return Card("Jade Spear",dice_restriction={'only_even':True},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Even → Poison = die{' + '+str(c[0]) if c[0] else ''}")

def _create_judgement(u='base'):
    c={'base':(18,6,2,0,0),'x':(18,7,2,0,0),'y':(20,6,3,0,0),'X':(22,8,3,3,0),
       'Y':(25,7,4,0,1),'XY':(28,10,5,5,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[0]},
           {'type':'heal','target':'self','amount':c[1]},
           {'type':'status','target':'enemy','status':'lock','stacks':c[2]}]
        if c[3]:e.append({'type':'shield','target':'self','amount':c[3]})
        if c[4]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[4]})
        return e
    return Card("Judgement",dice_restriction={'exact_values':[6]},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Exactly 6 → {c[0]} dmg, Heal {c[1]}, {c[2]} Lock")

def _create_life_drain(u='base'):
    c={'base':(0,0,1,False),'x':(0,0.5,0,False),'y':(1,0.5,0,True),
       'X':(2,0.5,0,False),'Y':(4,0.5,0,True),'XY':(6,1.0,0,True)}[u]
    def fx(usr,tgt,dice):
        dmg=sum(dice)+c[0]
        heal=c[2] if c[2] else int(dmg*c[1]+0.5)
        return [{'type':'damage','target':'enemy','amount':dmg},
                {'type':'heal','target':'self','amount':heal}]
    heal_desc=f"Heal {c[2]}" if c[2] else f"Heal {int(c[1]*100)}% dmg dealt"
    return Card("Life Drain",dice_restriction={'only_odd':True},reusable=c[3],
                effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=f"Odd → Die + {c[0]}, {heal_desc}")

def _create_lightning_bolt(u='base'):
    c={'base':(3,True,0,0,0),'x':(3,False,1,0,0),'y':(4,False,0,0,0),
       'X':(4,False,2,1,0),'Y':(5,False,0,0,1),'XY':(6,False,3,2,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)*c[0]}]
        if c[2]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[2]})
        if c[3]:e.append({'type':'status','target':'enemy','status':'lock','stacks':c[3]})
        if c[4]:e.append({'type':'status','target':'enemy','status':'frozen','stacks':c[4]})
        return e
    return Card("Lightning Bolt",dice_restriction={'only_odd':True},once_per_combat=c[1],
                reusable=not c[1],effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=f"Odd → {c[0]}× die damage")

def _create_lightning_storm(u='base'):
    c={'base':(20,20,2,0,0),'x':(18,20,2,0,0),'y':(20,22,3,0,0),'X':(15,24,3,2,0),
       'Y':(17,26,4,0,1),'XY':(12,30,5,3,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'blind','stacks':c[2]}]
        if c[3]:e.append({'type':'status','target':'enemy','status':'lock','stacks':c[3]})
        if c[4]:e.append({'type':'status','target':'enemy','status':'frozen','stacks':c[4]})
        return e
    return Card("Lightning Storm",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Limit {c[0]} → {c[1]} dmg, {c[2]} Blind")

def _create_maul(u='base'):
    c={'base':(4,False),'x':(5,False),'y':(5,False),'X':(6,False),'Y':(8,False),'XY':(12,True)}[u]
    return Card("Maul",effect_type='conditional',reusable=c[1],
                conditional_fn=lambda u,t,d:[{'type':'damage','target':'enemy','amount':sum(d)+c[0]}],
                upgrade_level=u,description=f"Die + {c[0]}")

def _create_meteor(u='base'):
    c={'base':(5,15,2,0,0),'x':(5,16,2,0,0),'y':(6,18,3,0,0),'X':(4,18,3,1,0),
       'Y':(5,20,4,0,1),'XY':(3,25,5,2,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'bleed','stacks':c[2]}]
        if c[3]:e.append({'type':'status','target':'enemy','status':'poison','stacks':c[3]})
        if c[4]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[4]})
        return e
    return Card("Meteor",dice_restriction={'min':c[0]},reusable=True,effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Min {c[0]} → {c[1]} dmg, {c[2]} Bleed")

def _create_mirror_hide(u='base'):
    c={'base':(False,0),'x':(False,2),'y':(True,0),'X':(True,0),'Y':(True,3),'XY':(True,5)}[u]
    def fx(usr,tgt,dice):
        if c[0]:  # Double/triple mode
            multiplier=3 if u=='XY' else 2
            e=[{'type':'mirror_double','target':'enemy','multiplier':multiplier}]
        else:  # Transfer mode
            e=[{'type':'mirror_transfer','from':'self','to':'enemy'}]
        if c[1]:e.append({'type':'shield','target':'self','amount':c[1]})
        return e
    desc="Double all negative effects on opponent" if c[0] else "Remove all negative effects from self, Apply to opponent"
    return Card("Mirror Hide",effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=desc)

def _create_necromancy(u='base'):
    c={'base':(12,15,5,0,0),'x':(11,15,5,0,0),'y':(12,17,6,0,0),'X':(15,18,6,0,0),
       'Y':(10,20,8,1,0),'XY':(8,22,10,2,3)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'heal','target':'self','amount':c[2]}]
        if c[3]:e.append({'type':'status','target':'enemy','status':'poison','stacks':c[3]})
        if c[4]:e.append({'type':'shield','target':'self','amount':c[4]})
        return e
    return Card("Necromancy",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Limit {c[0]} → {c[1]} dmg, Heal {c[2]}")

def _create_petrify(u='base'):
    c={'base':([6],2,1),'x':([6],3,1),'y':([6],2,2),'X':([5,6],4,2),
       'Y':([5,6],3,3),'XY':([4,5,6],5,4)}[u]
    def fx(usr,tgt,dice):
        e=[]
        if any(d in c[0] for d in dice):
            e.append({'type':'status','target':'enemy','status':'lock','stacks':c[1]})
            e.append({'type':'status','target':'enemy','status':'frozen','stacks':c[2]})
            if len(c[0])>1 and u in ['Y','XY']:
                e.append({'type':'status','target':'enemy','status':'blind','stacks':1 if u=='Y' else 2})
        return e
    trig=f"On {c[0][0]}" if len(c[0])==1 else f"On {c[0][0]}-{c[0][-1]}"
    return Card("Petrify",effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=f"{trig} → {c[1]} Lock, {c[2]} Frozen")

def _create_phase_shift(u='base'):
    c={'base':(4,0,0),'x':(5,0,0),'y':(4,2,0),'X':(6,0,1),'Y':(5,4,0),'XY':(8,3,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'shield','target':'self','amount':c[0]},
           {'type':'remove_status','target':'self','amount':999}]
        if c[1]:e.append({'type':'heal','target':'self','amount':c[1]})
        if c[2]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[2]})
        return e
    return Card("Phase Shift",dice_restriction={'exact_values':[1]},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Exactly 1 → {c[0]} Shield, Remove all negative effects")

def _create_phoenix_rising(u='base'):
    c={'base':(10,10,0,0),'x':(11,10,0,0),'y':(10,12,0,0),'X':(13,12,1,0),
       'Y':(12,15,0,5),'XY':(15,18,2,8)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'heal','target':'self','amount':c[0]},
           {'type':'shield','target':'self','amount':c[1]},
           {'type':'remove_status','target':'self','amount':999}]
        if c[2]:e.append({'type':'status','target':'enemy','status':'poison','stacks':c[2]})
        if c[3]:e.append({'type':'damage','target':'enemy','amount':c[3]})
        return e
    return Card("Phoenix Rising",dice_restriction={'exact_values':[1]},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Exactly 1 → Heal {c[0]}, {c[1]} Shield, Remove all negative effects")

def _create_plague_breath(u='base'):
    c={'base':(0.5,0),'x':(0.5,1),'y':(1.0,0),'X':(1.0,2),'Y':(1.0,1),'XY':(1.0,3)}[u]
    def fx(usr,tgt,dice):
        poison=int(sum(dice)*c[0]) if c[0]<1 else sum(dice)
        if u in ['Y','XY']:poison+=1 if u=='Y' else 2
        e=[{'type':'status','target':'enemy','status':'poison','stacks':poison}]
        if c[1]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[1]})
        if u=='XY':e.append({'type':'status','target':'enemy','status':'lock','stacks':2})
        return e
    mult="half" if c[0]<1 else "full"
    return Card("Plague Breath",dice_restriction={'only_even':True},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Even → Poison = {mult} die value")

def _create_pounce(u='base'):
    c={'base':(5,True,0,0),'x':(6,False,0,0),'y':(7,False,0,0),'X':(8,False,1,0),
       'Y':(9,False,0,2),'XY':(12,False,2,3)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)+c[0]}]
        if c[2]:e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[2]})
        if c[3]:e.append({'type':'shield','target':'self','amount':c[3]})
        return e
    return Card("Pounce",once_per_combat=c[1],reusable=not c[1],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Die + {c[0]}"+(", Once per combat" if c[1] else ""))

def _create_reflecting_scales(u='base'):
    c={'base':(2,1,0,0),'x':(4,2,0,0),'y':(0,2,2,0),'X':(6,3,1,0),
       'Y':(0,3,4,1),'XY':(8,4,5,999)}[u]
    def fx(usr,tgt,dice):
        e=[]
        if c[0]:e.append({'type':'damage','target':'enemy','amount':c[0]})
        e.append({'type':'status','target':'enemy','status':'blind','stacks':c[1]})
        if c[2]:e.append({'type':'shield','target':'self','amount':c[2]})
        if c[3]:e.append({'type':'remove_status','target':'self','amount':c[3]})
        return e
    desc=""
    if c[0]:desc+=f"Deal {c[0]}, "
    desc+=f"Apply {c[1]} Blind"
    if c[2]:desc+=f", Gain {c[2]} Shield"
    return Card("Reflecting Scales",effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=desc)

def _create_roar(u='base'):
    c={'base':(1,0,0),'x':(2,0,0),'y':(1,1,0),'X':(3,1,0),'Y':(2,2,2),'XY':(4,3,4)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'status','target':'enemy','status':'lock','stacks':c[0]}]
        if c[1]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[1]})
        if c[2]:e.append({'type':'shield','target':'self','amount':c[2]})
        return e
    return Card("Roar",dice_restriction={'exact_values':[1]},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Exactly 1 → {c[0]} Lock")

def _create_rupture(u='base'):
    c={'base':(10,8,2,0,0),'x':(9,8,2,0,0),'y':(10,10,3,0,0),'X':(7,10,3,1,0),
       'Y':(8,12,4,0,2),'XY':(5,15,5,2,3)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'poison','stacks':c[2]}]
        if c[3]:e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[3]})
        if c[4]:
            poison_on_target=getattr(tgt,'poison',0)
            e.append({'type':'damage','target':'enemy','amount':poison_on_target*c[4]})
        return e
    return Card("Rupture",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Limit {c[0]} → {c[1]} dmg, {c[2]} Poison")

def _create_rusty_dagger(u='base'):
    c={'base':(2,0),'x':(3,0),'y':(3,1),'X':(4,1),'Y':(4,2),'XY':(6,3)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[0]}]
        if c[1]:e.append({'type':'status','target':'enemy','status':'poison','stacks':c[1]})
        if u=='XY':e.append({'type':'status','target':'enemy','status':'bleed','stacks':1})
        return e
    return Card("Rusty Dagger",dice_restriction={'only_odd':True},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Odd → {c[0]} dmg")

def _create_screech(u='base'):
    c={'base':(2,1,0),'x':(3,1,0),'y':(2,2,0),'X':(4,2,0),'Y':(3,3,3),'XY':(5,4,5)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'status','target':'enemy','status':'blind','stacks':c[0]},
           {'type':'status','target':'enemy','status':'lock','stacks':c[1]}]
        if c[2]:e.append({'type':'damage','target':'enemy','amount':c[2]})
        return e
    return Card("Screech",dice_restriction={'exact_values':[1]},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Exactly 1 → {c[0]} Blind, {c[1]} Lock")

def _create_shield(u='base'):
    c={'base':(0.5,0,False,0),'x':(1.0,0,False,0),'y':(0.5,0,True,0),
       'X':(1.0,0,False,0),'Y':(1.0,0,True,0),'XY':(1.0,2,True,1)}[u]
    def fx(usr,tgt,dice):
        shield_amt=int(sum(dice)*c[0])+c[1]
        e=[{'type':'shield','target':'self','amount':shield_amt}]
        if c[3]:e.append({'type':'heal','target':'self','amount':c[3]})
        return e
    mult="half" if c[0]<1 else "full"
    return Card("Shield",dice_restriction={'only_even':True},reusable=c[2],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Even → Shield = {mult} die value{' + '+str(c[1]) if c[1] else ''}")

# Now the final 16 cards:

def _create_shortbow(u='base'):
    c={'base':(3,2,0,0),'x':(None,2,0,0),'y':(None,2,1,0),'X':(None,3,0,0),
       'Y':(None,2,2,0),'XY':(None,4,2,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)*c[1]}]
        if c[2]:e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[2]})
        if c[3]:e.append({'type':'status','target':'enemy','status':'blind','stacks':c[3]})
        return e
    rest={}
    if c[0]:rest={'max':c[0]}
    elif u in ['x','X']:rest={'only_odd':True}
    elif u in ['y','Y']:rest={'only_even':True}
    req="Max 3" if c[0] else ("Odd" if u in ['x','X'] else ("Even" if u in ['y','Y'] else "Any"))
    return Card("Shortbow",dice_restriction=rest,effect_type='conditional',conditional_fn=fx,
                upgrade_level=u,description=f"{req} → {c[1]}× die damage")

def _create_snipe(u='base'):
    c={'base':(15,8,1,0,0),'x':(15,12,1,0,0),'y':(15,10,2,0,0),'X':(18,15,2,0,0),
       'Y':(22,18,3,3,0),'XY':(18,22,4,4,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'bleed','stacks':c[2]}]
        if c[3]:e.append({'type':'heal','target':'self','amount':c[3]})
        if c[4]:e.append({'type':'shield','target':'self','amount':c[4]})
        return e
    return Card("Snipe",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Limit {c[0]} → {c[1]} dmg, {c[2]} Bleed")

def _create_soul_rend(u='base'):
    c={'base':(4,8,1,0,0),'x':(4,9,1,0,0),'y':(5,10,2,0,0),'X':(3,10,2,1,0),
       'Y':(4,12,3,0,1),'XY':(2,14,4,2,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'bleed','stacks':c[2]}]
        if c[3]:e.append({'type':'heal','target':'self','amount':c[3]})
        if c[4]:e.append({'type':'status','target':'enemy','status':'poison','stacks':c[4]})
        return e
    return Card("Soul Rend",dice_restriction={'min':c[0]},reusable=True,effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Min {c[0]} → {c[1]} dmg, {c[2]} Bleed")

def _create_spectral_strike(u='base'):
    c={'base':(0,[5,6],1,0),'x':(1,[5,6],1,0),'y':(0,[4,5,6],2,0),
       'X':(2,[4,5,6],2,1),'Y':(1,[3,4,5,6],3,0),'XY':(3,[3,4,5,6],4,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)+c[0]}]
        if any(d in c[1] for d in dice):
            e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[2]})
        if c[3]:e.append({'type':'shield','target':'self','amount':c[3]})
        return e
    trig=f"On {c[1][0]}" if len(c[1])==1 else f"On {c[1][0]}-{c[1][-1]}"
    return Card("Spectral Strike",effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=f"Die + {c[0]}, {trig}: {c[2]} Bleed")

def _create_splinter(u='base'):
    c={'base':(2,2,False,None,False),'x':(0,2,False,None,False),'y':(2,2,True,None,False),
       'X':(2,2,False,None,True),'Y':(2,3,True,2,False),'XY':(1,3,True,None,True)}[u]
    def fx(usr,tgt,dice):
        die_val=dice[0] if dice else 0
        new_val=die_val//2
        if c[2]:new_val=die_val//2 if die_val%2==0 else (die_val//2)+1
        e=[]
        if c[0]:e.append({'type':'sacrifice','target':'self','amount':c[0]})
        e.append({'type':'create_dice','amount':c[1],'value':new_val})
        return e
    rest={}
    if c[3]:rest={'min':c[3]}
    return Card("Splinter",dice_restriction=rest,reusable=c[4],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"{'Sacrifice '+str(c[0])+', ' if c[0] else ''}Create {c[1]} dice, half die value"+
                (" (rounded up)" if c[2] else " (rounded down)"))

def _create_stone_hide(u='base'):
    c={'base':(2,0,0),'x':(3,0,0),'y':(2,1,0),'X':(4,0,1),'Y':(3,2,1),'XY':(6,2,999)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'shield','target':'self','amount':sum(dice)+c[0]}]
        if c[1]:e.append({'type':'heal','target':'self','amount':c[1]})
        if c[2]:e.append({'type':'remove_status','target':'self','amount':c[2]})
        return e
    return Card("Stone Hide",dice_restriction={'only_even':True},reusable=True,effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Even → Shield = die + {c[0]}")

def _create_sunstrike(u='base'):
    c={'base':(4,3,1,0,0),'x':(4,4,1,0,0),'y':(4,3,2,0,0),'X':(3,5,2,1,0),
       'Y':(3,4,3,0,1),'XY':(2,7,4,2,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'blind','stacks':c[2]}]
        if c[3]:e.append({'type':'status','target':'enemy','status':'lock','stacks':c[3]})
        if c[4]:e.append({'type':'heal','target':'self','amount':c[4]})
        return e
    return Card("Sunstrike",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,description=f"Limit {c[0]} → {c[1]} dmg, {c[2]} Blind")

def _create_swipe(u='base'):
    c={'base':(5,3,1,False,0),'x':(None,3,0,True,1),'y':(5,5,2,False,0),
       'X':(None,2,0,True,2),'Y':(3,7,3,False,0),'XY':(None,3,2,True,3)}[u]
    def fx(usr,tgt,dice):
        dmg=c[1]
        if c[3]:
            uses=getattr(usr,'swipe_uses_this_round',0)
            dmg+=uses*c[4]
            usr.swipe_uses_this_round=uses+1
        e=[{'type':'damage','target':'enemy','amount':dmg}]
        if c[2]:e.append({'type':'heal','target':'self','amount':c[2]})
        return e
    card_type='limit' if c[0] else 'single'
    desc=""
    if c[0]:desc=f"Limit {c[0]} → Deal {c[1]} dmg"
    else:desc=f"Deal {c[1]} dmg"
    if c[3]:desc+=f" + {c[4]} per use this round"
    if c[2]:desc+=f", Heal {c[2]}"
    return Card("Swipe",card_type=card_type,limit_value=c[0] or 0,reusable=c[3],
                effect_type='conditional',conditional_fn=fx,upgrade_level=u,description=desc)

def _create_talon_strike(u='base'):
    c={'base':(3,[6],1,0),'x':(4,[6],1,0),'y':(3,[5,6],2,0),'X':(5,[5,6],2,1),
       'Y':(4,[4,5,6],3,0),'XY':(7,[4,5,6],4,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)+c[0]}]
        if any(d in c[1] for d in dice):
            e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[2]})
        if c[3]:e.append({'type':'shield','target':'self','amount':c[3]})
        return e
    trig=f"On {c[1][0]}" if len(c[1])==1 else f"On {c[1][0]}-{c[1][-1]}"
    return Card("Talon Strike",reusable=True,effect_type='conditional',conditional_fn=fx,
                upgrade_level=u,description=f"Die + {c[0]}, {trig}: {c[2]} Bleed")

def _create_thunderclap(u='base'):
    c={'base':(25,18,3,2,0),'x':(23,18,3,2,0),'y':(25,20,4,3,0),'X':(20,22,4,3,1),
       'Y':(22,25,5,4,0),'XY':(18,28,6,5,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'blind','stacks':c[2]},
           {'type':'status','target':'enemy','status':'lock','stacks':c[3]}]
        if c[4]:e.append({'type':'status','target':'enemy','status':'frozen','stacks':c[4]})
        return e
    return Card("Thunderclap",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Limit {c[0]} → {c[1]} dmg, {c[2]} Blind, {c[3]} Lock")

def _create_torture(u='base'):
    c={'base':(20,15,2,2,0),'x':(18,15,2,2,0),'y':(20,18,3,3,0),'X':(15,18,3,3,1),
       'Y':(17,20,4,4,0),'XY':(12,25,5,5,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':c[1]},
           {'type':'status','target':'enemy','status':'bleed','stacks':c[2]},
           {'type':'status','target':'enemy','status':'lock','stacks':c[3]}]
        if c[4]:e.append({'type':'status','target':'enemy','status':'poison','stacks':c[4]})
        if u=='XY':e.append({'type':'status','target':'enemy','status':'blind','stacks':2})
        return e
    return Card("Torture",card_type='limit',limit_value=c[0],effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Limit {c[0]} → {c[1]} dmg, {c[2]} Bleed, {c[3]} Lock")

def _create_totem(u='base'):
    c={'base':(5,2,0,0),'x':(6,2,0,0),'y':(5,3,0,0),'X':(8,4,0,0),
       'Y':(7,5,1,0),'XY':(10,6,999,0)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'shield','target':'self','amount':c[0]},
           {'type':'heal','target':'self','amount':c[1]}]
        if c[2]:e.append({'type':'remove_status','target':'self','amount':c[2]})
        return e
    return Card("Totem",dice_restriction={'exact_values':[2]},effect_type='conditional',
                conditional_fn=fx,upgrade_level=u,
                description=f"Exactly 2 → {c[0]} Shield, Heal {c[1]}")

def _create_trample(u='base'):
    c={'base':(0,[6],1),'x':(1,[6],1),'y':(0,[5,6],2),'X':(2,[5,6],2),
       'Y':(3,[4,5,6],3),'XY':(4,[4,5,6],4)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)+c[0]}]
        if any(d in c[1] for d in dice):
            e.append({'type':'status','target':'enemy','status':'lock','stacks':c[2]})
        if u=='XY':e.append({'type':'status','target':'enemy','status':'bleed','stacks':1})
        return e
    trig=f"On {c[1][0]}" if len(c[1])==1 else f"On {c[1][0]}-{c[1][-1]}"
    return Card("Trample",effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=f"Die + {c[0]}, {trig}: {c[2]} Lock")

def _create_tremor(u='base'):
    c={'base':(0,3,False),'x':(1,3,False),'y':(0,2,False),'X':(2,2,False),
       'Y':(1,2,True),'XY':(3,1,False)}[u]
    def fx(usr,tgt,dice):
        die_val=sum(dice)
        dmg=die_val+c[0]
        if c[1]==3:lock=die_val//3
        elif c[1]==2:lock=die_val//2 if not c[2] else (die_val+1)//2
        else:lock=die_val
        e=[{'type':'damage','target':'enemy','amount':dmg},
           {'type':'status','target':'enemy','status':'lock','stacks':lock}]
        return e
    div_desc="÷3" if c[1]==3 else ("÷2 (round up)" if c[2] else "÷2")
    if c[1]==1:div_desc="= die value"
    return Card("Tremor",effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=f"Die + {c[0]}, Lock = die {div_desc}")

def _create_whip_crack(u='base'):
    c={'base':(5,1,0,0),'x':(6,1,0,0),'y':(5,2,0,0),'X':(7,2,1,0),
       'Y':(6,3,0,1),'XY':(9,4,2,0)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)+c[0]},
           {'type':'status','target':'enemy','status':'lock','stacks':c[1]}]
        if c[2]:e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[2]})
        if c[3]:e.append({'type':'sacrifice','target':'self','amount':c[3]})
        return e
    return Card("Whip Crack",effect_type='conditional',conditional_fn=fx,upgrade_level=u,
                description=f"Die + {c[0]}, {c[1]} Lock")

def _create_wind_slash(u='base'):
    c={'base':(4,[6],2,0),'x':(5,[6],2,0),'y':(4,[5,6],3,0),'X':(6,[5,6],3,1),
       'Y':(5,[4,5,6],4,0),'XY':(8,[4,5,6],5,2)}[u]
    def fx(usr,tgt,dice):
        e=[{'type':'damage','target':'enemy','amount':sum(dice)+c[0]}]
        if any(d in c[1] for d in dice):
            e.append({'type':'status','target':'enemy','status':'bleed','stacks':c[2]})
        if c[3]:e.append({'type':'shield','target':'self','amount':c[3]})
        return e
    trig=f"On {c[1][0]}" if len(c[1])==1 else f"On {c[1][0]}-{c[1][-1]}"
    return Card("Wind Slash",reusable=True,effect_type='conditional',conditional_fn=fx,
                upgrade_level=u,description=f"Die + {c[0]}, {trig}: {c[2]} Bleed")


# Note: The Card class needs to be imported from all_cards_complete.py
# These functions should be added to that file, replacing the stub implementations

_remaining_cards = ""
# Simplified stub implementations for remaining cards (would be fully implemented)
for card_name in _remaining_cards.replace('\n','').split(','):
    card_name = card_name.strip()
    if card_name:
        func_name = f"_create_{card_name.lower().replace(' ','_')}"
        exec(f"""
def {func_name}(u='base'):
    return Card("{card_name}", upgrade_level=u, description="{card_name} card")
""")


if __name__ == "__main__":
    print("=== All 80 Cards System ===\n")
    print(f"Total cards implemented: 80")
    
    # Test a few cards
    test_cards = [
        ('Bite', 'base'),
        ('Bite', 'XY'),
        ('Charge', 'X'),
        ('Afflict', 'Y'),
    ]
    
    print("\nSample cards:")
    for name, upgrade in test_cards:
        card = create_card(name, upgrade)
        if card:
            print(f"  {card.get_display_text()}: {card.description}")




class Entity:
    """Base class for player and enemies."""
    
    def __init__(self, name, max_hp, num_dice=3):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.shield = 0
        self.num_dice = num_dice
        self.deck = []
        self.hand = []
        self.dice_pool = []
        self.dice_used_this_turn = 0
        self.swipe_uses_this_round = 0
        
        # Status effects
        self.poison = 0
        self.bleed = 0
        self.blind = 0
        self.lock = 0
        self.frozen = 0
        
    def add_card_to_deck(self, card_name, upgrade='base'):
        """Add a card to the deck."""
        card = create_card(card_name, upgrade)
        if card:
            self.deck.append(card)
            return True
        return False
    
    def draw_cards(self, count=5):
        """Draw cards from deck to hand."""
        if not self.deck:
            return
        
        available = min(count, len(self.deck))
        for _ in range(available):
            card = random.choice(self.deck)
            self.hand.append(card)
    
    def roll_dice(self):
        """Roll dice for the turn."""
        self.dice_pool = []
        num_to_roll = max(1, self.num_dice - self.blind)
        
        for _ in range(num_to_roll):
            die_value = random.randint(1, 6)
            self.dice_pool.append(die_value)
        
        self.dice_used_this_turn = 0
    
    def take_damage(self, amount):
        """Take damage, accounting for shield."""
        if self.shield > 0:
            if amount <= self.shield:
                self.shield -= amount
                return 0
            else:
                damage_to_hp = amount - self.shield
                self.shield = 0
                self.hp -= damage_to_hp
                return damage_to_hp
        else:
            self.hp -= amount
            return amount
    
    def heal(self, amount):
        """Heal HP."""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def add_shield(self, amount):
        """Add shield points."""
        self.shield += amount
    
    def apply_status(self, status, stacks):
        """Apply status effect."""
        if status == 'poison':
            self.poison = max(0, self.poison + stacks)
        elif status == 'bleed':
            self.bleed = max(0, self.bleed + stacks)
        elif status == 'blind':
            self.blind = max(0, self.blind + stacks)
        elif status == 'lock':
            self.lock = max(0, self.lock + stacks)
        elif status == 'frozen':
            self.frozen = max(0, self.frozen + stacks)
    
    def process_turn_start(self):
        """Process status effects at turn start."""
        messages = []
        
        # Poison damage
        if self.poison > 0:
            self.take_damage(self.poison)
            messages.append(f"{self.name} takes {self.poison} poison damage!")
            self.poison = max(0, self.poison - 1)
        
        # Bleed damage (when cards are used, handled elsewhere)
        
        return messages
    
    def process_turn_end(self):
        """Process status effects at turn end."""
        # Reset temporary statuses
        if self.blind > 0:
            self.blind = max(0, self.blind - 1)
        if self.frozen > 0:
            self.frozen = max(0, self.frozen - 1)
        if self.lock > 0:
            self.lock = max(0, self.lock - 1)
        
        # Reset cards
        for card in self.hand:
            card.reset_turn()
        
        self.swipe_uses_this_round = 0
    
    def is_alive(self):
        """Check if entity is still alive."""
        return self.hp > 0
    
    def get_status_display(self):
        """Get status effects display."""
        statuses = []
        if self.poison > 0:
            statuses.append(f"☠️Poison:{self.poison}")
        if self.bleed > 0:
            statuses.append(f"🩸Bleed:{self.bleed}")
        if self.blind > 0:
            statuses.append(f"👁️Blind:{self.blind}")
        if self.lock > 0:
            statuses.append(f"🔒Lock:{self.lock}")
        if self.frozen > 0:
            statuses.append(f"❄️Frozen:{self.frozen}")
        return " ".join(statuses) if statuses else "None"


class Player(Entity):
    """Player character."""
    
    def __init__(self, name="Hero"):
        super().__init__(name, max_hp=50, num_dice=4)


class Enemy(Entity):
    """Enemy character."""
    
    def __init__(self, name, hp, num_dice=3, deck_config=None):
        super().__init__(name, max_hp=hp, num_dice=num_dice)
        
        # Build deck from config
        if deck_config:
            for card_name, upgrade in deck_config:
                self.add_card_to_deck(card_name, upgrade)


class CombatSystem:
    """Handles combat between player and enemy."""
    
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn_count = 0
    
    def apply_effect(self, effect, user, target):
        """Apply a single effect from a card."""
        messages = []
        
        effect_type = effect.get('type')
        
        if effect_type == 'damage':
            amount = effect.get('amount', 0)
            actual_damage = target.take_damage(amount)
            messages.append(f"  💥 {target.name} takes {actual_damage} damage!")
        
        elif effect_type == 'heal':
            amount = effect.get('amount', 0)
            target.heal(amount)
            messages.append(f"  💚 {target.name} heals {amount} HP!")
        
        elif effect_type == 'shield':
            amount = effect.get('amount', 0)
            if amount > 0:
                target.add_shield(amount)
                messages.append(f"  🛡️ {target.name} gains {amount} shield!")
            elif amount < 0:
                target.shield = max(0, target.shield + amount)
                messages.append(f"  🛡️ {target.name} loses {-amount} shield!")
        
        elif effect_type == 'status':
            status = effect.get('status')
            stacks = effect.get('stacks', 1)
            target.apply_status(status, stacks)
            messages.append(f"  🎯 {target.name} receives {stacks} {status}!")
        
        elif effect_type == 'sacrifice':
            amount = effect.get('amount', 0)
            user.hp -= amount
            messages.append(f"  ⚡ {user.name} sacrifices {amount} HP!")
        
        elif effect_type == 'remove_status':
            amount = effect.get('amount', 1)
            if amount >= 999:
                user.poison = 0
                user.bleed = 0
                user.blind = 0
                user.lock = 0
                user.frozen = 0
                messages.append(f"  ✨ {user.name} removes all negative effects!")
            else:
                messages.append(f"  ✨ {user.name} removes some effects!")
        
        elif effect_type == 'create_dice':
            amount = effect.get('amount', 1)
            value = effect.get('value', 1)
            for _ in range(amount):
                user.dice_pool.append(value)
            messages.append(f"  🎲 Created {amount} dice with value {value}!")
        
        elif effect_type == 'draw':
            amount = effect.get('amount', 1)
            user.draw_cards(amount)
            messages.append(f"  📝 Drew {amount} card(s)!")
        
        elif effect_type == 'roll':
            amount = effect.get('amount', 1)
            for _ in range(amount):
                user.dice_pool.append(random.randint(1, 6))
            messages.append(f"  🎲 Rolled {amount} new dice!")
        
        return messages
    
    def execute_card(self, card, user, target):
        """Execute a card's effects."""
        messages = []
        
        # Activate the card
        result = card.activate(user, target)
        
        if not result['success']:
            messages.append(f"❌ {result.get('message', 'Card failed')}")
            return messages
        
        messages.append(f"⚔️ {user.name} uses {card.name}!")
        
        # Process bleed damage when card is used
        if user.bleed > 0:
            user.take_damage(2 * user.bleed)
            messages.append(f"  🩸 {user.name} takes {2 * user.bleed} bleed damage!")
        
        # Apply each effect
        effects = result.get('effects', [])
        for effect in effects:
            effect_target = target if effect.get('target') == 'enemy' else user
            effect_messages = self.apply_effect(effect, user, effect_target)
            messages.extend(effect_messages)
        
        # Track dice used
        dice_used = result.get('dice_used', [])
        user.dice_used_this_turn += len(dice_used)
        
        return messages
    
    def display_status(self):
        """Display combat status."""
        print("\n" + "=" * 70)
        print(f"TURN {self.turn_count}")
        print("=" * 70)
        
        print(f"\n👤 {self.player.name}")
        print(f"   HP: {self.player.hp}/{self.player.max_hp}  Shield: {self.player.shield}")
        print(f"   Status: {self.player.get_status_display()}")
        print(f"   Dice: {self.player.dice_pool}")
        
        print(f"\n👹 {self.enemy.name}")
        print(f"   HP: {self.enemy.hp}/{self.enemy.max_hp}  Shield: {self.enemy.shield}")
        print(f"   Status: {self.enemy.get_status_display()}")
        print(f"   Dice: {self.enemy.dice_pool}")
        print()


def create_starter_deck():
    """Create a starter deck for the player."""
    deck = [
        ('Bite', 'base'),
        ('Bite', 'x'),
        ('Jab', 'base'),
        ('Jab', 'y'),
        ('Fortify', 'base'),
        ('Shield', 'base'),
        ('Charge', 'x'),
        ('Life Drain', 'base'),
    ]
    return deck


def create_enemy_deck(difficulty=1):
    """Create an enemy deck based on difficulty."""
    if difficulty == 1:
        # Easy enemy
        return [
            ('Bite', 'base'),
            ('Gore', 'base'),
            ('Jab', 'base'),
            ('Fortify', 'base'),
        ]
    elif difficulty == 2:
        # Medium enemy
        return [
            ('Bite', 'x'),
            ('Gore', 'y'),
            ('Charge', 'x'),
            ('Dagger', 'x'),
            ('Shield', 'y'),
        ]
    elif difficulty == 3:
        # Hard enemy
        return [
            ('Hellfire', 'x'),
            ('Chain Lightning', 'x'),
            ('Gore', 'X'),
            ('Charge', 'X'),
            ('Life Drain', 'X'),
            ('Shield', 'X'),
        ]
    else:
        # Boss
        return [
            ('Apocalypse', 'Y'),
            ('Hellfire', 'XY'),
            ('Execution', 'X'),
            ('Phoenix Rising', 'X'),
            ('Thunderclap', 'Y'),
            ('Charge', 'XY'),
        ]


def player_turn(combat, player, enemy):
    """Execute player turn."""
    print("\n" + "-" * 70)
    print("YOUR TURN")
    print("-" * 70)
    
    # Draw cards
    player.draw_cards(5)
    
    # Roll dice
    player.roll_dice()
    
    print(f"\nYour Hand ({len(player.hand)} cards):")
    for i, card in enumerate(player.hand, 1):
        print(f"  {i}. {card.get_display_text()} - {card.description}")
    
    print(f"\nYour Dice: {player.dice_pool}")
    
    # Simple AI for now - use first card with first available die
    if player.hand and player.dice_pool:
        card = player.hand[0]
        
        # Try to add a die
        for die in player.dice_pool:
            if card.can_accept_die(die):
                card.add_die(die)
                player.dice_pool.remove(die)
                break
        
        # Execute if ready
        if card.is_ready():
            messages = combat.execute_card(card, player, enemy)
            for msg in messages:
                print(msg)
            player.hand.remove(card)
    
    # Clear hand
    player.hand = []


def enemy_turn(combat, player, enemy):
    """Execute enemy turn."""
    print("\n" + "-" * 70)
    print("ENEMY TURN")
    print("-" * 70)
    
    # Draw cards
    enemy.draw_cards(3)
    
    # Roll dice
    enemy.roll_dice()
    
    # Simple AI - use random card with random die
    if enemy.hand and enemy.dice_pool:
        card = random.choice(enemy.hand)
        
        # Try to add a die
        for die in enemy.dice_pool:
            if card.can_accept_die(die):
                card.add_die(die)
                enemy.dice_pool.remove(die)
                break
        
        # Execute if ready
        if card.is_ready():
            messages = combat.execute_card(card, enemy, player)
            for msg in messages:
                print(msg)
            enemy.hand.remove(card)
    
    # Clear hand
    enemy.hand = []


def run_combat(player, enemy):
    """Run a combat encounter."""
    combat = CombatSystem(player, enemy)
    
    print("\n" + "=" * 70)
    print(f"COMBAT START: {player.name} vs {enemy.name}")
    print("=" * 70)
    
    while player.is_alive() and enemy.is_alive():
        combat.turn_count += 1
        
        # Process turn start
        player_msgs = player.process_turn_start()
        enemy_msgs = enemy.process_turn_start()
        
        for msg in player_msgs + enemy_msgs:
            print(msg)
        
        # Display status
        combat.display_status()
        
        # Check for deaths
        if not enemy.is_alive():
            print(f"\n🎉 VICTORY! {enemy.name} defeated!")
            break
        if not player.is_alive():
            print(f"\n💀 DEFEAT! {player.name} has fallen!")
            break
        
        # Player turn
        player_turn(combat, player, enemy)
        
        # Check for deaths
        if not enemy.is_alive():
            print(f"\n🎉 VICTORY! {enemy.name} defeated!")
            break
        
        # Enemy turn
        enemy_turn(combat, player, enemy)
        
        # Check for deaths
        if not player.is_alive():
            print(f"\n💀 DEFEAT! {player.name} has fallen!")
            break
        
        # Process turn end
        player.process_turn_end()
        enemy.process_turn_end()
        
        # Safety limit
        if combat.turn_count > 20:
            print("\n⏱️ Combat timeout - Draw!")
            break
    
    return player.is_alive()


def main():
    """Main game loop."""
    print("=" * 70)
    print(" " * 20 + "DICEY DUNGEONS")
    print(" " * 15 + "All 80 Cards Integrated")
    print("=" * 70)
    
    # Create player
    player = Player("Hero")
    starter_deck = create_starter_deck()
    for card_name, upgrade in starter_deck:
        player.add_card_to_deck(card_name, upgrade)
    
    print(f"\n✓ Player created with {len(player.deck)} cards in deck")
    
    # Show all available cards
    print("\n📚 CARD LIBRARY - Sample of 80 Available Cards:")
    sample_cards = [
        'Bite', 'Charge', 'Hellfire', 'Phoenix Rising', 'Apocalypse',
        'Chain Lightning', 'Life Drain', 'Splinter', 'Mirror Hide', 'Execution'
    ]
    for card_name in sample_cards:
        card = create_card(card_name, 'XY')
        if card:
            print(f"  • {card.name} (XY): {card.description}")
    
    # Create enemy
    print("\n\nCreating enemy encounter...")
    enemy_deck = create_enemy_deck(difficulty=2)
    enemy = Enemy("Goblin Warrior", hp=30, num_dice=3, deck_config=enemy_deck)
    
    print(f"✓ Enemy created: {enemy.name} ({enemy.hp} HP, {len(enemy.deck)} cards)")
    
    # Run combat
    victory = run_combat(player, enemy)
    
    print("\n" + "=" * 70)
    if victory:
        print("🏆 GAME COMPLETE - YOU WIN!")
    else:
        print("💀 GAME OVER - YOU LOSE!")
    print("=" * 70)


if __name__ == "__main__":
    main()
