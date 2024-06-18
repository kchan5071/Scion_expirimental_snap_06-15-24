from Motor.MotorWrapper import Can_Wrapper
from multiprocessing import Process, Value
import math
import time
import numpy as np

#from MotorWrapper import Can_Wrapper

class MotorInterface:

    def __init__(self, linear_acceleration_x , linear_acceleration_y, linear_acceleration_z, 
                angular_velocity_x, angular_velocity_y, angular_velocity_z, 
                orientation_x, orientation_y, orientation_z, 
                depth,
                offset_x, offset_y):
        self.linear_acceleration_x = linear_acceleration_x
        self.linear_acceleration_y = linear_acceleration_y
        self.linear_acceleration_z = linear_acceleration_z
        self.angular_velocity_x = angular_velocity_x
        self.angular_velocity_y = angular_velocity_y
        self.angular_velocity_z = angular_velocity_z
        self.orientation_x = orientation_x
        self.orientation_y = orientation_y
        self.orientation_z = orientation_z
        self.depth = depth
        self.offset_x = offset_x
        self.offset_y = offset_y 

        self.previous_x_offsets = []

        self.max_iterations = 10000
        self.can = Can_Wrapper()

        #TUNE----------------------resize zed camera input-----------------------------------
        self.x_hard_deadzone = 400
        self.y_hard_deadzone = 400

        self.x_soft_deadzone = 100
        self.y_soft_deadzone = 200

        self.x_turn_speed = 5
        self.y_turn_speed = 5
        self.normalizer_value = 640

        self.depth_stop_value = 1000
        self.speed = 20
        self.turn_down_speed = 10

        self.iteration_since_last_detection = 0


    def follow(self):
            #print(self.offset_x.value)
            # print(self.offset_y.value)        
            # print(self.depth.value)
            
            #NO OBJECT -------------------------------------------------
            if self.offset_x.value == 0:
                self.iteration_since_last_detection += 1
                self.can.stop()
            #HARD DEADZONE----------------------------------------------
            #turn right hard deadzone
            #turn right if to the left of the hard deadzone
            elif(self.offset_x.value < -self.x_hard_deadzone):
                self.can.turn_right(abs(self.offset_x.value / self.normalizer_value * self.x_turn_speed))
                self.iteration_since_last_detection = 0
            #turn left hard deadzone
            #turn left if to the right of the hard deadzone
            elif (self.offset_x.value > self.x_hard_deadzone):
                self.can.turn_left(abs(self.offset_x.value / self.normalizer_value * self.x_turn_speed))
                self.iteration_since_last_detection = 0
            #SOFT DEADZONE----------------------------------------------
            #turn right soft deadzone
            #turn right and move forward if to the left of the soft deadzone
            elif (self.offset_x.value < -self.x_soft_deadzone):
                self.can.turn_right(abs(self.offset_x.value / self.normalizer_value * self.x_turn_speed))
                self.can.move_forward(self.speed)
                self.iteration_since_last_detection = 0
            #turn left soft deadzone
            #turn left and move forward if to the right of the soft deadzone
            elif (self.offset_x.value > self.x_soft_deadzone):
                self.can.turn_left(abs(self.offset_x.value / self.normalizer_value * self.x_turn_speed))
                self.can.move_forward(self.speed)
                self.iteration_since_last_detection = 0
            #CENTERED---------------------------------------------------
            #move forward if inside soft deadzone    
            else: 
                #print("centered")
                self.can.move_forward(self.speed)
                self.iteration_since_last_detection = 0
            #else: print(f"x: {self.offset_x.value} x_deadzone: {self.x_soft_deadzone}")
            #HARD DEADZONE----------------------------------------------
            #turn down hard deadzone
            if (self.offset_y.value < -self.y_hard_deadzone):
                self.can.turn_down(abs(self.offset_y.value / self.normalizer_value * self.y_turn_speed))
            #turn up hard deadzone
            elif (self.offset_y.value > self.y_hard_deadzone):
                self.can.turn_up(abs(self.offset_y.value / self.normalizer_value * self.y_turn_speed))
            #SOFT DEADZONE----------------------------------------------
            #turn down soft deadzone
            elif (self.offset_y.value < -self.y_soft_deadzone):
                self.can.turn_down(abs(self.offset_y.value / self.normalizer_value * self.y_turn_speed))
                self.can.move_forward(self.speed)
            
            #turn up soft deadzone
            elif (self.offset_y.value > self.y_soft_deadzone):
                self.can.turn_up(abs(self.offset_y.value / self.normalizer_value * self.y_turn_speed))
                self.can.move_forward(self.speed)    
            
            #STOP DEPTH-----------------------------------------------
            #stop if depth is less than stop value
            if (self.depth.value < self.depth_stop_value and self.depth.value != 0.0):
                print("stop")
                self.can.move_backward(5)
                self.can.send_command()
                time.sleep(.2)
                self.can.send_command()
                self.can.stop()
            
            #MOVE FORWARD---------------------------------------------
            self.can.send_command()
            time.sleep(.05)

    def move_down(self, down_time):
        self.can.move_down(20)
        self.can.send_command()
        time.sleep(down_time)

    def move_forward(self, forward_time):
        self.can.move_forward(20)
        self.can.move_down(.3)
        self.can.send_command()
        time.sleep(forward_time)

    def look_for_detection(self):
        #turn left if nothing in front
        if self.offset_x.value == 0:
        #if self.offset_x.value == 0:
            self.can.turn_right(10) #lower turn speed?
            self.can.send_command()
            time.sleep(.3)
            self.can.stop()
            self.can.send_command()
            time.sleep(1)
        
        if self.offset_x.value != 0:
            self.iteration_since_last_detection = 0
        else:
            self.iteration_since_last_detection += 1

        

    #def look_for_detection(self):
            #turn left if nothing in front
            #if self.offset_x.value == 0:
                #self.can.turn_left(self.x_turn_speed)
                #self.can.send_command()
                #time.sleep(.5)
                #self.can.stop()
                #self.can.send_command()

            #turn right if noting in front    
            #if self.offset_x.value == 0:
                #self.can.turn_right(self.x_turn_speed)
                #self.can.send_command()
                #time.sleep(.5)
                #self.can.stop()
                #self.can.send_command()
            #if self.offset_x.value == 0:
                #return False

    def run_loop(self):
        time.sleep(20)

        # self.move_down(2)
        # self.can.stop()
        # self.can.send_command()



        # for i in range(self.max_iterations):
        #     if (self.iteration_since_last_detection < 20):
        #         print(self.iteration_since_last_detection)
        #         self.follow()
        #     else:
        #         self.look_for_detection()
        #         print(self.iteration_since_last_detection)


        # #print("down")

        #self.move_down(2)
        #self.can.stop()
        #self.can.send_command()

        #print("forward")

        #self.move_forward(5)
        #self.can.stop()
        #self.can.send_command()

        


if __name__ == '__main__':
    ang_vel_x = Value('d', 0.0)
    ang_vel_y = Value('d', 0.0)
    ang_vel_z = Value('d', 0.0)
    lin_acc_x = Value('d', 0.0)
    lin_acc_y = Value('d', 0.0)
    lin_acc_z = Value('d', 0.0)
    orientation_x = Value('d', 0.0)
    orientation_y = Value('d', 0.0)
    orientation_z = Value('d', 0.0)
    depth = Value('d', 0.0)
    offset_x = Value('d', 0.0)
    offset_y = Value('d', 0.0)

    interface = MotorInterface(linear_acceleration_x=lin_acc_x, linear_acceleration_y=lin_acc_y, linear_acceleration_z=lin_acc_z,        #linear accel x y z
                    angular_velocity_x=ang_vel_x, angular_velocity_y=ang_vel_y, angular_velocity_z=ang_vel_z,               #angular velocity x y z
                    orientation_x=orientation_x, orientation_y=orientation_y, orientation_z=orientation_z,                  #orientation x y z
                    depth=depth,                                                                                            #depth
                    offset_x=offset_x, offset_y=offset_y)  
                
    offset_x.value = 0.0
    depth.value = 100   

    interface.run_loop()
