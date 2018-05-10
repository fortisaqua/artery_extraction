import sys
import os
import numpy as np
import SimpleITK as ST
import dicom_read
import cPickle as pickle
import scipy.io as sio
import gc
import sys

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
        mask_names=["airway","artery"]
        root_dir = os.getcwd()
        if not os.path.exists("./" + self.output_loc):
            os.makedirs("./" + self.output_loc)
        output_dir = root_dir + "/" + self.output_loc
        output_name = output_dir + "/data_" + str(self.number) + ".mat"
        output_dict = {}
        for name, data in self.imgs.items():
            if "origin" in name:
                output_dict["original"] = data
            elif name in mask_names:
                output_dict[name] = data
        # exclude specific confusion area between airway and artery
        commen_mask = output_dict["airway"]*output_dict["artery"]
        output_dict["airway"] -= commen_mask
        output_dict["artery"] -= commen_mask
        sio.savemat(output_name,output_dict)
        return output_name

    def output_specific(self,type,threshold):
        root_dir = os.getcwd()
        self.output_loc = "output_"+type
        if not os.path.exists("./" + self.output_loc):
            os.makedirs("./" + self.output_loc)
        output_dir = root_dir + "/" + self.output_loc
        output_name = output_dir + "/data_" + str(self.number) + "_"+str(threshold)+".mat"
        output_dict = {}
        for name,data in self.imgs.items():
            if "origin" in name:
                if "airway" in type:
                    data = np.int16(data < threshold) * data
                if "artery" in type:
                    data = np.int16(data > threshold) * data
                output_dict["original"] = data
            if type in name:
                output_dict["mask"] = data
        sio.savemat(output_name, output_dict)
        return output_name

# usage : python data_class.py datadir mode [specific mask name if mode is "mask"] [threshold]
if __name__ == "__main__":
    root_dir=sys.argv[1]
    mode = sys.argv[2]
    data_meta = dict()
    type = ""
    threshold = 0
    output_file = './data_meta_'+mode+'.pkl'
    if mode == "mask":
        try:
            type = sys.argv[3]
            threshold = int(sys.argv[4])
            output_file = './data_meta_'+type+'_'+str(threshold)+'.pkl'
        except Exception,e:
            type = ""
    if mode == "multi_class":
        output_file = './data_meta_' + mode + '.pkl'
    if os.path.isfile(output_file):
        pickle_reder = open(output_file,'rb')
        data_meta = pickle.load(pickle_reder)
        pickle_reder.close()
    number = len(data_meta)
    for patient_dir in os.listdir(root_dir):
        number += 1
        data = Data(root_dir+'/'+patient_dir,number)
        data.load_data()
        if mode == "mask":
            data_meta[number] = data.output_specific(type,threshold)
        else:
            data_meta[number] = data.output()
        del data
        gc.collect()
        print ""
    for num,loc in data_meta.items():
        print num," ",loc
    pickle_writer = open(output_file, 'wb')
    pickle.dump(data_meta, pickle_writer)
    pickle_writer.close()
