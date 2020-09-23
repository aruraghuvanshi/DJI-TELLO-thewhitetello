import logging
import cv2
import os
import socket
import subprocess
import threading
import time
import numpy as np


logger = logging.getLogger(__name__)

DEFAULT_DISTANCE = 0.30
DEFAULT_SPEED = 10
DEFAULT_DEGREE = 10

FRAME_X = int(960/3)
FRAME_Y = int(720/3)
FRAME_AREA = FRAME_X * FRAME_Y

FRAME_SIZE = FRAME_AREA * 3
FRAME_CENTER_X = FRAME_X / 2
FRAME_CENTER_Y = FRAME_Y / 2

CMD_FFMPEG = (f'ffmpeg -hwaccel auto -hwaccel_device opencl -i pipe:0 '
              f'-pix_fmt bgr24 -s {FRAME_X}x{FRAME_Y} -f rawvideo pipe:1')


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TheWhiteTello(metaclass=Singleton):
    def __init__(self, host_ip='192.168.10.2', host_port=8889,
                 drone_ip='192.168.10.1', drone_port=8889,
                 is_imperial=False, speed=DEFAULT_SPEED):

        self.host_ip = host_ip
        self.host_port = host_port
        self.drone_ip = drone_ip
        self.drone_port = drone_port
        self.drone_address = (drone_ip, drone_port)
        self.is_imperial = is_imperial
        self.speed = speed
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host_ip, self.host_port))

        self.response = None
        self.stop_event = threading.Event()
        self._response_thread = threading.Thread(target=self.receive_response, args=(self.stop_event, ))
        self._response_thread.start()

        self.patrol_event = None
        self.is_patrol = False
        self._patrol_semaphore = threading.Semaphore(1)
        self._thread_patrol = None

        self.proc = subprocess.Popen(CMD_FFMPEG.split(' '),
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE)
        self.proc_stdin = self.proc.stdin
        self.proc_stdout = self.proc.stdout

        self.video_port = 11111

        # self._receive_video_thread = threading.Thread(
        #     target=self.receive_video,
        #     args=(self.stop_event, self.proc_stdin,
        #           self.host_ip, self.video_port,))
        # self._receive_video_thread.start()

        self.set_speed(self.speed)


    def connect(self):
        return self.send_command('command')


    def receive_response(self, stop_event):
        while not stop_event.is_set():
            try:
                self.response, ip = self.socket.recvfrom(3000)
                logger.info({'action': 'receive_response',
                             'response': self.response})
            except socket.error as ex:
                logger.error({'action': 'receive_response',
                             'ex': ex})
                break


    def __dell__(self):
        self.stop()


    def stop(self):
        self.stop_event.set()
        retry = 0
        while self._response_thread.isAlive():
            time.sleep(0.3)
            if retry > 30:
                break
            retry += 1
        self.socket.close()
        os.kill(self.proc.pid, 9)
        # Windows
        # import signal
        # os.kill(self.proc.pid, signal.CTRL_C_EVENT)


    def send_command(self, command):
        logger.info({'action': 'send_command', 'command': command})
        self.socket.sendto(command.encode('utf-8'), self.drone_address)

        retry = 0
        while self.response is None:
            time.sleep(0.3)
            if retry > 3:
                break
            retry += 1

        if self.response is None:
            response = None
        else:
            response = self.response.decode('utf-8')
        self.response = None
        return response


    def takeoff(self):
        return self.send_command('takeoff')


    def land(self):
        return self.send_command('land')


    def move(self, direction, distance):
        distance = float(distance)
        if self.is_imperial:
            distance = int(round(distance * 30.48))
        else:
            distance = int(round(distance * 100))
        return self.send_command(f'{direction} {distance}')


    def up(self, distance=DEFAULT_DISTANCE):
        return self.move('up', distance)


    def down(self, distance=DEFAULT_DISTANCE):
        return self.move('down', distance)


    def left(self, distance=DEFAULT_DISTANCE):
        return self.move('left', distance)


    def right(self, distance=DEFAULT_DISTANCE):
        return self.move('right', distance)


    def forward(self, distance=DEFAULT_DISTANCE):
        return self.move('forward', distance)


    def back(self, distance=DEFAULT_DISTANCE):
        return self.move('back', distance)


    def set_speed(self, speed):
        return self.send_command(f'speed {speed}')


    def clockwise(self, degree=DEFAULT_DEGREE):
        return self.send_command(f'cw {degree}')


    def counter_clockwise(self, degree=DEFAULT_DEGREE):
        return self.send_command(f'ccw {degree}')


    def flip_front(self):
        return self.send_command('flip f')


    def flip_back(self):
        return self.send_command('flip b')


    def flip_left(self):
        return self.send_command('flip l')


    def flip_right(self):
        return self.send_command('flip r')


    def get_battery(self):
        print(f"BATTERY: {self.send_command('battery?')}%")
        return self.send_command('battery?')


    def streamon(self):
        return self.send_command('streamon')


    def streamoff(self):
        return self.send_command('streamoff')


    def startvideo(self):

        cap = cv2.VideoCapture('udp://@0.0.0.0:11111')
        cap.set(3, 960)  # set Width
        cap.set(4, 720)  # set Height

        while True:
            ret, img = cap.read()
            img = cv2.flip(img, 1)

            cv2.imshow('video', img)

            k = cv2.waitKey(30) & 0xff
            if k == 27:  # press 'ESC' to quit
                break
        cap.release()
        cv2.destroyAllWindows()
