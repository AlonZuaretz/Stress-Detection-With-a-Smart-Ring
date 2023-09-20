from load_data import load_data
from load_data import glob_filetypes
from preprocessing import preprocessing
from tkinter.filedialog import askdirectory
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn import metrics
from tkinter import Tk
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import RFE
from mlxtend.feature_selection import ExhaustiveFeatureSelector as EFS

import glob
import os
import feature_extraction as fe
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def classification(X, y, kernel, norm_flag, train_size, feature_names, selection_method = 'None'):
    test_size = 1-train_size

    # Train-Test Split:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, train_size=train_size, shuffle=True,
                                                        random_state=5)
    clf = svm.SVC(kernel=kernel)  # Sigmoid Kernel

    if norm_flag:
        # fit scaler on training data
        norm = MinMaxScaler().fit(X_train)
        # transform training data
        X_train = norm.transform(X_train)
        # transform testing dataabs
        X_test = norm.transform(X_test)

    if selection_method == "RFE":
        ## Recursive Feature Elimination
        max_accur = 0
        selected_features = []
        N_features = len(feature_names)
        for i in range(0, N_features):
            rfe = RFE(clf, n_features_to_select=i + 1)
            rfe_fit = rfe.fit(X_train, y_train)

            y_pred = rfe.predict(X_test)
            accuracy = metrics.accuracy_score(y_test, y_pred)
            print("Number of features: ", i + 1)
            print("current accuracy: ", accuracy)
            feature_idx_temp = pd.Series(data=rfe_fit.ranking_, index=feature_names)
            selected_features_temp = feature_idx_temp[feature_idx_temp == 1].index
            print("temp Selected features are: ", selected_features_temp.values)

            if accuracy > max_accur:
                max_accur = accuracy
                feature_idx = pd.Series(data=rfe_fit.ranking_, index=feature_names)
                selected_features = feature_idx[feature_idx == 1].index

        print("Selected features are: ", selected_features.values)
        print("Final Accuracy: ", max_accur)

    elif selection_method == "EFS":
        # Exhaustive Feature Selection
        efs1 = EFS(clf, min_features=2, max_features=5, scoring='accuracy', print_progress=True)
        efs1 = efs1.fit(X_train, y_train)

        print('Best accuracy score: %.2f' % efs1.best_score_)
        print('Best subset (indices):', efs1.best_idx_)
        print('Best subset (corresponding names):', efs1.best_feature_names_)
        y_pred = efs1.predict(X_test)
        print("accuracy: ", metrics.accuracy_score(y_test, y_pred))

    elif selection_method == 'None':
        # Train the model:
        clf.fit(X_train, y_train)
        # Predict the response for test dataset:
        y_pred = clf.predict(X_test)
        print("accuracy: ", metrics.accuracy_score(y_test, y_pred))

def import_data():
    # Select The experiment:
    print("Select the experiment: \n 1 for Ring \n 2 for Old project \n 3 for CEAP_360VR \n"
          " 4 for UBFC-phys \n 10 for all experiments \n")
    user_exp = input("Experiment number is: ")
    user_exp_str = []
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
    elif user_exp == str(10):
        user_exp_str = "all"
        exp_identifier = ''
    # Default
    else:
        user_exp_str = "Ring Experiment"
        exp_identifier = '.csv'
    
    # Get the path of folder:
    # For Alon:
    # initial_dir = "C:/Users/alonz/OneDrive - Technion/תואר/פרויקט/project" \
    #              " - Stress Detection with a Smart Ring/samples and data/for_classification"

    initial_dir = "C:/Users/alonz/OneDrive - Technion/תואר/פרויקט/project - Stress Detection with a Smart Ring/samples and data/MoodMetric Ring/CSV/28_8"

    # For Lilach:
    # initial_dir = "C:/Users/yossi/OneDrive - Technion/סמסטר 6/פרויקט א/project - Stress Detection with a Smart Ring/samples and data/for_classification"
    
    # PATH = askdirectory(initialdir=initial_dir)
    PATH = initial_dir
    
    # Get a list of all the files that match file identifier:
    # the for in for goes over all files in directory and its subdirectories
    EDA_files = []
    exp_str = []
    ctr = 0
    if user_exp_str == "all":
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
                    ctr = ctr + 1
    
    elif user_exp_str == "CEAP_360VR":
        for path, subdir, files in os.walk(PATH):
            for file in glob.glob(os.path.join(path, '*.json')):
                EDA_files.append(file)
                ctr = ctr + 1
    
    else:
        for path, subdir, files in os.walk(PATH):
            for file in glob.glob(os.path.join(path, '*.csv')):
                if exp_identifier in file:
                    EDA_files.append(file)
    
    files_num = len(EDA_files)
    CEAP_files_num = ctr
    vids_per_CEAP = 4
    regular_files_num = files_num - CEAP_files_num
    samples_num = regular_files_num + vids_per_CEAP * CEAP_files_num

    return EDA_files, files_num, samples_num, vids_per_CEAP, exp_str, user_exp_str


