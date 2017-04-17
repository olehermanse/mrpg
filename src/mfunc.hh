//  mfunc.h
//  Created by Ole Herman S. Elgesem on 26/02/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.

#pragma once

#include "definitions.hpp"

void mInit();
void mPause();
void mSwapBytes(char* a, char* b);
void mSwapNBytes(char*a, char* b, int n);
void mReverseNBytes(void* start, int n);
void mSubtractBytes(BYTE& a, BYTE& b);
BYTE mInputByte(int min, int max, const char* fmt, ...);
#ifdef WINDOWS_
void mprintf( const char* fmt, ...);
void mError( const char* fmt, ...);
std::string mInputString(const char* fmt, ...);
#else
void mprintf( const char* fmt, ...) __printflike(1,2);
void mError( const char* fmt, ...) __printflike(1,2);
std::string mInputString(const char* fmt, ...) __printflike(1,2);
#endif

std::string readFile(const std::string& path);
void writeFile(std::string& data, const std::string& path);
void writeJSON(Json::Value& data, const std::string& path);
Json::Value* readJSON(std::string& data);
Json::Value* readJSONFile(const std::string& path);
