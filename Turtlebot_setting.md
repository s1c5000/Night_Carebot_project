## 설치환경

virtualbox(ubuntu16)

기본 메모리, 프로세서, 비디오 메모리 가능한 많이, 프로세서 가능한 많이 

--> 속도를 위해서

 

네트워크

turtlebot과 remotePC는 같은 네트워크에 있어야 한다.

가상환경에서는 무선랜카드를 잡을 수 없으니

virturlbox 설정에서 네트워크를 바꿔준다.

어댑터2 -> 어댑터에 브리지 -> 무선랜카드



## 간편설치

**$ sudo apt-get install gcc g++ gedit python git # 필요라이브러리 다운**

**$ git clone https://github.com/ROBOTIS-GIT/ros_tutorials.git;**

**$ sudo apt-get install -y chrony ntpdate;**

**$ sudo ntpdate -q ntp.ubuntu.com;**



**$ sudo apt-get update**

**$ sudo apt-get upgrade**

**$wgethttps://raw.githubusercontent.com/ROBOTIS-GIT/robotis_tools/master/install_ros_kinetic.sh && chmod 755 ./install_ros_kinetic.sh && bash ./install_ros_kinetic.sh**



터틀봇의 경우 robotis에서 제공하는 라즈비안을 받으면 ros가 자동으로 설치된다

https://www.robotis.com/service/download.php?no=1738



## 종속 ros 패키지 설정

### #remotePC 

**$ sudo apt-get install ros-kinetic-joy ros-kinetic-teleop-twist-joy ros-kinetic-teleop-twist-keyboard ros-kinetic-laser-proc ros-kinetic-rgbd-launch ros-kinetic-depthimage-to-laserscan ros-kinetic-rosserial-arduino ros-kinetic-rosserial-python ros-kinetic-rosserial-server ros-kinetic-rosserial-client ros-kinetic-rosserial-msgs ros-kinetic-amcl ros-kinetic-map-server ros-kinetic-move-base ros-kinetic-urdf ros-kinetic-xacro ros-kinetic-compressed-image-transport ros-kinetic-rqt-image-view ros-kinetic-gmapping ros-kinetic-navigation ros-kinetic-interactive-markers**

**$ cd ~/catkin_ws/src/**

**$ git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git**

**$ git clone -b kinetic-devel https://github.com/ROBOTIS-GIT/turtlebot3.git**

**$ git clone https://github.com/ROBOTIS-GIT/hls_lfcd_lds_driver.git**

**$ git clone https://github.com/ROBOTIS-GIT/turtlebot3.git**

**$ cd ~/catkin_ws && catkin_make**



### #turtlebot

**$ sudo apt-get install ros-kinetic-joy ros-kinetic-teleop-twist-joy ros-kinetic-teleop-twist-keyboard ros-kinetic-laser-proc ros-kinetic-rgbd-launch ros-kinetic-depthimage-to-laserscan ros-kinetic-rosserial-arduino ros-kinetic-rosserial-python ros-kinetic-rosserial-server ros-kinetic-rosserial-client ros-kinetic-rosserial-msgs ros-kinetic-amcl ros-kinetic-map-server ros-kinetic-move-base ros-kinetic-urdf ros-kinetic-xacro ros-kinetic-compressed-image-transport ros-kinetic-rqt-image-view ros-kinetic-gmapping ros-kinetic-navigation ros-kinetic-interactive-markers**

**$ cd ~/catkin_ws/src/**

**$ git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git**

**$ git clone -b kinetic-devel https://github.com/ROBOTIS-GIT/turtlebot3.git**

**$ git clone https://github.com/ROBOTIS-GIT/hls_lfcd_lds_driver.git**

**$ git clone https://github.com/ROBOTIS-GIT/turtlebot3.git**



##### 터틀봇에서 필요하지 않은 패키지 삭제

$ cd ~/catkin_ws/src/turtlebot3

$ rm -r turtlebot3_description/ turtlebot3_teleop/ turtlebot3_navigation/ turtlebot3_slam/ turtlebot3_example/



##### 터틀봇 종속 패키지 설치

$ cd ~/catkin_ws/src/turtlebot3

$ rm -r turtlebot3_description/ turtlebot3_teleop/ turtlebot3_navigation/ turtlebot3_slam/ turtlebot3_example/



##### 패키지 설치 후 Respberry Pi 3 재부팅



##### 터틀봇 패키지 빌드

$ source /opt/ros/kinetic/setup.bash

$ cd ~/catkin_ws && catkin_make -j1





### **bashrc의 uri수정**

ifconfig로 ip주소를 확인하고

![image-20210117003120204](C:\Users\s1c50\AppData\Roaming\Typora\typora-user-images\image-20210117003120204.png)

 bachrc를 수정해준다

무선환경이라면 무선랜카드의 inet addr로 한다.

gedit ~/.bashrc로 bashrc들어갈수있다.

![image-20210117003148017](C:\Users\s1c50\AppData\Roaming\Typora\typora-user-images\image-20210117003148017.png)

![image-20210117003153890](C:\Users\s1c50\AppData\Roaming\Typora\typora-user-images\image-20210117003153890.png)

해당 그림처럼

remotepc에선 ROS_MASTER_URI, ROS_HOSTNAME 둘 다 remotePC ip로 설정해 준다.

turtlebot에선 ROS_MASTER_URI는 remotePC ip로 HOSTNAME은 turtlebot ip로 설정한다.

(turtlebot은 nano를 편집기로 사용한다 → nano ~/.bashrc)

수정 후 remote, turtlebot둘다

**$ source ~/.bash**

를 해준다.



### **opencr 설정**

https://emanual.robotis.com/docs/en/platform/turtlebot3/opencr_setup/#opencr-setup

메뉴얼대로 하면된다.

리모트 PC

$ sudo dpkg --add-architecture armhf

$ sudo apt-get update

$ sudo apt-get install libc6:armhf

 

터틀봇에서 설정

$ export OPENCR_PORT=/dev/ttyACM0

$ export OPENCR_MODEL=waffle

$ rm -rf ./opencr_update.tar.bz2

$ wget https://github.com/ROBOTIS-GIT/OpenCR-Binaries/raw/master/turtlebot3/ROS1/latest/opencr_update.tar.bz2 && tar -xvf opencr_update.tar.bz2 && cd ./opencr_update && ./update.sh $OPENCR_PORT $OPENCR_MODEL.opencr && cd ..

### 이제 구동에 필요한 준비를 끝냈다





## 터틀봇 bringup 후 ros package 실행



### **remotePC에서 turtlebot 접속**

remotepc의 터미널에서 

**$ ssh [turtlebotID]@[turtlebotIP]**

로turtlebot에 접속가능



### bringUP

로봇을 활성화

##### #remotePC

$ roscore

 

##### #turtlebot

$ roslaunch turtlebot3_bringup turtlebot3_robot.launch

 

##### #remotePC

$ export TURTLEBOT3_MODEL=waffle_pi

$ roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch

로 키보드로 turtlebot 조종가능





### 터틀봇 카메라

\#turtlebot

$ git clone https://github.com/UbiquityRobotics/raspicam_node.git

$ sudo apt-get install ros-kinetic-compressed-image-transport ros-kinetic-camera-info-manager

$ cd ~/catkin_ws && catkin_make

 

\#remotePC

$ roscore

 

\#turtlebot

$ roslaunch turtlebot3_bringup turtlebot3_rpicamera.launch

 

\#remote

$ rqt_image_view





### slam

\#remotePC

$ rescore

 

\# turtlebot

$ roslaunch turtlebot3_bringup turtlebot3_robot.launch

 

\#remotePC

$ export TURTLEBOT3_MODEL=waffle_pi

$ roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping

 

\#remotePC

$ export TURTLEBOT3_MODEL=waffle_pi

$ roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch

로 이동하면서 맵핑을 한다.

 

### 맵저장

rosrun map_server map_saver -f ~/map

 

 

 ### 네비게이션

\#remotePC

$ rescore

 

\#turtlebot

$ roslaunch turtlebot3_bringup turtlebot3_robot.launch

 

\#remotePC

$ export TURTLEBOT3_MODEL=waffle_pi

$ roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml