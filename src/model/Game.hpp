//
//  Game.h
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 26/04/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
//

#ifndef __mRPG__Game__
#define __mRPG__Game__

#include "Player.hpp"
#include "Passives.hpp"
#include "Skills.hpp"

class Game{
public:
	Player* player;
    Game(){
        passives = Passives::Init();
        skills = Skills::Init();
    }

    ~Game(){
        delete passives;
        passives = NULL;
        delete skills;
        skills = NULL;
    }
    Passives* passives;
    Skills* skills;
};

#endif /* defined(__mRPG__Game__) */
