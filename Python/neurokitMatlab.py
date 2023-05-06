import neurokit2 as nk
import numpy as np


def neurokit(eda_signal, phasicMethod, peakMethod):
    # Separate components:
    if len(phasicMethod):
        match phasicMethod:
            case "Smooth Median":
                phasicmethod = "smoothmedian"
            case "High Pass":
                phasicmethod = "highpass"
            case "Convex":
                phasicmethod = "cvxEDA"
            case _:
                phasicmethod = "highpass"
                print("Default method was used - High Pass filter")

        phasic_df = nk.eda_phasic(eda_signal, sampling_rate=3, method=phasicmethod)
        tonic, phasic = phasic_df["EDA_Tonic"].values.tolist(), phasic_df["EDA_Phasic"].values.tolist()
        EDA_peaks = []

    # EDA Peaks:
    if len(peakMethod):
        phasic = np.array(eda_signal)
        match peakMethod:
            case "Kim2004":
                peakmethod = "kim2004"
            case "NeuroKit":
                peakmethod = "neurokit"
            case "Nabian2018":
                peakmethod = "nabian2018"
            case "Gamboa2008":
                peakmethod = "gamboa2008"
            case "Vanhalem2020":
                peakmethod = "vanhalem2020"
            case _:
                peakmethod = "neurokit"
        _, peaks_df = nk.eda_peaks(phasic, sampling_rate=3, method=peakmethod)
        EDA_peaks = peaks_df["SCR_Peaks"].tolist()
        tonic = []

    return tonic, phasic, EDA_peaks




tonic, phasic, EDA_peaks = neurokit(eda_signal, phasicMethod, peakMethod)


