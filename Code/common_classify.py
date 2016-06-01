# coding: utf-8


import numpy as np
from sklearn import preprocessing
import os

# read vectors
def read_vectors(vec_dir_path):
    filtered_data = list()
    for filename in os.listdir(vec_dir_path):
        if "vectors" in filename:
            filepath = vec_dir_path + "/" + filename
            # convert the file to array of objects
            data = np.array(np.genfromtxt(filepath, delimiter=',', autostrip=True))
            data=data[1:data.size-1] # cut headline
            filtered_data.append(data)
    filtered_data = np.asarray(filtered_data)[0]
    return filtered_data


def scale_and_filter_vectors_with_negative(filtered_data):
    # cut headline
   # sz = filtered_data.size
   # filtered_data = filtered_data[1:sz]

    # save labels
    lsz=len(filtered_data[0])-1
    labels = filtered_data[:, lsz]
    for i in range(0, len(labels)):
        labels[i] = int(labels[i])

    # cut labels
    scaled_filtered_data = preprocessing.scale(filtered_data)
    scaled_filtered_data = scaled_filtered_data[:, :-1]

    return scaled_filtered_data, labels

def scale_and_filter_vectors_without_negative(filtered_data):
    # cut headline
  #  sz = filtered_data.size
  #  filtered_data = filtered_data[1:sz]

    # save labels
    lsz=len(filtered_data[0])-1
    labels = filtered_data[:, lsz]
    for i in range(0, len(labels)):
        labels[i] = int(labels[i])

    # cut labels
    filtered_data = filtered_data[:, :-1]

    return filtered_data, labels
