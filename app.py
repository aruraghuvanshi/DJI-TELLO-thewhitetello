from thewhitetello import TheWhiteTello
import time

drone = TheWhiteTello()

print('\n\n\t\tPYTHON \033[1;31mUAV\033[0m CONTROLLER')
drone.connect()
drone.streamon()
drone.get_battery()          # Get battery level (0 - 100%)
drone.takeoff()              # take off
drone.forward(20)            # fly forward 20 cms
drone.clockwise(30)          # turn left 30 degrees
drone.up(10)                 # fly up 10 cms
drone.land()                 # land

drone.stop()                 # disconnect drone



