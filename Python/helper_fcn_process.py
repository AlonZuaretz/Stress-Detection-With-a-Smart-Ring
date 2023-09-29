import neurokit2 as nk
import numpy as np
import pandas as pd
import sparsEDA
import pywt

def moving_avg(input, window_size):
    result = []
    moving_sum = sum(input[:window_size])
    result.append(moving_sum/window_size)
    for i in range(len(input)-window_size):
        moving_sum += (input[i+window_size]-input[i])
        result.append(moving_sum/window_size)
    return result


def preprocessing(raw_eda, fs, norm_method="Standardization", cutoff_freq=0.2, order=4, window_size=20):
    # Filter the data:
    filtered_eda = nk.signal_filter(raw_eda, fs, highcut=cutoff_freq, order=order, method="butterworth")

    mavg_filtered_eda = moving_avg(filtered_eda, window_size)
    # mavg_filtered_eda = filtered_eda

    if norm_method == "Normalization":
        max_val = max(mavg_filtered_eda)
        min_val = min(mavg_filtered_eda)
        eda = (mavg_filtered_eda - min_val) / (max_val - min_val)
        var = np.var(eda)

    elif norm_method == "Standardization":
        var = np.var(mavg_filtered_eda)
        mu = np.mean(mavg_filtered_eda)
        eda = (mavg_filtered_eda - mu) / np.sqrt(var)

    return eda, var


