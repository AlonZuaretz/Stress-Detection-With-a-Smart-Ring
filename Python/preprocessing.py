import neuroki2 as nk
import numpy as np
def preprocessing(raw_eda, fs)
    filtered_eda = nk.signal_filter(raw_eda, fs, highcut = 0.5, order = 4, method = "butterworth")
    eda = nk.standardize(filtered_eda, robust = True)

    ## Tonic and Phasic seperation:

    ## Using cvxEDA
    seperated_cvxEDA = nk.eda_phasic(eda, sampling_rate=fs, method="cvxEDA")
    tonic_cvxEDA, phasic_cvxEDA = seperated_cvxEDA["EDA_Tonic"].values.tolist(), seperated_cvxEDA["EDA_Phasic"].values.tolist()


    ## Using cvxEDA