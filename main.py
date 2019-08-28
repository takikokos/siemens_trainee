"""
    main file

    shows functional of audio.py and audioIO.py
"""
from audio import Audio
from audioIO import record_to_file


if __name__ == "__main__":

    # you can record your own file,
    # it's better to remove noise from it
    # with s.prepare_file(trim=False, nnoise=True)
    sample = Audio("./audio/samples/reduced_noise/nnoise_sample5.wav")

    input("Prepare to record pattern, LENGTH = 1.5sec!")
    record_to_file("./demo_patt.wav", 1.5)
    pattern = Audio("./demo_patt.wav")
    pattern.prepare_file()

    # you can change use_fastdtw for more correct search, but time of search will be ~20sec
    # without dwt it will be worse and longer
    # no need to change k, it affects the time of search
    result, eval_time = sample.find_patt(pattern, with_dwt=True, use_fastdtw=False)
    print(f"Found at {result:.2f} sec, execution time : {eval_time:.2f} sec")
    sample.draw_waveform_plotly("demo.html", select_interval=[result, result + pattern.duration])
    