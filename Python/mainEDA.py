from load_data import load_data
from preprocessing import preprocessing
from tkinter import Tk
from tkinter.filedialog import askdirectory
import matplotlib.pyplot as plt
import glob
#import feature_extraction as fe
#import features_selection

# TODO: use multiple experiments to use a lot of data
# What's making things hard is that experiment CEAP has 8 samples in each file


# Select The experiment:
print("Select the experiment: \n 1 for Ring \n 2 for Old project \n 3 for CEAP_360VR \n 10 for all experiments \n")
user_exp = input("Experiment number is: ")
if user_exp == str(1):
    user_exp_str = "Ring Experiment"
    file_identifier = '/*.csv'
elif user_exp == str(2):
    user_exp_str = "Empatica SIPL Experiment"
    file_identifier = '/*.csv'
elif user_exp == str(3):
    user_exp_str = "CEAP_360VR"
    file_identifier = '/*.json'
elif user_exp == str(10):
    user_exp_str = "all"
    file_identifier = ''
# Default
else:
    user_exp_str = "Ring Experiment"

# Get the path of folder:
# For Alon:
in_dir = "C:/Users/alonz/OneDrive - Technion/תואר/פרויקט/project - Stress Detection with a Smart Ring/samples and data"
# For Lilach:
#in_dir =


path = askdirectory(initialdir=in_dir)
# Get a list of all the files that match file identifier:
files = glob.glob(path + file_identifier)
files_num = len(files)

# Initialize variables to store data from file
eda_dict = [dict() for x in range(files_num)]
raw_eda = [[] for x in range(files_num)]
time_stamps = [[] for x in range(files_num)]
fs = [0] * files_num
label = [0] * files_num
experiment = [''] * files_num


for i in range(files_num):
    eda_dict[i] = load_data(files[i], user_exp_str)
    raw_eda[i] = eda_dict[i]['Data']['Raw EDA']
    time_stamps[i] = eda_dict[i]['Data']['Time Stamps']
    fs[i] = eda_dict[i]['Sampling Rate']
    label[i] = eda_dict[i]['Label']

# eda_dict has the following fields for each array cell:
# Number of samples, Sampling rate, Participant ID, Device, Label, DataFrame that holds the EDA and Time stamps

plt.plot(time_stamps[1], raw_eda[1])
plt.show()

# For TODO
"""
for i in range(files_num):
    if experiment is CEAP_360VR:
        # Extract data in a certain way
    else:
    eda_dict[i] = load_data(files[i], experiment[i])
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

