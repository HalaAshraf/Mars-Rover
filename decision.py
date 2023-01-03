
import numpy as np


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
        # Check for Rover.mode status
        if Rover.mode == 'forward': 
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:  
                Rover.Rover_direction_after_stuck=0
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.obstacle_at_the_end_of_pixel or Rover.left_side_obstacle or Rover.right_side_obstacle or Rover.two_sides_obstacles:
                    Rover.throttle = 0
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode='stop'
                else:  
                    if Rover.vel < Rover.max_vel:
                        # Set throttle value to throttle setting
                        Rover.throttle = Rover.throttle_set
                    else: # Else coastdddddddddddddddddddddddddd
                        Rover.throttle = 0
                Rover.brake = 0
               
                if (Rover.count_avarage_steer>10000) and (Rover.Rover_last_turn=='left') and (Rover.Rover_avarage_left_turn<30 ):
                    Rover.throttle = 0
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.count_avarage_steer=0
                    Rover.mode="right_forward"
                elif (Rover.count_avarage_steer>10000 ) and (Rover.Rover_last_turn=='right') and (Rover.Rover_avarage_right_turn<30):
                    Rover.throttle = 0
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.count_avarage_steer=0
                    Rover.mode="left_forward"
                else:    
                    Rover.Rover_avarage_left_turn=0
                    Rover.Rover_avarage_right_turn=0
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.count_avarage_steer+=1
                    if(Rover.steer<0):
                        Rover.Rover_last_turn='right' 
                    else:
                        Rover.Rover_last_turn='left' 
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward or Rover.obstacle_at_the_end_of_pixel or Rover.left_side_obstacle or Rover.right_side_obstacle or Rover.two_sides_obstacles:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    #Rover.steer = -15 
                    for a in range(1,int((Rover.yaw+360*2)/15)):                        
                        Rover.steer=15
                 # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'

        elif Rover.mode=='left':
            if Rover.vel > 0.2:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = Rover.brake_set
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = 0 # Could be
            else: # Else coast             
                    Rover.throttle =Rover.throttle_set
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = 15 
                    if(Rover.Rover_direction_after_stuck<70):
                        Rover.Rover_direction_after_stuck+=1
                    else:    
                        Rover.Rover_direction_after_stuck=0
                        Rover.mode ='forward'     
                        
        elif Rover.mode=='left_forward':
            if Rover.vel > 0.2:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = Rover.brake_set
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = 0 # Could be
            else: # Else coast             
                    Rover.throttle =Rover.throttle_set
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = 15  
                    if(Rover.Rover_avarage_left_turn <120):
                        Rover.Rover_avarage_left_turn+=1
                    else:
                        Rover.Rover_avarage_left_turn=0
                        Rover.mode ='forward'
        
        elif Rover.mode=='right_forward':
            if Rover.vel > 0.2:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = Rover.brake_set
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = 0 # Could be
            else: # Else coast             
                    Rover.throttle =Rover.throttle_set
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -15 
                    if(Rover.Rover_avarage_right_turn <120):
                        Rover.Rover_avarage_right_turn+=1
                    else:
                        Rover.Rover_avarage_right_turn=0
                        Rover.mode ='forward'
 
    
    # *************************** Added by Hala*****************************
        elif Rover.mode == 'rock':
            if Rover.near_sample ==0:
                dist_rock = min(Rover.nav_dists)
                #check the distance if small then the rover need to rotate, else go to the rock
                if (dist_rock<10):
                    if(Rover.vel>0.2):
                        #stop the rover
                        Rover.throttle =0
                        Rover.brake = Rover.brake_set
                        Rover.steer = 0  
                    else:
                        # the rover is stopped, but the rock not in front of the rover
                        # let the rover steer toward the rock
                        Rover.throttle =0
                        Rover.brake = 0
                        Rover.steer = np.clip(np.mean(Rover.rock_angles * 180/np.pi), -15, 15) 
                        
                else:
                    #move rover to the direciton of the rock by taking the avarage of rock_angle
                    Rover.throttle =Rover.throttle_set
                    Rover.brake = 0
                    Rover.steer = np.clip(np.mean(Rover.rock_angles * 180/np.pi), -15, 15)
                    
            else:
                #then the rover is near sample, stop the rover and go to the forward mode
                Rover.throttle =0
                Rover.brake = Rover.brake_set
                Rover.steer = 0 
                
        
#*******************************************************************************************
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake=0  
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover

