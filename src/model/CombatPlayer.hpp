//
//  CombatPlayer.h
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 11/02/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.

#ifndef __mRPG__CombatPlayer__
#define __mRPG__CombatPlayer__

#include "Player.hpp"
#include "SkillBase.hpp"
#include "Effect.hpp"
#include "Passives.hpp"

class CombatPlayer: public Player{
public:
    Stats current;
    Effect* effects[NUM_EFFECTS];

    BYTE cast;
    BYTE skillInput;
    SkillBase* skillPointers[NUM_SKILLS];
    BYTE cooldownTimers[NUM_SKILLS];

    CombatPlayer(const Player & copyFrom):
    Player(copyFrom){
        Init();
    }

    CombatPlayer(std::string name, const char* ID):
    Player(name, ID){
        Init();
    }

    ~CombatPlayer(){
        skillInput = 0;
        cast = 0;
        for(int i=0; i<NUM_EFFECTS; ++i){
            if(effects[i] != NULL){
                delete effects[i];
                effects[i] = NULL;
            }
            if(i<NUM_SKILLS){
                cooldownTimers[i] = 0;
                skillPointers[i] = NULL;//This class does not create or destroy skills
            }
        }
    }

    void Init(){
        base.copyTo(current);
        skillInput = 0;
        cast = 0;

        for(int i=0; i<NUM_EFFECTS; ++i){
            effects[i] = NULL;
            if(i<NUM_SKILLS){
                cooldownTimers[i] = 0;
                skillPointers[i] = SkillBase::sArr[skills[i]];
            }
        }
    }

    //Combat:
    BYTE damage(BYTE dmg, BYTE type);
    void heal(BYTE life);
    void addEffect(Effect* e);
    void addEffect( std::string name, SSHORT duration,
                    type_stat specifier, type_effect op, double value);
    bool hasEffect(std::string name);
    void removeEffect(BYTE i);
    void removeEffect(std::string name);

    //Messages:
    void encounter();

    //Set Variables:
    void die();
    void restore();
    void updateTurn();
    void updateCombatStats();

    //Check Variables:
    bool isDead();
    bool isAlive();
    bool canUse();

    //Printing:
    void printSkills();
    void printInfo();
    void printEffects();
};

#endif /* defined(__mRPG__CombatPlayer__) */
