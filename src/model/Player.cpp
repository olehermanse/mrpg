//
//  Player.cpp
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 11/02/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
//

#include "Player.hpp"

Player::Player(std::string name, const char* ID){
    this->name = name;

    setLevel(1);

    for(int i = 0; i<8; ++i){
        this->skills[i] = 0;
    if(ID == NULL)
        return;
    for(int i = 0; i<4; ++i)
        this->playerID[i] = ID[i];
    }
}


Player::Player(const Player & copyFrom){
    this->name = copyFrom.name;
    for(int i = 0; i<4; ++i){
        this->playerID[i] = copyFrom.playerID[i];
        this->passives[i] = 0;
    }
    base = copyFrom.base;
    lvl = copyFrom.lvl;
    for(int i = 0; i<8; ++i){
        this->skills[i] = copyFrom.skills[i];
    }
}

void Player::setLevel(BYTE level){
    if(level == this->lvl)
        return;
    if(level > MAX_LEVEL)
        level = MAX_LEVEL;
    this->lvl = level;
    base.speed  = base.attack
                = base.magic
                = base.defense
                = base.resist
                = level;

    base.maxHP = level*4;
    base.hp = 0;
}

std::string Player::sprint(){
	std::ostringstream mstream;
	std::string r;
	mstream << this->name << "(" << (int)this->lvl << ")" << std::endl;
	mstream << playerID[0] << playerID[1] << playerID[2] << playerID[3] << std::endl;
	mstream << (int)playerID[0] << " " << (int)playerID[1] << " " << (int)playerID[2] << " " << (int)playerID[3];
	mstream << std:: endl << "Skills: ";
	for(int i = 0; i<8; ++i){
		mstream << (int)skills[i] << " ";
	}
	mstream << std::endl << "Passives: ";
	for(int i = 0; i<4; ++i){
		mstream << (int)passives[i] << " ";
	}
	mstream << std::endl;
	r = mstream.str();
	return r;
}


std::string Player::saveString(){
	std::string r;
	std::ostringstream mstream;
	BYTE l = this->name.length();
	mstream << l << this->name << lvl;
	for(BYTE i = 0; i<8; ++i){
		if(i < 4){
			mstream << playerID[i] << passives[i];
		}
		mstream << skills[i];
	}
	r = mstream.str();

	mprintf("SIZE: %lu", r.length());
	return r;
}

void Player::loadString(std::string save){
	if(save.length() < 19){
		mprintf("SIZE: %lu", save.length());
		return;
	}
	int ci = 0;
	BYTE l = save[ci++];
	this->name = save.substr(ci,l);
	ci += l;
	this->lvl = save[ci++];
	for(BYTE i = 0; i<8; ++i){
		if(i < 4){
			playerID[i] = save[ci++];
			passives[i] = save[ci++];
		}
		skills[i] = save[ci++];
	}
}
