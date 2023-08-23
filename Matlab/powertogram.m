
function [p,t, winIdx] = powertogram(a,time, N_win, OL)


    
    N = length(a.M);
    winSize = floor((N-OL)/(N_win-OL));
    winIdx = zeros(1,winSize);
    p = zeros(1,winSize);
    t = zeros(1,winSize);
    if winSize*(N_win-OL)+1+N_win > N
        aMpadded = [a.M; zeros(winSize*(N_win-OL)+1+N_win-N,1)];
    end

    jj = 1;
    for ii=1:winSize
        p(ii) = sum((abs(aMpadded(jj:jj+N_win-1)-1).^2));
        winIdx(ii) = jj;
        t(ii) = time(jj);
        jj = jj+N_win-OL;
    end
%% True powertogram
    % Fs = 3;
    % dt = 1/Fs;
    % x = a.x;
    % winsize = 40;
    % numoverlap = round(0.6*winsize);
    % win = hamming(winsize);
    % X = buffer(x,winsize,numoverlap);
    % for nn = 1:size(X,2)
    % [Pxx(:,nn),F] = pwelch(X(:,nn),win,length(win)/2,length(win),Fs);
    % end
    %  % create a time vector
    %  idxbegin = find(X(:,1) == 0);
    %  numpresteps = length(idxbegin);
    %  idxend = find(X(:,end) == 0);
    %  numpoststeps = length(idxend);
    %  tbegin = -(numpresteps*dt)/2;
    %  tend = time(end)+((numpoststeps*dt))/2;
    %  tvec = linspace(tbegin,tend,size(Pxx,2));
    %  figure;
    %  surf(tvec,F,10*log10(abs(Pxx)),'EdgeColor','none');   
    %  axis xy; axis tight; colormap(jet); view(0,90);
    %  xlabel('Time (sec)');
    %  ylabel('Frequency (Hz)');

end

