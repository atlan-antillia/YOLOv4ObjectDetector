# Copyright 2020-2021 antillia.com Toshiyuki Arai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# DetectConfigParser.py
#
import os
import sys
import glob
import json
from collections import OrderedDict
import pprint
import configparser
import traceback

class DetectConfigParser:
  MODEL     = "model"
  DATASET   = "dataset"
  WEIGHTS   = "weights"
  CONFIG    = "config"
  DATA      = "data"
  
  DETECTION = "detection"
  OUTPUTS   = "outputs"
  THRESHOLD = "threshold"  
  SAVE_LABELS = "save_labels"

  # Constructor
  # 
  def __init__(self, detect_config_path="./coco_detect.config"):
    print("==== TrainConfigParser {}".format(detect_config_path))
    if not os.path.exists(detect_config_path):
      raise Exception("Not found: detect.parser_path {}".format(detect_config_path))
    if not os.path.isfile(detect_config_path):
      raise Exception("Not file : detect.parser_path {}".format(detect_config_path))

    try:
      self.parse(detect_config_path)
    except Exception as ex:
      traceback.print_exc()


  def parse(self, detect_config_path):
    self.parser = configparser.ConfigParser()
    self.parser.read(detect_config_path)
    self.dump_all()


  def dataset(self):
    return self.parser[self.MODEL][self.DATASET]

  def weights(self):
    return self.parser[self.MODEL][self.WEIGHTS]

  def config(self):
    return self.parser[self.MODEL][self.CONFIG]

  def data(self):
    return self.parser[self.MODEL][self.DATA]

  def outputs(self):
    return self.parser[self.DETECTION][self.OUTPUTS]
    
  def threshold(self):
    return float(self.parser[self.DETECTION][self.THRESHOLD])
