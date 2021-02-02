# YOLOv4ObjectDetector
Python YOLOv4ObjectDetector based on darknet/YOLOv4



<h1> YOLOv4ObjectDetector</h1>
YOLOv4ObjectDetector is simple Python class to detect objects in an image by using
<a href="https://github.com/AlexeyAB/darknet">darknet YOLOv4</a>.<br>
<br>
 We have added the following new Python classes to the darknet.<br>
- <a href="./YOLOv4ObjectDetector.py>YOLOv4ObjectDetector</a><br>
- <a href="./DetectedObjectDrawer.py>DetectedObjectDrawer</a><br>
- <a href="./DetectConfigParser.py>DetectConfigParser</a><br>
- <a href="./FiltersParser.py>FiltersParser</a><br>


<h2>
1 Installation
</h2>
<h3>
1.1 Clone darknet
</h3>
Please clone darknet.git in a working folder from the following Web site.<br>

<a href="https://github.com/AlexeyAB/darknet">darknet YOLOv4</a>.<br>
<br>
<h3>
1.2 Clone YOLOv4ObjectDetector
</h3>
Please clone YOLOv4ObjectDetector.git in a folder from the following Web site.<br>

<a href="https://github.com/atlan-antillia/YOLOv4ObjectDetector">YOLOv4ObjectDetector</a>.<br>
<br>

<h3>
1.3 Download weight file(yolov4.weights)
</h3>
Please download weight file(yolov4.weights) from <a href="https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights">here</a>
or <a href="https://drive.google.com/open?id=1cewMfusmPjYWbrnuJRuKhPMwRe_b9PaT">Google drive </a>, and copy it to
 ./dataset/coco/weights/ folder in YOLOv4ObjectDetector.
<br>

<h3>
1.3 Deploy YOLOv4ObjectDetector to darknet
</h3>
Please copy files and folders in YOLOv4ObjectDetector to darknet or darknet/build/darknet/build/x64 (Windows10)



<h2>
2 Run YOLOv4ObjectDetector
</h2>

In darknet folder or or darknet/build/darknet/build/x64, run the following command.<br>

>python YOLOv4ObjectDetector.py image_file_dir coco_detect.config
<br>
coco_detect.config<br>
<pre>
</pre>

Example 1:<br>

>python YOLOv4ObjectDetector.py images/img.png coco_detect.config

<img src="./dataset/coco/outputs/img.png">
<br>

