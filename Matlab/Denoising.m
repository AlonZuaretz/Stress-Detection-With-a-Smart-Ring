
close all
clc
clear

%%
[fileName,pathToCSV] = uigetfile('*.csv','',['C:\Users\alonz\OneDrive - ' ...
    'Technion\תואר\סמסטר 6\פרויקט\project - Stress Detection with a Smart Ring\Ring Samples\CSV']);
filePath = [pathToCSV,fileName];
d = data2struct(filePath);
a = processAcc(d.acc);

%%

% find noisy segments:
winSize = 24;
OL = 0.5*winSize;
[p, t, winIdx] = powertogram(a,d.Tsec,winSize,OL);
threshold = 0.2;
data_preProcessed = preprocess(d.raw,3,8,0.1,'Hamming');
dataFilLin = data_preProcessed;
vec = p>threshold;
InterpIdx = winIdx.*vec;

% replace noisy segments:

%linear interpolation
[startIdx, endIdx, dataFilLin] = denoise(data_preProcessed,InterpIdx,winSize,OL);
treatedRanges = [startIdx;endIdx]';
if ~isempty(treatedRanges)
    treatedRanges_fixed(:,1) = treatedRanges(treatedRanges(:,1)>0,1);
    treatedRanges_fixed(:,2) = treatedRanges(treatedRanges(:,2)>0,2);
else 
    treatedRanges_fixed = [];
end

% polynom fitting:
[startIdx, endIdx, dataFilPoly,~] = polynomFiller(data_preProcessed,d.Tsec,InterpIdx);
% treatedRanges = [startIdx;endIdx]';
% if ~isempty(treatedRanges)
%     treatedRanges_fixed(:,1) = treatedRanges(treatedRanges(:,1)>0,1);
%     treatedRanges_fixed(:,2) = treatedRanges(treatedRanges(:,2)>0,2);
% else 
%     treatedRanges_fixed = [];
% end


%% Extract Features:
% Preprocessed data:
[tonic_preProcessed, phasic_preProcessed,ampEDA_peaks_preProcessed,tEDA_peaks_preProcessed] = ...
    extractFeatures(data_preProcessed,d.Tsec);

%Linear Interpolation Data:
[tonicLin, phasicLin,ampEDA_peaksLin,tEDA_peaksLin] = extractFeatures(dataFilLin,d.Tsec);

%Polynom Interpolation Data:
[tonicPoly, phasicPoly,ampEDA_peaksPoly,tEDA_peaksPoly] = extractFeatures(dataFilPoly,d.Tsec);

%% plot
% figure('Name', 'Accelerometer');
% p11 = subplot(2,1,1);
% plot(d.Tsec,a.M,'DisplayName','Acceleration');
% legend()
% p12 = subplot(2,1,2);
% plot(t,p,'DisplayName','Powertogram');
% legend()

figure('Name', 'EDA');

p21 = subplot(3,1,1);
plot(d.Tsec,tonic_preProcessed,'DisplayName','Tonic','LineWidth',1.5,'Color','red')
hold on;
plot(d.Tsec,data_preProcessed,'DisplayName','EDA','LineWidth',1.5,'Color','blue');
plot(d.Tsec,phasic_preProcessed, 'DisplayName','Phasic','LineWidth',1.5,'Color','green')
plot(tEDA_peaks_preProcessed,ampEDA_peaks_preProcessed,'o','DisplayName','SCR','Color',[0.5 0 0.4])

title('Basic LPF with Hamming window','FontSize',20);
xlabel('t [Sec]','FontSize',12)
ylabel('EDA [\muS]','FontSize',12)
legend();
hold off;

p22 = subplot(3,1,2);
plot(d.Tsec,tonicLin,'LineWidth',1.5,'Color','red')
hold on;
plot(d.Tsec,dataFilLin,'LineWidth',1.5,'Color','blue');
plot(d.Tsec,phasicLin,'LineWidth',1.5,'Color','green')
plot(tEDA_peaksLin,ampEDA_peaksLin,'o','Color',[0.5 0 0.4])
title('Motion Artifacts Processing Linear','FontSize',20);
if ~isempty(treatedRanges_fixed)
    xregion(d.Tsec(treatedRanges_fixed(:,1)),d.Tsec(treatedRanges_fixed(:,2)))