def feature_extraction(eda_signal, fs, eda_var, decompose_method, amplitude_min):
    fs = int(fs)
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
    peak_signal, peaks_info = nk.eda_peaks(eda_phasic, sampling_rate=fs, method='neurokit', amplitude_min=amplitude_min) #amplitude_min can be changed

    #process_signals, process_info = nk.eda_process(eda_signal, sampling_rate=fs, method='neurokit')

    # Feature Extraction for Classification
    Tonic_energy = np.sum(np.power(decomposed_eda_df["EDA_Tonic"], 2))/len(decomposed_eda_df["EDA_Tonic"])
    Tonic_mean = np.nanmean(decomposed_eda_df["EDA_Tonic"])
    Tonic_std = np.std(decomposed_eda_df["EDA_Tonic"])
    Tonic_median = np.median(decomposed_eda_df["EDA_Tonic"])
    Phasic_energy = np.sum(np.power(decomposed_eda_df["EDA_Phasic"], 2))/len(decomposed_eda_df["EDA_Phasic"])
    Phasic_mean = np.nanmean(decomposed_eda_df["EDA_Phasic"])
    Phasic_std = np.std(decomposed_eda_df["EDA_Phasic"])
    Phasic_median = np.median(decomposed_eda_df["EDA_Phasic"])
    SCR_num = len(peaks_info["SCR_Peaks"])
    try:
        SCR_mean_amplitude = np.nan_to_num(np.nanmean(peaks_info["SCR_Amplitude"]))
        SCR_mean_riseTime = np.nan_to_num(np.nanmean(peaks_info["SCR_RiseTime"]))
        SCR_mean_recoveryTime = np.nan_to_num(np.nanmean(peaks_info["SCR_RecoveryTime"]))
        SCR_mean_height = np.nan_to_num(np.nanmean(peaks_info["SCR_Height"]))
        SCR_std_height = np.nan_to_num(np.std(peaks_info["SCR_Height"]))
    except RuntimeWarning:
        a = 5

    eda_energy = np.sum(np.power(eda_signal, 2))/len(eda_signal)
    eda_mean = np.nanmean(eda_signal)
    eda_std = np.sqrt(eda_var)
    eda_median = np.median(eda_signal)
    eda_max = np.max(eda_signal)
    eda_min = np.min(eda_signal)

    eda_derivative_1 = np.gradient(eda_signal)
    eda_mean_derivative_1 = np.nanmean(eda_derivative_1)
    eda_std_derivative_1 = np.std(eda_derivative_1)
    eda_derivative_2 = np.gradient(eda_signal, edge_order=2)
    eda_mean_derivative_2 = np.nanmean(eda_derivative_2)
    eda_std_derivative_2 = np.std(eda_derivative_2)

    # wavelet transform features - 3 Hz
    wvt_coeff = pywt.dwt(eda_signal, 'haar')
    wvt_energy = np.sum(np.power(wvt_coeff,2))
    wvt_mean = np.nanmean(wvt_coeff)
    wvt_std = np.std(wvt_coeff)
    wvt_median = np.median(wvt_coeff)

    # wavelet transform features - 1.5 Hz
    eda_signal_1p5hz = eda_signal[::2]
    wvt_coeff_1p5hz = pywt.dwt(eda_signal_1p5hz, 'haar')
    wvt_energy_1p5hz = np.sum(np.power(wvt_coeff_1p5hz, 2))
    wvt_mean_1p5hz = np.nanmean(wvt_coeff_1p5hz)
    wvt_std_1p5hz = np.std(wvt_coeff_1p5hz)
    wvt_median_1p5hz = np.median(wvt_coeff_1p5hz)

    # wavelet transform features - 0.75 Hz
    eda_signal_0p75hz = eda_signal[::4]
    wvt_coeff_0p75hz = pywt.dwt(eda_signal_0p75hz, 'haar')
    wvt_energy_0p75hz = np.sum(np.power(wvt_coeff_0p75hz, 2))
    wvt_mean_0p75hz = np.nanmean(wvt_coeff_0p75hz)
    wvt_std_0p75hz = np.std(wvt_coeff_0p75hz)
    wvt_median_0p75hz = np.median(wvt_coeff_0p75hz)

    # Dynamic range between the max and min value in every 5 second window
    max_of_5 = [max(eda_signal[i:i + 5*fs]) for i in range(0, len(eda_signal), 5*fs)]
    min_of_5 = [min(eda_signal[i:i + 5*fs]) for i in range(0, len(eda_signal), 5*fs)]
    dynamic_range_mean = np.nanmean(np.array(max_of_5) - np.array(min_of_5))

    features = pd.DataFrame([[Tonic_energy, Tonic_mean, Tonic_std, Tonic_median, Phasic_energy, Phasic_mean, Phasic_std,
                            Phasic_median, SCR_num, SCR_mean_amplitude, SCR_mean_riseTime, SCR_mean_recoveryTime,
                            SCR_mean_height, SCR_std_height, eda_energy, eda_mean, eda_std, eda_median, eda_max, eda_min,
                            eda_mean_derivative_1, eda_std_derivative_1, eda_mean_derivative_2, eda_std_derivative_2,
                            wvt_energy, wvt_mean, wvt_std, wvt_median, wvt_energy_1p5hz, wvt_mean_1p5hz, wvt_std_1p5hz,
                            wvt_median_1p5hz, wvt_energy_0p75hz, wvt_mean_0p75hz, wvt_std_0p75hz, wvt_median_0p75hz,
                            dynamic_range_mean]],
                            columns=['Tonic_energy', 'Tonic_mean', 'Tonic_std', 'Tonic_median', 'Phasic_energy', 'Phasic_mean',
                                     'Phasic_std', 'Phasic_median', 'SCR_num', 'SCR_mean_amplitude', 'SCR_mean_riseTime',
                                     'SCR_mean_recoveryTime', 'SCR_mean_height', 'SCR_std_height', 'eda_energy', 'eda_mean', 'eda_std',
                                     'eda_median', 'eda_max', 'eda_min', 'eda_mean_derivative_1', 'eda_std_derivative_1',
                                     'eda_mean_derivative_2', 'eda_std_derivative_2','wvt_energy', 'wvt_mean', 'wvt_std',
                                     'wvt_median', 'wvt_energy_1p5hz', 'wvt_mean_1p5hz', 'wvt_std_1p5hz', 'wvt_median_1p5hz',
                                     'wvt_energy_0p75hz', 'wvt_mean_0p75hz', 'wvt_std_0p75hz', 'wvt_median_0p75hz',
                                     'dynamic_range_mean'])
    return features