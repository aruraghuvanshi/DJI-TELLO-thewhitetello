# thewhitetello
An API to control the DJI Ryze Tello and the DJI Ryze Tello Edu Drone.

Refer to app.py to get an idea on how to use the API.

# How to Use:

Cloan this repository, or download the zip file and extract it on your PC. Then open a new python script in any IDE of your choice.

from thewhitetello import TheWhiteTello

drone = TheWhiteTello()

drone.connect()               # Create an instance

// From here on you can use all the available functions from the TheWhiteTello class and control the drone.

drone.streamon()             # Start Streaming video

drone.startvideo()           # starts the video feed on your PC

drone.get_battery()          # Get battery level (0 - 100%)

drone.takeoff()              # take off

drone.forward(20)            # fly forward 20 cms

drone.clockwise(30)          # turn left 30 degrees

drone.up(10)                 # fly up 10 cms

drone.land()                 # land


drone.stop()                 # disconnect drone
