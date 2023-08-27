import numpy as np
import pandas as pd
import json

# Documentation:
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

    if experiment == "Ring Experiment":
        df = pd.read_csv(path)
        fs = 3
        raw_eda = df.raw
        N_samples = len(raw_eda)
        time_stamps = df['time(sec)']
        start_date_stamp = df['date_time'][0]
        if ():
            label = 1
        else:
            label = -1
        device = "Ring"
        participantID = ''
        df_flag = True
##
    elif experiment == "Empatica SIPL Experiment":
        df = pd.read_csv(path)
        start_date_stamp = df.columns.values[0]
        fs = df[start_date_stamp][0]
        raw_eda = df[start_date_stamp][2:]
        N_samples = len(raw_eda)
        time_stamps = np.arange(0, N_samples)/fs

        if ():
            label = 1
        else:
            label = -1


        device = "Empatica E4"
        participantID = ''
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

        json_df = pd.json_normalize(data,  record_path=['Physio_RawData', 'Video_Physio_RawData'])
        json_df = json_df.drop(columns=['ACC_RawData', 'SKT_RawData', 'BVP_RawData', 'IBI_RawData', 'HR_RawData'])

        for row in range(len(json_df)):
            df_tmp = pd.DataFrame([])
            df_dict[json_df['VideoID'][row]] = {}
            N_samples = len(json_df['EDA_RawData'][row])

            tmp_eda = np.zeros(N_samples)
            tmp_timestamp = np.zeros(N_samples)
            for i in range(N_samples):
                tmp_eda[i] = json_df['EDA_RawData'][row][i]['EDA']
                tmp_timestamp[i] = json_df['EDA_RawData'][row][i]['TimeStamp']

            df_tmp['Raw EDA'] = tmp_eda
            df_tmp['Time Stamps'] = tmp_timestamp
            df_dict[json_df['VideoID'][row]]['Data'] = df_tmp
            df_dict[json_df['VideoID'][row]]['Number of Samples'] = N_samples
            df_dict[json_df['VideoID'][row]]['Label'] = ' '
        df_flag = False
##

    if df_flag:
        df_dict = {}
        df_tmp = pd.DataFrame([])
        df_dict['Sample Path'] = path
        df_dict['Participant ID'] = participantID
        # df_dict['Start Date and Time'] = start_date_stamp
        df_dict['Device'] = device
        df_dict['Number of Samples'] = N_samples
        df_dict['Sampling Rate'] = fs
        df_dict['Label'] = label
        df_tmp['Raw EDA'] = raw_eda
        df_tmp['Time Stamps'] = time_stamps
        df_dict['Data'] = df_tmp
    return df_dict
