function [y] = preprocess(x, fs, order, cutoff_freq, windowStr)

    % Filter the data:
    switch windowStr
        case "Bartlett"
            window = bartlett(order+1);
        case "Hamming"
            window = hamming(order+1);
        case "Blackman"
            window = blackman(order+1);
        case "Gaussian"
            window = gausswin(order+1);
        case "Hann"
            window = hann(order+1);
        otherwise
            window = hamming(order+1);
            disp("Default window selected");
    end
            
    
    normalized_freq = cutoff_freq/(fs/2);
    b = fir1(order, normalized_freq,window);
    filtered_x = filter(b,1,x);
    y = filtered_x;
end

