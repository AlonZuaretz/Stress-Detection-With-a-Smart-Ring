
from datetime import datetime, timedelta
import numpy as np

ring_ID = 'Ring ID: F5:B5:7A:68:8F:87\n'
# path = 'C:\Users\yossi\OneDrive - Technion\סמסטר 6\פרויקט א\project - Stress Detection with a Smart Ring\Ring Samples\MMDataF5B57A688F87_6.txt'
path = 'C:/Users/alonz/OneDrive - Technion/תואר/סמסטר 6/פרויקט/project ' \
     '- Stress Detection with a Smart Ring/Ring Samples/MMDataF5B57A688F87_6.txt'


f = open(path, 'r')
lines = f.readlines()
f.close()

# find different sections start index:
sections_idx = []
ii = 0
for x in lines:
    if x == ring_ID:
        sections_idx.append(ii)
    ii += 1
num_of_sections = len(sections_idx)

# add index to the last line
sections_idx.append(len(lines)-1)

######################
section_to_process = 3
######################
if section_to_process > num_of_sections:
    print('error, section doesn\'t exist')

# extract data to vectors:
lines_idx = [sections_idx[section_to_process-1]+1, sections_idx[section_to_process]]
time = []
raw = []
ax = []; ay = []; az = []
MM = []
SCR = []
for x in lines[lines_idx[0]:lines_idx[1]]:
    time.append((float(x.split()[0][2:]))/1e3)
    raw.append(float(x.split()[4][4:]))
    ax.append(float(x.split()[5][3:]))
    ay.append(float(x.split()[6][3:]))
    az.append(float(x.split()[7][3:]))
    MM.append(int(x.split()[2][3:]))
    SCR.append(int(x.split()[8][4:]))


time_no_offset = [x - time[0] for x in time]

# find date and time for the specific test:
reference_date = datetime(1970, 1, 1)
time_to_add = time[0]
# add 3 hours for world time difference
test_initial_time = reference_date + timedelta(seconds=time_to_add) + timedelta(hours=3)






