from thewhitetello import TheWhiteTello
import time

drone = TheWhiteTello()

print('\n\n\t\tPYTHON \033[1;31mUAV\033[0m CONTROLLER')

drone.connect()              # Puts the tello in the command mode
drone.streamon()             # Enables video streaming from drone

drone.startvideo()           # Starts the video feed from the drone

drone.get_battery()          # Get battery level (0 - 100%)
drone.takeoff()              # take off
drone.forward(20)            # fly forward 20 cms
drone.clockwise(30)          # turn left 30 degrees
drone.up(10)                 # fly up 10 cms
drone.flip_left()            # cartwheel to the left
drone.land()                 # land

drone.stop()                 # disconnect drone
