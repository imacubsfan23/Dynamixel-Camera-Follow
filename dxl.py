#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# Author: Ryu Woon Jung (Leon)

#
# *********     Read and Write Example Modified to list wrapper functions      *********
#
#
# Available Dynamixel model on this example : All models using Protocol 2.0
# This example is designed for using a Dynamixel PRO 54-200, and an USB2DYNAMIXEL.
# Confirmed works with XL430-W250-T Model and U2D2
# To use another Dynamixel model, such as X series, see their details in E-Manual(emanual.robotis.com) and edit below variables yourself.
# Be sure that Dynamixel PRO properties are already set as %% ID : 1 / Baudnum : 1 (Baudrate : 57600)
#

import os
from dynamixel_sdk import *                     # Uses Local Dynamixel SDK library for python.
                                                #If installed into site_packages, delete dynamixel_sdk folder

# Control table address
ADDR_TORQUE_ENABLE      = 64                    # Control table address is different in Dynamixel model
ADDR_GOAL_POSITION      = 116
ADDR_PRESENT_POSITION   = 132

# Data Byte Length
LEN_GOAL_POSITION       = 4
LEN_PRESENT_POSITION    = 4

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
BAUDRATE                    = 1000000           # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
    print("Enter your com port as an int")
    DEVICENAME = 'COM{}'.format(input())
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Initialize GroupBulkWrite instance
groupBulkWrite = GroupBulkWrite(portHandler, packetHandler)

# Initialize GroupBulkRead instace for Present Position
groupBulkRead = GroupBulkRead(portHandler, packetHandler)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:

    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

#Enable Torque
def enable_torque(dxl_id):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, 1)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel id {} has been successfully connected".format(dxl_id))

#Disable Torque
def disable_torque(dxl_id):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, 0)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

def add_param_read(dxl_id, param, param_byte_size = 4):#param_byte_size would be different for a function such as LED on where it is either 0 or 1
    if not groupBulkRead.isAvailable(dxl_id, param, param_byte_size):
        dxl_addparam_result = groupBulkRead.addParam(dxl_id, param, param_byte_size)
        if dxl_addparam_result != True:
            print("[ID:%03d] groupBulkRead addparam failed" % dxl_id)
            quit()

def add_param_write(dxl_id, data, param, param_byte_size = 4):#param_byte_size would be different for a function such as LED on where it is either 0 or 1
    data_byte_array = [ DXL_LOBYTE(DXL_LOWORD(data)),
                        DXL_HIBYTE(DXL_LOWORD(data)),
                        DXL_LOBYTE(DXL_HIWORD(data)),
                        DXL_HIBYTE(DXL_HIWORD(data))]
    write = groupBulkWrite.addParam(dxl_id, param, param_byte_size, data_byte_array)
    if write != True:
        groupBulkWrite.changeParam(dxl_id, param, param_byte_size, data_byte_array)

def group_read():
    dxl_comm_result = groupBulkRead.txRxPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

def get_goal_position(dxl_id):
    dxl_goal_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, dxl_id, ADDR_GOAL_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        return dxl_goal_position

def get_present_position(dxl_id):
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, dxl_id, ADDR_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        return dxl_present_position

def group_write():
    dxl_comm_result = groupBulkWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

def group_write_positions(all_servos=[]):
    for servo in all_servos:
        if(abs(get_goal_position(servo.id) - get_present_position(servo.id)) > 5):
            group_write()
            group_write_positions()

def group_write_positions_from_id(servo_ids=[]):
    for id in servo_ids:
        if(abs(get_goal_position(id) - get_present_position(id)) > 50):
            group_write()
            group_write_positions_from_id()

def clear_params():
    groupBulkRead.clearParam()
    groupBulkWrite.clearParam()

#Set Absolute Position of Servo
def set_position(dxl_id, dxl_goal_position):
    add_param_write(dxl_id, dxl_goal_position, ADDR_GOAL_POSITION)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_GOAL_POSITION, dxl_goal_position)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

#Set Relative Position of Servo
def rotate_servo(dxl_id, dist=0):#positive dist = clockwise
    set_position(dxl_id, get_present_position(dxl_id)-dist)
    #print("{}: {}".format(dxl_id, get_present_position(dxl_id)))

#Start Specific XL430 Turret Code
def tilt_horizontal(dist=0):
    rotate_servo(1, dist)

def tilt_vertical(dist=0):
    rotate_servo(2, dist)

def set_coordinates(x,y,horizontal_servo=1, vertical_servo=2):
    #print("{}, {}".format(get_present_position(horizontal_servo)+x, get_present_position(vertical_servo)+y))
    set_position(horizontal_servo, get_present_position(horizontal_servo) - x)
    set_position(vertical_servo, get_present_position(vertical_servo) + y)
    time.sleep(0.02)
    group_write_positions_from_id([horizontal_servo, vertical_servo])

#Set Absolute Position of Servo to its home
def set_home(dxl_id, servo_type='XL430'):
    if(servo_type == 'XL430'):
        set_position(dxl_id, 2000);#true home for XL430-W250-T

#close port
def close_port():
    portHandler.closePort()
