from multiprocessing import Process, Value
from vision.vision.vision_main import VideoRunner
from shared_memory_reader import SharedMemoryReader
from sensors.dvl_interface import DVL_Interface
from Motor.MotorInterface import MotorInterface

'''
    discord: @kialli
    github: @kchan5071
    
    creates shared memory and processes to communicate between vision and control
    
    vision: writes to shared memory
    currently just printing process data, later to use with PID control
    
    could use arrays, too lazy
    
'''


def main():
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
    
    dvl_x = Value('d', 0.0)
    dvl_y = Value('d', 0.0)    
    dvl_z = Value('d', 0.0)    
    dvl_yaw = Value('d', 0.0)    
    dvl_pitch = Value('d', 0.0)    
    dvl_roll = Value('d', 0.0) 
    
    dvl = DVL_Interface(x=dvl_x, y=dvl_y, z=dvl_z, yaw=dvl_yaw, pitch=dvl_pitch, roll=dvl_roll)
    
    vis = VideoRunner(linear_acceleration_x=lin_acc_x, linear_acceleration_y=lin_acc_y, linear_acceleration_z=lin_acc_z,        #linear accel x y z
                        angular_velocity_x=ang_vel_x, angular_velocity_y=ang_vel_y, angular_velocity_z=ang_vel_z,               #angular velocity x y z
                        orientation_x=orientation_x, orientation_y=orientation_y, orientation_z=orientation_z,                  #orientation x y z
                        depth=depth,                                                                                            #depth
                        offset_x=offset_x, offset_y=offset_y)                                                                   #offset x y

    interface = MotorInterface(linear_acceleration_x=lin_acc_x, linear_acceleration_y=lin_acc_y, linear_acceleration_z=lin_acc_z,        #linear accel x y z
                        angular_velocity_x=ang_vel_x, angular_velocity_y=ang_vel_y, angular_velocity_z=ang_vel_z,               #angular velocity x y z
                        orientation_x=orientation_x, orientation_y=orientation_y, orientation_z=orientation_z,                  #orientation x y z
                        depth=depth,                                                                                            #depth
                        offset_x=offset_x, offset_y=offset_y)       
    
    shm = SharedMemoryReader(linear_acceleration_x=lin_acc_x, linear_acceleration_y=lin_acc_y, linear_acceleration_z=lin_acc_z, #linear accel x y z
                        angular_velocity_x=ang_vel_x, angular_velocity_y=ang_vel_y, angular_velocity_z=ang_vel_z,               #angular velocity x y z
                        orientation_x=orientation_x, orientation_y=orientation_y, orientation_z=orientation_z,                  #orientation x y z                 
                        depth=depth,                                                                                            #depth
                        offset_x=offset_x, offset_y=offset_y)                                                                 #offset x y
    
    #create processes
    zed_process = Process(target=vis.run_loop)
    #reader_process = Process(target=shm.run_loop)
    dvl_process = Process(target=dvl.run_loop)
    interface = Process(target=interface.run_loop)
    
    # start processes
    zed_process.start()
    #reader_process.start()
    dvl_process.start()
    interface.start()
    
    # join processes
    zed_process.join()
    #reader_process.join()
    dvl_process.join()
    interface.join()
    

if __name__ == '__main__':
    main()
