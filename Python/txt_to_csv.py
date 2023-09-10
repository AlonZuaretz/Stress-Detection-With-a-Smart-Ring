from datetime import datetime, timedelta
import regex as re
import os

path_to_txt = input("please enter path to ring txt file: ")
# C:/Users/yossi/Desktop/MMDataF5B57A688F87_4.txt
# C:/Users/alonz/OneDrive - Technion/תואר/פרויקט/project - Stress Detection with a Smart Ring/samples and data/MoodMetric Ring/Roy Samples.txt
txt_file_name = (os.path.basename(path_to_txt)).replace('.txt', '')
# maybe we need to change name
path_to_dir = input("please enter path to directory: ")
# C:/Lilach/Technion/Project A
# C:/Users/alonz/OneDrive - Technion/תואר/פרויקט/project - Stress Detection with a Smart Ring/Ring Samples/CSV/Roy_Samples

ring_ID = 'Ring ID: F5:B5:7A:68:8F:87\n'
outputs = []
section_num = 0
start_line = False
start_time = []
end_time = []
time_msec_ref = 0
date_ref = datetime(1970, 1, 1)
txt_file = open(path_to_txt, 'r').readlines()

for line in txt_file:
    if line == ring_ID:
        # section_num += 1
        # outputs.append("date_time,time(sec),st,mm,ii,raw,ax,ay,az,scr")
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
            section_num += 1
            outputs.append("date_time,time(sec),st,mm,ii,raw,ax,ay,az,scr")

            time_msec_ref = time_msec
            time_ref_full = date_ref + timedelta(seconds=time_msec/1e3) + timedelta(hours=3)
            start_time.append(time_ref_full)
            start_line = False
        time_sec_from_start = (time_msec - time_msec_ref)/1e3
        time_full = date_ref + timedelta(seconds=time_sec) + timedelta(hours=3)

        if txt_file.index(line) == len(txt_file)-1 or txt_file[txt_file.index(line)+1] == ring_ID:
            end_time.append(time_full)

        outputs[-1] += f"\n{time_full},{time_sec_from_start},{st},{mm},{ii},{raw},{ax},{ay},{az},{scr}"

# print(f"sections = {section_num}")
# print(f"outputs len = {len(outputs)}")
# print(f"start_time len = {len(start_time)}")
# print(f"end_time len = {len(end_time)}")

for x in range(section_num):
    curr_start_time = start_time[x].strftime("%d%m%Y_%H-%M-%S")
    curr_end_time = end_time[x].strftime("%d%m%Y_%H-%M-%S")
    print(f"Created output csv file '{curr_start_time}-{curr_end_time}' in given directory")
    output_csv = open(f"{path_to_dir}/{curr_start_time}-{curr_end_time}.csv", 'w')
    output_csv.write(outputs[x])
    output_csv.close()

