# ColorMyScreen

## Description

This was a fun little project my friends and I put together for our computer vision project. We simple used a motion tracking algorithm with thresholding via OpenCV to create an app that allows you to draw on your screen with an object and webcam. The algorithm averages out the pixels in our tracking box to determine what object should be tracked and what color is used when drawing. 

## Requirements

Before running the application, make sure you install all of the application's dependencies with the command below:

```
pip install -r requirements.txt
```

## Running the App

To run the application, run the command below:

```
python handdrawn.py 
```

After running the command, you should be prompted with the following message: Running on http://127.0.0.1:5000/

Go to the above address, click the button, follow the rules, and have fun drawing!
