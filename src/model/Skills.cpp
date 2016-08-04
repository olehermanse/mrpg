//
//  skills.cpp
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 09/02/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
//

#include "Skills.hpp"

Skills* Skills::s = NULL;

Skills::Skills(){
    for(int i = 0; i < 256; ++i){
        skills[i] = NULL;
    }

    makeSkill(0, "Nothing", 0,0, &skill_nothing);
    makeSkill(1, "Attack", 0, 0, &skill_attack);
    makeSkill(2, "Cast", 0, 0, &skill_cast);
    makeSkill(3, "Heal", 1, 5, &skill_heal);
    makeSkill(4, "Shock", 1, 1, &skill_shock);
    makeSkill(5, "Fire", 1, 0, &skill_fire);
    makeSkill(6, "Ice", 1, 0, &skill_ice);
    makeSkill(7, "Block", 0, 0, &skill_block);
    makeSkill(8, "Protect", 0, 0, &skill_protect);
    makeSkill(9, "Shout", 0, 0, &skill_shout);
    makeSkill(10, "Empower", 0, 0, &skill_empower);
    makeSkill(11, "Kick", 0, 0, &skill_kick);
    makeSkill(12, "Disable", 0, 0, &skill_disable);
    makeSkill(13, "Execute", 0, 0, &skill_execute);
    makeSkill(14, "Lifesteal", 0, 0, &skill_lifesteal);
    makeSkill(15, "Quick Strike", 0, 0, &skill_quickstrike);
    makeSkill(16, "Slow Swing", 0, 0, &skill_slowswing);
    makeSkill(17, "Blood Bolt", 0, 0, &skill_bloodbolt);
    makeSkill(18, "Blood Boil", 0, 0, &skill_bloodboil);
}

Skills::~Skills(){
    for(int i = 0; i < 256; ++i){
        if(skills[i] != NULL){
            delete skills[i];
            skills[i] = NULL;
        }
    }
    for(int i = 0; i<256; ++i){
        if(SkillBase::sArr[i] != NULL){
            debug_print("This could be a problem: Found a SkillBase that wasn't deleted as Skill. i=%d: %s\n", i, SkillBase::sArr[i]->name.c_str());
            delete SkillBase::sArr[i];
            SkillBase::sArr[i] = NULL;
        }
    }
}

Skill* Skills::get(BYTE num){
    return skills[num];
}

void Skills::makeSkill(BYTE i, std::string name, BYTE cast, BYTE cooldown, void (*perform)( CombatPlayer&,  CombatPlayer&)){
    skills[i] = new Skill(name, cast, cooldown+1, perform, i);
}

void Skills::printAll(){
    printf("All available skills:\n");
    for(int i=0; i<256; ++i){
        if(skills[i]){
            printf("%d: %s\n", i, skills[i]->name.c_str());
        }
    }
    printf("\n");
}
