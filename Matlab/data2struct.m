



function struct = data2struct(pathToCSV,saveTo,fileName)
        T = readtable(pathToCSV);
        data.Time = timeofday(T.date_time);
        data.Tsec = T.time_sec_;
        data.raw = T.raw;
        data.acc = [T.ax, T.ay, T.az];
        data.st = T.st;
        data.ii = T.ii;
        data.MM = T.mm;
        data.SCR = T.scr;
        struct = data;
        % save(saveTo+fileName,"data");  
end
% 
% % Constant Parameters:
% fs = 3; %Hertz
% 
% %% Preprocess:
% N = length(secsFromStart);
% NFFT = 2^nextpow2(N);
% fvec = (fs/NFFT)*(-NFFT/2:(NFFT/2-1));
% 
% %preprocess parameters:
% order = 64;
% cutoffFreq = 0.5; % Hz
% preproccesedData = preprocess(raw,fs,order,cutoffFreq);
% 
% % Recieve Tonic and Phasic components:
% [tonic, phasic] = tonicPhasicFilter(preproccesedData,fs);
% 
% 
% %find size of acceleration vector for each sample:
% accNorm = normalize(sqrt(acc(:,1).^2+acc(:,2).^2+acc(:,3).^3));
% 
% %% plotting:
% %suspected times of stimulation:
% stimulationTimes = [];%['12:46:38'; '13:01:11'];
% 
% figure;
% % Plot any 3 vectors (change legend accordignly):
% x1 = preproccesedData;
% x2 = phasic;
% x3 = tonic;
% 
% plot(Time,x1,Time,x2,Time,x3);
% hold on
% xlabel('Time of day');
% if ~isempty(stimulationTimes)
%     tStim = timeofday(datetime(stimulationTimes,'InputFormat','HH:mm:ss'));
%     xline(tStim);
% end
% grid on
% legend('Preproccesed Data', 'phasic','tonic');
% 
% 
% 
% % % plot the fft for a wanted signal:
% % x = preproccesed_data;
% % X = fftshift(fft(x,NFFT));
% 
% % figure;
% % plot(fvec,abs(X));

