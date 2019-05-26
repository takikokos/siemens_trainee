"""
    audio

    This lib contains main class for searching 
    and visualization of audio waveform 
"""
import wave
import numpy as np
import math
from sox import Transformer
from time import time
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from pywt import dwt


types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def format_time(x, audio, pos=None):
    w, h = 800, 300
    k = audio.nframes//w//32
    progress = int(x / float(audio.nframes) * audio.duration * k)
    mins, secs = divmod(progress, 60)
    hours, mins = divmod(mins, 60)
    out = "%d:%02d" % (mins, secs)
    if hours > 0:
        out = "%d:" % hours
    return out

def format_db(x, audio, pos=None):
    '''
        log scale
    '''
    if pos == 0:
        return ""
    if x == 0:
        return "-inf"

    db = 20 * math.log10(abs(x) / float(audio.peak))
    return int(db)

class Audio:
    def __init__(self, fname):
        '''
            opens .wav audio file with fname
        '''
        self.wav_fname = fname
        try:
            with wave.open(fname, mode="r") as wav:
                self.nchannels,  self.sampwidth,  self.framerate,  self.nframes,  self.comptype,  self.compname = wav.getparams()
                self.duration = self.nframes / self.framerate
                self.peak = 256 ** self.sampwidth / 2
                self.content = wav.readframes(self.nframes)
                self.samples = np.fromstring(self.content, dtype=types[self.sampwidth])
                self.tsm = Transformer()
                return
        except FileNotFoundError as err:
            print(err)
            print("Try Audio.reload_file function")
            raise FileNotFoundError

    def reload_file(self, fname=None):
        '''
            recalls the init function
        '''
        if fname:
            self.__init__(fname)
        else:
            self.__init__(self.wav_fname)
        return

    def prepare_file(self, fname=None, trim=True, nnoise=True, reload=True):
        '''
            trims and reduce noise on file

            should automatically trim the silent regions from the beginning/end,
            so you should use trim with nnoise

            reload - determines whether to reload the audio file
            fname - name of output, changed file
        '''
        if nnoise:
            self.tsm.noiseprof(self.wav_fname, self.wav_fname.rstrip(".wav") + '_noiseprof')
            self.tsm.noisered(self.wav_fname.rstrip(".wav") + '_noiseprof')
        if trim:
            self.tsm.silence(1)
            self.tsm.silence(-1)
        if fname:
            outname = fname
        else:
            outname = self.wav_fname.rstrip(".wav") + "_nnoise_trim.wav"
        self.tsm.build(self.wav_fname, outname)
        if reload:
            self.reload_file(fname=outname)
    
    def find_patt(self, patt, k=100, use_fastdtw=False, with_dwt=True ) -> (float, float):
        '''
            patt - pattern, Audio object
            k - downsampling coefficient, integer
            use_fastdtw - determines whether to use dtw for distance or just euclidean distance
            with_dwt - use single level Discrete Wavelet Transform for data

            return: time of found pattern in seconds and time of search
        '''

        evaltime = time()

        # prepare samples
        data = self.samples
        pattern = patt.samples
        data = data[0::k]
        pattern = pattern[0::k]
        data = (data - data.mean()) / data.std()
        pattern = (pattern - pattern.mean()) / pattern.std()
        if with_dwt:
            data, *_ = dwt(data, 'db1')
            pattern, *_ = dwt(pattern, 'db1')

        distances = []
        maxcount = len(data) - len(pattern) + 1
        for i in range(maxcount):
            if use_fastdtw:
                distances.append(fastdtw(data[i:i+len(pattern)], pattern, dist=euclidean)[0])
            else:
                distances.append(euclidean(data[i:i+len(pattern)], pattern))

        evaltime = time() - evaltime
        res = (distances.index(min(distances)) / len(data)) * self.duration

        return res, evaltime

    def draw_waveform_matplotlib(self, fname=None, save=False):
        '''
            better use plotly, does the same
        '''
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker

        w, h = 800, 300
        # k = self.nframes//w//32
        DPI = 72

        plt.figure(1, figsize=(float(w)/DPI, float(h)/DPI), dpi=DPI)
        plt.subplots_adjust(wspace=0, hspace=0)

        for n in range(self.nchannels):
            channel = self.samples[n::self.nchannels]

            # channel = channel[0::k]
            # if self.nchannels == 1:
            #     channel = channel - self.peak

            axes = plt.subplot(2, 1, n+1)
            axes.plot(channel, "g")
            axes.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos = None : format_db(x, self, pos=pos)))
            plt.grid(True, color="w")
            axes.xaxis.set_major_formatter(ticker.NullFormatter())

        axes.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos = None : format_time(x, self, pos=pos)))
        if save:
            if fname == None:
                plt.savefig(self.wav_fname.rstrip(".wav") + "_waveform", dpi=DPI)
            else:
                plt.savefig(fname, dpi=DPI)
        plt.show()

    def draw_waveform_plotly(self, fname=None, save=False, select_interval=None):
        '''
            fname - name for .html file
            save - if True saves to png with the fname
            select_interval - (float, float) - time for colouring the data
        '''

        import plotly.offline as py
        import plotly.graph_objs as go

        time = [(x / float(self.nframes) * self.duration) for x in range(self.nframes)]
        # samples = [20 * math.log10(abs(x-peak) / float(peak)) if x != 0 else "-inf" for x in samples]
        graphs = []
        if select_interval:
            start = round((select_interval[0] / self.duration) * self.nframes)
            end = round((select_interval[1] / self.duration) * self.nframes)

            before_start = go.Scatter(
                x = time[:start],
                y = self.samples[:start],
                mode = 'lines',
                name = 'sample',
                line={
                        "color" : "#0000ff"
                }
            )
            graphs.append(before_start)
            after_start = go.Scatter(
                x = time[start:end],
                y = self.samples[start:end],
                mode = 'lines',
                name = 'pattern',
                line={
                        "color" : "#ff0000"
                }
            )
            graphs.append(after_start)
            after_end = go.Scatter(
                x = time[end:],
                y = self.samples[end:],
                mode = 'lines',
                name = 'sample',
                line = {
                        "color" : "#0000ff"
                }
            )
            graphs.append(after_end)
        else:
            trace = go.Scatter(
                x = time,
                y = self.samples,
                mode = 'lines',
                name = 'sample'
            )
            graphs.append(trace)

        layout = dict(title = f"{self.wav_fname[self.wav_fname.rfind('/'):]} waveform",
            #   yaxis = dict(zeroline = False),
              xaxis = dict(title = "Time in seconds")
             )
        fig = dict(data=graphs, layout=layout)
        if fname == None:
            if save:
                py.plot(fig, filename=(self.wav_fname.rstrip(".wav") + "_waveform.html"), image='png')
            else:
                py.plot(fig, filename=(self.wav_fname.rstrip(".wav") + "_waveform.html"))
        else:
            if save:
                py.plot(fig, filename=fname, image='png')
            else:
                py.plot(fig, filename=fname)
            

if __name__ == "__main__":
    s = Audio("./audio_samples/samples/sample1.wav")
    p = Audio("./audio_samples/patterns/patt1.wav")
    print("\nResults of find_patt for sample1.wav and patt1.wav")
    res, evaltime = s.find_patt(p)
    print(f"\nPattern starts at {res}sec, evaltime : {evaltime}, not used fastdtw, not used dwt")
    res, evaltime = s.find_patt(p, use_fastdtw=True)
    print(f"\nPattern starts at {res}sec, evaltime : {evaltime}, used fastdtw, not used dwt")
    res, evaltime = s.find_patt(p, with_dwt=True)
    print(f"\nPattern starts at {res}sec, evaltime : {evaltime}, not used fastdtw, used dwt")
    res, evaltime = s.find_patt(p, use_fastdtw=True, with_dwt=True)
    print(f"\nPattern starts at {res}sec, evaltime : {evaltime}, used fastdtw, used dwt")