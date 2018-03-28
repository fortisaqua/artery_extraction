import numpy as np
import scipy.io as sio
import SimpleITK as ST
import os

output_root = "./vtks_multi"
if not os.path.exists(output_root):
    os.mkdir(output_root)
names = ['original','mask']
data_sample = sio.loadmat("./output_multi/data_1.mat")
for name,data in data_sample.items():
    try:
        img = ST.GetImageFromArray(np.transpose(data_sample[name],[2,1,0]))
        ST.WriteImage(img,output_root+ "/" +name+".vtk")
    except Exception,e:
        print ""
print "over"