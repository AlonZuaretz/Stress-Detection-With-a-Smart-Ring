from helper_fcn_data import extract_data, import_data
from helper_fcn_classify import classification, our_tsne
from helper_fcn_process import preprocessing, feature_extraction
import pandas as pd
import numpy as np

if __name__ == "__main__":

    # Parameters:

    # Preprocess:
    norm_method = "Standardization"
    # norm_method = "Normalization"

    # Tonic Phasic Seperation:
    decompose_method = 'cvxEDA'
    # decompose_method = 'sparsEDA'

    amplitude_min = 0.1

    # Classification:
    classifier = "KNN"
    # classifier = "SVM"

    # selection_method = "RFE"
    selection_method = "None"

    kernel = 'linear'
    norm_flag = False
    train_size = 0.74

    # Extract data:
    EDA_files, files_num, samples_num, vids_per_CEAP, exp_str, user_exp_str = import_data()
    raw_eda, fs, labels, experiment = extract_data(EDA_files, files_num, samples_num, vids_per_CEAP, exp_str,
                                                   user_exp_str)

    # Preprocess data:
    preprocessed_EDA = [[] for x in range(samples_num)]
    var = [[] for x in range(samples_num)]
    for i in range(samples_num):
        if experiment[i] == "CEAP_360VR":
            cutoff_freq = 0.5
            window_size = 1
        else:
            cutoff_freq = 0.5
            window_size = 1

        preprocessed_EDA[i], var[i] = preprocessing(raw_eda[i], fs[i],
                                                    norm_method, cutoff_freq, window_size=window_size)

    # Feature Extraction:
    # features is a matrix of size M by N (or N by M) where N is the number of samples
    # and M is the number of features

    # amplitude_min = np.linspace(0.01, 0.5, 20)
    amplitude_min = [0.1]
    accuracy = 0
    for j in range(len(amplitude_min)):
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
                                                decompose_method, amplitude_min[j])
                features_df = pd.concat([features_df, new_row], ignore_index=True)
            except IndexError:
                print("IndexError in file", EDA_files[i])
                del labels[i]
                continue
            except:
                print("Error in file", EDA_files[i])
                del labels[i]
                continue

        # features_df = features_df.drop(columns=['Tonic_energy', 'Phasic_energy'])

        # ------- Classification  ------- #
        X = np.array(features_df)
        y = np.array(labels).squeeze()

        accuracy_temp = classification(X, y, kernel, norm_flag, train_size,
                                       features_df.columns, classifier, selection_method)
        if accuracy_temp > accuracy:
            accuracy = accuracy_temp
            best_idx = j
        print(accuracy, j)
    print("best accuracy is: ", accuracy)
    print("best amplitude :", amplitude_min[best_idx])

    our_tsne(X, experiment, labels, norm_flag)




    



