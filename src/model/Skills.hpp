//
//  skills.h
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 09/02/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
//

#ifndef __mRPG__skills__
#define __mRPG__skills__
#include "skillfuncs.hpp"

//Derived Skill class introduces skill function pointer
class Skill: public SkillBase{
public:
    Skill(std::string name, BYTE cast, BYTE cooldown, void (*perform)( CombatPlayer&,  CombatPlayer&), BYTE index){
        this->name = name;
        this->cast = cast;
        this->cooldown = cooldown;
        this->perform = perform;
    }
    void (*perform)( CombatPlayer& user,  CombatPlayer& target);
};

class Skills{
public:
    //Singleton
    static Skills* s;
    static Skills* Init(){
        s = new Skills();
        return s;
    }
    Skills();

    ~Skills();

    Skill* get(BYTE num);

    void printAll();
    BYTE size(){
        int i = 0;
        for(; i<256;++i){
            if(skills[i] == NULL){
                return (BYTE)i;
            }
        }
        return (BYTE)i;
    }

private:
    Skill* skills[256];

    void makeSkill(BYTE i, std::string name, BYTE cast, BYTE cooldown, void (*perform)( CombatPlayer&,  CombatPlayer&));
};

#endif /* defined(__mRPG__skills__) */
