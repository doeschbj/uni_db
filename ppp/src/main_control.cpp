#include "ppp/main_control.h"
#include "ros/ros.h"
#include <sstream>
#include <iostream> 
#include <string>
#include <regex>
#include "ppp/barcode.h"

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "robot_station");
    ros::NodeHandle n;
    if(!getParams(n)){return -1;}
    ROS_INFO("Robot number = %d", robot_nmbr);
    for(int i = 0; i < amofbots; i++){
        status.push_back(0);
    }
    std::stringstream ss;
    ss << robot_nmbr;
    status_pub = n.advertise<std_msgs::Int32MultiArray>("/robot/status", 100);
    status_sub = n.subscribe("/robot/status", 100, updateStatus);
    scanQR = n.subscribe("/robot"+ss.str()+"/scanQR", 100, startScan);

    if(robot_nmbr == 2){
        client_pi = n.serviceClient<ppp::barcode>("barcode_read_pi");
    }else if(robot_nmbr == 3){
        client_pixy = n.serviceClient<ppp::barcode>("barcode_read_pixy");
    }
    initSleep();

    ros::AsyncSpinner spinner(6); // Use 3 threads
    spinner.start();
    return 0;
}

void callPi(){
    ppp::barcode srv;
    srv.request.start = 1;
    int res = -1;
    int count = 0;
    do{
        if (!client_pi.call(srv)){
            ROS_ERROR("Failed to call service barcode_read_pi");
            return;
        }else{
            res = srv.response.result;
        }
        count++;
    }while(res < 0 && count < 20);
    wait_at_station(res);
    //evtl drehen hinzufügen bei keinem erkannten code
}

void callPixy(){
    ppp::barcode srv;
    srv.request.start = 1;
    int res = -1;
    int count = 0;
    do{
        if (!client_pixy.call(srv)){
            ROS_ERROR("Failed to call service barcode_read_pixy");
            return;
        }else{
            res = srv.response.result;
        }
        count++;
    }while(res < 0 && count < 20);
    wait_at_station(res);
}

void wait_at_station(int res){

    //erkenne station warte festgelegten wert evtl neu 
    //kalibrieen während warten.
    //publishb einmal 51 für wartn und 50 ende warten
    if(res < 0){
        ROS_ERROR("Cannot find code");
    }
    status[robot_nmbr -1] = (res * 10 + 1);
    publishStatus();

    ros::Duration(sleeptime[res]).sleep();

    status[robot_nmbr -1] = (res * 10);
    publishStatus();
}

void startScan(std_msgs::Int32 msg){
    int data = msg.data;
    if(data == 1){
        switch(robot_nmbr){
            case 1:
                //noch nichts
                break;
            case 2:
                callPi(); 
                break;
            case 3:
                callPixy();
                break;
            default:
                break;
        }
    }
}

bool getParams(ros::NodeHandle n){
    node_name = ros::this_node::getName();
    extractIntegerWords(node_name);
    if(!(n.getParam("/HeadController/num_robots", amofbots))){
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

void initSleep(){
    //Wielang die roboter an welcher station warten müssen
    for(int i = 0; i < 10; i++){
        sleeptime.push_back(5.0);
    }
}