[fileName,pathToCSV] = uigetfile('*.csv','',['C:\Users\alonz\OneDrive - ' ...
    'Technion\תואר\סמסטר 6\פרויקט\project - Stress Detection with a Smart Ring\Ring Samples\CSV']);
filePath = [pathToCSV,fileName];
d = data2struct(filePath);
% signal = d.raw;
