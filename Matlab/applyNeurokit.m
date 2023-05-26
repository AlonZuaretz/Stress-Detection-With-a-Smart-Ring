function [tonic,phasic,tEDA_peaks,ampEDA_peaks] =  applyNeurokit(EDA, t)
%extract tonic and phasic components:
phasicMethod = 'Convex';
tonic = pyrunfile('neurokitMatlab.py', "tonic", ...
    eda_signal = EDA, phasicMethod = phasicMethod, peakMethod='');
phasic = pyrunfile('neurokitMatlab.py', "phasic", ...
    eda_signal = EDA, phasicMethod = phasicMethod, peakMethod='');
% transfer from pylist to matlab array:
tonic = double(tonic);
phasic = double(phasic);

%find peaks:
peakMethod = 'NeuroKit';
EDA_peaks = pyrunfile('neurokitMatlab.py', "EDA_peaks", ...
    eda_signal = phasic, phasicMethod = '',peakMethod=peakMethod);


%find the time and amplitude of the peaks to plot them:
tEDA_peaks = t(double(EDA_peaks)+1+1*strcmp(peakMethod,'Kim2004'));
ampEDA_peaks = phasic(double(EDA_peaks)+1+1*strcmp(peakMethod,'Kim2004'));