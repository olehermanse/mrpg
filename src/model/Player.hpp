//  Player.h
//  Created by Ole Herman S. Elgesem on 11/02/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
#pragma once

#include "stats.hpp"

#define NUM_PASSIVES 4
#define NUM_SKILLS 8
#define NUM_EFFECTS 16

#define MAX_LEVEL 50

//Basic class
class Player{
public:
    std::string name;
    BYTE playerID[4];

    Stats base;
    BYTE lvl;

    BYTE skills[NUM_SKILLS];
    BYTE passives[NUM_PASSIVES];

    Player(std::string name, const char* ID);
    Player(const Player & copyFrom);
    void setLevel(BYTE level);
    void statReset();
	std::string sprint();
	std::string saveString();
	void loadString(std::string save);
};
