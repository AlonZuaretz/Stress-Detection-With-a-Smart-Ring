function [y] = filterFixDistortion(x, fs, order, cutoffFreq)

    firLPF = designfilt('lowpassfir','FilterOrder',order, ...
        'CutoffFrequency',cutoffFreq,'SampleRate',fs);
    y = filtfilt(firLPF,x);
    % xFiltered = filter(firLPF,x);
    % delay = mean(grpdelay(firLPF,order,fs));
    % y = [xFiltered(1:end - delay);zeros(delay,1)];

end


