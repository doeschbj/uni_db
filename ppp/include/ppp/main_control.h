#ifndef MAIN_CONTROL_H
#define MAIN_CONTROL_H

#include "ros/ros.h"
#include <vector>
#include "std_msgs/Int32MultiArray.h"
#include <mutex>
#include "std_msgs/Int32.h"

int robot_nmbr = -1;
int amofbots = -1;
std::vector<int> status;
std::string node_name;
ros::Publisher status_pub;
ros::Subscriber status_sub;
ros::Subscriber scanQR;
std::mutex status_mutex;

bool getParams(ros::NodeHandle n);
void extractIntegerWords(std::string str);
void publishStatus();
void updateStatus(std_msgs::Int32MultiArray msg);
void startScan(std_msgs::Int32 msg);
#endif