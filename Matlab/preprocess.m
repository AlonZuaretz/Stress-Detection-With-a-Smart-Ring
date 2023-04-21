function [y] = preprocess(x, fs, order, cutoff_freq)

% Filter the data:
normalized_freq = cutoff_freq/(fs/2);
b = fir1(order, normalized_freq);

filtered_x = filter(b,1,x);

y = filtered_x;

