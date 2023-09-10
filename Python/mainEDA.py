from load_data import load_data
from load_data import glob_filetypes
from preprocessing import preprocessing
from tkinter import Tk
from tkinter.filedialog import askdirectory
import matplotlib.pyplot as plt
import glob
import os
# import feature_extraction as fe
# import features_selection

# TODO: extract data from the CEAP_360VR experiment and add labels
# TODO: fix the array index shift when reading with [2:] in load_data
# TODO: add a method to determine labels from ECSMP_A files
# What's making things hard is that experiment CEAP_360VR has 8 samples in each file

# Select The experiment:
print("Select the experiment: \n 1 for Ring \n 2 for Old project \n 3 for CEAP_360VR \n"
      " 4 for UBFC-phys \n 5 for ECSMP_A \n 10 for all experiments \n")
user_exp = input("Experiment number is: ")
if user_exp == str(1):
    user_exp_str = "Ring Experiment"
    exp_identifier = 'ring'
elif user_exp == str(2):
    user_exp_str = "Empatica SIPL Experiment"
    exp_identifier = 'EDA_'
elif user_exp == str(3):
    user_exp_str = "CEAP_360VR"
    exp_identifier = ''
elif user_exp == str(4):
    user_exp_str = "UBFC-phys"
    exp_identifier = 'eda'
elif user_exp == str(5):
    user_exp_str = "ECSMP_A"
    exp_identifier = 'EDA'
elif user_exp == str(10):
    user_exp_str = "all"
    exp_identifier = ''
# Default
else:
    user_exp_str = "Ring Experiment"
    exp_identifier = '.csv'

# Get the path of folder:
# For Alon:
initial_dir = "C:/Users/alonz/OneDrive - Technion/תואר/פרויקט/project" \
              " - Stress Detection with a Smart Ring/samples and data/for_classification"
# For Lilach:
# initial_dir =

PATH = askdirectory(initialdir=initial_dir)

# Get a list of all the files that match file identifier:
# the for in for goes over all files in directory and its subdirectories
EDA_files = []
if user_exp_str == "all":
    exp_str = []
    for path, subdir, files in os.walk(PATH):
        for file in glob_filetypes(path, '*.csv', '*.json'):
            if "SIPL Project" in path:
                exp_str.append("Empatica SIPL Experiment")
                EDA_files.append(file)
            elif "UBFC_phys" in path:
                if "eda" in file:
                    EDA_files.append(file)
                    exp_str.append("UBFC-phys")
            elif "Ring Samples" in path:
                exp_str.append("Ring Experiment")
                EDA_files.append(file)
            elif "ECSMP_ A - only EDA" in path:
                if "EDA" in file:
                    exp_str.append("ECSMP_A")
                    EDA_files.append(file)
            elif "CEAP_360VR" in path:
                exp_str.append("CEAP_360VR")
                EDA_files.append(file)

elif user_exp_str == "CEAP_360VR":
    for path, subdir, files in os.walk(PATH):
        for file in glob.glob(os.path.join(path, '*.json')):
            EDA_files.append(file)

else:
    for path, subdir, files in os.walk(PATH):
        for file in glob.glob(os.path.join(path, '*.csv')):
            if exp_identifier in file:
                EDA_files.append(file)

files_num = len(EDA_files)

# Initialize variables to store data from file
eda_dict = [dict() for x in range(files_num)]
raw_eda = [0] * files_num
time_stamps = [0] * files_num
fs = [0] * files_num
label = [0] * files_num
experiment = [''] * files_num
participantID = [''] * files_num
device = [''] * files_num

# Without considering CEAP_360VR:
for i in range(files_num):
    if user_exp_str == "all":
        eda_dict[i] = load_data(EDA_files[i], exp_str[i])
    else:
        eda_dict[i] = load_data(EDA_files[i], user_exp_str)

    raw_eda[i] = eda_dict[i]['Data']['Raw EDA']
    time_stamps[i] = eda_dict[i]['Data']['Time Stamps']
    fs[i] = eda_dict[i]['Sampling Rate']
    label[i] = eda_dict[i]['Label']
    experiment[i] = eda_dict[i]['Experiment']
    participantID[i] = eda_dict[i]['Participant ID']
    device[i] = eda_dict[i]['Device']

# eda_dict has the following fields for each array cell:
# Number of samples, Sampling rate, Participant ID, Device, Label, DataFrame that holds the EDA and Time stamps

"""
# For TODO read files from CEAP_360VR
Initialize variables:

for i in range(files_num):
    if i >= csv_json_sep:
        # Extract data in a certain way
    else:
    eda_dict[i] = load_data(EDA_files[i], experiment[i])
    raw_eda[i] = eda_dict[i]['Data']['Raw EDA']
    time_stamps[i] = eda_dict[i]['Data']['Time Stamps']
    fs[i] = eda_dict[i]['Sampling Rate']
    label[i] = eda_dict[i]['Label']
    experiment[i] = [''] = eda_dict[i]['Experiment']
"""

# Preprocess data:
preprocessed_EDA = [[] for x in range(files_num)]
var = [[] for x in range(files_num)]
for i in range(files_num):
    preprocessed_EDA[i], var[i] = preprocessing(raw_eda[i], fs[i])

# Feature Extraction:
# features is a matrix of size M by N (or N by M) where N is the number of samples
# and M is the number of features

"""
features = [[] for x in range(files_num)]
for i in range(files_num):
    preprocessed_EDA[i], var[i] = preprocessing(raw_eda[i], fs[i])
    tonic_phasic_method = ''
    features[i] = fe(preprocessed_EDA[i], fs[i], tonic_phasic_method )
#filtered_features = features_selection()
"""


# Train-Test Split:
# X_train, X_test, y_train, y_test =

# Train the model using the training sets
# clf.fit(X_train, y_train)
#
# Predict the response for test dataset
# y_pred = clf.predict(X_test)
#
# Print score
# print("accuracy: ", metrics.accuracy_score(y_test, y_pred))
