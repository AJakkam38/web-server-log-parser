#!/usr/bin/env python3

"""
This script takes a log file, start_time, end_time and error_code as input arguments and 
returns output in below format

The site has returned a total of <number> 200 responses, and <number>
<error code> responses, out of total <number> requests between time
XXXXX and time YYYYY
That is a <percent> <error code> errors, and <percent> of 200
responses.

USAGE: nginx-log-parser.py -l LOG_FILE_PATH -s START_TIME -e END_TIME -c ERROR_CODE
"""

import argparse
import logging
import re
from datetime import datetime
import pytz

tz = pytz.timezone('UTC')
# set log level
logging.basicConfig(level=logging.INFO)

def log_parser(log_file, start_time, end_time, error_code):
    total = 0 
    status_200 = 0
    status_error_code = 0
    log_format = r'^(?P<ipaddress>\S+) - - \[(?P<datetime>[^\]]+)\] "(GET|POST)([^."]+)?.HTTP\/1\.1" (?P<statuscode>[0-9]{3}) ([0-9]+|-) (-|"([^"]+)") (["]([^"]+)["])'
    
    try:
        with open(log_file, 'r') as file:
            logging.info(f'Reading the log file - {log_file}')
            for line in file:
                log = re.search(log_format, line)
                if log:
                    total += 1
                    logging.info(f'Calculating the count of response codes...')
                    date_time = log.group('datetime')
                    log_datetime = tz.normalize(datetime.strptime(date_time, '%d/%b/%Y:%H:%M:%S %z'))

                    if start_time <= log_datetime <= end_time:
                        if log.group('statuscode') == 200:
                            status_200 += 1
                        elif log.group('statuscode') == error_code:
                            status_error_code += 1

        logging.info(f'Calculating the percent of response codes...')
        return {
            'Total':total,
            '200_code': status_200, 
            'error_code': status_error_code, 
            '200_code_percent': round((status_200/total)*100, 2), 
            'error_code_percent': round((status_error_code/total)*100, 2)
            }

    except Exception as e:
        logging.exception(e)

def valid_datetime(d):
    try:
        logging.info(f'Converting datetime {d} string to datetime object...')
        dt = datetime.strptime(d, '%d/%b/%Y:%H:%M:%S %z')
        logging.info(f'Normalizing {dt} timezone to UTC...')
        return tz.normalize(dt)
    except ValueError as err:
        logging.critical(f'Not a Valid datetime {d}')
        logging.exception(err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Script to parse Nginx logs')
    parser.add_argument('-l', '--log_file_path', help='Logs file path', required=True)
    parser.add_argument('-s', '--start_time', help='Start datetime - format DD/MONTH/YYYY:H:M:S +/-tz', required=True, type=valid_datetime)
    parser.add_argument('-e', '--end_time', help='End datetime - format DD/MONTH/YYYY:H:M:S +/-tz', required=True, type=valid_datetime)
    parser.add_argument('-c', '--error_code', help='Server response code', required=True)
    args = parser.parse_args()

    output = log_parser(args.log_file_path, args.start_time, args.end_time, args.error_code)

    result = f'''The site has returned a total of {output['200_code']} 200 responses, and {output['error_code']} {args.error_code} responses, 
    out of total {output['Total']} requests between time {args.start_time} and time {args.end_time}
    That is a {output['error_code_percent']}% {args.error_code} errors, and {output['200_code_percent']}% of 200 responses.'''

    print(result)