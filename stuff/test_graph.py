import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import wave

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def format_time(x, pos=None):
    global duration, nframes, k
    progress = int(x / float(nframes) * duration * k)
    mins, secs = divmod(progress, 60)
    hours, mins = divmod(mins, 60)
    out = "%d:%02d" % (mins, secs)
    if hours > 0:
        out = "%d:" % hours
    return out

def format_db(x, pos=None):
    if pos == 0:
        return ""
    global peak
    if x == 0:
        return "-inf"

    db = 20 * math.log10(abs(x) / float(peak))
    return db#int(db)

def draw_wave_form(filename : str):
    wav = wave.open(filename, mode="r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

    duration = nframes / framerate
    w, h = 800, 300
    k = nframes//w//32
    DPI = 72
    peak = 256 ** sampwidth / 2

    content = wav.readframes(nframes)
    samples = np.fromstring(content, dtype=types[sampwidth])

    import plotly.offline as py
    import plotly.graph_objs as go

    time = [(x / float(nframes) * duration) for x in range(nframes)]
    # samples = [20 * math.log10(abs(x-peak) / float(peak)) if x != 0 else "-inf" for x in samples]

    # Create a trace
    trace = go.Scatter(
        x = time,
        y = samples,
        mode = 'lines',
        # line={
        #     "color" : "#0000ff"
        # }
    )
    data = [trace]

    # Plot and embed in ipython notebook!
    py.plot(data, filename=(filename.rstrip(".wav") + "_waveform.html"))



# double the volume 

# from struct import pack
# data = [x * 20 for x in samples]
# data = pack('<' + ('i'*len(samples)), *data)

# wf = wave.open("demo2.wav", 'wb')
# wf.setnchannels(1)
# wf.setsampwidth(sampwidth)
# wf.setframerate(framerate)
# wf.writeframes(data)
# wf.close()

# end

# matplotlib waveform


# plt.figure(1, figsize=(float(w)/DPI, float(h)/DPI), dpi=DPI)
# plt.subplots_adjust(wspace=0, hspace=0)

# for n in range(nchannels):
#     channel = samples[n::nchannels]

#     channel = channel[0::k]
#     if nchannels == 1:
#         channel = channel - peak

#     axes = plt.subplot(2, 1, n+1)#, axisbg="k")
#     axes.plot(channel, "g")
#     axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db))
#     plt.grid(True, color="w")
#     axes.xaxis.set_major_formatter(ticker.NullFormatter())

# axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
# plt.savefig("wave", dpi=DPI)
# plt.show()


# plotly waveform

# import plotly.offline as py
# import plotly.graph_objs as go

# time = [(x / float(nframes) * duration) for x in range(nframes)]
# # samples = [20 * math.log10(abs(x-peak) / float(peak)) if x != 0 else "-inf" for x in samples]

# # Create a trace
# trace = go.Scatter(
#     x = time[:len(time) // 3],
#     y = samples[:len(time) // 3],
#     mode = 'lines',
#     line={
#         "color" : "#0000ff"
#     }
# )

# trace2 = go.Scatter(
#     x = time[len(time) // 3:len(time) // 3 * 2],
#     y = samples[len(time) // 3:len(time) // 3 * 2],
#     mode = 'lines',
#     line={
#         "color" : "#FFBAD2"
#     }
# )

# trace3 = go.Scatter(
#     x = time[len(time) // 3 * 2:],
#     y = samples[len(time) // 3 * 2:],
#     mode = 'lines',
#     line={
#         "color" : "#0000ff"
#     }
# )

# data = [trace, trace2, trace3]

# # Plot and embed in ipython notebook!
# py.plot(data, filename='basic-scatter.html')

# # or plot with: plot_url = py.plot(data, filename='basic-line')

if __name__ == "__main__":
    from audiorec import Audio
    s = Audio("./audio_samples/samples/sample1.wav")
    data = s.samples
    from pywt import dwt
    data, *_ = dwt(data, 'db1')

    import plotly.offline as py
    import plotly.graph_objs as go

    time = [(x / float(s.nframes) * s.duration) for x in range(s.nframes)]
        # samples = [20 * math.log10(abs(x-peak) / float(peak)) if x != 0 else "-inf" for x in samples]

    trace = go.Scatter(
        x = time,
        y = data,
        mode = 'lines',
    )
    py.plot([trace], filename="./audio_samples/stuff_waveforms/sample1_after_dwt_waveform.html")