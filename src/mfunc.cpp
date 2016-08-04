//
//  mfunc.cpp
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 26/02/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
//

#include "mfunc.hpp"

void mInit(){
    server_print("Server output is enabled.\n");
    client_print("Client output is enabled.\n");
    debug_print("Debug output is enabled.\n\n");

    srand((unsigned int)time(NULL));
}

void mPause(){
    std::cin.ignore();
}

void mSwapBytes(char* a, char* b){
    char temp = *a;
    *a = *b;
    *b = temp;
}

void mSwapNBytes(char*a, char* b, int n){
    for(int i=0; i<n; ++i){
        mSwapBytes(a+n, b+n);
    }
}

void mReverseNBytes(void* start, int n){
    for(int i=0; i<n/2; ++i){
        mSwapBytes((char*)(start), (char*)(start) + n - 1 - i);
    }
}

void mSubtractBytes(BYTE& a, BYTE& b){
    if(b>a){
        a = 0;
        return;
    }
    a -= b;
}

BYTE mInputByte(int min, int max, const char* fmt, ...){
	int temp = 0;
	do{
		va_list args;
		va_start(args, fmt);
		vprintf(fmt, args);
		va_end(args);
		scanf("%i", &temp);
	}while( temp < min || temp > max);
	char c;
	while((c = getchar()) != '\n' && c != EOF){}
	return temp;
}

std::string mInputString(const char* fmt, ...){
	char buffer[256];
	va_list args;
	va_start(args, fmt);
	vprintf(fmt, args);
	va_end(args);
	scanf("%s", buffer);
	for(int i = 0; i<256 && buffer[i] != 0; ++i){
		if(buffer[i] == '\n' || buffer[i] == EOF){
			buffer[i] = 0;
		}else if(buffer[i] == '\t'){
			buffer[i] = ' ';
		}
	}
	std::string ret = buffer;
	return ret;
}

void mprintf( const char* fmt, ...){
    va_list args;
    va_start(args, fmt);
    vprintf(fmt, args);
    va_end(args);
}

void mError( const char* fmt, ...){
	va_list args;
    va_start(args, fmt);
    vprintf(fmt, args);
    va_end(args);
	exit(1);
}
