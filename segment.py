#!/usr/bin/python
import numpy as np
import cv2
from skimage import morphology
import argparse, sys


def stddev_thresh(img_in, ws, thr):
    # converting image to float32
    img = np.float32(img_in)
    
    # blur(img^2) 
    img_sq = cv2.multiply(img, img)
    blur_sq_avg = cv2.blur(img_sq, (ws, ws))

	# blur(img)^2)
    blur_avg = cv2.blur(img,(ws, ws))
    blur_avg_sq = cv2.multiply(blur_avg, blur_avg)
    
    # sqrt(blur(img^2) - blur(img)^2)
    std_dev = cv2.sqrt(blur_sq_avg - blur_avg_sq)
    
    # converting input image to uint8, segmentation
    # std_int = (std_dev*255./np.max(std_dev)).astype(np.uint8)
    std_int = std_dev.astype(np.uint8)
    ret, std_thr = cv2.threshold(std_int, thr, 255, cv2.THRESH_BINARY)
    
    return std_dev, std_thr
	
	
def clust_mask(img, std_thr, size):
	# AttributeError: module 'numpy' has no attribute 'bool'.
	# `np.bool` was a deprecated alias for the builtin `bool`. 	
	thr_bool = std_thr.astype(np.bool_)
	thr_rem = morphology.remove_small_objects(thr_bool, min_size=size, connectivity=2)
	thr_rem = morphology.remove_small_objects(~thr_rem, min_size=size, connectivity=2)
	thr_rem = ((~thr_rem).astype(np.uint8)*255)
	
	img_masked = cv2.bitwise_and(img, img, mask = thr_rem)
	
	return thr_rem, img_masked


def img_layer(img_orig, img_segm):
    
    img_orig_rgb = cv2.cvtColor(img_orig, cv2.COLOR_GRAY2BGR)
    img_found = np.zeros_like(img_orig_rgb)
    img_found[:, :, 0] = img_segm.astype(np.uint8)
    img_layered = cv2.addWeighted(img_orig_rgb, 0.8, img_found, 0.2, 0)
    
    return img_layered


###########################################################
# Argument parser
p = argparse.ArgumentParser(description='segmentation')
# to take more than on argument in the command line
p.add_argument('-i', action='store', dest='inp', type=str, nargs='+',
               required=True, help='input image path')
p.add_argument('-o', action='store', dest='outp', type=str, 
               help='output image path')
p.add_argument('-S', action='store', dest='thr', type=int, 
               default=2, help='stddev threshold value')
p.add_argument('-area', action='store_true', dest='area', default=False,
               help='calculates white pixel ratio')
p.add_argument('-test', action='store', dest='test', type=str, 
               help='layered image path')
args = p.parse_args()
############################################################      
# iterating through command-line arguments with try except
try:
    for _ in img_name:
        img_load = cv2.imread(_, 0)
        win_size = 10

        sigma, sigma_thr = stddev_thresh(img_load, win_size, thr_val)
        sigma_mask, img_masked = clust_mask(img_load, sigma_thr, size=100)
        sigma_layered = img_layer(img_load, sigma_mask)


        if args.outp:
            cv2.imwrite(out_name, sigma_mask)

        if args.test:
            cv2.imwrite(args.test, sigma_layered)

        if args.area:
            # counts the ratio of white pixels
            total = np.sum(sigma_mask)/255.
            ratio = np.around(100*total/np.size(sigma_mask), 2)

            area_dat = ['255', str(total.astype(int)), '100%', str(ratio)+'%']
            sys.stdout.write("\t".join(area_dat) + '\n')

except Exception:
     print("encountered an error!")
     print(traceback.format_exc())
