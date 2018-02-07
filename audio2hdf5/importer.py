import os
import subprocess as sp

FFMPEG_BIN = "ffmpeg"

"""
Class for importing mp3 audio to hdf5 format using
- preprocessing (conversion to ogg format)
- import ogg to python
"""


class Importer:
    extension_mp3 = ".mp3"
    extension_ogg = ".ogg"

    def __init__(self, directory):
        self.directory = directory

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