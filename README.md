
![image of a sample collimation](collimation.png)

## Collimation Tool

This repo contains a simple python app to help you
collimate your telescope.  When run, the app connects
to a video streaming device, for example
a "USB Streaming" supporting camera
with a T-ring adapter attached, and displays it
with a HUD reticle on top.

Use the scroll wheel on the mouse to zoom or dag the mouse to pan.
The app works on the mac using the trackpad as well.  When using the mouse or
trackpad, dagging will pan the video stream.  However using the keyboard the
keys pans the reticle instead.

## Application Keys

Use the following keys to pan and zoom:

```
LEFT:   move reticle left        
RIGHT:  move reticle right       
UP:     move reticle up 
DOWN:   move reticle down
EQUALS: zoom video stream in
MINUS:  zoom video stream out
SHIFT:  hold shift to pan or zoom faster
```

## Running the App

If you have uv installed you can either run the app
using "sh collimate.py" or directly using "./collimate.py".
uv will automatically install the proper python dependencies.
Otherwise ensure both opencv-python, numpy, and
pygame are installed in your python environment before running.

## Command Line Usage

```
usage: collimation.py [-h] [--device DEVICE]

collimation circle tool

options:
  -h, --help       show this help message and exit
  --device DEVICE  video device number (default: 0)
```


