import os
import re
import subprocess as sp

import soundfile

FFMPEG_BIN = "ffmpeg"

"""
Class for importing mp3 audio to hdf5 format using
- preprocessing (conversion to ogg format)
- import ogg to python
"""


def transform_data(data):
    # normalization to the interval [0, 1]
    return (data + 1) / 2


class Importer:
    extension_mp3 = ".mp3"
    extension_ogg = ".ogg"

    def __init__(self, directory, cutinterval=44100, overlap=0):
        """
        Init importer on given directory
        :param directory:
        :param cutinterval: length of one sample
        :param overlap: size of overlapping
        """
        self.directory = directory
        self.data_mapping = None

        assert cutinterval > overlap, "Cutinterval must be longer than overlap"
        self.cut_interval = cutinterval
        self.overlap = overlap

        self.cached_data = (None, None)

    def get_files_with_extension(self, extension):
        return [file_name for file_name in os.listdir(self.directory) if file_name.endswith(extension)]

    def get_mp3_files(self):
        return self.get_files_with_extension(self.extension_mp3)

    def get_ogg_files(self):
        return self.get_files_with_extension(self.extension_ogg)

    def convert_mp3_to_ogg(self, filename: str):
        """
            converts given filename from mp3 to ogg file if ogg does not already exists
            this function is definitely NOT SAFE
        """
        mp3_path = os.path.join(self.directory, filename)
        ogg_path = mp3_path.replace(self.extension_mp3, self.extension_ogg)
        if os.path.isfile(ogg_path):
            # already done
            return
        command = [FFMPEG_BIN, '-i', mp3_path, ogg_path]
        pipe = sp.Popen(command, shell=False, stdout=sp.PIPE)
        pipe.wait()

    def read_data_from_ogg(self, filename):
        filepath = os.path.join(self.directory, filename)
        data, sample_rate = soundfile.read(filepath)

        return data, sample_rate

    def parse_index(self, filename: str):
        index = int(re.findall(r'\d+\.ogg$', filename)[0].replace('.ogg', ''))
        return index

    def is_initialized(self):
        return self.data_mapping is not None

    def initialize(self):
        data_mapping = []
        for mp3_file in self.get_mp3_files():
            self.convert_mp3_to_ogg(mp3_file)

        sample_rate_check = None
        for ogg_file in self.get_ogg_files():
            data, sample_rate = self.read_data_from_ogg(ogg_file)
            if sample_rate_check is not None:
                if sample_rate != sample_rate_check:
                    print("Skipping file {} due sample rate mismatch (base :{}, current: {})"
                          .format(ogg_file, sample_rate_check, sample_rate))
            else:
                sample_rate_check = sample_rate

            audio_file_index = self.parse_index(ogg_file)
            # count samples in file and create mapping

            for i in range(0, data.shape[0] - self.cut_interval, self.cut_interval - self.overlap):
                data_mapping.append((ogg_file, audio_file_index, i))

        self.data_mapping = data_mapping

    def cache_data(self, filename):

        if self.cached_data[0] != filename:
            data, _ = self.read_data_from_ogg(filename)
            self.cached_data = (filename, data)

    def read_cached_data(self, filename, start_index, end_index):
        self.cache_data(filename)
        if (len(self.cached_data[1].shape) > 1) and (self.cached_data[1].shape[1] > 1):
            # more than one audio channel
            return self.cached_data[1][start_index: end_index, 0]
        else:
            # one audio channel
            return self.cached_data[1][start_index: end_index]

    def __len__(self):
        return len(self.data_mapping)

    def __getitem__(self, item):
        mapping = self.data_mapping[item]
        data = transform_data(self.read_cached_data(mapping[0], mapping[2], mapping[2] + self.cut_interval))
        return data, mapping[1]
