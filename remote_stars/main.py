import numpy as np
import matplotlib.pyplot as plt
import socket
from skimage.measure import label
from scipy import ndimage

host = "84.237.21.36"
port = 5152

def recvall(sock, nbytes):
    data = bytearray()
    while len(data) < nbytes:
        packet = sock.recv(nbytes - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

plt.ion()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    sock.send(b"124ras1")
    sock.recv(10)
    
    beat = b"nope"
    while beat != b"yep":
        sock.send(b"get")
        bts = recvall(sock, 40002)

        im = np.frombuffer(bts[2:40002], dtype="uint8")
        im = im.reshape(bts[0], bts[1])

        binary = im > 150
        labeled = label(binary)

        centroids = ndimage.center_of_mass(binary, labeled, range(1, labeled.max() + 1))
        print(centroids)

        pos1 = np.array(centroids[0])
        pos2 = np.array(centroids[1])

        distance = ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
        print(round(distance, 1))

        sock.send(f"{distance:.1f}".encode())
        print(sock.recv(100))
        print("---")

        plt.clf()
        plt.subplot(131)
        plt.imshow(im)
        plt.subplot(132)
        plt.imshow(binary)
        plt.subplot(133)
        plt.imshow(labeled)
        plt.pause(2)

        sock.send(b"beat")
        beat = sock.recv(10)