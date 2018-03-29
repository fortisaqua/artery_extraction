import numpy as np
import scipy.io as sio
import SimpleITK as ST
import os

output_root = "./vtks_airway"
mat_dir = "./output_airway/data1.mat"
if not os.path.exists(output_root):
    os.mkdir(output_root)
names = ['original','mask']
data_sample = sio.loadmat(mat_dir)
for name,data in data_sample.items():
    try:
        img = ST.GetImageFromArray(np.transpose(data_sample[name],[2,1,0]))
        ST.WriteImage(img,output_root+ "/" +name+".vtk")
    except Exception,e:
        print ""
print "over"