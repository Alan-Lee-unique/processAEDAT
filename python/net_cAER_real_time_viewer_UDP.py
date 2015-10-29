#!/usr/bin/env python

######################################
# REAL TIME EVENT DISPLAY FROM cAER
# ONLY POLARITY make sure you change
# PARAMETERS according to your setup
# author federico.corradi@inilabs.com
######################################

import socket
import struct
import sys
import numpy as np
import time
import matplotlib
matplotlib.use('GTKAgg')
from matplotlib import pyplot as plt

# PARAMETERS
host = "127.0.0.1"
port = 8888
xdim= 240
ydim= 180

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

def matrix_active(x,y, pol):
    matrix = np.zeros([ydim,xdim])
    if(len(x)==len(y)):
        for i in range(len(x)):
            matrix[y[i],x[i]] = pol[i]#matrix[x[i],y[i]] + pol[i]
    else:
        print("error x,y missmatch")
    return matrix

def sub2ind(array_shape, rows, cols):
    ind = rows*array_shape[1] + cols
    ind[ind < 0] = -1
    ind[ind >= array_shape[0]*array_shape[1]] = -1
    return ind

def ind2sub(array_shape, ind):
    ind[ind < 0] = -1
    ind[ind >= array_shape[0]*array_shape[1]] = -1
    rows = (ind.astype('int') / array_shape[1])
    cols = ind % array_shape[1]
    return (rows, cols)

def read_events():
    """ A simple function that read events from cAER tcp"""

    data, addr = sock.recvfrom(64 * 1024) #we read the full packet, which is one UDP message. Use a big size to ensure we get it all.

    #read header
    eventtype = struct.unpack('H',data[0:2])
    if(eventtype[0] == 1):  #something is wrong as we set in the cAER to send only polarity events
        eventsource = struct.unpack('H',data[2:4])
        eventsize = struct.unpack('I',data[4:8])
        eventoffset = struct.unpack('I',data[8:12])
        eventtsoverflow = struct.unpack('I',data[12:16])
        eventcapacity = struct.unpack('I',data[16:20])
        eventnumber = struct.unpack('I',data[20:24])
        eventvalid = struct.unpack('I',data[24:28])
        counter = 28 #eventnumber[0]
        x_addr_tot = []
        y_addr_tot = []
        pol_tot = []
        while(data[counter:counter+4]):  #loop over all event packets
            aer_data = struct.unpack('I',data[counter:counter+4])
            timestamp = struct.unpack('I',data[counter+4:counter+4+4])
            x_addr = (aer_data[0] >> 17) & 0x00007FFF
            y_addr = (aer_data[0] >> 2) & 0x00007FFF
            x_addr_tot.append(x_addr)
            y_addr_tot.append(y_addr)
            pol = (aer_data[0] >> 1) & 0x00000001
            pol_tot.append(pol)
            #print (timestamp[0], x_addr, y_addr, pol)
            counter = counter + 16

    return x_addr_tot, y_addr_tot, pol_tot

def run(doblit=True):
    """
    Display the simulation using matplotlib, optionally using blit for speed
    """

    fig, ax = plt.subplots(1, 1)
    ax.set_aspect('equal')
    ax.set_xlim(0, xdim)
    ax.set_ylim(0, ydim)
    ax.hold(True)
    x,y,p = read_events()
    this_m = matrix_active(x,y,p)

    plt.show(False)
    plt.draw()

    if doblit:
        # cache the background
        background = fig.canvas.copy_from_bbox(ax.bbox)

    points = ax.imshow(this_m, interpolation='nearest', cmap='gray')
    tic = time.time()

    while(1):
        # update the xy data
        x,y,p = read_events()
        this_m = matrix_active(x,y,p)
        points.set_data(this_m)

        if doblit:
            # restore background
            fig.canvas.restore_region(background)

            # redraw just the points
            ax.draw_artist(points)

            # fill in the axes rectangle
            fig.canvas.blit(ax.bbox)
        else:
            # redraw everything
            fig.canvas.draw()

    plt.close(fig)
    print "Blit = %s, average FPS: %.2f" % (
        str(doblit), niter / (time.time() - tic))

if __name__ == '__main__':
    run(doblit=True)