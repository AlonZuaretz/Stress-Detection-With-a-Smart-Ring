
close all
clc
[fileName,pathToCSV] = uigetfile('*.csv','',['C:\Users\alonz\OneDrive - ' ...
    'Technion\תואר\סמסטר 6\פרויקט\project - Stress Detection with a Smart Ring\Ring Samples\CSV']);
filePath = [pathToCSV,fileName];
d = data2struct(filePath);
a = processAcc(d.acc);


winSize = 20;
[p, t, winIdx] = powertogram(a,d.Tsec,winSize,0);
threshold = 0.05;
dataFiltered = preprocess(d.raw,3,16,0.1,'Hamming');
dataFilP = dataFiltered;
treatedRanges = zeros(0,2);
for ii = 2:length(winIdx)
    if p(ii)>threshold
        [startIdx, endIdx, dataFilP] = denoise(dataFilP,winIdx(ii),winSize);
        treatedRanges(end+1,:) = [startIdx;endIdx];
    end
end
% dataFilLinLier = filloutliers(dataFilP,"previous","mean");
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
figure;
p11 = subplot(2,1,1);
plot(d.Tsec,a.M,'DisplayName','Acceleration');
legend()
p12 = subplot(2,1,2);
plot(t,p,'DisplayName','Powertogram');
legend()

figure;
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



% %% Correlation
% [tonic, phasic] = tonicPhasicFilter(dataFiltered,3,0.01,4);
% xAxisCorr = corrcoef(a.x,phasic);
% yAxisCorr = corrcoef(a.y,phasic);
% zAxisCorr = corrcoef(a.z,phasic);
% MagCorr = corrcoef(a.M,phasic);
% 
% sprintf("xAxisCorr:" + string(xAxisCorr(1,2)) + "\n"+ "yAxisCorr:" + string(yAxisCorr(1,2))+ "\n" ...
%     + "zAxisCOrr:" +string(zAxisCorr(1,2))+ "\n"+ "Mag Corr:" + string(yAxisCorr(1,2))+ "\n")



% originalSignal = p;
% numElementsToAdd = length(phasicFiltered)-length(p);
% % Original signal length
% originalLength = length(p);
% % Expanded signal length
% expandedLength = originalLength + numElementsToAdd;
% % Indices for the expanded signal
% expandedIndices = linspace(1, originalLength , expandedLength);
% % Interpolating the signal
% expandedSignal = interp1(originalSignal, expandedIndices, 'linear');
% 
% pInterpNorm = normalize(expandedSignal);
% phasicNorm = normalize(phasicFiltered);
% 
% coeff_Corr = corrcoef(phasicNorm,pInterpNorm)
% figure;
% plot(phasicNorm); hold on;
% plot(pInterpNorm);

%% functions
function [startIdx, endIdx, data] = denoise(data,winIdx,winSize)
    if winIdx+winSize < length(data)
        filler = linspace(data(winIdx),data(winIdx+winSize),winSize)';
        startIdx = winIdx;
        endIdx = winIdx+winSize;
    elseif winIdx+winSize >= length(data)
        filler = linspace(data(winIdx),data(end),winSize)';
        startIdx = winIdx;
        endIdx = length(data);
    end
    data = [data(1:winIdx-1);filler;data(winIdx+winSize:end)];
end
