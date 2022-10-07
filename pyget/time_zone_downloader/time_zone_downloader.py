from pyget.argument_parser import CommonArgumentParse
import argparse
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import csv
import os

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

# DOWNLOAD_URL should be set as ENVIRONMENT VARIABLE as a part of deployment
DOWNLOAD_URL = 'https://raw.githubusercontent.com/dmfilipenko/timezones.json/master/timezones.json'


class DownloadException(Exception):
    pass


class TimeZoneDownloader(CommonArgumentParse):

    @classmethod
    def parse_args(cls, args=None):
        parser = argparse.ArgumentParser()
        parser.add_argument('--match', help='Return the time zone which matches the value with supplied string')
        parser.add_argument('--offset', help='Matches the offset in the response and returns the matched time zones')
        parser.add_argument('--output_file_directory', help='Writes the output file to specified location, '
                                                            'default is current working directory',
                            default=os.getcwd())
        parser.add_argument('--output_file_name', help='Name of file to write to, default is time_zone_output.csv',
                            default='time_zone_output.csv')
        return parser.parse_args(args)

    @classmethod
    def create_object_from_args(cls, args):
        return cls(args.output_file_directory, args.output_file_name, args.match, args.offset)

    def __init__(self, output_file_directory, output_file_name, match=None, offset=None):
        self.match = match
        self.offset = offset
        self.output_file_directory = output_file_directory
        self.output_file_name = output_file_name

    def execute(self):
        """
        Executor function
        :return:None
        """
        _logger.info("Starting download.....")
        time_zone_response = self.get_url_data()
        filtered_data = self.filter_data(time_zone_response)
        self.write_to_csv(filtered_data)

    @staticmethod
    def get_url_data():
        """
        Make GET request to the API
        :return: Return JSON response from the API
        """

        with requests.Session() as sess:
            retries = Retry(
                total=3,
                backoff_factor=0.2,
                status_forcelist=[500, 502, 503, 504])

            sess.mount('http://', HTTPAdapter(max_retries=retries))
            sess.mount('https://', HTTPAdapter(max_retries=retries))

            response = sess.get(DOWNLOAD_URL)

        if response.status_code == 200:
            return response.json()
        else:
            raise DownloadException(
                f"Something went wrong..Status code returned - {response.status_code}. Please check")

    def filter_data(self, api_response_data):
        """
        Filters data based on match and offset supplied
        :param api_response_data: JSON response from the API
        :return:Filtered data if filter options are provided
        """
        filtered_result = api_response_data.copy()
        time_zone_index = 0
        if self.match:
            _logger.info(f"Filter based on following match - {self.match}")
            while time_zone_index < len(filtered_result):
                if filtered_result[time_zone_index]['value'].lower() != self.match.lower():
                    filtered_result.pop(time_zone_index)
                else:
                    time_zone_index = time_zone_index + 1
        # again resetting to 0, poping while traversing to reduce number of loops, also it is thread safe
        time_zone_index = 0
        if self.offset:
            _logger.info(f"Filter based on following offset - {self.offset}")
            while time_zone_index < len(filtered_result):

                if abs(filtered_result[time_zone_index]['offset']) != abs(int(self.offset)):
                    print(filtered_result[time_zone_index]['offset'])
                    filtered_result.pop(time_zone_index)
                else:
                    time_zone_index = time_zone_index + 1
        _logger.info(f"Number of records after filtering - {str(len(filtered_result))}")
        return filtered_result

    def write_to_csv(self, filtered_data):
        """
        Function to write response from API to CSV file, user readable form
        :param filtered_data: List of dicts to write
        :return: None
        """
        if len(filtered_data) == 0:
            _logger.info("Nothing to write.....skipping")
        else:
            output_path = os.path.join(self.output_file_directory, self.output_file_name)
            with open(output_path, 'w', encoding='utf8', newline='') as output_file:
                fc = csv.DictWriter(output_file,
                                    fieldnames=filtered_data[0].keys(),
                                    )
                fc.writeheader()
                fc.writerows(filtered_data)
            _logger.info(f"Output file written to {output_path}")

