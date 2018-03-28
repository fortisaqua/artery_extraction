import numpy as np
import scipy.io as sio
import SimpleITK as ST
import os

if not os.path.exists("./vtks"):
    os.mkdir("./vtks")
names = ['original','mask']
data_sample = sio.loadmat("./output/data1.mat")
for name in names:
    img = ST.GetImageFromArray(np.transpose(data_sample[name],[2,1,0]))
    ST.WriteImage(img,"./vtks/"+name+".vtk")
print "over"