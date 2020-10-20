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
    for(int i = 0; i < robot_nmbr; i++){
        status.push_back(0);
    }
    std::stringstream ss;
    ss << robot_nmbr;
    status_pub = n.advertise<std_msgs::Int32MultiArray>("/robot/status", 100);
    status_sub = n.subscribe("/robot/status", 100, updateStatus);
    scanQR = n.subscribe("/robot"+ss.str()+"/scanQR", 100, startScan);


    ros::AsyncSpinner spinner(6); // Use 3 threads
    spinner.start();
    return 0;
}

void startScan(std_msgs::Int32 msg){
    int data = msg.data;
    if(data == 1){
        //startScanQr
        //mit drehen rechts links usw
        //unterscheide hier roboter
        //roboter -1
        //erkenne station warte festgelegten wert evtl neu 
        //kalibrieen während warten.
        //publishb einmal 51 für wartn und 50 ende warten
    }
}

bool getParams(ros::NodeHandle n){
    node_name = ros::this_node::getName();
    extractIntegerWords(node_name);
    if(!(n.getParam("/HeadController/num_robots", robot_nmbr))){
        ROS_ERROR("Could not get number of robots");
        return false;
    }
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

void publishStatus(){
    std_msgs::Int32MultiArray msg;
    status_mutex.lock();
    msg.data = status;
    status_mutex.unlock();
    status_pub.publish(msg);
}
void updateStatus(std_msgs::Int32MultiArray msg){
    status_mutex.lock();
    status = msg.data;
    status_mutex.unlock();
}