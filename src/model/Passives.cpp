//
//  Passives.cpp
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 21/04/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
//

#include "Passives.hpp"

Passives* Passives::s = NULL;

void Passives::createPassives(){
    int i = 0;
    pArr[i++] = new Effect("Physical Strength", -1, STAT_ATTACK, EFFECT_ADD, 10.0);
    pArr[i++] = new Effect("Physical Defense", -1, STAT_DEFENSE, EFFECT_ADD, 10.0);
	pArr[i++] = new Effect("Magical Power", -1, STAT_MAGIC, EFFECT_ADD, 10.0);
	pArr[i++] = new Effect("Magical Resistance", -1, STAT_RESIST, EFFECT_ADD, 10.0);
}

void Passives::printAll(){
    for(int i=0; i<256; ++i){
        if(pArr[i] != NULL){
            mprintf("%d: %s\n", i, pArr[i]->name.c_str());
        }
    }
    mprintf("\n");
}
