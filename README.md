# empatica_python_driver
Python code to read data from Empatica and forward it via OSC to Max MSP

# How to use:
python empatica.py

with following options:

  parser.add_argument("--emp_ip",
                        help="IP address of Empatica", default="127.0.0.1")    
  parser.add_argument("--emp_port", help="the port", type=int, default=9999)
  parser.add_argument("--dest_ip",
                        help="IP address of the destination", default="127.0.0.1")    
  parser.add_argument("--dest_port", help="the port", type=int, default=9999)
  parser.add_argument("--osc_path", help="the osc path prefix", default="Empatica")
  parser.add_argument("--emp_name", default = "862D64")
  parser.add_argument("--eda", help="record EDA", action="store_true", default="True")
  parser.add_argument("--bvp", help="record BVP", action="store_true")
  parser.add_argument("--bat", help="record battery", action="store_true")
  parser.add_argument("--acc", help="record accelometer", action="store_true")
  parser.add_argument("--tmp", help="record temperature", action="store_true")
  parser.add_argument("--offline", help="run in offline mode", action="store_true")
  parser.add_argument("--logging", help="Log the data", action="store_true", default="True")
  parser.add_argument("--EDA_max", help="Initial EDA Maximum", default = 1)
  parser.add_argument("--EDA_baseline_length", help="baseline length", default = 20)
