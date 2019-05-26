"""
    audioIO

    Lib that wraps some input/output for .wav files
    record_to_file()
    play_from_file()
"""
from array import array
from struct import pack
import pyaudio
import wave


THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100


def record(seconds):
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
                    input=True, output=True,
                    frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h', stream.read(int(RATE * seconds)))

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    return sample_width, r

def record_to_file(path, length=3):
    '''
    Records from the microphone and outputs the
    resulting data to 'path'
    '''

    sample_width, data = record(length)
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

def play_from_file(path):
    wf = wave.open(path, 'rb')

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=1,
                    rate=RATE,
                    output=True)
    # getting info works wrong :/
    # stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
    #                 channels=wf.getnchannels(),
    #                 rate=wf.getframerate(),
    #                 output=True)
    # read data
    data = wf.readframes(CHUNK_SIZE)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK_SIZE)

    stream.stop_stream()
    stream.close()

    p.terminate()


if __name__ == '__main__':
    print("please speak a word into the microphone")
    record_to_file('demo.wav')
    print("done - result written to demo.wav")
    input("ready to listen?")
    play_from_file("demo.wav")
