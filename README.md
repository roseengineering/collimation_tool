
![image of a sample collimation](collimation.png)

## Collimation Tool

This repo contains a simple python app to help collimate your telescope.  The app connects to your video streaming device, for example a "USB Streaming" supporting camera with a T-1.25" adapter attached, and displays the feed in a window with a HUD reticle on top.  

Use the scroll wheel on the mouse to zoom or drag the mouse to pan the video stream.  The app also works on the mac using the trackpad.

## Application Keys

The following keys pan and zoom:

```
LEFT:   move video stream left        
RIGHT:  move video stream right       
UP:     move video stream up 
DOWN:   move video stream down
EQUALS: zoom video stream in
MINUS:  zoom video stream out
SHIFT:  hold shift to pan or zoom faster
R:      resets zoom to 1
Q:      quits app
ESC:    quits app
```

## Running the App

If you have [uv](https://docs.astral.sh/uv/) installed you can either run the app using "sh collimate.py" or directly using "./collimate.py".  [uv](https://docs.astral.sh/uv/) will automatically install the proper python dependencies.  Otherwise ensure opencv-python, numpy, and pygame are installed in your python environment before running.

## Command Line Usage

```
usage: collimation.py [-h] [--device DEVICE] [--color COLOR]

collimation circle tool

options:
  -h, --help       show this help message and exit
  --device DEVICE  video device number (default: 0)
  --color COLOR    reticle color (default: green)
```

## Notes

In the image, I inserted a reflector safety sticker, punched with a center hole, behind the adapter so I could see the center donut.  Changing the exposure setting on the camera will also bring it out.  



