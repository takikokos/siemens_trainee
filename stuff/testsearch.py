from searcheng import search, find_min_euclidean
from test_io import record_to_file
from audiorec import Audio


from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np

s = Audio(f"audio_samples/nonoise_sample_normilezeddb.wav")
p = Audio("audio_samples/no_noise_trimed_patt_normilezeddb.wav")


from pywt import dwt
cA, cD = dwt(s.samples, 'db1')

# data, *_ = dwt(s.samples, 'db1')
# pattern, *_ = dwt(p.samples, 'db1')
# data = data[0::100]
# pattern = pattern[0::100]


data = s.samples[::100]
pattern = p.samples[::100]

# print(len(data), len(pattern))
data = (data - data.mean()) / data.std()
pattern = (pattern - pattern.mean()) / pattern.std()


distances = []

maxcount = len(data) - len(pattern) + 1
for i in range(maxcount):
    print(i, "/", maxcount)
    # distances.append(fastdtw(data[i:i+len(pattern)], pattern, dist=euclidean)[0])
    x, *_ = dwt(data[i:i+len(pattern)], 'db1')
    y, *_ = dwt(pattern, 'db1')
    # distances.append(euclidean(x, y))
    distances.append(fastdtw(x, y, dist=euclidean)[0])

ind = distances.index(min(distances))
print(ind/len(data) * s.duration)