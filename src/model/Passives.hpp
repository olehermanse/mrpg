//
//  Passives.h
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 21/04/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
//

#ifndef __mRPG__Passives__
#define __mRPG__Passives__

#include "Effect.hpp"

class Passives{
public:
    //Singleton:
    static Passives* s;

    //Init:
    static Passives* Init(){
        s = new Passives();
        return s;
    }

    Passives(){
        bool done = false;
        BYTE i = 0;
        while(!done){
            createPassives();
            if(i==255)
                done = true;
            ++i;
        }
    }

    ~Passives(){
        for(int i = 0; i<256; ++i){
            if(pArr[i] != NULL){
                delete pArr[i];
                pArr[i] = NULL;
            }
        }
    }

    //All passives:
    Effect* pArr[256];

    //Get:
    Effect* get(BYTE i){
        return pArr[i];
    }

    //Fills Passive array:
    void createPassives();

    void printAll();

    BYTE size(){
        int i = 1;
        for(; i< 256; ++i){
            if(pArr[i] == NULL){
                return (BYTE)i;
            }
        }
        return (BYTE)i;
    }
};

#endif /* defined(__mRPG__Passives__) */
