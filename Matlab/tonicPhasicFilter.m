
% This function is used to seperate the phasic and tonic components of raw
% data using filtering.
function [tonic, phasic] = tonicPhasicFilter(x, fs, cutoffFreq, order)


    % Perform a lowpass filter to get the tonic component:
    if (nargin == 2)
        cutoffFreq = 0.005; %Hz
        order = 64;
    else if (nargin == 3 && isempty(cutoffFreq))
        cutoffFreq = 0.005; %Hz
    else         
        order = 64;

            
    end
    firLPF = designfilt('lowpassfir','FilterOrder',order, ...
        'CutoffFrequency',cutoffFreq,'SampleRate',fs);

    tonic = filtfilt(firLPF,x);
    phasic = x - tonic;
end
