from datetime import datetime, timedelta
import regex as re
import os

path_to_txt = input("please enter path to ring txt file: ")
# C:/Users/yossi/Desktop/MMDataF5B57A688F87_6.txt
# C:/Users/alonz/OneDrive - Technion/תואר/סמסטר 6/פרויקט/project - Stress Detection with a Smart Ring/Ring Samples/MMDataF5B57A688F87_1.txt
txt_file_name = (os.path.basename(path_to_txt)).replace('.txt','')
# maybe we need to change name
path_to_dir = input("please enter path to directory: ")
# C:/Lilach/Technion/Project A
# C:/Users/alonz/OneDrive - Technion/תואר/סמסטר 6/פרויקט
ring_ID = 'Ring ID: F5:B5:7A:68:8F:87\n'
outputs = []
section_num = 0
start_line = False
time_msec_ref = 0
date_ref = datetime(1970, 1, 1)
txt_file = open(path_to_txt, 'r')

for line in txt_file:
    if line == ring_ID:
        section_num += 1
        #globals()[f"output_{section_num}"] = "date_time,time(sec),st,mm,ii,raw,ax,ay,az,scr"
        #outputs.append(f"{f'output_{section_num}'}")
        outputs.append("date_time,time(sec),st,mm,ii,raw,ax,ay,az,scr")
        start_line = True
    else:
        line_split = re.split('\t|\n', line)
        line_split = list(filter(None, line_split))

        time_msec = int((re.split(':', line_split[0]))[1])
        st = (re.split(':', line_split[1]))[1]
        mm = int((re.split(':', line_split[2]))[1])
        ii = int((re.split(':', line_split[3]))[1])
        raw = float((re.split(':', line_split[4]))[1])
        ax = int((re.split(':', line_split[5]))[1])
        ay = int((re.split(':', line_split[6]))[1])
        az = int((re.split(':', line_split[7]))[1])
        scr = int((re.split(':', line_split[8]))[1])

        time_sec = time_msec/1e3
        if start_line:
            time_msec_ref = time_msec
            start_line = False
        time_sec_from_start = (time_msec - time_msec_ref)/1e3
        time_full = date_ref + timedelta(seconds=time_sec) + timedelta(hours=3)

        outputs[-1] += f"\n{time_full},{time_sec_from_start},{st},{mm},{ii},{raw},{ax},{ay},{az},{scr}"

for output in outputs:
    print(f"Created output csv file '{txt_file_name}_{outputs.index(output)}' in given directory")
    output_csv = open(f"{path_to_dir}/{txt_file_name}_{outputs.index(output)}.csv", 'w')
    output_csv.write(output)
    output_csv.close()
