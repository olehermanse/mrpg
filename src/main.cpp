//
//  main.cpp
//  mRPG
//
//  Created by Ole Herman S. Elgesem on 28/01/14.
//  Copyright (c) 2014 olehermanse. All rights reserved.
#include "controller/controller.hpp"

using boost::property_tree::ptree;
using boost::property_tree::read_json;
using boost::property_tree::write_json;

void example() {
  // Write json.
  ptree pt;
  pt.put ("foo", "bar");
  std::ostringstream buf;
  write_json (buf, pt, false);
  std::string json = buf.str(); // {"foo":"bar"}
  printf("%s", buf.str().c_str());

  // Read json.
  ptree pt2;
  std::istringstream is (json);
  read_json (is, pt2);
  std::string foo = pt2.get<std::string> ("foo");
}

std::string map2json (const std::map<std::string, std::string>& map) {
  ptree pt;
  for (auto& entry: map)
      pt.put (entry.first, entry.second);
  std::ostringstream buf;
  write_json (buf, pt, false);
  return buf.str();
}

int main(int argc, const char * argv[])
{
    example();
    ClientController* c = new ClientController();
    c->start();
    delete c;
    c = NULL;
	return 0;
}
