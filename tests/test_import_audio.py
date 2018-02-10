import unittest
import audio2hdf5.importer

"""
Positive testing - I know it is bad, but I do not want to spent time with negative test cases for now :-)
"""


class AudioImportTestSet(unittest.TestCase):
    def setUp(self):
        print("SETUP!")
        self.test_directory = "/home/hanz/tmp/sounds/accents/"
        self.importer = audio2hdf5.importer.Importer(self.test_directory, overlap=22050)

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

    def test_name_to_index(self):
        sample_names = [("english1.ogg", 1), ("english22.ogg", 22), ("english001.ogg", 1)]
        for (name, idx) in sample_names:
            self.assertEqual(self.importer.parse_index(name), idx)

    def test_initialize(self):
        self.importer.initialize()
        self.assertTrue(self.importer.is_initialized())

    def test_read_data(self):
        self.importer.initialize()
        assert self.importer.__len__() > 0
        data_first = self.importer.__getitem__(0)
        data_last = self.importer.__getitem__(self.importer.__len__() - 1)

        assert data_first[0].shape[0] == self.importer.cut_interval
        assert data_last[0].shape[0] == self.importer.cut_interval
