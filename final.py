from nnabla.utils import nnp_graph
import numpy as np
from socket import *
import socket as sc


# 受信側
SrcIP = "0.0.0.0"
SrcPort = 12345
SrcAddr = (SrcIP, SrcPort)
BUFSIZE = 2000
udpServSock = socket(AF_INET, SOCK_DGRAM)
udpServSock.bind(SrcAddr)

# 送信用
spresense_ip = ''  # SpresenseのIPアドレスい
spresense_port = 54321  # Spresenseのポート番号に置き換えてください
# message = 'Success to receive message'
cli_addr = (spresense_ip, spresense_port)  

host = '0.0.0.0'
port = 11111 
locaddr = (host, port)
sock = sc.socket(sc.AF_INET, type=sc.SOCK_DGRAM)
sock.bind(locaddr)

nnp = nnp_graph.NnpLoader("result_train_best.nnp")
graph = nnp.get_network("MainRuntime", batch_size=1)

x = list(graph.inputs.values())[0]
y = list(graph.outputs.values())[0]

data_accumulator = []
DATA_LENGTH = 340
INFERENCE_INTERVAL = 3
counter = 0

while True:                                     
    data, addr = udpServSock.recvfrom(BUFSIZE)
    # data, addr = sock.recvfrom(BUFSIZE)
    data_str = data.decode('utf-8')
    currentMillis, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z = map(float, data_str.split(','))

    data_accumulator.append([acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z])

    if len(data_accumulator) > DATA_LENGTH:
        data_accumulator.pop(0)

    if len(data_accumulator) == DATA_LENGTH:
        counter += 1
        input_data = np.array(data_accumulator)

        if counter % INFERENCE_INTERVAL == 0:
            x.d = input_data.reshape(1, DATA_LENGTH, 6)
            y.forward()

            output_class = np.argmax(y.d, axis=1)[0]
            print(f"Detected action: {output_class}")
            send_data = f"{output_class},0.3".encode('utf-8')
            sock.sendto(send_data, cli_addr)
sock.close()