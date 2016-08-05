//  Combat CombatPlayer.cpp
//  Created by Ole Herman S. Elgesem on 11/02/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.

#include "CombatPlayer.hpp"

bool CombatPlayer::isDead(){
    if(current.hp == 0)
        return true;
    return false;
}

bool CombatPlayer::isAlive(){
    return !isDead();
}

BYTE CombatPlayer::damage(BYTE dmg, BYTE type){
    //DAMAGE MITIGATION: 95/(1+2^(-(x-60)/7)) for x = 0 to 100, y = 0 to 100
    float fMit= 0.0f;
    float fDef = 0.0f;
    float fDmg = 0.0f;
    if(type == DMG_TRUE){
        //No reduction
    }else if(type == DMG_PHYSICAL){
        fDef = (float)current.defense;
    }else if(type == DMG_MAGICAL){
        fDef = (float)current.resist;
    }else if(type == DMG_NONE){
        return 0;
    }else{
        return 0;
    }

    fMit = 20.0f + 75.0f/(1.0f+exp(-(fDef-60.0f)/7.0f));
    fDmg = (float)dmg;
    fDmg = fDmg*(fMit/100.0f);
    signed int iDmg = (int)fDmg+0.5;
    if(iDmg < 0 || iDmg > 255){
        mError("Floating point overflow error in damage calculation");
        dmg = 0;
    }
    dmg = (unsigned char)iDmg;
    client_print("%s took %d damage.(%i%% mitigation)\n", name.c_str(), dmg,(int)(fMit+0.5f));
    if(dmg >= current.hp)
        this->die();
    else
        current.hp -= dmg;
    return dmg;
}

void CombatPlayer::heal(BYTE life){
    BYTE diff = current.maxHP - current.hp;
    if( diff < life )
        life = diff;
    client_print("%s was healed for %d health points.\n", name.c_str(), life);
    current.hp += life;
}

void CombatPlayer::restore(){
    current.hp = current.maxHP;
}

void CombatPlayer::die(){
    client_print("%s died...\n", name.c_str());
    current.hp = 0;
}

void CombatPlayer::encounter(){
    client_print("Encountered a level %d %s.\n", lvl, name.c_str());
}

void CombatPlayer::addEffect(Effect* e){
	if(e == NULL){
		debug_error("Cannot add null effect.\n");
		return;
	}
	removeEffect(e->name);
    for(BYTE i=0; i<NUM_EFFECTS; ++i){
        if(effects[i] == NULL){
            effects[i] = e;
            updateCombatStats();
            client_print("Effect %d - '%s' effect will be active for %d turns.\n", i, e->name.c_str(), e->duration);
            return;
        }
    }
}


void CombatPlayer::addEffect(   std::string name, SSHORT duration,
                                type_stat specifier, type_effect op, double value){
    addEffect(new Effect(name, duration, specifier, op, value));
}

bool CombatPlayer::hasEffect(std::string name){
    for(BYTE i=0; i<NUM_EFFECTS; ++i){
        if(effects[i]){
            if(name == effects[i]->name)
                return true;
        }
    }
    return false;
}

void CombatPlayer::removeEffect(BYTE i){
    client_print("Effect %d - '%s' faded...\n", i, effects[i]->name.c_str());
    delete effects[i];
    effects[i] = NULL;
}
void CombatPlayer::removeEffect(std::string name){
    for(BYTE i=0; i<NUM_EFFECTS; ++i){
        if(effects[i]){
            if(name == effects[i]->name)
                removeEffect(i);
        }
    }
}

void CombatPlayer::updateTurn(){
    bool update = false;
    for(int i=0; i<NUM_EFFECTS; ++i){
        //Tick effect timers:
        if(effects[i] != NULL){
            if(effects[i]->duration == 0){
                removeEffect(i);
                update = true;
            }else{
                --effects[i]->duration;
            }
        }
        //Tick Cooldowns:
        if(i<NUM_SKILLS){
            if(cooldownTimers[i] > 0)
                --cooldownTimers[i];
        }
    }
    if(update)
        updateCombatStats();
}

void CombatPlayer::updateCombatStats(){
    base.copyTo(current);
    for(int i=0; i<NUM_EFFECTS; ++i){
        if(effects[i]){
            effects[i]->apply(current);      //Adds an active effect to combat stats
        }
    }
    for(int i=0; i<NUM_PASSIVES; ++i){
        if(passives[i] > 0){
            Passives::s->get(passives[i])->apply(current);
        }
    }
    current.checkLimits();
}

bool CombatPlayer::canUse(){
    if( cooldownTimers[skillInput])
        return false;
    if( cast < skillPointers[skillInput]->cast )
        return false;
    return true;
}


void CombatPlayer::printSkills(){
    for(int i = 0; i<8; ++i){
        if(skillPointers[i] != NULL){
            std::string sName = skillPointers[i]->name;
            if(i > 0){
                if(skillPointers[i] != skillPointers[i-1]){
                    mprintf("(%d) %s", i, sName.c_str());
                    if(cooldownTimers[i] > 0){
                        mprintf(" - Cooldown: %d", cooldownTimers[i]);
                    }
                    mprintf("\n");
                }

            }else{
                mprintf("(%d) %s", i, sName.c_str());
                if(cooldownTimers[i] > 0){
                    mprintf(" - Cooldown: %d", cooldownTimers[i]);
                }
                mprintf("\n");
            }
        }
    }
}

void CombatPlayer::printInfo(){
    mprintf("%s(%d) - HP: %d/%d Cast: %d\n", name.c_str(), lvl,
           current.hp, current.maxHP, cast);
}

void CombatPlayer::printEffects(){
    for(int i = 0; i<NUM_EFFECTS;++i){
        if(effects[i] != NULL){
            //effects[i]->print();
        }
    }
}
