//
//  ClientController.h
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 26/04/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
//

#ifndef __mRPG__ClientController__
#define __mRPG__ClientController__

#include "../model/model.hpp"

class ClientController{
public:
    Game* game;
    void start(){
		welcome();
		characterCreation();
        testBattle();
    }
    ClientController(){
        mInit();
        game = new Game();
    }
    ~ClientController(){
        delete game;
        game = NULL;
    }

    Player* player;
	void welcome();
	void characterCreation();
    void testBattle();
};

#endif /* defined(__mRPG__ClientController__) */
