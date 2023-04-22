
% This function is used to seperate the phasic and tonic components of raw
% data using filtering.
function [tonic, phasic] = tonicPhasicFilter(x, fs)

    % Perform a lowpass filter to get the tonic component:
    cutoffFreq = 0.005; %Hz
    order = 64;

    firLPF = designfilt('lowpassfir','FilterOrder',order, ...
        'CutoffFrequency',cutoffFreq,'SampleRate',fs);

    tonic = filtfilt(firLPF,x);
    phasic = x - tonic;
end
