% Constant Parameters:
fs = 3; %Hertz

%% Extract data:
if ~exist('T', 'var')
    T = readtable(['C:\Users\alonz\OneDrive - Technion\תואר\סמסטר 6\פרויקט\' ...
        'project - Stress Detection with a Smart Ring\' ...
        'Ring Samples\CSV\MMDataF5B57A688F87_4_27.csv']);
    
    Time = timeofday(T.date_time);
    secsFromStart = T.time_sec_;
    raw = T.raw;
    acc = [T.ax, T.ay, T.az];
    st = T.st;
    ii = T.ii;
    MM = T.mm;
    SCR = T.scr;
end

%% Preprocess:
N = length(secsFromStart);
NFFT = 2^nextpow2(N);
fvec = (fs/NFFT)*(-NFFT/2:(NFFT/2-1));

%preprocess parameters:
order = 64;
cutoffFreq = 0.5; % Hz
preproccesedData = preprocess(raw,fs,order,cutoffFreq);

% Recieve Tonic and Phasic components:
[tonic, phasic] = tonicPhasicFilter(preproccesedData,fs);


%find size of acceleration vector for each sample:
accNorm = normalize(sqrt(acc(:,1).^2+acc(:,2).^2+acc(:,3).^3));

%% plotting:
%suspected times of stimulation:
stimulationTimes = [];%['12:46:38'; '13:01:11'];

figure;
% Plot any 3 vectors (change legend accordignly):
x1 = preproccesedData;
x2 = phasic;
x3 = tonic;

plot(Time,x1,Time,x2,Time,x3);
hold on
xlabel('Time of day');
if ~isempty(stimulationTimes)
    tStim = timeofday(datetime(stimulationTimes,'InputFormat','HH:mm:ss'));
    xline(tStim);
end
grid on
legend('Preproccesed Data', 'phasic','tonic');



% % plot the fft for a wanted signal:
% x = preproccesed_data;
% X = fftshift(fft(x,NFFT));

% figure;
% plot(fvec,abs(X));

