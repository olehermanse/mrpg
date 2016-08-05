//  current.cpp
//  Created by Ole Herman S. Elgesem on 28/01/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.

#include "Combat.hpp"

void Combat::setInputs(SSHORT inpA, SSHORT inpB){
    this->inputA = inpA;
    this->inputB = inpB;
}
type_winner Combat::checkWinner(){
    if(a.isAlive() && b.isAlive())
        return WINNER_NO;
    if(a.isDead() && b.isDead())
        return WINNER_DRAW;
    if(a.isAlive())
        return WINNER_A;
    if(b.isAlive())
        return WINNER_B;
    debug_error("Cannot check winner");
    return WINNER_DRAW;
}
void Combat::doTurn(){
    SSHORT as = a.current.speed;
    SSHORT bs = b.current.speed;
    if(as == bs)
        speedTieTurn();
    else if(as > bs)
        orderedTurn(a,b);
    else if(as < bs)
        orderedTurn(b,a);
    else
        debug_error("Cannot determine speed priority");
    return;
}

void Combat::doSkill(CombatPlayer& a,  CombatPlayer& b){
    Skill* s = Skills::s->get(a.skills[a.skillInput]);
    s->perform(a,b);
    a.cooldownTimers[a.skillInput] = s->cooldown;
}

void Combat::orderedTurn( CombatPlayer& x,  CombatPlayer& y){
    doSkill(a,b);
    if(checkWinner() == WINNER_NO)
        doSkill(b,a);
}

void Combat::speedTieTurn(){
    if(a.lvl > b.lvl){
        orderedTurn(a,b);
    }else if(b.lvl > a.lvl){
        orderedTurn(b,a);
    }else if(a.current.hp > b.current.hp){
        orderedTurn(a,b);
    }else if(b.current.hp > a.current.hp){
        orderedTurn(b,a);
    }else{
        printf("%s and %s acted at the same time:\n", a.name.c_str(), b.name.c_str());
        Stats preA;
        Stats preB;
        Stats postB;

        //SAVE BEGIN STATE
        a.current.copyTo(preA);
        b.current.copyTo(preB);
        //DO ONE SKILL
        doSkill(a,b);
        //SAVE B
        b.current.copyTo(postB);
        //RESET
        preA.copyTo(a.current);
        preB.copyTo(b.current);
        //DO SKILL 2
        doSkill(b,a);
        //CARRY OVER B
        postB.copyTo(b.current);
        //FINISHED
    }
}
