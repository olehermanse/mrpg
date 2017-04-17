//  stats.h
//  Created by Ole Herman S. Elgesem on 30/01/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
#pragma once

#include "../mfunc.hpp"

enum type_stat { STAT_SPEED,
                STAT_ATTACK, STAT_DEFENSE,
                STAT_MAGIC, STAT_RESIST,
                STAT_HP, STAT_MAXHP,
                STAT_NUM };

class Stats{
public:
    SSHORT speed;

    SSHORT attack;
    SSHORT defense;

    SSHORT magic;
    SSHORT resist;

    SSHORT hp;
    SSHORT maxHP;

    Stats();
    Stats(BYTE sp, BYTE atk, BYTE def, BYTE mg, BYTE res, BYTE h, BYTE mH);

    void copyTo(Stats& a);
    void addTo(Stats& a);
    void checkLimits();
};

