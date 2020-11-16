#!/usr/bin/env python3

"""
This script takes a log file url, start_time, end_time and error_code as input arguments and 
returns output in below format

The site has returned a total of <number> 200 responses, and <number>
<error code> responses, out of total <number> requests between time
XXXXX and time YYYYY
That is a <percent> <error code> errors, and <percent> of 200
responses.

USAGE: python3 nginx-log-parser.py -l LOG_FILE_URL -s START_TIME -e END_TIME -c ERROR_CODE
"""

import urllib.request
import argparse
import logging
import re
from datetime import datetime
import pytz

# set timezone to UTC
tz = pytz.timezone('UTC')
# set log level
logging.basicConfig(level=logging.INFO)


def log_parser(log_file_url, start_time, end_time, error_code):
    """Reads logs from log file url.
    Does the required calculations and returns a dict object."""

    total = status_200 = status_error_code = 0      # Declaring initial values for total, 200 status code and input error code requests
    log_format = r'^(?P<ipaddress>\S+) - - \[(?P<datetime>[^\]]+)\] "(GET|POST)([^."]+)?.HTTP\/1\.1" (?P<statuscode>[0-9]{3}) ([0-9]+|-) (-|"([^"]+)") (["]([^"]+)["])'

    try:
        logging.info('Reading the logs from file...')
        file = urllib.request.urlopen(log_file_url)

        logging.info('Calculating the count of response codes...')
        for line in file:
            decoded_line = line.decode("utf-8")
            log = re.search(log_format, decoded_line)       # Check if log(each line in the file) is of proper format
            if log:
                # Increase total response count by 1 and Normalizes log's timezone to UTC
                total += 1
                date_time = log.group('datetime')
                log_datetime = tz.normalize(datetime.strptime(date_time, '%d/%b/%Y:%H:%M:%S %z'))

                # Compare log's datetime with start & end times. Do calculation for both 200 and error status codes
                if start_time <= log_datetime <= end_time:
                    if log.group('statuscode') == 200:
                        status_200 += 1
                    elif log.group('statuscode') == error_code:
                        status_error_code += 1

        logging.info('Calculating the percent of response codes...')
        return {
            'Total': total,
            '200_code': status_200,
            'error_code': status_error_code,
            '200_code_percent': round((status_200/total)*100, 2),
            'error_code_percent': round((status_error_code/total)*100, 2)
            }

    except Exception as e:
        logging.exception(e)


def valid_datetime(d):
    """Validates the START and END TIME argument values
    and convert the times to UTC timezone."""

    try:
        logging.info(f'Converting datetime {d} string to datetime object...')
        dt = datetime.strptime(d, '%d/%b/%Y:%H:%M:%S %z')
        logging.info(f'Normalizing {dt} timezone to UTC...')
        return tz.normalize(dt)

    except ValueError as err:
        logging.critical(f'Not a Valid datetime {d}')
        logging.exception(err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to parse Nginx logs')
    parser.add_argument('-l', '--log_file_url', help='Logs file URL', required=True)
    parser.add_argument('-s', '--start_time', help='Start datetime - format DD/MONTH/YYYY:H:M:S +/-tz', required=True, type=valid_datetime)
    parser.add_argument('-e', '--end_time', help='End datetime - format DD/MONTH/YYYY:H:M:S +/-tz', required=True, type=valid_datetime)
    parser.add_argument('-c', '--error_code', help='Server response code', required=True)
    args = parser.parse_args()

    output = log_parser(args.log_file_url, args.start_time, args.end_time, args.error_code)

    result = f'''The site has returned a total of {output['200_code']} 200 responses, and {output['error_code']} {args.error_code} responses, 
    out of total {output['Total']} requests between time {args.start_time} and time {args.end_time}
    That is a {output['error_code_percent']}% {args.error_code} errors, and {output['200_code_percent']}% of 200 responses.'''

    print(result)
