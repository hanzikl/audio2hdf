import unittest
import audio2hdf5.importer


class Mp3TestSet(unittest.TestCase):

    def setUp(self):
        print("SETUP!")
        self.test_directory = "/home/hanz/tmp/sounds/accents/"

    def teardown(self):
        print("TEAR DOWN!")


    def test_mp3(self):
        importer = audio2hdf5.importer.Importer(self.test_directory)
        print(importer.get_mp3_files())

    def test_ogg(self):
        importer = audio2hdf5.importer.Importer(self.test_directory)
        mp3file = importer.get_mp3_files()[0]
        oggfile = mp3file.replace('.mp3', '.ogg')
        importer.convert_mp3_to_ogg(mp3file)
        self.assertIn(oggfile, importer.get_ogg_files())

