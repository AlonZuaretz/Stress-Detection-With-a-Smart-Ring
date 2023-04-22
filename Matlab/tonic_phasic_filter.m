function [tonic, phasic] = tonic_phasic_filter(x, fs)

% Perform a lowpass filter to get the tonic component:
cutoff_freq = 0.01;
order = 512;
normalized_freq = cutoff_freq/(fs/2);
b = fir1(order, normalized_freq);

tonic = filter(b,1,x);

phasic = x - tonic;
