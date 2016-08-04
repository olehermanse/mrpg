//
//  stats.cpp
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 30/01/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.

#include "Stats.hpp"

Stats::Stats(){
    speed = attack = defense = 0;
    magic = resist = 0;
    hp = maxHP = 0;
}

Stats::Stats(BYTE sp, BYTE atk, BYTE def, BYTE mg, BYTE res, BYTE h, BYTE mH){
    speed = sp;
    attack = atk;
    defense = def;
    magic = mg;
    resist = res;
    hp = h;
    maxHP = mH;
}

void Stats::copyTo(Stats &a){
    a.speed = this->speed;
    a.attack = this->attack;
    a.defense = this->defense;
    a.magic = this->magic;
    a.resist = this->resist;
    a.maxHP = this->maxHP;
}

void Stats::addTo(Stats &a){
    a.speed += this->speed;
    a.attack += this->attack;
    a.defense += this->defense;
    a.magic += this->magic;
    a.resist += this->resist;
    a.hp += this->hp;
    a.maxHP += this->maxHP;
}

void Stats::checkLimits(){
    if(hp>maxHP)
        hp = maxHP;
}
