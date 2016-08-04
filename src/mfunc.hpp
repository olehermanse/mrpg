//
//  mfunc.h
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 26/02/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
//

#ifndef mRPG_mfunc_h
#define mRPG_mfunc_h

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
#endif
