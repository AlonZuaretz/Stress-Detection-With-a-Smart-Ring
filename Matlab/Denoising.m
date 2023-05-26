
close all
clc

[file,pathToCSV] = uigetfile('*.csv','',['C:\Users\alonz\OneDrive - ' ...
    'Technion\תואר\סמסטר 6\פרויקט\project - Stress Detection with a Smart Ring\Ring Samples\CSV']);
filePath = [pathToCSV,file];
winSize = 16;
d = data2struct(filePath);
[p, t, winIdx,aT] = powertogram(d.acc,d.Tsec,winSize,0);
threshold = 0.1;
dataFiltered = preprocess(d.raw,3,8,0.25,'Hamming');
dataFilP = dataFiltered;
treatedRanges = zeros(0,2);
for ii = 2:length(winIdx)
    if p(ii)>threshold
        dataFilP = denoise(dataFilP,winIdx(ii),winSize);
        treatedRanges(end+1,:) = [winIdx(ii);winIdx(ii)+winSize];
    end
end
dataFilLinLier = filloutliers(dataFilP,"previous","mean");
MedWinSize = 8;
dataMedFil = medfilt1(dataFiltered,MedWinSize);

%% Extract Features:

% Filtered Data:
[tonicFiltered, phasicFiltered,~,~] = applyNeurokit(dataFiltered,d.Tsec);

%Powertogram Data:
[tonicP, phasicP,~,~] = applyNeurokit(dataFilP,d.Tsec);

%Median filtered:
[tonicMed, phasicMed,~,~] = applyNeurokit(dataMedFil,d.Tsec);


%% plot
figure(1);
p11 = subplot(2,1,1);
plot(aT,'DisplayName','Acceleration');
legend()
p12 = subplot(2,1,2);
plot(p,'DisplayName','Powertogram');
legend()

figure(2);
p21 = subplot(3,1,1);
plot(d.Tsec,dataFiltered,'DisplayName','Lowpass filtered');
hold on;
plot(d.Tsec,tonicFiltered,d.Tsec,phasicFiltered)
title('Filtered');
hold off;

p22 = subplot(3,1,2);
plot(d.Tsec,dataFilP,'DisplayName','Processed with acceleration');
hold on;
plot(d.Tsec,tonicP,d.Tsec,phasicP)
title('Accelerometer');
if ~isempty(treatedRanges(:,1))
    xregion(d.Tsec(treatedRanges(:,1)),d.Tsec(treatedRanges(:,2)))
end

hold off


p23 = subplot(3,1,3);
plot(d.Tsec,dataMedFil,'DisplayName','Median Filter');
hold on;
plot(d.Tsec,tonicMed,d.Tsec,phasicMed)
title('Med Filter');
hold off

linkaxes([p21,p22,p23])


%% functions
function data = denoise(data,winIdx,winSize)
    filler = linspace(data(winIdx-1),data(winIdx+winSize+1),winSize)';
    data = [data(1:winIdx-1);filler;data(winIdx+winSize:end)];
end
