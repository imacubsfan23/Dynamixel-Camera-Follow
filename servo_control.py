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

import dxl

class Servo:
    def __init__(self, id, servo_type, range_min=0, range_max=4000):
        self.id = id
        self.type = servo_type
        self.range_min = range_min
        self.range_max = range_max

all_servos = [Servo(1,'XL430',0,4000),Servo(2,'XL430',1000,3000)]

def start_sequence():
    for servo in all_servos:
        dxl.enable_torque(servo.id)
    dxl.set_home(1, 'XL430')
    dxl.set_home(2, 'XL430')

#needs to close port every time program runs
def end_sequence():
    #if using an arm, needs a set_rest function
    for servo in all_servos:
        dxl.disable_torque(servo.id)
    dxl.close_port()

def main():
    start_sequence()
    end_sequence()

if __name__ == '__main__':
    main()
