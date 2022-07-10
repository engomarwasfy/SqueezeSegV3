
#!/usr/bin/env python3
# This file is covered by the LICENSE file in the root of this project.

import argparse
import subprocess
import datetime
import yaml
from shutil import copyfile
import os
import shutil
import __init__ as booger

from tasks.semantic.modules.demo_user import *


if __name__ == '__main__':
  parser = argparse.ArgumentParser("./demo.py")
  parser.add_argument(
      '--dataset', '-d',
      type=str,
      default = "../../../sample_data/", 
      help='Dataset to sample'
  )
  parser.add_argument(
      '--log', '-l',
      type=str,
      default=  '../../../sample_output/',
      help='Directory to put the predictions. Default: ~/logs/date+time'
  )
  parser.add_argument(
      '--model', '-m',
      type=str,
      required=True,
      default=None,
      help='Directory to get the trained model.'
  )
  FLAGS, unparsed = parser.parse_known_args()

  # print summary of what we will do
  print("----------")
  print("INTERFACE:")
  print("dataset", FLAGS.dataset)
  print("log", FLAGS.log)
  print("model", FLAGS.model)
  print("----------\n")


  # open arch config file
  try:
    print(f"Opening arch config file from {FLAGS.model}")
    ARCH = yaml.safe_load(open(f"{FLAGS.model}/arch_cfg.yaml", 'r'))
  except Exception as e:
    print(e)
    print("Error opening arch yaml file.")
    quit()

  # open data config file
  try:
    print(f"Opening data config file from {FLAGS.model}")
    DATA = yaml.safe_load(open(f"{FLAGS.model}/data_cfg.yaml", 'r'))
  except Exception as e:
    print(e)
    print("Error opening data yaml file.")
    quit()

  # create log folder
  try:
    if os.path.isdir(FLAGS.log):
      shutil.rmtree(FLAGS.log)
    os.makedirs(FLAGS.log)
    os.makedirs(os.path.join(FLAGS.log, "sequences"))

    for seq in DATA["split"]["sample"]:
      seq = '{0:02d}'.format(int(seq))
      print("sample_list",seq)
      os.makedirs(os.path.join(FLAGS.log, "sequences", seq))
      os.makedirs(os.path.join(FLAGS.log, "sequences", seq, "predictions"))

  except Exception as e:
    print(e)
    print("Error creating log directory. Check permissions!")
    raise

  except Exception as e:
    print(e)
    print("Error creating log directory. Check permissions!")
    quit()

  # does model folder exist?
  if os.path.isdir(FLAGS.model):
    print(f"model folder exists! Using model from {FLAGS.model}")
  else:
    print("model folder doesnt exist! Can't infer...")
    quit()
  # create user and infer dataset
  user = User(ARCH, DATA, FLAGS.dataset, FLAGS.log, FLAGS.model)
  user.infer()
