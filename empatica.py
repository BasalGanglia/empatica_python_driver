# -*- coding: utf-8 -*-
"""
Empatica with command line etc.

@author: Ilkka
"""

import argparse
import random
import time
import sys
import socket
import signal
import datetime
import argparse


from pythonosc import osc_message_builder
from pythonosc import udp_client
from struct import *
from my_utils import logWriter


if __name__ == "__main__":
# # Attempt to ctrl-c work in windows.. not very succesful.
  parser = argparse.ArgumentParser()
  parser.add_argument("--emp_ip",
                        help="IP address of Empatica", default="127.0.0.1")    
  parser.add_argument("--emp_port", help="the port", type=int, default=9999)
  parser.add_argument("--dest_ip",
                        help="IP address of the destination", default="127.0.0.1")    
  parser.add_argument("--dest_port", help="the port", type=int, default=9999)
  parser.add_argument("--osc_path", help="the osc path prefix", default="Empatica")
  parser.add_argument("--emp_name", default = "862D64")
  parser.add_argument("--eda", help="record EDA", action="store_true", default="True")
  parser.add_argument("--bvp", help="record BVP", action="store_true")  parser.add_argument("--bat", help="record battery", action="store_true")  parser.add_argument("--acc", help="record accelometer", action="store_true")  parser.add_argument("--tmp", help="record temperature", action="store_true")
  parser.add_argument("--offline", help="run in offline mode", action="store_true")
  parser.add_argument("--logging", help="Log the data", action="store_true", default="True")  parser.add_argument("--EDA_max", help="Initial EDA Maximum", default = 1)
  parser.add_argument("--EDA_baseline_length", help="baseline length", default = 20)
 # parser.add_argument("--logging", help="Log the data", default = 1)
# add args for logging and what signals to record, and offline mode
# maybe a way to sent to several places? dest_ip2

  args = parser.parse_args()
  
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
  sock.connect((args.emp_ip, args.emp_port))
  
  sock.sendall("device_list\r\n".encode())
  time.sleep(1)
# Specify the correct device ID:
  device_string = "device_connect " + args.emp_name + "\r\n"
 # sock.sendall("device_connect 862D64\r\n".encode())
  sock.sendall(device_string.encode())
  
  # sock.sendall("device_connect A219F2\r\n".encode())
 # sock.sendall("device_connect 033B64\r\n".encode())
  time.sleep(1)
  
  # Then subscribe to the physiological signals you wish to record:
  if args.eda:
      sock.sendall("device_subscribe gsr ON\r\n".encode())
      time.sleep(1)
   
  #time.sleep(1)
  if args.bat:
    sock.sendall("device_subscribe bat ON\r\n".encode())
    time.sleep(1)
  
  if args.bvp:
    sock.sendall("device_subscribe bvp ON\r\n".encode())
    time.sleep(1)
  
  if args.acc:
    sock.sendall("device_subscribe acc ON\r\n".encode())
    time.sleep(1)
    
  if args.tmp:
    sock.sendall("device_subscribe tmp ON\r\n".encode())
    time.sleep(1)
    #  Connect to Unity/Max whatever for real-time processing of the data:
    # #  client1 = udp_client.SimpleUDPClient(ADDRESS1, PORT1)
  if not args.offline:
    client1 = udp_client.SimpleUDPClient(args.dest_ip, args.dest_port)

  # we are going to make a veyr quick hack for normalizing the EDA
  EDA_counter = 0
  EDA_max = args.EDA_max
  EDA_BASELINE_LENGTH = args.EDA_baseline_length
  
# Read data from Empatica:
  interrupter = False
  while interrupter == False:
      
      data = sock.recv(1024).decode()

      data = data.replace(",", ".")
      sample_lines = data.split("\n")
      print("the full data: <{0}>".format(data))

# If the Empatica server sends more than one line (or more than one sample), parse each sample separately:
      if len(sample_lines) > 1:
          
          # ignore the last "line" as it is actually just the carriage return
          # splitlines above separate \n\r into two lines...
          for i in range(0, len(sample_lines) - 1):
              samples = sample_lines[i].split(" ")
              
              # Maybe do some more elegant solution later but if elses it is for now
              if samples[0] == "E4_Gsr":
                  osc_address = args.osc_path + "EDA"
                  msg = osc_message_builder.OscMessageBuilder(address = osc_address)
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
                    elif EDA_current < (EDA_max / 4 ):   #  If EDA max becomes too large start decreasing it
                      EDA_max = EDA_max - (EDA_current / 4)
                    
                    
                  EDA_normalized = EDA_current / EDA_max
                  
                  if args.logging:
                    the_logger.log_msg("EDA: " + str(EDA_current) + ", " + str(EDA_normalized) + "\n")
                  
                  print("EDA max is {0} and current EDA is {1} and normalized{2}".format(EDA_max, samples[2], EDA_normalized))
                  msg.add_arg(EDA_normalized)
                  msg = msg.build()
                  if not args.offline:
                    client1.send(msg)
              
              if samples[0] == "E4_Bvp":
                  msg = osc_message_builder.OscMessageBuilder(address = "/empatica/BVP")      
                  msg = msg.build()
                  if args.logging:
                    the_logger.log_msg("BVP: " + str(samples[2]));
                  if not args.offline:
                    client1.send(msg)                                            
                  
              if samples[0] == "E4_Temp":
                if args.logging:
                  the_logger.log_msg("Temp: " + str(samples[2]));
                if not args.offline:
                    client1.send(msg)
     
              if samples[0] == "E4_Bat":
                  print("Battery level: {0} ".format(samples[2]))
                  
                 
              if samples[0] == "E4_Ibi":
                  msg = osc_message_builder.OscMessageBuilder(address = "/empatica/IBI")        
                  msg = msg.build()
                  if args.logging:
                    the_logger.log_msg("IBI: " + str(samples[2]));
                  if not args.offline:
                    client1.send(msg)
   
              if samples[0] == "E4_Acc":
         
                  msg = osc_message_builder.OscMessageBuilder(address = "/empatica/acc")
                  print("The acc values are {0}-{1}-{2}".format(samples[2], samples[3], samples[4]))
                  msg.add_arg(abs(int(samples[2])/200))
                  msg.add_arg(abs(int(samples[3])/200))
                  msg.add_arg(abs(int(samples[4])/200))
                  msg = msg.build()
                  if args.logging:
                    the_logger.log_msg("ACC: " + str(samples[2]) + ", "+ str(samples[3]) + ", " + str(samples[4]));
                  if not args.offline:
                    client1.send(msg)                          
    
  the_logger.close_it_all()
  sock.close()
  
