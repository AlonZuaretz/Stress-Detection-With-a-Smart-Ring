
from avro.datafile import DataFileReader
from avro.io import DatumReader
import matplotlib.pyplot as plt
import datetime
import json
import numpy as np
import pandas as pd
import csv

# requires avro file to have been extracted using cyberduck, 
# messege itay or artium if needed.
# dependencies are avro ,datetime,json and numpy.

avro_file = ["home/itay/Documents/experiment3/1-1-2_1690797648.avro"]
# avro_file = 1-1-2_1690797648.avro
def extract_signal_avro(avro_files:list,user_num:int,testing=False):
    data = []
    for file in avro_files:
        reader = DataFileReader(open(file, "rb"), DatumReader())
        schema = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
        data = []
        for datum in reader:
            data.append(datum)
        reader.close()
    
    data.sort(key=lambda datum : int(datum["rawData"]["bvp"]["timestampStart"]))
    
   
    # print(schema)
    eda = []
    eda_stamps =[]
    eda_fs =[]
    bvp = []
    bvp_fs =[]
    bvp_stamps =[]
    accx = []
    accy = [] 
    accz = []
    acc_fs =[]
    accparams = []
    acc_stamps =[]
    tags = []
    for i,datum in enumerate(data):
        eda.extend(datum["rawData"]["eda"]["values"])
        eda_stamps.append(datum["rawData"]["eda"]["timestampStart"])
        eda_fs.append(datum["rawData"]["eda"]["samplingFrequency"])
        bvp.extend(datum["rawData"]["bvp"]["values"])
        bvp_stamps.append(datum["rawData"]["bvp"]["timestampStart"])
        bvp_fs.append(datum["rawData"]["bvp"]["samplingFrequency"])
        accx.extend(datum["rawData"]["accelerometer"]["x"])
        accy.extend(datum["rawData"]["accelerometer"]["y"])
        accz.extend(datum["rawData"]["accelerometer"]["z"])
        acc_stamps.append(datum["rawData"]["accelerometer"]["timestampStart"])
        acc_fs.append(datum["rawData"]["accelerometer"]["samplingFrequency"])
        tags.extend(datum["rawData"]["tags"]['tagsTimeMicros'])
    

    if testing:
        print(np.mean(bvp_fs),np.mean(eda_fs), np.mean(acc_fs),np.std(bvp_fs),np.std(eda_fs),np.std(acc_fs))
        if len(tags) ==0:
            tags.append(data[0]["rawData"]["bvp"]["timestampStart"])
        if len(tags) == 1:
            for i in range(3):
                tags.append(tags[0]+abs(300000000*np.random.randn()+i*10000000))
        print("testing")
        
    
    
    tags.sort()
    if len(tags) >1:
        indices =[]
        print("Available time stamps:")
        for i, ts in enumerate(tags):
            print(f"{i}: {datetime.datetime.fromtimestamp(int(ts)/1000000)}") 
        while True:
            selected_indices = input("Enter the indices of the time stamps you want (comma-separated): ")
            try:
                indices = [int(idx) for idx in selected_indices.split(",")]
                break
            except ValueError:
                print("Invalid input. Please enter indices as comma-separated integers.")
        tags = [tags[i] for i in indices]
        start_timestamp= bvp_stamps[0]
        fs1 = 64 
        fs2 = 4 
        sample_indices1 = [int((ts - start_timestamp)*fs1 // 1000000) for ts in tags]
        sample_indices2 = [int((ts - start_timestamp)*fs2 // 1000000) for ts in tags]
   
        for i in range(0,len(sample_indices1),2):
            np.savetxt("eda_"+str(user_num)+"_"+str(i)+".csv", -np.array(eda[sample_indices2[i]:sample_indices2[i+1]]), delimiter=",")
            np.savetxt("accx_"+str(user_num)+"_"+str(i)+".csv", -np.array(accx[sample_indices1[i]:sample_indices1[i+1]]), delimiter=",")
            np.savetxt("accy_"+str(user_num)+"_"+str(i)+".csv", -np.array(accy[sample_indices1[i]:sample_indices1[i+1]]), delimiter=",")
            np.savetxt("accz_"+str(user_num)+"_"+str(i)+".csv", -np.array(accy[sample_indices1[i]:sample_indices1[i+1]]), delimiter=",")
            np.savetxt("bvp_"+str(user_num)+"_"+str(i)+".csv", -np.array(bvp[sample_indices1[i]:sample_indices1[i+1]]), delimiter=",")
    np.savetxt("eda_stamps_"+str(user_num)+"_"+str(i)+".csv",np.array(eda_stamps),delimiter=",")
    np.savetxt("bvp_stamps_"+str(user_num)+"_"+str(i)+".csv",np.array(bvp_stamps),delimiter=",")
    np.savetxt("acc_stamps_"+str(user_num)+"_"+str(i)+".csv",np.array(acc_stamps),delimiter=",")
    np.savetxt("tags.csv",np.array(tags),delimiter=",")
    np.savetxt("eda_"+str(user_num)+".csv", np.array(eda), delimiter=",")
    np.savetxt("accx_"+str(user_num)+".csv", np.array(accx), delimiter=",")
    np.savetxt("accy_"+str(user_num)+".csv", np.array(accy), delimiter=",")
    np.savetxt("accz_"+str(user_num)+".csv", np.array(accy), delimiter=",")
    np.savetxt("acc_fs"+str(user_num)+".csv", np.array(acc_fs), delimiter=",")
    np.savetxt("bvp_fs"+str(user_num)+".csv", np.array(bvp_fs), delimiter=",")
    np.savetxt("eda_fs"+str(user_num)+".csv", np.array(eda_fs), delimiter=",")
    np.savetxt("bvp_"+str(user_num)+".csv", -np.array(bvp), delimiter=",")


    

        


if __name__== "__main__":
    while True:
        input_list = input_list = input("Enter a list of Avro files separated by spaces: ")
        try:
            input_list = [loc for loc in input_list.split()]
            break
        except ValueError:
            print("Invalid input. Please enter a list of Avro files separated by spaces.")
    while True:
        input_user = int(input("Please enter user number: "))
        try:
            if input_user not in [2,3,6,7]:
                raise ValueError("Input number is not in the allowed group.")
            break
        except ValueError:
            print("not a valid user num")
    input_testing = bool(int(input("If Testing, input 1 else 0, if you are running the experiment enter 0 : ")) ==1 )
    print(input_testing)

    extract_signal_avro(input_list,input_user,testing=input_testing)
