//
//  mdef.h
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 28/01/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
//

#ifndef mRPG_mdef_h
#define mRPG_mdef_h

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <time.h>
#include <math.h>

#include <string>
#include <map>
#include <iostream>
#include <sstream>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>

#define DEBUG_
#define CLIENT_
#define SERVER_
//#define WINDOWS_ //WINDOWS COMPATIBILITY

#ifdef CLIENT_
#define client_print printf("");printf
#else
#define client_print while(0)printf
#endif

#ifdef SERVER_
#define server_print printf("Server:");printf
#else
#define server_print while(0)printf
#endif

#ifdef DEBUG_
#define debug_print(fmt, args...) printf("%s[%d]: " fmt, __FUNCTION__, __LINE__, ##args)
#define debug_error(fmt, args...) printf("Error in %s[%d]: ", __FUNCTION__, __LINE__);mError(fmt, ##args)
#else
#define debug_print while(0)printf
#define debug_error while(0)printf
#endif

#define merror(fmt, args...) printf("Error in %s[%d]: ", __FUNCTION__, __LINE__);_merror(fmt, ##args)

typedef unsigned short USHORT;
typedef signed short SSHORT;
typedef unsigned char BYTE;
typedef double FLOAT;

enum DMG_TYPES {DMG_NONE = 0, DMG_PHYSICAL, DMG_MAGICAL, DMG_TRUE};

#endif
