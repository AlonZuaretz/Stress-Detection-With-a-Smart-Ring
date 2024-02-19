import numpy as np
import pandas as pd
import json
import os
import glob
from tkinter.filedialog import askdirectory


# Documentation load_data:
# Inputs: path to file, experiment : which experiment to load
# Output: dictionary
# For Ring Experiment and Empatica SIPL Experiment:
# Dictionary has the following fields:
# Number of samples, Sampling rate, Participant ID, Device, Label, DataFrame that holds the EDA and Time stamps
# For CEAP_360V$ Experiment:
# Dictionary has the following fields:
# Number of samples, Sampling rate, Participant ID, Device
# It also holds 8 more dictionaries (one for each experiment conducted)
# Each holds: Number of samples, Label, DataFrame that holds the EDA and Time stamps
# To access x experiment: dict['Vx'][Wanted field]

# Labels: stressed = 1, relaxed = -1

def load_data(path, experiment):

    file_name = os.path.basename(path)
    path_to_dir = os.path.dirname(path)
    folder = os.path.basename(path_to_dir)
    if experiment == "Ring Experiment":
        df = pd.read_csv(path)
        fs = 3
        raw_eda = df.raw
        N_samples = len(raw_eda)
        time_stamps = df['time(sec)']
        start_date_stamp = df['date_time'][0]

        #
        if "stress" in file_name:
            label = 1
            if "pres1" in file_name:
                exp_type = "P1"
            else:
                exp_type = "P2"

        elif "calm" in file_name:
            label = -1
            if "vid1" in file_name:
                exp_type = "V1"
            else:
                exp_type = "V2"

        device = "Ring"
        participantID = folder
        df_flag = True
##
    elif experiment == "Empatica SIPL Experiment":
        df = pd.read_csv(path)
        start_date_stamp = df.columns.values[0]
        fs = df[start_date_stamp][0]
        raw_eda = df[start_date_stamp][2:]
        raw_eda = raw_eda.reset_index(drop=True)
        N_samples = len(raw_eda)
        time_stamps = np.arange(0, N_samples)/fs

        if "V3" in file_name or "V4" in file_name:
            label = 1
        elif "V1" in file_name or "V2" in file_name:
            label = -1

        exp_type = ['']
        device = "Empatica E4"
        participantID = folder
        df_flag = True
##
    elif experiment == "CEAP_360VR":
        f = open(path)
        data = json.load(f)

        df_dict = {}
        participantID = data['Physio_RawData'][0]['ParticipantID']
        fs = 4

        df_dict['Sample Path'] = path
        df_dict['Sampling Rate'] = fs
        df_dict['Device'] = 'Empatica E4'
        df_dict['Participant ID'] = participantID
        df_dict['Experiment'] = experiment
        df_dict['exp_type'] = ['']

        json_df = pd.json_normalize(data,  record_path=['Physio_RawData', 'Video_Physio_RawData'])
        json_df = json_df.drop(columns=['ACC_RawData', 'SKT_RawData', 'BVP_RawData', 'IBI_RawData', 'HR_RawData'])
        idx = 0
        for row in range(len(json_df)):
            vidID = json_df['VideoID'][idx]
            if vidID == 'V3' or vidID == 'V7' or vidID == 'V2' or vidID == 'V6':
                df_tmp = pd.DataFrame([])
                df_dict[json_df['VideoID'][idx]] = {}
                N_samples = len(json_df['EDA_RawData'][idx])

                tmp_eda = np.zeros(N_samples)
                tmp_timestamp = np.zeros(N_samples)
                for i in range(N_samples):
                    tmp_eda[i] = json_df['EDA_RawData'][idx][i]['EDA']
                    tmp_timestamp[i] = json_df['EDA_RawData'][idx][i]['TimeStamp']

                df_tmp['Raw EDA'] = tmp_eda
                df_tmp['Time Stamps'] = tmp_timestamp
                df_dict[json_df['VideoID'][idx]]['Data'] = df_tmp
                df_dict[json_df['VideoID'][idx]]['Number of Samples'] = N_samples
                df_dict[json_df['VideoID'][idx]]['Label'] = 1 * (vidID == 'V3' or vidID == 'V7')\
                                                            - 1 * (vidID == 'V2' or vidID == 'V6')
                idx = idx + 1
            else:
                idx = idx + 1
        df_flag = False
##
    elif experiment == "UBFC-phys":
        df = pd.read_csv(path)
        fs = 4
        raw_eda = df.values
        N_samples = len(raw_eda)
        time_stamps = np.arange(0, N_samples) / fs
        participantID = folder
        device = "Empatica E4"

        # Determine label:
        f = open(os.path.join(path_to_dir, ("info_" + participantID + ".txt")), "r")
        exp_method = f.read()
        f.close()
        if "test" in exp_method and ("T2" in file_name or "T3" in file_name):
            label = 1
        else:
            label = -1

        if "test" in exp_method:
            if "T1" in file_name:
                exp_type = "T1"
            elif "T2" in file_name:
                exp_type = "T2"
            elif "T3" in file_name:
                exp_type = "T3"

        elif "ctrl" in exp_method:
            if "T1" in file_name:
                exp_type = "C1"
            elif "T2" in file_name:
                exp_type = "C2"
            elif "T3" in file_name:
                exp_type = "C3"

        df_flag = True


    if df_flag:
        df_dict = {}
        df_tmp = pd.DataFrame([])
        df_tmp['Raw EDA'] = []
        df_tmp['Time Stamps'] = []

        df_dict['Sample Path'] = path
        df_dict['Participant ID'] = participantID
        df_dict['Device'] = device
        df_dict['Number of Samples'] = N_samples
        df_dict['Sampling Rate'] = fs
        df_dict['Label'] = label
        df_dict['exp_type'] = exp_type
        df_tmp['Time Stamps'] = time_stamps
        df_tmp['Raw EDA'] = raw_eda
        df_dict['Data'] = df_tmp
        df_dict['Experiment'] = experiment
    return df_dict


def glob_filetypes(root_dir, *patterns):
    return [path
            for pattern in patterns
            for path in glob.glob(os.path.join(root_dir, pattern))]


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


    PATH = askdirectory()

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
    exp_type = [''] * samples_num
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
                exp_type[j + vidIdx] = eda_dict[i]['exp_type']
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
            exp_type[j] = eda_dict[i]['exp_type']
            experiment[j] = eda_dict[i]['Experiment']
            participantID[j] = eda_dict[i]['Participant ID']
            device[j] = eda_dict[i]['Device']
            j += 1
    return raw_eda, fs, labels, experiment, participantID, exp_type
