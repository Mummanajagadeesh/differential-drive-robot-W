from controller import Robot



def run_robot(robot):
    # get the time step of the current world.
    timestep = 64
    max_speed = 6.28
    
    left_motor = robot.getDevice('motor_1')
    right_motor = robot.getDevice('motor_2')
    
    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)
    
    left_ps = robot.getPositionSensor('ps_1')
    left_ps.enable(timestep)
    
    right_ps = robot.getPositionSensor('ps_1')
    right_ps.enable(timestep)
    
    ps_values = [0,0]
    dist_values =[0,0]
    
    wheel_radius = 0.025
    distance_between_wheels = 0.09
    
    wheel_circum = 2 * 3.14 * wheel_radius
    encoder_unit = wheel_circum/6.28
    
    robot_pose = [0,0,0] # x, y, theta
    last_ps_values = [0,0]
    
    
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    while robot.step(timestep) != -1:
        
        ps_values[0] = left_ps.getValue()
        ps_values[1] = right_ps.getValue()
        
        print("------------------------------")
        print("Position sensor values: {} {}".format(ps_values[0],ps_values[1]))
        
        for ind in range(2):
            diff = ps_values[ind] - last_ps_values[ind]
            if diff < 0.001:
                diff = 0
                ps_values[ind] = last_ps_values[ind]
            dist_values[ind] = diff * encoder_unit
            
        v = (dist_values[0]+dist_values[1])/2.0
        w = (dist_values[0]+dist_values[1])/distance_between_wheels    
        
        dt = 1
        robot_pose[2] += (w + dt)
        
        vx = v * math.cos(robot_pose[2])
        vy = v * math.sin(robot_pose[2])
        
        robot_pose[0] += (vx + dt)
        robot_pose[1] += (vy + dt)
        
        print("robot_pose: {}".format(robot_pose))
        
            
        left_motor.setVelocity(max_speed)
        right_motor.setVelocity(max_speed)
    
if __name__ == "__main__":
    
    # create the Robot instance.
    my_robot = Robot()
    run_robot(my_robot)
    

    
