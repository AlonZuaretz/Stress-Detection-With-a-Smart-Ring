



% filePath_noisy ="C:\Users\alonz\OneDrive - Technion\תואר\סמסטר 6\פרויקט\project -" + ...
%     " Stress Detection with a Smart Ring\Ring Samples\CSV\21042023_19-24-46-21042023_19-47-46.csv";
% filePath_quiet = "C:\Users\alonz\OneDrive - Technion\תואר\סמסטר 6\פרויקט\project -" + ...
%     " Stress Detection with a Smart Ring\Ring Samples\CSV\08052023_21-06-19-08052023_21-11-31_no_noise.csv";
% T = readtable(filePath_quiet);
% acc = [T.ax, T.ay, T.az];
% fs = 3;
% win = 32;
% % time = timeofday(T.date_time);
% time = T.time_sec_;
% OL = 0;
% plotPowerOverTime(acc,fs,time,win,OL);

function [p,t, winIdx,aT] = powertogram(acc,time, N_win, OL)
    ax = (acc(:,1)-128)/64;
    ay = (acc(:,2)-128)/64;
    az = (acc(:,3)-128)/64;
    aT = sqrt(ax.^2+ay.^2+az.^2);
       
    % [s, f, t] = spectrogram(aT-1,N_win,OL,[],fs);
    % power = (2/(fs*256))*abs(s).^2;
    % powerPerTime = sum(power,1);
    % figure; plot(t,powerPerTime);
    

   
    N = length(aT);
    size = floor((N-OL)/(N_win-OL));
    winIdx = zeros(1,size);
    p = zeros(1,size);
    t = zeros(1,size);
    if size*(N_win-OL)+1+N_win > N
        aT = [aT; zeros(size*(N_win-OL)+1+N_win-N,1)];
    end

    jj = 1;
    for ii=1:size
        p(ii) = sum((abs(aT(jj:jj+N_win-1)-1).^2));
        winIdx(ii) = jj;
        t(ii) = time(jj);
        jj = jj+N_win-OL;
    end

    % figure; plot(tvec,pvec*(1/fs));
    % yline(0.3);
end

