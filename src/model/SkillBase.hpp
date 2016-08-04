//
//  SkillBase.h
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 16/04/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
//

#ifndef __mRPG__SkillBase__
#define __mRPG__SkillBase__

#include "../definitions.hpp"

//Base class for all skills, used by CombatPlayer and Skills
class SkillBase{
public:

    SkillBase(){
        for(int i=0;i<256;++i){
            if(sArr[i] == NULL){
                sArr[i] = this;
                return;
            }
        }
    }
    virtual ~SkillBase(){
        cast = 0;
        cooldown = 0;
        num = 0;
        for(int i=0;i<256;++i){
            if(sArr[i] == this){
                sArr[i] = NULL;
            }
        }
    }
    std::string name;
    BYTE cast;
    BYTE cooldown;
    BYTE num;
    static SkillBase* sArr[256];
};

#endif /* defined(__mRPG__SkillBase__) */
