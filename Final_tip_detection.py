#----------------------------------------------------------------------------------------------
#code to detect the tip of a plant .First colour_detection using thresholding is done and the plant
#is extracted from the background.This image is converted to grayscale.To this image bilateral filter and
#canny edge detection is applied. The resulting image is eroded and dialated through morphological
#transformations to give solid contour.To this contour corner harris algorithm is applied and that point with the least coordinate
#is the required tip of the plant#
#----------------------------------------------------------------------------------------------------------
import numpy as np
import matplotlib
import cv2
from matplotlib import pyplot as plt

winname='TIP_DETECTION'

a='/home/subha/PycharmProjects/image_processing/noWS160514_102359.jpg'

cv2.namedWindow(winname, cv2.WINDOW_NORMAL)

upstate = cv2.imread('/home/subha/PycharmProjects/image_processing/noWS160514_102359.jpg')

upstate_hsv = cv2.cvtColor(upstate, cv2.COLOR_BGR2HSV)
#plt.imshow(cv2.cvtColor(upstate_hsv, cv2.COLOR_HSV2RGB))

blue_min=np.array([17,70,100], np.uint8)
blue_max=np.array([70,255,255], np.uint8)


# get mask of pixels that are in green range
mask_inverse = cv2.inRange(upstate_hsv, blue_min, blue_max)
mask_final=cv2.cvtColor(mask_inverse, cv2.COLOR_GRAY2RGB)
# inverse mask to get parts that are not green
mask = cv2.bitwise_not(mask_inverse)
blurred = cv2.bilateralFilter(mask_inverse,5,20,20)
auto = cv2.Canny(blurred,1,35)
thresh = cv2.adaptiveThreshold(auto, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 11, 1)
kernel = np.ones((3, 3), np.uint8)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=4)
img2,contours, hierarchy=cv2.findContours(closing.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    #if c==cmax:
        peri = cv2.arcLength(c, True)
        app= cv2.approxPolyDP(c, 0.001 * peri, True)
        cv2.drawContours(closing, [c], -1, (0, 255, 0), 3)
        #if (c==cmax):
new_img= a+'MODIFIED.jpg'
cv2.imwrite(new_img,closing)

img = cv2.imread(new_img)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray,100,0.001,7)
corners = np.int0(corners)
a=[]
b=[]

#for j in len(corners):
for i in corners:
        x,y = i.ravel()
        a.append(y)
        b.append(x)

t=a.index((min(a)))
Y=min(a)
for l,k in enumerate(b):
    if l==t:
        cv2.circle(img,(k,Y), 9, (0,0,255), -1)



cv2.imshow(winname,img)
key1=cv2.waitKey(100000)
if key1 == 27:
    cv2.destroyWindow(winname)
