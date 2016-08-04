//
//  skillfuncs.cpp
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 26/04/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
//

#include "skillfuncs.hpp"

void skill_nothing( CombatPlayer& user,  CombatPlayer & enemy){
    client_print("%s did nothing.\n", user.name.c_str());
}

void skill_attack( CombatPlayer& user,  CombatPlayer & enemy){
    client_print("%s attacked %s, ", user.name.c_str(), enemy.name.c_str());
    enemy.damage(user.current.attack, DMG_PHYSICAL);
}

void skill_cast( CombatPlayer& user, CombatPlayer & enemy){
    client_print("%s is casting...\n", user.name.c_str());
    ++user.cast;
}

void skill_heal( CombatPlayer& user, CombatPlayer& enemy){
    client_print("%s cast Heal.", user.name.c_str());
    user.heal(user.current.magic * 2);
    user.cast = 0;
}

void skill_shock( CombatPlayer& user, CombatPlayer& enemy){
    client_print("%s cast Shock at %s! ", user.name.c_str(), enemy.name.c_str());
    enemy.damage(user.current.magic * user.cast, DMG_MAGICAL);
    user.cast = 0;
}

void skill_fire( CombatPlayer& user, CombatPlayer& enemy){
	client_print("%s cast Fire at %s!", user.name.c_str(), enemy.name.c_str());
	enemy.damage(user.current.magic, DMG_MAGICAL);
	enemy.addEffect("Burn", 5, STAT_ATTACK, EFFECT_ADD, -10);
    enemy.removeEffect("Chill");
	user.cast = 0;
}

void skill_ice( CombatPlayer& user, CombatPlayer& enemy){
	client_print("%s cast Ice at %s!", user.name.c_str(), enemy.name.c_str());
    enemy.damage(user.current.magic, DMG_MAGICAL);
    enemy.addEffect("Chill", 5, STAT_SPEED, EFFECT_ADD, -10.0);
    enemy.removeEffect("Burn");
    user.cast = 0;
}

void skill_block( CombatPlayer& user, CombatPlayer& enemy){
    client_print("%s blocked.", user.name.c_str());
    user.addEffect("Block", 0, STAT_DEFENSE, EFFECT_ADD, 10.0);
	return;
}

void skill_protect( CombatPlayer& user, CombatPlayer& enemy){
    client_print("%s protected.", user.name.c_str());
    user.addEffect("Protect", 0, STAT_RESIST, EFFECT_ADD, 10.0);
    return;
}

void skill_shout( CombatPlayer& user, CombatPlayer& enemy){
    client_print("%s used Shout.", user.name.c_str());
    user.addEffect("Shout", 10, STAT_ATTACK, EFFECT_ADD, 10.0);
    return;
}

void skill_empower( CombatPlayer& user, CombatPlayer& enemy){
	user.addEffect("Empower", 10, STAT_MAGIC, EFFECT_ADD, 10.0);
    return;
}

void skill_kick( CombatPlayer& user, CombatPlayer& enemy){
    client_print("%s kicked %s!", user.name.c_str(), enemy.name.c_str());
	enemy.skillInput = 0;
    return;
}

void skill_disable( CombatPlayer& user, CombatPlayer& enemy){
    client_print("%s disabled %s.", user.name.c_str(), enemy.name.c_str());
	enemy.skillInput = 0;
    return;
}

void skill_execute( CombatPlayer& user, CombatPlayer& enemy){
	client_print("%s used execute!", user.name.c_str());
    if(enemy.current.hp < enemy.current.maxHP/3){
        BYTE atk = 0;
        if(user.current.attack*2 < user.current.attack){
            atk = 255;
        }else{
            atk = user.current.attack*2;
        }
        enemy.damage(atk, DMG_PHYSICAL);
    }else{
        enemy.damage(user.current.attack/2, DMG_PHYSICAL);
    }
    return;
}

void skill_lifesteal( CombatPlayer& user, CombatPlayer& enemy){
	client_print("%s used lifesteal!", user.name.c_str());
    BYTE dmg = enemy.damage(user.current.attack, DMG_PHYSICAL);
    user.heal(dmg);
    return;
}

void skill_quickstrike( CombatPlayer& user, CombatPlayer& enemy){
    client_print("%s used quickstrike!", user.name.c_str());
	if(user.current.speed >= enemy.current.speed){
        enemy.damage(5+user.current.attack+(user.current.speed-enemy.current.speed), DMG_PHYSICAL);
    }else{
        enemy.damage(5, DMG_PHYSICAL);
    }
    return;
}

void skill_slowswing( CombatPlayer& user, CombatPlayer& enemy){
	client_print("%s used slowswing!", user.name.c_str());
    if(user.current.speed <= enemy.current.speed){
        enemy.damage(5+user.current.attack+(enemy.current.speed-user.current.speed), DMG_PHYSICAL);
    }else{
        enemy.damage(5, DMG_PHYSICAL);
    }
    return;
}

void skill_bloodbolt( CombatPlayer& user, CombatPlayer& enemy){
    client_print("%s cast Bloodbolt!", user.name.c_str());
	user.damage(10, DMG_TRUE);
    BYTE cdmg = 0;
    if(user.isAlive()){
        cdmg += user.current.magic + 10;
        cdmg += (user.current.maxHP-user.current.hp)/2;
        enemy.damage(cdmg, DMG_TRUE);
    }
    return;
}

void skill_bloodboil( CombatPlayer& user, CombatPlayer& enemy){
	client_print("%s used Bloodboil!", user.name.c_str());
    user.damage(10, DMG_TRUE);
    if(user.isAlive()){
        user.addEffect("Bloodboil", 3, STAT_MAGIC, EFFECT_ADD, 10.0);
    }
    return;
}
