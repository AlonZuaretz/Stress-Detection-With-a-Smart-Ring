% Constant Parameters:
fs = 3; %Hertz

%% Extract data:
if ~exist('T', 'var')
    T = readtable(['C:\Users\alonz\OneDrive - Technion\תואר\סמסטר 6\פרויקט\' ...
        'project - Stress Detection with a Smart Ring\' ...
        'Ring Samples\CSV\MMDataF5B57A688F87_3_15.csv']);
    
    Time = timeofday(T.date_time);
    t = T.time_sec_;
    raw = T.raw;
    acc = [T.ax, T.ay, T.az];
    st = T.st;
    ii = T.ii;
    MM = T.mm;
    SCR = T.scr;
end

%% Preprocess:
N = length(t);
NFFT = 2^nextpow2(N);
fvec = (fs/NFFT)*(-NFFT/2:(NFFT/2-1));

%preprocess parameters:
order = 512;
cutoff_freq = 0.5;
preproccesed_data = preprocess(raw,fs,order,cutoff_freq);

% Recieve Tonic and Phasic components:
[tonic, phasic] = tonic_phasic_filter(preproccesed_data,fs);


%% plotting:
%suspected times of stimulation:
stimulationTimes = ['12:46:38'; '13:01:11'];
tStim = timeofday(datetime(stimulationTimes,'InputFormat','HH:mm:ss'));
figure;
x = tonic;
y = phasic;

ax1 = axes(gcf);
plot(ax1,t,x,t,y);

ax2 = axes(gcf);
plot(ax2,Time,x,Time,y);

xline(ax2,tStim);

ax2.XAxisLocation = 'Top';
ax1.YAxis.Visible = 'off';
xlabel(ax1,'Time (seconds)'); 
xlabel(ax2,'Time of day'); 
legend('tonic', 'phasic');


% plot the fft for a wanted signal:
x = preproccesed_data;
X = fftshift(fft(x,NFFT));

% figure;
% plot(fvec,abs(X));

