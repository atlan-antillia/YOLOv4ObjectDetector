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

#2021/02/02 
#YOLOv4ObjectDetector

#This is based on darknet/darknet_images.py

import argparse
import os
import sys
import traceback

import glob
import random
import darknet
import time
import cv2
import numpy as np
import darknet
from DetectedObjectDrawer import DetectedObjectDrawer
from FiltersParser import FiltersParser
from DetectConfigParser import DetectConfigParser

DARKNET_FORCE_CPU =True

class YOLOv4ObjectDetector:

  def __init__(self, detect_config):
    print("=== {}".format(YOLOv4ObjectDetector))
    parser = DetectConfigParser(detect_config)
    self.WEIGHTS    = parser.weights()
    self.CONFIG     = parser.config()
    self.DATA       = parser.data()
    self.OUTPUTS    = parser.outputs()
    
    self.THRESHOLD  = parser.threshold()
    
    self.SAVE_LABELS = True

    self.output_dir = os.path.join(os.getcwd(), self.OUTPUTS)
    if not os.path.exists(self.output_dir):
        os.makedirs(self.output_dir)
    
    #random.seed(3)  # deterministic bbox color
    self.BATCH_SIZE  = 1
    self.network, self.class_names, self.class_colors = darknet.load_network(
        self.CONFIG,
        self.DATA,
        self.WEIGHTS,
        batch_size=self.BATCH_SIZE
    )
    print("=== class_names {}".format(self.class_names))
    
    
  def detect_all(self, image_dir, filters):
      if not os.path.exists(image_dir):
        raise Exception("Not found input_image_dir {}".format(image_dir))
      image_list = []

      if os.path.isdir(image_dir):
        image_list.extend(glob.glob(os.path.join(image_dir, "*.png")) )
        image_list.extend(glob.glob(os.path.join(image_dir, "*.jpg")) )

      print("image_list {}".format(image_list) )
          
      for image_filename in image_list:
          #image_filename will take images/foo.png
          image_file_path = os.path.abspath(image_filename)
          
          print("filename {}".format(image_file_path))
          
          self.detect(image_file_path, filters)



  def detect(self, filename, filters):
      filtersParser = FiltersParser(self.class_names)
      filters = filtersParser.parse(filters)

      self.NL  = "\n"
      self.SEP = ","
      
      image = cv2.imread(filename)
      height, width, channels = image.shape[:3]

      # Darknet doesn't accept numpy images.
      # Create one with image we reuse for each detect

      darknet_image = darknet.make_image(width, height, 3)
      
      image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      image_resized = cv2.resize(image_rgb, (width, height),
                                 interpolation=cv2.INTER_LINEAR)

      darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
      detections = darknet.detect_image(self.network, self.class_names, darknet_image, thresh=self.THRESHOLD)
      darknet.free_image(darknet_image)
      drawer = DetectedObjectDrawer()
            
      image, objects_detail, objects_stats = drawer.draw_boxes_with_filters(detections, image_resized, 
                self.class_colors, filters)
      
      rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

      sfilters = self.filters_to_string(filters)
      out_filename = self.output_dir + "/" + sfilters + os.path.basename(filename)
          
      cv2.imwrite(out_filename, rgb_image)
      print("=== Saved image file {}".format(out_filename))
      
      self.save_detected_objects(out_filename, objects_detail)
      self.save_objects_stats(out_filename,    objects_stats)


  def filters_to_string(self, filters):
    sfilters = ""
    if filters == None:
      sfilters = ""
    else:
      sfilters = str(filters).replace(" ", "")
    return sfilters
          
      
  def save_detected_objects(self, image_name, detected_objects):

    detected_objects_csv = image_name + "_objects.csv"
    print("=== {}".format(detected_objects_csv))
    
    with open(detected_objects_csv, mode='w') as f:
      header = "id, class, score, x, y, w, h" + self.NL
      f.write(header)

      for item in detected_objects:
        line = str(item).strip("()").replace("'", "") + self.NL
        #print(line)
        f.write(line)
   
    print("=== Saved detected_objects {}".format(detected_objects_csv))


  def save_objects_stats(self, image_name, objects_stats):
    objects_stats_csv = image_name + "_stats.csv"
    print("=== {}".format(objects_stats_csv))
    
    with open(objects_stats_csv, mode='w') as s:
       header = "id, class, count" + self.NL
       s.write(header)
       
       for (k,v) in enumerate(objects_stats.items()):
         (name, value) = v
         line = str(k +1) + self.SEP + str(name) + self.SEP + str(value) + self.NL
         s.write(line)
    print("=== Saved objects_stats {}".format(objects_stats_csv))
  

  def convert2relative(self, image, bbox):
      """
      YOLO format use relative coordinates for annotation
      """
      x, y, w, h = bbox
      height, width, _ = image.shape
      return x/width, y/height, w/width, h/height


  def save_annotations(self, name, image, detections, class_names):
      """
      Files saved with image_name.txt and relative coordinates
      """
      file_name = name.split(".")[:-1][0] + ".txt"
      with open(file_name, "w") as f:
          for label, confidence, bbox in detections:
              x, y, w, h = self.convert2relative(image, bbox)
              label = class_names.index(label)
              f.write("{} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(label, x, y, w, h, float(confidence)))



if __name__ == "__main__":
  #python YOLOv4ObjectDetector.py ./images coco_detect.config [filters]
  
  try:
        
     image_file = None
     image_dir  = None
     detect_config = "coco_detect.config"
     
     filters = None  # classnames_list something like this "[person,car]"

     if len(sys.argv) >= 2:
       input = sys.argv[1]
       if not os.path.exists(input):
         raise Exception("Not found input {}".format(input))
       if os.path.isfile(input):
         image_file = input
       else:
         image_dir  = input

     if len(sys.argv) >= 3:
       detect_config = sys.argv[2]
     if not os.path.exists(detect_config):
       raise Exception("Not found detect_config {}".format(detect_config))
  
     if len(sys.argv) >= 4:
       filters = sys.argv[3]
         
     detector = YOLOv4ObjectDetector(detect_config)
     if image_dir is not None:
       detector.detect_all(image_dir, filters)
       
     if image_file is not None:
       detector.detect(image_file, filters)
  
  except Exception as ex:
    traceback.print_exc()
  
