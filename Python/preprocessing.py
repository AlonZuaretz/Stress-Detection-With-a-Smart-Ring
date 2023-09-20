import neurokit2 as nk
import numpy as np


def preprocessing(raw_eda, fs, norm_method, cutoff_freq):
    # Filter the data:
    filtered_eda = nk.signal_filter(raw_eda, fs, highcut=cutoff_freq, order=4, method="butterworth")

    if norm_method == "Normalization":
        max_val = max(filtered_eda)
        min_val = min(filtered_eda)
        eda = (filtered_eda - min_val) / (max_val - min_val)
        var = np.var(eda)

    elif norm_method == "Standardization":
        var = np.var(filtered_eda)
        mu = np.mean(filtered_eda)
        eda = (filtered_eda - mu) / np.sqrt(var)

    return eda, var