end
xlabel('t [Sec]','FontSize',12)
ylabel('EDA [\muS]','FontSize',12)
legend('EDA','Tonic','Phasic','SCR');
hold off

p23 = subplot(3,1,3);
plot(d.Tsec,tonicPoly,'LineWidth',1.5,'Color','red')
hold on;
plot(d.Tsec,dataFilPoly,'LineWidth',1.5,'Color','blue');
plot(d.Tsec,phasicPoly,'LineWidth',1.5,'Color','green')
plot(tEDA_peaksPoly,ampEDA_peaksPoly,'o','Color',[0.5 0 0.4])
title('Motion Artifacts Processing Polynom','FontSize',20);
% if ~isempty(treatedRanges_fixed)
%     xregion(d.Tsec(treatedRanges_fixed(:,1)),d.Tsec(treatedRanges_fixed(:,2)))
% end
xlabel('t [Sec]','FontSize',12)
ylabel('EDA [\muS]','FontSize',12)
legend('EDA','Tonic','Phasic','SCR');
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
function [startIdx, endIdx, data] = denoise(data,InterpIdx,winSize,OL)
    startIdx = [];
    endIdx = [];
    for ii = 1:(length(InterpIdx)-2)
        if (InterpIdx(ii)>0) && (InterpIdx(ii+1)>0)
            filler = linspace(data(InterpIdx(ii)),data(InterpIdx(ii+1)),winSize-OL)';
            endIdx(ii) = InterpIdx(ii+1);
        elseif (InterpIdx(ii)>0) && (InterpIdx(ii+1)==0)
            filler = linspace(data(InterpIdx(ii)),data(InterpIdx(ii)+winSize),winSize)';
            endIdx(ii) = InterpIdx(ii)+winSize;
        end

        if InterpIdx(ii)~=0
            startIdx(ii) = InterpIdx(ii);
            data = [data(1:startIdx(ii)-1);filler;data(endIdx(ii):end)];
        end
    end
end

function [startIdx, endIdx, dataFitted, timeFitted] =  polynomFiller(data,time,InterpIdx)
    startIdx = [];
    endIdx = [];
   
    % find sequences:
    ii = 1;
    dataFitted = data;
    polyMaxOrder = 8;
    while ii < length(InterpIdx)
        jj = ii;
        seqVec = [];
        while (InterpIdx(jj) && jj+1<=length(InterpIdx) && InterpIdx(jj+1))
            seqVec(end+1) = InterpIdx(jj);
            jj = jj+1;
        end
        if length(seqVec) >=2

            %find polynom that fits the downsampled data:
            dataToFit = downsample(data(seqVec(1):seqVec(end)),1);
            timeToFit = downsample(time(seqVec(1):seqVec(end)),1);
            p = polyfit(timeToFit, dataToFit,polyMaxOrder);
            poly = polyval(p,timeToFit);

            % upsample the received polynom to contain same number of
            % samples as the signal had in that time
            IdxVec = seqVec(1):seqVec(end);
            sectionTime = time(IdxVec);
            polyUpsampledInterp = interp1(timeToFit,poly,sectionTime,'cubic');
            dataFitted(seqVec(1):seqVec(end)) = polyUpsampledInterp;
            % timeFitted = [time(1:seqVec(1)-1);timeToFit;time(seqVec(end):end)];
            startIdx(end+1) = seqVec(1);
            endIdx(end+1) = seqVec(end);
        end
        ii = jj + 1;
    end
    timeFitted = time;
end

function [tonic,phasic,edaPeaks,tEDApeaks] = extractFeatures(data,time)
    peakMethod = 'NeuroKit';
    % Filtered Data:
    [tonic, phasic,~,~] = applyNeurokit(data,time,'Convex');
    %Find peaks:
    edaPeaksIdx = pyrunfile('neurokitMatlab.py', "EDA_peaks", ...
        eda_signal = phasic, phasicMethod = '',peakMethod=peakMethod);
    %find the time and amplitude of the peaks to plot them:
    tEDApeaks = time(double(edaPeaksIdx)+1);
    edaPeaks = phasic(double(edaPeaksIdx)+1);


end


