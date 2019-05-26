from audiorec import Audio
from datetime import datetime
from time import time


#  correct timestamps for samples
correct_time = {
    1: "1.53-1.75",
    2: "0.45-0.7",
    3: "2.23-2.8",
    4: "3.48-3.65",
    5: "1.36-1.55", # 3.42-4.1 - vtoroi
    6: "2.79-3.25",
    7: "2.20-2.70",
    8: "1.25-1.65",
    9: "0.83-1.35",
    10: "0.93-1.45"
}


result = open("data_output.txt", "w+")
for i in range(1, 6):
    result.write(f"\nPattern no. {i} - euclidean, starttime : {datetime.now()}\n")
    result.write("\nSample no.   {:^20}  {:^20}  {:^10}  {:^10}  {:^10}  {:^10}".format(\
                        "correct time", "norm trim nnoise", "basic", "nnoise", "trim nnoise", "cut out"))
    for j in range(1, 11):
        s = Audio(f"./audio/samples/normilized/norm_nnoise_sample{j}.wav")
        patt = Audio(f"./audio/patterns/normilized/norm_trimed_nnoise_patt{i}.wav")
        norm_trimed_nnoise, time_ntn = s.find_patt(patt, with_dwt=True)

        s = Audio(f"./audio/samples/basic/sample{j}.wav")
        patt = Audio(f"./audio/patterns/basic/patt{i}.wav")
        basic, stuff = s.find_patt(patt, with_dwt=True)

        s = Audio(f"./audio/samples/reduced_noise/nnoise_sample{j}.wav")
        patt = Audio(f"./audio/patterns/reduced_noise/nnoise_patt{i}.wav")
        nn_basic, stuff = s.find_patt(patt, with_dwt=True)

        patt = Audio(f"./audio/samples/answer_patterns/nnoise_sample{j}_ans.wav")
        cut, stuff = s.find_patt(patt, with_dwt=True)

        patt = Audio(f"./audio/patterns/trimed/trimed_nnoise_patt{i}.wav")
        nn_trimed, stuff = s.find_patt(patt, with_dwt=True)

        result.write("\nSample no.{:d}  {:^20}  {:^20}  {:>10.2f}  {:>10.2f}  {:>10.2f}  {:>10.2f}\n".format(\
                        j, correct_time[j], f"{round(norm_trimed_nnoise, 2)} / {round(time_ntn,2)}s", basic, nn_basic, nn_trimed, cut))
        result.flush()

    result.write(f"\nPattern no. {i} - fastdtw, starttime : {datetime.now()}\n")
    result.write("\nSample no.   {:^20}  {:^20}  {:^10}  {:^10}  {:^10}  {:^10}".format(\
                        "correct time", "norm trim nnoise", "basic", "nnoise", "trim nnoise", "cut out"))
    for j in range(1, 11):
        s = Audio(f"./audio/samples/normilized/norm_nnoise_sample{j}.wav")
        patt = Audio(f"./audio/patterns/normilized/norm_trimed_nnoise_patt{i}.wav")
        norm_trimed_nnoise, time_ntn = s.find_patt(patt, with_dwt=True, use_fastdtw=True)

        s = Audio(f"./audio/samples/basic/sample{j}.wav")
        patt = Audio(f"./audio/patterns/basic/patt{i}.wav")
        basic, stuff = s.find_patt(patt, with_dwt=True, use_fastdtw=True)

        s = Audio(f"./audio/samples/reduced_noise/nnoise_sample{j}.wav")
        patt = Audio(f"./audio/patterns/reduced_noise/nnoise_patt{i}.wav")
        nn_basic, stuff = s.find_patt(patt, with_dwt=True, use_fastdtw=True)

        patt = Audio(f"./audio/samples/answer_patterns/nnoise_sample{j}_ans.wav")
        cut, stuff = s.find_patt(patt, with_dwt=True, use_fastdtw=True)

        patt = Audio(f"./audio/patterns/trimed/trimed_nnoise_patt{i}.wav")
        nn_trimed, stuff = s.find_patt(patt, with_dwt=True, use_fastdtw=True)

        result.write("\nSample no.{:d}  {:^20}  {:^20}  {:>10.2f}  {:>10.2f}  {:>10.2f}  {:>10.2f}\n".format(\
                        j, correct_time[j], f"{round(norm_trimed_nnoise, 2)} / {round(time_ntn,2)}s", basic, nn_basic, nn_trimed, cut))
        result.flush()
        

result.close()