import unittest
from unittest import mock
from unittest.mock import patch
import os
from pyget.time_zone_downloader.time_zone_downloader import requests
from pyget.time_zone_downloader.time_zone_downloader import TimeZoneDownloader
from pyget.time_zone_downloader.time_zone_downloader import DownloadException


class TestTimeZoneDownloader(unittest.TestCase):
    def _mock_response(self, status_code=200, text='test', json=None):
        mock_resp = mock.Mock()
        mock_resp.status_code = status_code
        mock_resp.text = text
        if json:
            mock_resp.json = mock.Mock(return_value=json)
        return mock_resp

    def setUp(self) -> None:
        self.mock_response = [
            {
                "value": "Dateline Standard Time",
                "abbr": "DST",
                "offset": -12,
                "isdst": False,
                "text": "(UTC-12:00) International Date Line West",
                "utc": [
                    "Etc/GMT+12"
                ]
            },
            {
                "value": "Test Value String",
                "abbr": "U",
                "offset": -11,
                "isdst": False,
                "text": "(UTC-11:00) Coordinated Universal Time-11",
                "utc": [
                    "Etc/GMT+11",
                    "Pacific/Midway",
                    "Pacific/Niue",
                    "Pacific/Pago_Pago"
                ]
            }]
        self.offset = 12
        self.match = 'Test Value String'
        self.output_file_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resourcses')
        self.output_file_name = 'test.csv'
        self.expected_file = 'test-1.csv'

    @patch.object(requests.Session, 'get')
    @patch.object(requests.Session, 'mount')
    def test_get_url_data(self, mock_mount, mock_get):
        mock_get.return_value = self._mock_response(json={'a': 'b'})
        expected_value = {'a': 'b'}
        mock_mount.return_value = None
        test_object = TimeZoneDownloader('a', 'a.csv')
        actual_val = test_object.get_url_data()
        self.assertEqual(expected_value, actual_val)

    @patch.object(requests.Session, 'get')
    @patch.object(requests.Session, 'mount')
    def test_get_url_data_exception(self, mock_mount, mock_get):
        mock_get.return_value = self._mock_response(json={'a': 'b'}, status_code=404)
        mock_mount.return_value = None
        test_object = TimeZoneDownloader('a', 'a.csv')
        with self.assertRaises(DownloadException):
            test_object.get_url_data()

    def test_filter_data_match(self):
        expected_value = [{
            "value": "Test Value String",
            "abbr": "U",
            "offset": -11,
            "isdst": False,
            "text": "(UTC-11:00) Coordinated Universal Time-11",
            "utc": [
                "Etc/GMT+11",
                "Pacific/Midway",
                "Pacific/Niue",
                "Pacific/Pago_Pago"
            ]
        }]
        #This also tests the case insensitivity
        test_object = TimeZoneDownloader('a', 'a.csv', 'Test value string')
        actual_value = test_object.filter_data(self.mock_response)
        self.assertEqual(expected_value,actual_value)

    def test_filter_data_offset(self):
        expected_value = [{
            "value": "Test Value String",
            "abbr": "U",
            "offset": -11,
            "isdst": False,
            "text": "(UTC-11:00) Coordinated Universal Time-11",
            "utc": [
                "Etc/GMT+11",
                "Pacific/Midway",
                "Pacific/Niue",
                "Pacific/Pago_Pago"
            ]
        }]
        #This also tests - the check for absolute value of offset(i.e. ahead and behind)
        test_object = TimeZoneDownloader('a', 'a.csv', match=None,offset=11)
        actual_value = test_object.filter_data(self.mock_response)
        print(actual_value)
        self.assertEqual(expected_value,actual_value)

    def test_filter_data_offset_match(self):
        expected_value = [{
                "value": "Dateline Standard Time",
                "abbr": "DST",
                "offset": -12,
                "isdst": False,
                "text": "(UTC-12:00) International Date Line West",
                "utc": [
                    "Etc/GMT+12"
                ]
            }]
        #This also tests - the check for absolute value of offset(i.e. ahead and behind)
        test_object = TimeZoneDownloader('a', 'a.csv', match='Dateline Standard Time',offset=12)
        actual_value = test_object.filter_data(self.mock_response)
        self.assertEqual(expected_value,actual_value)
