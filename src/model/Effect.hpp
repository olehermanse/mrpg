//
//  Effect.h
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 18/04/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.

#ifndef __mRPG__Effect__
#define __mRPG__Effect__

#include "../definitions.hpp"
#include "Stats.hpp"

enum type_effect{
    EFFECT_NONE,
    EFFECT_ADD,
    EFFECT_MUL
};

//Abstract Base Class for all skill effects and passive effects
class Effect{
public:
    std::string name;
    SSHORT duration;
    type_stat specifier;
    type_effect op;
    FLOAT value;
    Effect( std::string name, SSHORT duration,
            type_stat specifier, type_effect op, double value){
        this->name = name;
        this->specifier = specifier;
        this->op = op;
        this->value = value;
        this->duration = duration;
    }
    void apply(Stats& s){

    }
    std::string text(){
        std::string sample = "Effect Sample Text";
        return sample;
    }
    ~Effect(){}
};

#endif
