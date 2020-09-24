from thewhitetello import TheWhiteTello
import threading

drone = TheWhiteTello()             # create instance
drone.connect()                     # connect 
print('\n\n\t\tPYTHON UAV CONTROLLER')
drone.get_battery()                 # check drone power level
drone.streamon()                    # enable streaming of video

# ------ START VIDEO STREAM IN EXTERNAL WINDOW ------]
p1 = threading.Thread(target=drone.recieve)  
p2 = threading.Thread(target=drone.display)
p1.start()
p2.start()
# ---------------------------------------------------]

drone.takeoff()
time.sleep(5)
drone.forward(20)                   # fly forward 20 cms
drone.clockwise(90)                 # turn clockwise 90 degrees
drone.up(20)                        # fly up 20 cms
drone.land()                        # land
drone.stop()                        # disconnect


