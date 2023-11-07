from nnabla.utils import nnp_graph
import numpy as np
from socket import *
import socket as sc
from numpy.fft import fft
##################
# 受信側プログラム#
##################

SrcIP = "0.0.0.0"
SrcPort = 12345
SrcAddr = (SrcIP, SrcPort)
BUFSIZE = 2000
udpServSock = socket(AF_INET, SOCK_DGRAM)
udpServSock.bind(SrcAddr)

# 送信用ソケット
# 接続するSpresenseのIPアドレスとポート番号
spresense_ip = ''  # SpresenseのIPアドレス
spresense_port = 54321  # Spresenseのポート番号
message = 'Success to receive message'
cli_addr = (spresense_ip, spresense_port)  # IPアドレスとポート番号のタプル

host = '0.0.0.0'
port = 11111  # EC2インスタンスポート

locaddr = (host, port)

# ①ソケットを作成
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

            # 推論結果が1または2の場合、gyr_xの周波数を計算
            if output_class in [1, 2]:
                gyr_x_data = input_data[:, 3]  # gyr_xデータを取得
                fft_values = fft(gyr_x_data)
                # サンプリング周期6ms、サンプリング周波数を計算
                sampling_frequency = 1 / (6e-3)  # 6ms -> 0.006秒
                freqs = np.fft.fftfreq(len(gyr_x_data), d=1/sampling_frequency)
                peak_freq = freqs[np.argmax(np.abs(fft_values))]
                send_data = f"{output_class},{peak_freq}".encode('utf-8')
            else:
                send_data = f"{output_class},0".encode('utf-8')  # 周波数は送信しない

            sock.sendto(send_data, cli_addr)
udp_send_sock.close()
