# Micro QR code repo for python using pyboof
This is the repo for detecting Micro QR codes in images/video.

## Prerequisites
- Python 3.7 ~ 3.10
- Java 7.0+

You can choose other versions of Python. Actually, I use Python 3.6.10 for this project. The versions listed above are tested by Py4J (The library used by pyboof) owner.

## Installation
Please install packages using pip.
```
$ pip install -r requirements.txt
```

## Usage
Sorry, I do not prepare scripts except detection in video.
If you want to try other detections, please read python source codes in `src/`.
#### Detect Micro QR codes in a video (Save mode)
You can detect QR codes in a video and draw the bounding box and labels in a video.
```
$ bash scritps/save_video.sh INPUT_VIDEO_PATH OUTPUT_VIDEO_PATH QR_ALIGNMENT_FILE
```
- INPUT_VIDEO_PATH: path to the input video
- OUTPUT_VIDEO_PATH: path you want to save the result (the video where bbox and its labels are drawn)
- QR_ALIGNMENT_FILE: path to the json file where the alignment between QR codes number and their labels are written

#### Detect Micro QR codes in a video (View mode)
You can detect QR codes in a video and check the detected result in frame (not save).
If you execute view mode, you should do it on your local machine.
```
$ bash scritps/view_video.sh INPUT_VIDEO_PATH QR_ALIGNMENT_FILE
```
Parameters are the same as ones above.