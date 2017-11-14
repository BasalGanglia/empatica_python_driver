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


EMPATICA_ADDRESS = "127.0.0.1"
EMPATICA_PORT = 28000

ADDRESS1 = "192.168.1.112"
PORT1 = 9998

OSCADDRESS = "/empatica"

if __name__ == "__main__":

  def signal_handler(signal, frame):
      print( "caught a signal")
      exit(0)
     
  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)
 # signal.signal(signal.CTRL_C_EVENT, signal_handler)

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((EMPATICA_ADDRESS, EMPATICA_PORT))
  #sock.send("device_subscribe gsr ON".encode('utf-8'))
 
 ## On windows machine if you dont put that \r\n it does not recognize it..
 # sock.sendall("device_list\r\n".encode())
  
  sock.sendall("device_connect A219F2\r\n".encode())
  time.sleep(1)
  sock.sendall("device_subscribe gsr ON\r\n".encode())
  time.sleep(1)
  sock.sendall("device_subscribe bvp ON\r\n".encode())
  time.sleep(1)
  sock.sendall("device_subscribe acc ON\r\n".encode())

#  
  client1 = udp_client.SimpleUDPClient(ADDRESS1, PORT1)

  
  #sock.setblocking(0)

  #time.sleep(1)
  print("Testin1")
  while True:

      data = sock.recv(1024).decode()
      ## first split into possibly several samples
    #  samples = data.splitlines()
      data = data.replace(",", ".")
      sample_lines = data.split("\n")
      print("the full data: <{0}>".format(data))
    #  print("Samples are {0},{1}".format(samples[1], samples[2]))
    
      if len(sample_lines) > 1:
          
          # ignore the last "line" as it is actually just the carriage return
          # splitlines above separate \n\r into two lines...
          for i in range(0, len(sample_lines) - 1):
              print("line numer {0} is: {1}".format(i, sample_lines[i]))
              samples = sample_lines[i].split(" ")
              
              # Maybe do some more elegant solution later but if elses it is for now
              if samples[0] == "E4_Gsr":
                  msg = osc_message_builder.OscMessageBuilder(address = "/empatica/EDA")
                  print("sample is as float {0}".format(float(samples[1])))
            
         #         timestamppi = timestamppi - 151000000.0
                  daitti = datetime.datetime.fromtimestamp(float(samples[1]))
                  print("timestamp is {0}".format(daitti))
                  teh_time = daitti.time();
                 # teh_time.
               #   msg.add_arg((daitti.second + (daitti.microsecond/1000000)))
                  msg.add_arg(teh_time.__str__());
                  msg.add_arg(samples[2])
                  msg = msg.build()
                  client1.send(msg)
                
              if samples[0] == "E4_Bvp":
                  msg = osc_message_builder.OscMessageBuilder(address = "/empatica/BVP")
                  print("sample is as float {0}".format(float(samples[1])))
            
         #         timestamppi = timestamppi - 151000000.0
                  daitti = datetime.datetime.fromtimestamp(float(samples[1]))
                  print("timestamp is {0}".format(daitti))
                  teh_time = daitti.time();
                 # teh_time.
               #   msg.add_arg((daitti.second + (daitti.microsecond/1000000)))
                  msg.add_arg(teh_time.__str__());
                  msg.add_arg(samples[2])
                  msg = msg.build()
                  client1.send(msg)
                 
              if samples[0] == "E4_Ibi":
                  msg = osc_message_builder.OscMessageBuilder(address = "/empatica/IBI")
                  print("sample is as float {0}".format(float(samples[1])))
            
         #         timestamppi = timestamppi - 151000000.0
                  daitti = datetime.datetime.fromtimestamp(float(samples[1]))
                  print("timestamp is {0}".format(daitti))
                  teh_time = daitti.time();
                 # teh_time.
               #   msg.add_arg((daitti.second + (daitti.microsecond/1000000)))
                  msg.add_arg(teh_time.__str__());
                  msg.add_arg(samples[2])
                  msg = msg.build()
                  client1.send(msg)
         
              if samples[0] == "E4_Acc":
                  msg = osc_message_builder.OscMessageBuilder(address = "/empatica/acc")
                  print("sample is as float {0}".format(float(samples[1])))
            
         #         timestamppi = timestamppi - 151000000.0
                  daitti = datetime.datetime.fromtimestamp(float(samples[1]))
                  print("timestamp is {0}".format(daitti))
                  teh_time = daitti.time();
                 # teh_time.
               #   msg.add_arg((daitti.second + (daitti.microsecond/1000000)))
                  msg.add_arg(teh_time.__str__());
                  msg.add_arg(samples[2])
                  msg.add_arg(samples[3])
                  msg.add_arg(samples[4])
                  msg = msg.build()
                  client1.send(msg)
         
              
              
         
        #  print ("we got more than one line: {0}".format(len(sample_lines)))
#          if len(samples) > 4:
#          
#          msg = osc_message_builder.OscMessageBuilder(address = OSCADDRESS)
#
#          msg.add_arg(data)     
#          #msg.add_arg(samples[3])
#          #msg.add_arg(samples[4])
#        
#   
#          msg = msg.build()
##  
#          client1.send(msg)
   #   print("the acc arguments are <{0}><{1}><{2}>".format(samples[0],samples[0],samples[0]);
   #   [print(x) for x in samples]
      #print(duh)
        # Here have one d (for double) for each input channel -- ilkka
    #  uruk_hai = data.decode().split(" ")
   #   print("data: {0} ".format(uruk_hai[2]))
      
  
    
#  for x in range(10):
#    client.send_message("/filter", random.random())
#    time.sleep(1)