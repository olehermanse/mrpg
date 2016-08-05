//  main.cpp
//  Created by Ole Herman S. Elgesem on 28/01/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.

#include "controller/controller.hpp"

int main(int argc, const char * argv[])
{
    Json::Value* character = readJSONFile("data/character.json");
    std::cout << character->toStyledString();
    writeJSON(*character, "data/character.json");
    delete character;
    character = NULL;

    ClientController* c = new ClientController();
    c->start();
    delete c;
    c = NULL;
	return 0;
}
