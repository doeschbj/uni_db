#include "ppp/main_control.h"
#include "ros/ros.h"
#include <sstream>
#include <iostream> 
#include <string>
#include <regex>

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "robot_station");
    ros::NodeHandle n;
    if(!getParams(n)){return -1;}
    ROS_INFO("Robot number = %d", robot_nmbr);

    
    ros::spin();
    return 0;
}

bool getParams(ros::NodeHandle n){
    node_name = ros::this_node::getName();
    extractIntegerWords(node_name);

    return true;
}

void extractIntegerWords(std::string str) { 
    std::string output = std::regex_replace(
        str,
        std::regex("[^0-9]*([0-9]+).*"),
        std::string("$1")
        );
        robot_nmbr = stoi(output);
} 