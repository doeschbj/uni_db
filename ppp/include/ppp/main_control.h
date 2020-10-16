#ifndef MAIN_CONTROL_H
#define MAIN_CONTROL_H

#include "ros/ros.h"

int robot_nmbr = -1;
std::string node_name;
bool getParams(ros::NodeHandle n);
void extractIntegerWords(std::string str);
#endif