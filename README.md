# CupTracking

```script1.py``` - the script that tracks the bounding box for the blue cup with intel logo on it. Cup detection is blue colour detection. To increase performance, I downscale the image by some specified factor (down_sample_factor). Gaussian Blur also used, because there is some noise in a video. I do dilation and erosion to achieve better cup position and size estimation. I found contours, check them for size just in case and draw bound box and tracking polyline. 

If the cup appeared the first time, or it is the first frame when it disappears from the video that image is saved to the specified folder (appeared/disappeared). 

## How to run

This is the first time I tried to make ```requirements.txt``` file. Run ```pip install -r requeriments.txt``` I hope it works.
In case it is doesn't, do following steps.

### Tracking script 

To run the script first install  ```python3``` and ```opencv2```. 

To install opencv2 with pip run 
```pip3 install opencv-python```

```numpy``` will be installed automatically in case you do not have it

Then run ```python script1.py```

### Web service

To run web service install ```flask``` via command ```pip3 install flask```

Run script first and then run ```python web_service.py```

http://127.0.0.1:5000/appeared - Images where the cup appeared 

http://127.0.0.1:5000/disappeared - Images where the cup disappeared
