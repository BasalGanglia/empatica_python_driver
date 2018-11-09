# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:16:30 2017
Small program to read data from the Empatica.

@author: Ilkka
"""

import argparse
import random
import time
import sys
import socket
import signal
import datetime

from pythonosc import osc_message_builder
from pythonosc import udp_client
from struct import *
from my_utils import logWriter

from pynput.keyboard import Key, Listener

EDA_max = 1
def on_press(key):
  print('{0} pressed'.format(
      key))
  if key == Key.space:
    print("Space pressed, resetting EDA normalization.")
    EDA_max = 1  
    
  

def on_release(key):
  print('{0} release'.format(
      key))
  if key == Key.esc:
    # Stop listener
    return False

# Collect events until released
with Listener(
  on_press=on_press,
        on_release=on_release) as listener:
  listener.join()



EMPATICA_ADDRESS = "127.0.0.1"
EMPATICA_PORT = 9999

ADDRESS1 = "192.168.0.130"
#ADDRESS1 = "127.0.0.1"

PORT1 = 8001

#OSCADDRESS = "/empatica"



if __name__ == "__main__":
# Attempt to ctrl-c work in windows.. not very succesful.
  
  # Start logging
  current_time = str(datetime.datetime.now().timestamp())
  current_time = current_time.replace(".", "_")
  logfilename = current_time + ".log"
  
  the_logger = logWriter(logfilename)
  the_logger.log_msg("Testing the logger")
  def signal_handler(signal, frame):
      print( "caught a signal")
      global interrupter
      interrupter = True
     
  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)

# Connect toe the Empatica BLE Server
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
  sock.connect((EMPATICA_ADDRESS, EMPATICA_PORT))
  
 # On windows machine if you dont put that \r\n it does not recognize it..
 
 
 # sock.sendall("device_list\r\n".encode())
 
# Specify the correct device ID:
 
  sock.sendall("device_connect A219F2\r\n".encode())
 # sock.sendall("device_connect 033B64\r\n".encode())
  time.sleep(1)
  
  # Then subscribe to the physiological signals you wish to record:
  
  sock.sendall("device_subscribe gsr ON\r\n".encode())
   
  #time.sleep(1)
  #sock.sendall("device_subscribe bat ON\r\n".encode())
  
  #time.sleep(1)
  #sock.sendall("device_subscribe bvp ON\r\n".encode())
  time.sleep(1)
#  sock.sendall("device_subscribe acc ON\r\n".encode())
  #time.sleep(1)
  #sock.sendall("device_subscribe tmp ON\r\n".encode())
  

  #  Connect to Unity/Max whatever for real-time processing of the data:
#  client1 = udp_client.SimpleUDPClient(ADDRESS1, PORT1)

  
  
  #logWrite = UnicodeWriter(logfilename, dialect=csv.excel, encoding="utf-8")
  #logWrite.writerow("Testing the logger")
  #logfile_handle = open('eggs.csv', 'rb') as c


# open('eggs.csv', 'rb') as csvfile



  
  # we are going to make a veyr quick hack for normalizing the EDA
#  EDA_max = 1
  EDA_counter = 0
  EDA_BASELINE_LENGTH = 20
  
# Read data from Empatica:
  interrupter = False
  while interrupter == False:
      
      data = sock.recv(1024).decode()

      data = data.replace(",", ".")
      sample_lines = data.split("\n")
      print("the full data: <{0}>".format(data))

    #  print("Samples are {0},{1}".format(samples[1], samples[2]))

# If the Empatica server sends more than one line (or more than one sample), parse each sample separately:
      if len(sample_lines) > 1:
          
          # ignore the last "line" as it is actually just the carriage return
          # splitlines above separate \n\r into two lines...
          for i in range(0, len(sample_lines) - 1):
       #       print("line numer {0} is: {1}".format(i, sample_lines[i]))
              samples = sample_lines[i].split(" ")
              
              # Maybe do some more elegant solution later but if elses it is for now
              if samples[0] == "E4_Gsr":
                  msg = osc_message_builder.OscMessageBuilder(address = "/empatica/EDA")
                  EDA_current = float(samples[2])
                  print("Current EDA: {0}".format(EDA_current))
                  # quick baseline on the first n samples...
                  if EDA_counter < EDA_BASELINE_LENGTH:
                    EDA_max += EDA_current
                    EDA_counter += 1
                    continue
                  elif EDA_counter == EDA_BASELINE_LENGTH:
                    EDA_max = 2 * (EDA_max / EDA_BASELINE_LENGTH)
                    EDA_counter += 1
                    continue;
                  else:
                    if EDA_current > EDA_max:
                      EDA_max = EDA_current
                    
                  EDA_normalized = EDA_current / EDA_max
                  the_logger.log_msg("EDA: " + str(EDA_current) + ", " + str(EDA_normalized) + "\n")
                  
                  print("EDA max is {0} and current EDA is {1} and normalized{2}".format(EDA_max, samples[2], EDA_normalized))
                  msg.add_arg(EDA_normalized)
                  msg = msg.build()
                  client1.send(msg)
              
              if samples[0] == "E4_Bvp":
                  msg = osc_message_builder.OscMessageBuilder(address = "/empatica/BVP")
          #        print("sample is as float {0}".format(float(samples[1])))
            
     
                  daitti = datetime.datetime.fromtimestamp(float(samples[1]))
           #       print("timestamp is {0}".format(daitti))
                  teh_time = daitti.time();
                     
                  msg.add_arg(teh_time.__str__());
                  msg.add_arg(samples[2])
                  msg = msg.build()
                  
                  the_logger.log_msg("BVP: " + str(samples[2]));
#                  client1.send(msg)
              if samples[0] == "E4_Temp":                            
                  the_logger.log_msg("Temp: " + str(samples[2]));
#                  client1.send(msg)              
              if samples[0] == "E4_Bat":
                  print("Battery level: {0} ".format(samples[2]))
                 
              if samples[0] == "E4_Ibi":
                  msg = osc_message_builder.OscMessageBuilder(address = "/empatica/IBI")
                  daitti = datetime.datetime.fromtimestamp(float(samples[1]))

                  teh_time = daitti.time();
                 # teh_time.
               #   msg.add_arg((daitti.second + (daitti.microsecond/1000000)))
                  msg.add_arg(teh_time.__str__());
                  msg.add_arg(samples[2])
                  msg = msg.build()
                  the_logger.log_msg("IBI: " + str(samples[2]));
                  #client1.send(msg)
         
              if samples[0] == "E4_Acc":
                  print("The raw data is {0}".format(samples[1]) )
                  msg = osc_message_builder.OscMessageBuilder(address = "/empatica/acc")
                  print("sample is as float {0}".format(float(samples[1])))
            
                  daitti = datetime.datetime.fromtimestamp(float(samples[1]))
                  print("timestamp is {0}".format(daitti))
                  teh_time = daitti.time();
                  print("The acc values are {0}-{1}-{2}".format(samples[2], samples[3], samples[4]))
                 # teh_time.
               #   msg.add_arg((daitti.second + (daitti.microsecond/1000000)))
#                  msg.add_arg(teh_time.__str__());
                  msg.add_arg(abs(int(samples[2])/200))
                  msg.add_arg(abs(int(samples[3])/200))
                  msg.add_arg(abs(int(samples[4])/200))
                  msg = msg.build()
                  the_logger.log_msg("ACC: " + str(samples[2]) + ", "+ str(samples[3]) + ", " + str(samples[4]));
                  
                  client1.send(msg)
      #           client1.send_message("/empatica/acc", "1, 2, 3")
  the_logger.close_it_all()
  


