[fileNameCSV,pathToCSVdir] = uigetfile('*.csv','',['C:\Users\alonz\OneDrive - ' ...
    'Technion\תואר\סמסטר 6\פרויקט\project - Stress Detection with a Smart Ring\Ring Samples\CSV']);
filePath = [pathToCSVdir,fileNameCSV];

saveToDir = ['C:\Users\alonz\OneDrive - ' ...
    'Technion\תואר\סמסטר 6\פרויקט\project - Stress Detection with a Smart Ring\Ring Samples\mat'];
% uigetdir(['C:\Users\alonz\OneDrive - ' ...
%     'Technion\תואר\סמסטר 6\פרויקט\project - Stress Detection with a Smart Ring\Ring Samples\mat']);
fileNameMat = fileNameCSV(1:end-4);

createLedStruct([],[],fileNameMat,filePath,saveToDir)
% clear;

