% Constant Parameters:
fs = 3; %Hertz

% Fetch data:

% t_vec =
% raw = 
% n = length(t);

% Create parameters for fourier transform (mainly for plotting):

% nfft = nextpow2(n);
% f_vec = (fs/nfft)*(-nfft/2:(nfft/2-1));


% Preprocess:
order = 256;
cutoff_freq = 0.5;

preproccesed_data = preprocess(raw,fs,order,cutoff_freq);



% Recieve Tonic and Phasic components:
[tonic, phasic] = tonic_phasic_filter(preproccesed_data,fs);


% plot the fft for a wanted signal:
% x = 
X = fftshift(fft(x,nfft));

figure;
plot(f_vec,abs(X));

