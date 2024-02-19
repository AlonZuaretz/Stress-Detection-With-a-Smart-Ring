%Copyright 2016 The MathWorks, Inc.
%% Load a signal
load noisysig.mat
figure; 
subplot(2,1,1); plot(f0); grid on; title('Original signal'); axis tight; 
subplot(2,1,2); plot(f); title('Original signal with noise'); 
axis tight; grid on;
%%  Decompose signal using Discrete Wavelet Transform  
dwtmode('per','nodisplay');
wname = 'sym6';
level = 5;
[C, L] = wavedec(f,level,wname);
plotDetCoefHelper(f,C,L); %helperFunction to plot the coefficients at every level
%% Analyze the subbands and determine the threshold
%% Denoise the signal 
fd = wden(f,'rigrsure','s','sln',level,wname);
figure; 
subplot(2,1,1); 
plot(f);axis tight; grid on;title('Noisy Signal');
subplot(2,1,2)
plot(fd); axis tight; grid on;
title(sprintf('Denoised Signal SNR:  %0.2f dB',-20*log10(norm(abs(f0-fd))/norm(f0))));
%% Comparing with other techniques
figure; 
subplot(2,2,1); 
plot(f);axis tight; grid on;title('Noisy Signal');
subplot(2,2,2)
plot(fd); axis tight; grid on;
title(sprintf('Wavelet Denoising SNR:  %0.2f dB',-20*log10(norm(abs(f0-fd))/norm(f0))));
subplot(2,2,3)
fsg = sgolayfilt(f,31,101);
plot(fsg); axis tight; grid on;
title(sprintf('Savitzky Golay SNR:  %0.2f dB',-20*log10(norm(abs(f0-fsg))/norm(f0))));
subplot(2,2,4)
movavg = 1/20*ones(20,1);
fmv = filtfilt(movavg,1,f);
plot(fmv); axis tight; grid on;
title(sprintf('Moving Average SNR:  %0.2f dB',-20*log10(norm(abs(f0-fmv))/norm(f0))));


function plotDetCoefHelper(f,C,L)
%Copyright 2016 The MathWorks, Inc.
 D = detcoef(C,L,'cells');
% % [cD1, cD2, cD3, cD4, cD5] = detcoef(C,L,[1,2,3,4,5]);
figure; set(gcf,'Position', [402         139        1378         923]);
subplot(6,1,1)
plot(f); axis tight; grid on; title('Original Signal');
subplot(6,1,2) 
h = stem(dyadup(D{1}));
h.ShowBaseLine = 'off';
h.Marker = '.';
h.MarkerSize = 2;
axis tight; grid on; title('Level 1 Details');
subplot(6,1,3)
h = stem(dyadup(dyadup(D{2})));
h.ShowBaseLine = 'off';
h.Marker = '.';
h.MarkerSize = 2;
axis tight; grid on;title('Level 2 Details');
subplot(6,1,4);
h = stem(dyadup(dyadup(dyadup(D{3}))));
h.ShowBaseLine = 'off';
h.Marker = '.';
h.MarkerSize = 2;
axis tight; grid on; title('Level 3 Details');
subplot(6,1,5);
h = stem(dyadup(dyadup(dyadup(dyadup(D{4})))));
h.ShowBaseLine = 'off';
h.Marker = '.';
h.MarkerSize = 2;
axis tight; grid on;title('Level 4 Details');
subplot(6,1,6);
h = stem(dyadup(dyadup(dyadup(dyadup(dyadup(D{5}))))));
h.ShowBaseLine = 'off';
h.Marker = '.';
h.MarkerSize = 2;
axis tight; grid on;title('Level 5 Details');
end