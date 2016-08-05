//  combat.h
//  Created by Ole Herman S. Elgesem on 28/01/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.

#pragma once
#include "Skills.hpp"

enum type_winner {WINNER_NO = 0, WINNER_A, WINNER_B, WINNER_DRAW};

class Combat{
public:
    Combat(CombatPlayer& a, CombatPlayer& b):
    a(a),
    b(b){
        inputA = inputB = 0;
    }

    void setInputs(SSHORT inpA, SSHORT inpB);
    type_winner checkWinner();
    void doTurn();
    void orderedTurn(CombatPlayer& x, CombatPlayer& y);
    void speedTieTurn();

    void doSkill(CombatPlayer& x,  CombatPlayer& y);

private:
    CombatPlayer& a;
    CombatPlayer& b;

    SSHORT inputA;
    SSHORT inputB;
};
