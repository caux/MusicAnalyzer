import os
import numpy as np
import scipy.io.wavfile as wav
from pipes import quote


def convert_wav_files_to_nptensor(wavFile, block_size, useTimeDomain=False):
    print 'Processing Filename: ', wavFile

    bitrate, data = readWav(wavFile)

    x_t = breakWavIntoBlocks(data, block_size)
    y_t = x_t[1:]

    y_t.append(np.zeros(block_size))  # Add special end block composed of all zeros

    if useTimeDomain:
        return x_t, y_t

    X = fftBlocks(x_t)
    Y = fftBlocks(y_t)

    return X, Y


def breakWavIntoBlocks(song_np, block_size):
    block_lists = []
    total_samples = len(song_np)
    num_samples_so_far = 0
    while num_samples_so_far < total_samples:
        block = song_np[num_samples_so_far:num_samples_so_far + block_size]
        if block.shape[0] < block_size:
            padding = np.zeros((block_size - block.shape[0],))
            block = np.concatenate((block, padding))
        block_lists.append(block)
        num_samples_so_far += block_size
    return block_lists


def fftBlocks(blocks_time_domain):
    fft_blocks = []
    for block in blocks_time_domain:
        fft_block = np.fft.fft(block)
        new_block = np.concatenate((np.real(fft_block), np.imag(fft_block)))
        fft_blocks.append(new_block)
    return fft_blocks


def readWav(wavFile):
    bitrate, loadedData = wav.read(wavFile)
    data = loadedData.astype('float32') / 32767.0

    return bitrate, data


def convert_mp3_to_wav(filename, sample_frequency):
    ext = filename[-4:]

    if ext != '.mp3':
        return

    files = filename.split('/')
    orig_filename = files[-1][0:-4]
    new_path = ''

    if filename[0] == '/':
        new_path = '/'

    for i in xrange(len(files) - 1):
        new_path += files[i] + '/'

    tmp_path = new_path + 'tmp'

    if not os.path.exists(new_path):
        os.makedirs(new_path)
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    filename_tmp = tmp_path + '/' + orig_filename + '.mp3'
    new_name = new_path + orig_filename + '.wav'

    if os.path.exists(new_name):
        print "File exists, done!"
        return new_name

    sample_freq_str = "{0:.1f}".format(float(sample_frequency) / 1000.0)
    cmd = 'lame -a -m m {0} {1}'.format(quote(filename), quote(filename_tmp))
    os.system(cmd)
    cmd = 'lame --decode {0} {1} --resample {2}'.format(quote(filename_tmp), quote(new_name),
                                                        sample_freq_str)
    os.system(cmd)

    # cleanup
    os.remove(filename_tmp)
    os.rmdir(tmp_path)

    return new_name
