import numpy as np
import scipy.io as sio
import SimpleITK as ST
import os

data_type = "multi"
output_root = "./vtks_"+data_type
mat_dir = "./output_"+data_type+"/data_1.mat"
if not os.path.exists(output_root):
    os.mkdir(output_root)
data_sample = sio.loadmat(mat_dir)
for name,data in data_sample.items():
    try:
        print type(data_sample[name])
        img = ST.GetImageFromArray(np.transpose(data_sample[name],[2,1,0]))
        ST.WriteImage(img,output_root+ "/" +name+".vtk")
    except Exception,e:
        print ""
print "over"