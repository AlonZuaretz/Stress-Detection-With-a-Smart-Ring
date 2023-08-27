from load_data import load_data
from preprocessing import preprocessing
import matplotlib.pyplot as plt
#import feature_extraction as fe
#import features_selection


path = 'C:/Users/alonz/OneDrive - Technion/Documents/GitHub/Stress-Detection-With-a-Smart-Ring/Python/ring_sample.csv'
experiment = 'Ring Experiment'
#experiment = "Empatica SIPL Experiment"
#experiment = "CEAP_360VR"

eda_dict = load_data(path, experiment)

raw_eda = eda_dict['Data']['Raw EDA']
time_stamps = eda_dict['Data']['Time Stamps']
fs = eda_dict['Sampling Rate']
label = eda_dict['Label']

preproccessed_EDA, var = preprocessing(raw_eda, fs)

plt.plot(preproccessed_EDA)
plt.show()
#tonic_phasic_method = ''
#features = fe(preproccessed_EDA, fs, tonic_phasic_method )

#filtered_features = features_selection()
