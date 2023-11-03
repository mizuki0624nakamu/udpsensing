import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from socket import *
import csv  


SrcIP = "0.0.0.0"                          
SrcPort = 12345
SrcAddr = (SrcIP, SrcPort)
BUFSIZE = 2000

# ソケット作成
udpServSock = socket(AF_INET, SOCK_DGRAM)
udpServSock.bind(SrcAddr)

with open('data3.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    
    while True:                                     
        data, addr = udpServSock.recvfrom(BUFSIZE)
        data_str = data.decode('utf-8')
        currentMillis, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z = map(float, data_str.split(','))
        csvwriter.writerow([currentMillis, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z])

        print(f"Received message from {addr}:")
        print(f"CurrentMillis: {currentMillis}")
        print(f"Accel - X: {acc_x}, Y: {acc_y}, Z: {acc_z}")
        print(f"Gyro  - X: {gyr_x}, Y: {gyr_y}, Z: {gyr_z}")
