# cellconfluency

## dependencies:
* skimage module
pip install scikit-image
* cv2 module
pip install opencv-python

## usage:
### to test/visualize threshold of standard deviation of local brightness
* image.jpg: name of image to be tested/visualised
* threshold: thresold number to test (default = 2)
```
	segment.py -i image.jpg -S threshold -test test.jpg
```
	
### to calculate confluency
edit area.sh to change path to segment.py file, then

```
	area.sh -S {int: threshold} img1_001.jpg img2_002.jpg ....
```
	
### to process time lapse experiment
edit area.make, then 
```
	make -f area.make AREA	
```
See example folder:
* AF-GAMMA: images to be analyzed
* makefiles: location of area.make
* image_proc: output
* segment_thr: standard deviation threshold
* to run:
```
cd example
rm -rf image_proc segment_thr
cd makefiles
make AREA
```
