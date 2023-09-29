
%%
% [fileName,pathToCSV] = uigetfile('C:\Users\alonz\OneDrive - Technion\תואר\פרויקט\project - Stress Detection with a Smart Ring\samples and data\MoodMetric Ring\CSV','',[]);
filePath_ring = "C:\Users\alonz\OneDrive - Technion\תואר\פרויקט\project - Stress Detection with a Smart Ring\samples and data\MoodMetric Ring\CSV\28_8\ring_28082023_10-46-46-28082023_12-33-21_stress.csv";
% filePath_ring = [pathToCSV, fileName] ;

filePath_wrist = "C:\Users\alonz\OneDrive - Technion\תואר\פרויקט\project - Stress Detection with a Smart Ring\samples and data\Empatica New bracelet\eda_3.csv";

T_ring = readtable(filePath_ring);
date_ring = T_ring.date_time;
raw_data_ring = T_ring.raw;
time_stamps_ring = T_ring.time_sec_;

T_wrist = readtable(filePath_wrist);
% start time wristband: 10:47:22.58
raw_data_wrist =  T_wrist.Var1;
fs_wrist = 4;
time_stamps_wrist = 0:1/fs_wrist:1/fs_wrist*length(raw_data_wrist) - 1/fs_wrist;

raw_data_ring =raw_data_ring(107:end);
time_stamps_ring = time_stamps_ring(107:end);

%%

%preprocess:
pre_data_ring = preprocess(raw_data_ring,3,8,0.1,'');
pre_data_wrist = preprocess(raw_data_wrist,4,8,0.1,'');

% remove outliers:
% figure;
% plot(pre_data_ring); hold on
% pre_data_ring = rmoutliers(pre_data_ring, "movmedian" , 4);
% plot(pre_data_ring);

%normalize:
norm_data_ring = pre_data_ring/ max(pre_data_ring);
norm_data_wrist = pre_data_wrist / max(pre_data_wrist);


figure; plot(time_stamps_ring,norm_data_ring);
hold on
plot(time_stamps_wrist, norm_data_wrist)
legend('ring','wrist');


%convexEDA

phasicMethod = 'Convex';

tonic_ring = pyrunfile('neurokitMatlab.py', "tonic", ...
                    eda_signal = pre_data_ring, phasicMethod = phasicMethod, peakMethod='');
phasic_ring = pyrunfile('neurokitMatlab.py', "phasic", ...
                    eda_signal = pre_data_ring, phasicMethod = phasicMethod, peakMethod='');
tonic_ring = double(tonic_ring);
phasic_ring = double(phasic_ring);


tonic_wrist = pyrunfile('neurokitMatlab.py', "tonic", ...
                    eda_signal = pre_data_wrist, phasicMethod = phasicMethod, peakMethod='');
phasic_wrist = pyrunfile('neurokitMatlab.py', "phasic", ...
                    eda_signal = pre_data_wrist, phasicMethod = phasicMethod, peakMethod='');
tonic_wrist = double(tonic_wrist);
phasic_wrist = double(phasic_wrist);

% remove outliers:
phasic_ring_outliers_removed = rmoutliers(phasic_ring);


%find peaks:
peakMethod = 'NeuroKit';

EDA_peaks_ring = pyrunfile('neurokitMatlab.py', "EDA_peaks", ...
    eda_signal = phasic_ring_outliers_removed, phasicMethod = '',peakMethod=peakMethod);

EDA_peaks_wrist = pyrunfile('neurokitMatlab.py', "EDA_peaks", ...
    eda_signal = phasic_wrist, phasicMethod = '',peakMethod=peakMethod);


%find the time and amplitude of the peaks to plot them:
Idx_peaks_ring = double(EDA_peaks_ring)+1;
ampEDA_peaks_ring = phasic_ring_outliers_removed(double(EDA_peaks_ring)+1);

Idx_peaks_wrist = time_stamps_wrist(double(EDA_peaks_wrist)+1);
ampEDA_peaks_wrist = phasic_wrist(double(EDA_peaks_wrist)+1);

figure;
plot(phasic_ring_outliers_removed, 'Color', 'blue');
hold on
plot(phasic_wrist, 'Color', 'red');

plot(Idx_peaks_ring, ampEDA_peaks_ring, 'o')
plot(Idx_peaks_wrist, ampEDA_peaks_wrist, 'o')













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