def extract_data(EDA_files , files_num , samples_num , vids_per_CEAP, exp_str, user_exp_str):
    # Initialize variables to store data from file
    eda_dict = [dict() for x in range(samples_num)]
    raw_eda = [0] * samples_num
    time_stamps = [0] * samples_num
    fs = [0] * samples_num
    labels = [0] * samples_num
    experiment = [''] * samples_num
    participantID = [''] * samples_num
    device = [''] * samples_num

    # eda_dict has the following fields for each array cell:
    # Number of samples, Sampling rate, Participant ID, Device, Label, DataFrame that holds the EDA and Time stamps

    j = 0
    for i in range(files_num):
        if user_exp_str == "all":
            eda_dict[i] = load_data(EDA_files[i], exp_str[i])
        else:
            eda_dict[i] = load_data(EDA_files[i], user_exp_str)

        if (user_exp_str == "all" and exp_str[i] == "CEAP_360VR") or user_exp_str == "CEAP_360VR":
            vidIdx = 0
            for vidID in ['V2', 'V3', 'V6', 'V7']:
                raw_eda[j + vidIdx] = eda_dict[i][vidID]['Data']['Raw EDA']
                time_stamps[j + vidIdx] = eda_dict[i][vidID]['Data']['Time Stamps']
                fs[j + vidIdx] = eda_dict[i]['Sampling Rate']
                labels[j + vidIdx] = eda_dict[i][vidID]['Label']
                experiment[j + vidIdx] = eda_dict[i]['Experiment']
                participantID[j + vidIdx] = eda_dict[i]['Participant ID']
                device[j + vidIdx] = eda_dict[i]['Device']
                vidIdx += 1
            j += vids_per_CEAP
        else:
            raw_eda[j] = eda_dict[i]['Data']['Raw EDA']
            time_stamps[j] = eda_dict[i]['Data']['Time Stamps']
            fs[j] = eda_dict[i]['Sampling Rate']
            labels[j] = eda_dict[i]['Label']
            experiment[j] = eda_dict[i]['Experiment']
            participantID[j] = eda_dict[i]['Participant ID']
            device[j] = eda_dict[i]['Device']
            j += 1
    return raw_eda, fs, labels


if __name__=="__main__":

    # Parameters:
    cutoff_freq = 0.1
    norm_method = "Standardization"
    # norm_method = "Normalization"
    selection_method = "EFS"
    kernel = 'linear'
    norm_flag = True
    train_size = 0.7
    decompose_method = 'cvxEDA'


    EDA_files, files_num, samples_num, vids_per_CEAP, exp_str, user_exp_str = import_data()
    raw_eda, fs, labels = extract_data(EDA_files, files_num, samples_num, vids_per_CEAP, exp_str, user_exp_str)

    # Preprocess data:


    preprocessed_EDA = [[] for x in range(samples_num)]
    var = [[] for x in range(samples_num)]
    for i in range(samples_num):
        preprocessed_EDA[i], var[i] = preprocessing(raw_eda[i], fs[i], norm_method, cutoff_freq)

    # Feature Extraction:
    # features is a matrix of size M by N (or N by M) where N is the number of samples
    # and M is the number of features
    features_df = pd.DataFrame([],
           columns=['Tonic_energy', 'Tonic_mean', 'Tonic_std', 'Tonic_median', 'Phasic_energy',
                    'Phasic_mean',
                    'Phasic_std', 'Phasic_median', 'SCR_num', 'SCR_mean_amplitude', 'SCR_mean_riseTime',
                    'SCR_mean_recoveryTime', 'SCR_mean_height', 'SCR_std_height', 'eda_energy',
                    'eda_mean', 'eda_std',
                    'eda_median', 'eda_max', 'eda_min', 'eda_mean_derivative_1', 'eda_std_derivative_1',
                    'eda_mean_derivative_2', 'eda_std_derivative_2', 'wvt_energy', 'wvt_mean',
                    'wvt_std',
                    'wvt_median', 'wvt_energy_1p5hz', 'wvt_mean_1p5hz', 'wvt_std_1p5hz',
                    'wvt_median_1p5hz',
                    'wvt_energy_0p75hz', 'wvt_mean_0p75hz', 'wvt_std_0p75hz', 'wvt_median_0p75hz',
                    'dynamic_range_mean'])

    for i in range(samples_num):
        try:
            new_row = fe.feature_extraction(preprocessed_EDA[i], fs[i], var[i], decompose_method)
            features_df = pd.concat([features_df, new_row], ignore_index=True)
        except IndexError:
            print("IndexError in file", EDA_files[i])
            del labels[i]
            continue
        except:
            print("Error in file", EDA_files[i])
            del labels[i]
            continue


    # ------- Classification  ------- #
    X = np.array(features_df)
    y = np.array(labels).squeeze()

    classification(X, y, kernel, norm_flag, train_size, features_df.columns, selection_method)


    



