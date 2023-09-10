[fileName,pathToCSV] = uigetfile('*.csv','',[]);
filePath = [pathToCSV,fileName];
d = data2struct(filePath);
signal = d.raw;
time = d.Tsec;
figure;
plot(time,signal);

