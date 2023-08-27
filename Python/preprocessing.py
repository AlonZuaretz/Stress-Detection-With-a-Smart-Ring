import neurokit2 as nk
import numpy as np


def preprocessing(raw_eda, fs):
    # Filter the data:
    filtered_eda = nk.signal_filter(raw_eda, fs, highcut=0.5, order=4, method="butterworth")

    # Z score Normalization:
    var = np.var(filtered_eda)
    mu = np.mean(filtered_eda)
    eda = (filtered_eda-mu)/np.sqrt(var)
    return eda, var



