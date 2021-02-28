 #βιβλιοθήκες
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
#άνοιγμα φωτογραφίας
im1 = Image.open('image2.png')
a = np.array(im1)
a = a / 255
#print(a)
#εφαρμογή του φίλτρου Sobel
der_2a = np.array([[0,1,0],[1,-4,1],[0,1,0]])
der_2b = np.array([[1,0,1],[0,-4,0],[1,0,1]])
der_all = np.array([[1,1,1],[1,-8,1],[1,1,1]])
pre_x = np.array([[-1,-1,-1],[0,0,0],[1,1,1]])
pre_y = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
sob_x = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
sob_y = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
#εμφάνιση της αρχικής φωτογραφίας
plt.imshow(a, cmap='gray', vmin=0, vmax=1)
def convolution(a,b):
 c = np.ones((a.shape[0]+2,a.shape[1]+2))
 d = np.zeros(a.shape)
 c[1:-1,1:-1] = a
 for x in range(1,c.shape[0]-1):
 for y in range(1,c.shape[1]-1):
5
 d[x-1,y-1] = np.sum(c[x-1:x+2,y-1:y+2]*b)
 return d.astype(np.uint8)
im_der_2a = convolution(a,der_2a)
plt.imshow(im_der_2a, cmap='gray', vmin=0, vmax=1)
im_der_2b = convolution(a,der_2b)
plt.imshow(im_der_2b, cmap='gray', vmin=0, vmax=1)
im_der_all = convolution(a,der_all)
plt.imshow(im_der_all, cmap='gray', vmin=0, vmax=1)
#εμφάνιση και αποθήκευση της φωτογραφίας έπειτα από ανίχνευση των ακμών στην
διεύθυνση Χ
im_sob_x = convolution(a,sob_x)
plt.imshow(im_sob_x, cmap='gray', vmin=0, vmax=1)
plt.savefig('image2_sobel_x.png.png')
#εμφάνιση και αποθήκευση της φωτογραφίας έπειτα από ανίχνευση των ακμών στην
διεύθυνση Υ
im_sob_y = convolution(a,sob_y)
plt.imshow(im_sob_y, cmap='gray', vmin=0, vmax=1)
plt.savefig('image2_sobel_y.png.png')
#εμφάνιση και αποθήκευση της φωτογραφίας έπειτα από το άθροισμα των δύο
προηγούμενων.
im_sob_all = im_sob_x + im_sob_y
plt.imshow(im_sob_all, cmap='gray', vmin=0, vmax=1)
plt.savefig('image2_sobel_xy.png.png')
