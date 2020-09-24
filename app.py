from thewhitetello import TheWhiteTello
import time, queue
import threading
import cv2

q = queue.Queue()
drone = TheWhiteTello()
print('\n\n\t\tPYTHON \033[1;31mUAV\033[0m CONTROLLER')
p1 = threading.Thread(target=drone.recieve)
p2 = threading.Thread(target=drone.display)

drone.connect()
drone.get_battery()
drone.streamon()

p1.start()
p2.start()





