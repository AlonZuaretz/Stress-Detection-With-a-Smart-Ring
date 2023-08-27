import neurokit2 as nk
import numpy as np
import pandas as pd
import sparsEDA

eda_df = pd.read_csv("C:/Lilach/Technion/Project A/09042023_10-03-44-09042023_10-06-51.csv")
eda_signal = eda_df["raw"].values

def feature_extraction(eda_signal, fs, decompose_method):
    #extra_features_df = pd.DataFrame([]) # In case we want to extract more features using cvxEDA (not from neurokit)

    # Phasic and Tonic Decomposition
    if decompose_method == 'highpass':
        decomposed_eda_df = nk.eda_phasic(eda_signal, sampling_rate=fs, method='highpass')

    elif decompose_method == 'cvxEDA':
        decomposed_eda_df = nk.eda_phasic(eda_signal, sampling_rate=fs, method='cvxEDA')

    elif decompose_method == 'sparsEDA':
        [_, scl, _] = sparsEDA.sparsEDA(eda_signal, sr=fs, epsilon=0.001, Kmax=500, dmin=1.25*fs, rho=0.025)
        decomposed_eda_df = pd.DataFrame([])
        decomposed_eda_df["EDA_Tonic"] = scl
        decomposed_eda_df["EDA_Phasic"] = eda_signal - scl

    # SCR Peaks Detection
    eda_phasic = decomposed_eda_df["EDA_Phasic"].values
    peak_signal, peaks_info = nk.eda_peaks(eda_phasic, sampling_rate=fs, method='neurokit', amplitude_min=0.1) #amplitude_min can be changed

    #process_signals, process_info = nk.eda_process(eda_signal, sampling_rate=fs, method='neurokit')

    # Feature Extraction for Classification
    Tonic_mean = np.nanmean(decomposed_eda_df["EDA_Tonic"])
    Tonic_std = np.std(decomposed_eda_df["EDA_Tonic"])
    Tonic_median = np.median(decomposed_eda_df["EDA_Tonic"])
    Phasic_mean = np.nanmean(decomposed_eda_df["EDA_Phasic"])
    Phasic_std = np.std(decomposed_eda_df["EDA_Phasic"])
    Phasic_median = np.median(decomposed_eda_df["EDA_Phasic"])
    SCR_num = len(peaks_info["SCR_Peaks"])
    SCR_mean_amplitude = np.nan_to_num(np.nanmean(peaks_info["SCR_Amplitude"]))
    SCR_mean_riseTime = np.nan_to_num(np.nanmean(peaks_info["SCR_RiseTime"]))
    SCR_mean_recoveryTime = np.nan_to_num(np.nanmean(peaks_info["SCR_RecoveryTime"]))
    SCR_mean_height = np.nan_to_num(np.nanmean(peaks_info["SCR_Height"]))
    SCR_std_height = np.nan_to_num(np.std(peaks_info["SCR_Height"]))

    eda_mean = np.nanmean(eda_signal)
    eda_std = np.std(eda_signal)
    eda_median = np.median(eda_signal)
    eda_max = np.max(eda_signal)
    eda_min = np.min(eda_signal)

    eda_derivative_1 = np.gradient(eda_signal)
    eda_mean_derivative_1 = np.nanmean(eda_derivative_1)
    eda_std_derivative_1 = np.std(eda_derivative_1)
    eda_derivative_2 = np.gradient(eda_signal, edge_order=2)
    eda_mean_derivative_2 = np.nanmean(eda_derivative_2)
    eda_std_derivative_2 = np.std(eda_derivative_2)

    # Dynamic range between the max and min value in every 5 second window
    max_of_5 = [max(eda_signal[i:i + 5*fs]) for i in range(0, len(eda_signal), 5*fs)]
    min_of_5 = [min(eda_signal[i:i + 5*fs]) for i in range(0, len(eda_signal), 5*fs)]
    dynamic_range_mean = np.nanmean(np.array(max_of_5) - np.array(min_of_5))


    features = pd.DataFrame([[Tonic_mean, Tonic_std, Tonic_median, Phasic_mean, Phasic_std, Phasic_median, SCR_num,
                            SCR_mean_amplitude, SCR_mean_riseTime, SCR_mean_recoveryTime, SCR_mean_height, SCR_std_height,
                            eda_mean, eda_std, eda_median, eda_max, eda_min, eda_mean_derivative_1, eda_std_derivative_1,
                            eda_mean_derivative_2, eda_std_derivative_2, dynamic_range_mean]],
                            columns=['Tonic_mean', 'Tonic_std', 'Tonic_median', 'Phasic_mean',
                                     'Phasic_std', 'Phasic_median', 'SCR_num', 'SCR_mean_amplitude', 'SCR_mean_riseTime',
                                     'SCR_mean_recoveryTime', 'SCR_mean_height', 'SCR_std_height','eda_mean', 'eda_std',
                                     'eda_median', 'eda_max', 'eda_min', 'eda_mean_derivative_1', 'eda_std_derivative_1',
                                     'eda_mean_derivative_2', 'eda_std_derivative_2', 'dynamic_range_mean'])
    return features

features = feature_extraction(eda_signal, 3, decompose_method='cvxEDA')
print(features)
