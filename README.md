## CCTV / camera detector for street  view

* I built a few components in order to crawl and detect the presence of security cameras in goog street view.
* The project consists of the following:
    * photo_downloader.py, a script to download a bunch of images from a goog image search
    * classifier.py, a file that trains a photo classifier on the downloaded images
    * walker.py, a class and script that uses browser automation library selenium to do a random walk in street view and 
    take pics, tileize them, and then detect the presence of cameras.  If it detects a camera, it logs the lat/lng and saves a pic of the camera.
    * plotter.py is a small script that can be used to plot lat/lng points from the walker over an image (think map)
* I learned a lot about machine learning, particulary convolutional neural nets and their structure.  I tried a lot of different 2d convolutional model structures based on research papers which was cool.  I also used Tensorflow and Keras for the first time.
* The classifier does not work well at all at this point.  Because it is an image classification model as opposed to an object detection model, it is hard for the model to handle such dense, complex imagery from a fairly small (~ 1000 image) dataset. That's why I'm working on using detecto to get this to work better, which allows you to fine tune an object classifier on a pre-trained model.

