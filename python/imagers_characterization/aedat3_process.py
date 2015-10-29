# ############################################################
# python class that deals with cAER aedat3 file format
# author  Federico Corradi - federico.corradi@inilabs.com
# ############################################################
from __future__ import division
import os
import struct
import threading
import sys
import numpy as np

class aedat3_process:
    def __init__(self):
        self.V3 = "aedat3"
        self.V2 = "aedat" # current 32bit file format
        self.V1 = "dat" # old format
        self.header_length = 28
        self.EVT_DVS = 0 # DVS event type
        self.EVT_APS = 2 # APS event
        self.file = []
        self.x_addr = []
        self.y_addr = []
        self.timestamp = []

    def load_file(self, filename):
        '''
            load aedat file return
            ----
                frames  - 2d vector - frames over time (y,x,dim) - frames are flipped vertically
                xaddr   - 1D vector
                yaddr   - 1D vector
                ts      - 1D vector - timestamps
                pol     - 1D vector - polarity 
        '''
        x_addr_tot = []
        y_addr_tot = []
        pol_tot = []
        ts_tot = []
        frame_tot = []
        test_c = 0
        with open(filename, "rb") as f:       
            while True:
                data = f.read(self.header_length)
                if not data:
                    break
                # read header
                eventtype = struct.unpack('H',data[0:2])[0]
                eventsource = struct.unpack('H',data[2:4])[0]
                eventsize = struct.unpack('I',data[4:8])[0]
                eventoffset = struct.unpack('I',data[8:12])[0]
                eventtsoverflow = struct.unpack('I',data[12:16])[0]
                eventcapacity = struct.unpack('I',data[16:20])[0]
                eventnumber = struct.unpack('I',data[20:24])[0]
                eventvalid = struct.unpack('I',data[24:28])[0]
                next_read =  eventcapacity*eventsize # we now read the full packet
                data = f.read(next_read) #we read exactly the N bytes 
                # change behavior depending on event type      
                if(eventtype == 1):  #something is wrong as we set in the cAER to send only polarity events
                    counter = 0 #eventnumber[0]
                    while(data[counter:counter+8]):  #loop over all event packets
                        aer_data = struct.unpack('I',data[counter:counter+4])[0]
                        timestamp = struct.unpack('I',data[counter+4:counter+8])[0]
                        x_addr = (aer_data >> 17) & 0x00007FFF
                        y_addr = (aer_data >> 2) & 0x00007FFF
                        x_addr_tot.append(x_addr)
                        y_addr_tot.append(y_addr)
                        pol = (aer_data >> 1) & 0x00000001
                        pol_tot.append(pol)
                        ts_tot.append(timestamp)
                        #print (timestamp[0], x_addr, y_addr, pol)
                        counter = counter + 8
                elif(eventtype == 2): #aps event
                    counter = 0 #eventnumber[0]
                    while(data[counter:counter+eventsize]):  #loop over all event packets
                        info = struct.unpack('I',data[counter:counter+4])[0]
                        ts_start_frame = struct.unpack('I',data[counter+4:counter+8])[0]
                        ts_end_frame = struct.unpack('I',data[counter+8:counter+12])[0]
                        ts_start_exposure = struct.unpack('I',data[counter+12:counter+16])[0]
                        ts_end_exposure = struct.unpack('I',data[counter+16:counter+20])[0]
                        length_x = struct.unpack('I',data[counter+20:counter+24])[0]        
                        length_y = struct.unpack('I',data[counter+24:counter+28])[0]
                        pos_x = struct.unpack('I',data[counter+28:counter+32])[0]  
                        pos_y = struct.unpack('I',data[counter+32:counter+36])[0]
                        bin_frame = data[counter+36:counter+36+(length_x*length_y*2)]
                        frame = struct.unpack(str(length_x*length_y)+'H',bin_frame)
                        frame = np.reshape(frame,[length_y, length_x])
                        frame_tot.append(frame)
                        counter = counter + eventsize
                elif(eventtype == 3): #imu event
                    continue
                else:
                    print("packet data type not understood")
                    raise Exception
                test_c+=1
            return frame_tot, x_addr_tot, y_addr_tot, pol_tot, ts_tot

    
if __name__ == "__main__":
    #analyse ptc

    import matplotlib
    from pylab import *

    aedat = aedat3_process()

    #directory = 'measurements/ptc_dark_29_10_15-11_53_36/'
    #files_in_dir = os.listdir(directory)
    #files_in_dir.sort()  
    #this_file = 0
    #exp = float(files_in_dir[this_file].strip(".aedat").strip("ptc_")) # in us
    #[frame, xaddr, yaddr, pol, ts] = aedat.load_file(directory+files_in_dir[this_file])
    #frame = np.right_shift(frame,6)
    #n_frames, ydim, xdim = np.shape(frame)        
    #u_dark = (1.0/(n_frames*ydim*xdim)) * np.sum(np.sum(frame,0))   # mean dark value

    u_dark = 0.1

    ## PTC measurements
    illuminance = 10
    pixel_area = (18e-6*18e-6)
    exposure_time_scale = 10e-6
    planck_cost = 6.62607004e-34
    speed_of_light = 299792458
    wavelenght_red = 650e-9
    sensor_area = 180*240*pixel_area
    luminous_flux = 0.09290304 * illuminance * (sensor_area * 10.764)
    scale_factor_ = 0.107  # RED light 650 nm
                           # ******** 1988 C.I.E. Photopic Luminous Efficiency Function ********
                           # http://donklipstein.com/photopic.html
    


    directory = 'measurements/ptc_29_10_15-13_23_40/'
    files_in_dir = os.listdir(directory)
    files_in_dir.sort()
    u_y_tot = []
    exposures = []
    for this_file in range(len(files_in_dir)):
        exp = float(files_in_dir[this_file].strip(".aedat").strip("ptc_")) # in us
        [frame, xaddr, yaddr, pol, ts] = aedat.load_file(directory+files_in_dir[this_file])
        #rescale frame to their values
        frame = np.right_shift(frame,6)
        n_frames, ydim, xdim = np.shape(frame)        
        u_y = (1.0/(n_frames*ydim*xdim)) * np.sum(np.sum(frame,0))  # 
        u_y_tot.append(u_y)
        exposures.append(exp)

    u_y_tot = np.array(u_y_tot)
    exposures = np.array(exposures)
    u_photon = ((scale_factor_*luminous_flux)*sensor_area*(exposures*exposure_time_scale))/((planck_cost*speed_of_light)/wavelenght_red) 
    u_photon_pixel = u_photon/(xdim*ydim)

    # sensitivity plot 
    title("Sensitivity APS")
    plot( u_photon_pixel, u_y_tot-u_dark, 'o--' )  
    xlabel('irradiation photons/pixel') 
    ylabel('gray value - dark value <u_y> - <u_d>')    



 

