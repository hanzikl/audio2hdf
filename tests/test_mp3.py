import unittest
import audio2hdf5.importer


class Mp3TestSet(unittest.TestCase):

    def setUp(self):
        print("SETUP!")
        self.test_directory = "/home/hanz/tmp/sounds/accents/"
        self.importer = audio2hdf5.importer.Importer(self.test_directory)

    def teardown(self):
        print("TEAR DOWN!")


    def test_mp3(self):
        print(self.importer.get_mp3_files())

    def test_convert_ogg(self):
        mp3file = self.importer.get_mp3_files()[0]
        oggfile = mp3file.replace('.mp3', '.ogg')
        self.importer.convert_mp3_to_ogg(mp3file)
        self.assertIn(oggfile, self.importer.get_ogg_files())

    def test_read_ogg(self):
        filename = self.importer.get_ogg_files()[0]
        data = self.importer.read_data_from_ogg(filename)

        self.assertIsNotNone(data)

