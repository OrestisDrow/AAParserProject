"""
run_parser.py

This script is an entry point to the log parsing application. Its primary function is to
facilitate the extraction, parsing, and saving of structured metrics and errors from a specified
log file using the LogFileParser class.

Usage:
    To run this script, ensure that 'logfile.txt' is present in the same directory as the script 
    (or adjust the path as required). Simply execute the script, and it will process the log file, 
    parse the relevant sections, and save the parsed results to disk.

    The results, including structured summaries and parsing errors, are saved under the './RunResults/' directory.

Steps:
1. The script identifies the path to 'logfile.txt' using the resource_filename method.
2. An instance of LogFileParser is created with the log file path.
3. The log file is parsed using the parse() method of LogFileParser.
4. The parsed results and errors are saved to the disk using the save() method of LogFileParser.

Note:
    This script is designed to be a standalone utility. To adapt to different log file structures or 
    requirements, adjustments may need to be made to the LogFileParser class or the log file path specified in this script in case
    the user wants different behaviours (e.g. be able to explicitly specify the path and name of the log file etc.)

"""

import os
from pkg_resources import resource_filename
from logparser.log_file_parser import LogFileParser

def main():
    # The logfile.txt should be located in the same directory as run_parser.py
    log_file_path = resource_filename('logparser', 'logfile.txt')

    parser = LogFileParser(log_file_path)

    # Using the parse() method
    parsed_data = parser.parse()

    # Using the save() method to save results 
    # Automatically saves summaries and errors under ./RunResults/ 
    parser.save()

if __name__ == "__main__":
    main()
