from helper_fcn_data import extract_data, import_data
from helper_fcn_classify import classification, our_tsne
from helper_fcn_process import preprocessing, feature_extraction
import pandas as pd
import numpy as np
import warnings

if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    # Parameters:

    # Preprocess:
    norm_method = "Standardization"
    # norm_method = "Normalization"

    # Tonic Phasic Seperation:
    decompose_method = 'cvxEDA'
    # decompose_method = 'sparsEDA'
    # decompose_method = 'highpass'

    amplitude_min = 0.1

    # Classification:
    K = 5 # Neighbors for KNN classifier
    classifier = "KNN"
    # classifier = "SVM"

    # selection_method = "RFE"
    selection_method = "None"
    # selection_method = "EFS"

    kernel = 'linear'
    norm_flag = False
    train_size = 0.73

    # Extract data:
    EDA_files, files_num, samples_num, vids_per_CEAP, exp_str, user_exp_str = import_data()
    raw_eda, fs, labels, experiment, participantID, exp_type = extract_data(EDA_files, files_num, samples_num, vids_per_CEAP, exp_str,
                                                   user_exp_str)

    # Preprocess data:
    preprocessed_EDA = [[] for x in range(samples_num)]
    var = [[] for x in range(samples_num)]
    cutoff_freq = 0.5
    for i in range(samples_num):
        preprocessed_EDA[i], var[i] = preprocessing(raw_eda[i], fs[i],
                                                    norm_method, cutoff_freq)

    # Feature Extraction:
    # features is a matrix of size M by N (or N by M) where N is the number of samples
    # and M is the number of features

    features_df = pd.DataFrame([],
                               columns=['Tonic_energy', 'Tonic_mean', 'Tonic_std', 'Tonic_median', 'Phasic_energy',
                                        'Phasic_mean',
                                        'Phasic_std', 'Phasic_median', 'SCR_num', 'SCR_mean_amplitude',
                                        'SCR_mean_riseTime',
                                        'SCR_mean_recoveryTime', 'SCR_mean_height', 'SCR_std_height', 'eda_energy',
                                        'eda_mean', 'eda_std',
                                        'eda_median', 'eda_max', 'eda_min', 'eda_mean_derivative_1',
                                        'eda_std_derivative_1',
                                        'eda_mean_derivative_2', 'eda_std_derivative_2', 'wvt_energy', 'wvt_mean',
                                        'wvt_std',
                                        'wvt_median', 'wvt_energy_1p5hz', 'wvt_mean_1p5hz', 'wvt_std_1p5hz',
                                        'wvt_median_1p5hz',
                                        'wvt_energy_0p75hz', 'wvt_mean_0p75hz', 'wvt_std_0p75hz',
                                        'wvt_median_0p75hz',
                                        'dynamic_range_mean'])
    for i in range(samples_num):
        try:
            new_row = feature_extraction(preprocessed_EDA[i], fs[i], var[i],
                                            decompose_method, amplitude_min)
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

    accuracy = classification(X, y, kernel, norm_flag, train_size,
                                   features_df.columns, classifier, selection_method, K)

    our_tsne(X, experiment, exp_type, participantID, labels, norm_flag)




    



