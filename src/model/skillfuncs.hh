//  skillfuncs.h
//  Created by Ole Herman S. Elgesem on 26/04/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
#pragma once

#include "CombatPlayer.hpp"

void skill_nothing( CombatPlayer& user,  CombatPlayer& enemy);
void skill_attack( CombatPlayer& user,  CombatPlayer& enemy);
void skill_cast( CombatPlayer& user, CombatPlayer& enemy);
void skill_heal( CombatPlayer& user, CombatPlayer& enemy);
void skill_shock( CombatPlayer& user, CombatPlayer& enemy);
void skill_fire( CombatPlayer& user, CombatPlayer& enemy);
void skill_ice( CombatPlayer& user, CombatPlayer& enemy);
void skill_block( CombatPlayer& user, CombatPlayer& enemy);
void skill_protect( CombatPlayer& user, CombatPlayer& enemy);
void skill_shout( CombatPlayer& user, CombatPlayer& enemy);
void skill_empower( CombatPlayer& user, CombatPlayer& enemy);
void skill_kick( CombatPlayer& user, CombatPlayer& enemy);
void skill_disable( CombatPlayer& user, CombatPlayer& enemy);
void skill_execute( CombatPlayer& user, CombatPlayer& enemy);
void skill_lifesteal( CombatPlayer& user, CombatPlayer& enemy);
void skill_quickstrike( CombatPlayer& user, CombatPlayer& enemy);
void skill_slowswing( CombatPlayer& user, CombatPlayer& enemy);
void skill_bloodbolt( CombatPlayer& user, CombatPlayer& enemy);
void skill_bloodboil( CombatPlayer& user, CombatPlayer& enemy);

