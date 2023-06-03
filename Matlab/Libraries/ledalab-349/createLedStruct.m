function createLedStruct(conductance,time,fileName,CSVPath,saveToDir)
    if isempty(conductance)
        T = readtable(CSVPath);
        data.time = T.time_sec_(:).';
        data.conductance = T.raw(:).';
    
    elseif isempty(CSVPath)
        data.time = time(:).';
        data.conductance = conductance(:).';
        saveToDir = ['C:\Users\alonz\OneDrive - ' ...
    'Technion\תואר\סמסטר 6\פרויקט\project - Stress Detection with a Smart Ring\Ring Samples\mat'];
    end
    data.timeoff = 0;
    data.event = repmat(struct('time',0,'nid',0,'name','0','userdata',[]),1,1);
    

        
    save([saveToDir,'\',fileName],"data");  
end