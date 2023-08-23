EDApath = "C:\Users\alonz\OneDrive - Technion\תואר\סמסטר 6\פרויקט\project - " + ...
    "Stress Detection with a Smart Ring\Ring Samples\Empatica Results\eda.csv";
T = readtable(EDApath);
raw = T.Var1;
startTime = hours(12)+minutes(27)+seconds(44.5);
tVec = [startTime:seconds(1/3):seconds(length(raw)/3)+startTime-seconds(1/3)];
plot(tVec,raw);
% t = datetime(tVec,'ConvertFrom',dateType)

