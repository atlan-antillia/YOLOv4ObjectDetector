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
#DetectedObjectDrawer.py

#This is based on darknet/darknet.py

from ctypes import *
import math
import random
import os
import cv2

class DetectedObjectDrawer:
  
  def __init__(self):
    self.font = cv2.FONT_HERSHEY_SIMPLEX
    pass


  def draw_boxes_with_filters(self, detections, image, colors, filters):
    objects_detail = []
    objects_stats  = {}
  
    id = 0
    detections = reversed(detections)
     
    for label, confidence, bbox in detections:
    
      left, top, right, bottom = self.bbox2points(bbox)
        
      if (filters is None) or (filters is not None and label in filters):

        cv2.rectangle(image, (left, top), (right, bottom), colors[label], 1)
        confidence = float(confidence) / 100.0
        s = format(confidence, '.2f')
        
        cv2.putText(image, "{}:{} {}".format(id, label, s),
                    (left, top - 5), self.font, 0.5,
                    colors[label], 2)
        
        detected_object = (id, label, s, int(left), int(top), int(right-left), int(bottom-top) )
        id +=  1
        
        #Update the objects_detail list
        objects_detail.append(detected_object)

        #Update the objects_stats
        if label not in objects_stats:
          objects_stats[label] = 1
        else:
          count = int(objects_stats[label]) 
          objects_stats.update({label: count+1})
                    
    return image, objects_detail, objects_stats


  def bbox2points(self, bbox):
    """
    From bounding box yolo format
    to corner points cv2 rectangle
    """
    x, y, w, h = bbox
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax

  
