import sys
import os
import numpy as np
import SimpleITK as ST
import dicom_read
import cPickle as pickle
import scipy.io as sio
import gc
import sys

changed_root = "/usr/deeplearning/airway_extraction/output_airway"
pkl_url = "./data_meta_airway_1.pkl"
pickle_writer = open(pkl_url,'wb')
new_data = dict()
number = 1
for sub_dir in os.listdir(changed_root):
    new_data[number] = changed_root+"/"+sub_dir
    number += 1
pickle.dump(new_data,pickle_writer)