import sys
import os
import numpy as np
import SimpleITK as ST
import dicom_read
import cPickle as pickle
import scipy.io as sio
import gc

class Data:
    def __init__(self,data_dir,number):
        self.dir = data_dir
        self.number = number
        self.names = []
        self.output_loc = "output_multi"

    def get_array(self,dicom_dir):
        img = dicom_read.read_dicoms(dicom_dir)
        ret_array = ST.GetArrayFromImage(img)
        ret_array = np.transpose(ret_array, [2, 1, 0])
        return ret_array

    def load_data(self):
        self.imgs = dict()
        root_dir = self.dir
        for sub_dir in os.listdir(root_dir):
            dicom_dir = root_dir + '/' + sub_dir
            self.imgs[sub_dir] = self.get_array(dicom_dir)
            self.names.append(sub_dir)

    def output(self):
        root_dir = os.getcwd()
        if not os.path.exists("./" + self.output_loc):
            os.makedirs("./" + self.output_loc)
        output_dir = root_dir + "/" + self.output_loc
        output_name = output_dir + "/data_" + str(self.number) + ".mat"
        sio.savemat(output_name,{name : self.imgs[name] for name in self.names})
        return output_name


root_dir='/opt/Multi-Task-data-process/multi_task_data_train'
number = 0
data_meta = dict()
for patient_dir in os.listdir(root_dir):
    number += 1
    data = Data(root_dir+'/'+patient_dir,number)
    data.load_data()
    data_meta[number] = data.output()
    del data
    gc.collect()
    print ""
for num,loc in data_meta.items():
    print num," ",loc
pickle_writer = open('./data_meta_multi.pkl', 'wb')
pickle.dump(data_meta, pickle_writer)
pickle_writer.close()
