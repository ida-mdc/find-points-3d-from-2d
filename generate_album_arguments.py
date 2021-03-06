import pandas as pd
import yaml
import os
import json

# From functions_common module


def read_parameters():
    parameters = dict()

    with open("base/parameters.yml") as file:
        parameters = yaml.load(file, Loader=yaml.FullLoader)
    with open("local/parameters.yml") as file:
        parameters_local = yaml.load(file, Loader=yaml.FullLoader)

    # overwrite global parameters with local setting
    for key in parameters_local:
        parameters[key] = parameters_local[key]

    return parameters


def read_key_file(parameters):
    file_path = parameters['data_folder'] + parameters["key_file_path"]

    key_file = pd.read_excel(file_path)

    return key_file


### read parameters

parameters = read_parameters()
print("#" * 5, "parameters", "#" * 5)
print(parameters)
key_file = read_key_file(parameters)
print("#" * 5, "key_file", "#" * 5)
print(key_file.head())

data_path = parameters["data_folder"]
folder_2d_data = "/03_Preprocessed_Data/01_2D/"
folder_3d_data = "/03_Preprocessed_Data/02_3D/"
folder_macrophage_annotations = '/04_Processed_Data/01_Annotated_Macrophages/'
use_gpu = parameters["use_gpu"]
output_folder = parameters["output_folder"]
experiments = "annotated"
#experiments = "all"

param_list = []

for index, row in key_file.iterrows():

    short_name = str(row["short_name"])
    file_path = data_path + folder_3d_data + short_name + ".tif"
    csv_path = data_path + folder_macrophage_annotations + short_name + ".tif"
    
    # print([index, row])

    if not os.path.exists(file_path):
        continue

    if (experiments == "annotated") and (not row["macrophages_annotated"]):
        print("No annotation available for %s" % short_name)
        continue

    # print("open image file %s" % file_path)

    args = {'image_filename':file_path, 'csv_filename':csv_path}
    param_list += [args]

with open('arguments.json', 'w') as fout:
    json.dump(param_list, fout)
