//  ClientController.cpp
//  Created by Ole Herman S. Elgesem on 26/04/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.

#include "ClientController.hpp"

void ClientController::welcome(){
	mprintf("Welcome to this early alpha test.\n");
	mprintf("Nothing is finished, everything is subject to change.\n");
	mprintf("Thanks for helping me improve the game!\n\n");
	mPause();
}

void ClientController::characterCreation(){
	mprintf("Character creation:\n");
	char name[256] = "";
	mprintf("Enter name: ");
	scanf("%s", name);

	Player* p1 = new Player(name, "0101");
	p1->setLevel(50);

	mprintf("\nPassives:\n");
	game->passives->printAll();
	for(int i = 0; i<NUM_PASSIVES;++i){
		p1->passives[i] = mInputByte(1, game->passives->size()-1, "Pick passive no. %i: ",i);
	}

	mprintf("\nSkills:\n");
	game->skills->printAll();
	for(int i = 1; i<NUM_SKILLS; ++i){
        p1->skills[i] = mInputByte(1, game->skills->size()-1, "Pick a skill for slot %i:\n", i);
	}

	player = p1;
}

void ClientController::testBattle(){
	mprintf("Test Battle:\n");
	Player p1(*player), cp("Enemy", "CPID");
	p1.setLevel(50);
	p1.base.speed += 2;
	cp.setLevel(50);
	cp.base.attack += 2;

	//msecPacket* msecEnPacket(char* data, BYTE length);
	//char* msecDePacket(void* packet);
	std::cout << p1.sprint() << std::endl;
	std::cout << p1.sprint() << std::endl;

	printf("Welcome to my RPG Combat Demo!\n");
	std::string inString;

	char in = 'y';
	while(in == 'y'){
		//doCombat(p1, cp);
		printf("Thank you for playing. Play again?\n");
		fflush(stdin);
		fflush(stdout);
		scanf(" %c", &in);
	}
}
