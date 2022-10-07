PyGet - Generic Python downloader repo
It can be used to download, data from API and write to CSV.
Any new implementation, needs to inherit and implement CommonArgumentParser class and get going.

Implementations -
TimeZoneDownloader
1.Downloads JSON dats from API
2.Filters data based on params passed.
3.Writes the data to CSV(user readable form) - default is current working directory

Python version - 3.9

Steps to setup -
1.Clone the code
2.Run the following command to create virtual env - python3 -m venv
3.Run the following command in project directory to see parameter description - venv/bin/python3 time_zone_executor.py -h
4.To test the command, run the following - venv/bin/python3 time_zone_executor.py --<arguments>


