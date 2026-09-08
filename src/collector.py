#!/usr/bin/env python


import cli_output
import process_operations
import psutil
import logging


author = "Stathis Lytras"
collector_version = "1.0.5"
python_version = "3.9"
date = "28.03.2021"


def main():
    # INFO, WARNING (default) and ERROR are in use.
    logging.basicConfig(level=logging.WARNING)

    filename = "report.csv"

    process_name, duration, interval = cli_output.get_cmd_arguments(collector_version)

    logging.info("Check if the process is running.")
    process_operations.check_if_process_running(process_name)

    logging.info("Find process id by name call.")
    pid = process_operations.find_process_id_by_name(process_name)[0]['pid']

    logging.info("Program greeting call.")
    cli_output.program_greeting(process_name, pid, duration)

    process_info = psutil.Process(pid)

    logging.info("Collect metrics call.")
    # Collect data to a .csv every interval in the duration given
    process_operations.collect_metrics_in_csv_for_pid(process_info, duration, interval, filename)

    logging.info("Output data call.")
    # Print collected stats to table at cmd
    cli_output.format_data_output_to_cmd(process_operations.calculate_metrics_average_from_csv(filename))


if __name__ == '__main__':
    main()
