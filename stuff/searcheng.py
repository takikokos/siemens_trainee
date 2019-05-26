import numpy as np
from audiorec import Audio
from test_io import record_to_file
from math import sqrt
import sox


def euclidean(x : np.array ,y : np.array):
    return sqrt(sum((x-y) ** 2))


def find_min_euclidean(x, y, debug_print=False):
    """
        x, y : iterables
        x must be greater than y
        return list with min indexs
    """
    distances = []
    if len(y) > len(x) :
        x, y = y, x
        print("find_min_euclidian func changed arguments!")

    maxcount = len(x) - len(y) + 1
    for i in range(maxcount):
        if debug_print:
            print(i, "/", maxcount)
        distances.append(euclidean(x[i:i+len(y)], y))

    result = [index for index, value in enumerate(distances) if value == min(distances)]
    return result


def search(samples, patt):
    """
        samples, patt : numpy.array
        all data is being thin out and standartized
    """

    data = samples[0::100]
    pattern = patt[0::100]

    data = (data - data.mean()) / data.std()
    pattern = (pattern - pattern.mean()) / pattern.std()

    res = find_min_euclidean(data, pattern)
    # return (res[0]/len(data))
    return res
    # print(f"Reults for searching {patt.wav_fname} in {sample.wav_fname} : ")
    # for ind in res:
    #     timeres = sample.duration * (ind/len(data))
    #     print("time ", timeres)


if __name__ == "__main__":
        
    # input("press enter to record sample")
    # record_to_file("sample.wav", 5)
    # input("press enter to record pattern")
    # record_to_file("patt.wav", 1)

    # убирем тишину из шаблона
    # tfm = sox.Transformer()
    # # tfm.silence(location=-1)
    # tfm.silence(location=1)
    # tfm.build("patt.wav", "nosilence_patt.wav")

    # пробуем трим
    # tfm = sox.Transformer()
    # tfm.trim(0.6, 1)
    # tfm.build("patt.wav", "trimed_patt.wav")

    sample = Audio("sample.wav")
    patt = Audio("trimed_patt.wav")

    # sample.draw_waveform_plotly()

    # # прореживание
    # k = sample.nframes/800/32
    # sample.samples = sample.samples[0::int(k)]
    # k = patt.nframes/800/32
    # patt.samples = patt.samples[0::int(k)]

    sample.samples = sample.samples[0::100]
    patt.samples = patt.samples[0::100]

    # стандартизируем
    data = (sample.samples - sample.samples.mean()) / sample.samples.std()
    pattern = (patt.samples - patt.samples.mean()) / patt.samples.std()


    distances = []

    maxcount = len(data) - len(pattern) + 1

    for i in range(maxcount):
        # print(f"{i}/{maxcount}")
        distances.append(euclidean(data[i:i+len(pattern)], pattern))

    # print(distances[::750])
    res = distances.index(min(distances))
    timeres = sample.duration * (res/len(data))
    print(timeres)
    print(timeres - patt.duration)

