import logging
import argparse

from prettytable import PrettyTable


def program_greeting(process_name, pid, duration):
    """
    Prints greeting info for the program at the beginning.

    :param process_name: proc_name
    :type process_name: str
    :param pid: process id
    :type pid: int
    :param duration: duration the simple-process-collector will run
    :type duration: int
    :returns: Print to cmd
    """

    logging.info("In program_greeting")

    print("---------------------------------------------------------------------")
    print(f"Process: {process_name} /  PID: {pid} \n")
    print(f"Please wait {duration} seconds until data are collected...\n")


def get_cmd_arguments(program_version):
    """
    Get user input from cmd with arguments.

    :param program_version: program version
    :returns: The process name, duration, interval from user input (cmd)
    :rtype: list
    """

    logging.info("In get_cmd_arguments")

    parser = argparse.ArgumentParser()

    parser.add_argument("process_name", type=str, help="The exact process name to get metrics")
    parser.add_argument("duration", type=int, help="Duration of data collection")
    parser.add_argument("-i", "--interval", type=int, help="Interval of data collection")
    parser.add_argument("-v", "--version", action="version", version=program_version, help="Show the version number")

    args = parser.parse_args()

    logging.info(f"User input: proc_name - {args.process_name}, duration - {args.duration}, interval - {args.interval}")

    # Default interval 5 secs else get from cmd
    interval = args.interval if args.interval else 5

    if interval <= args.duration:
        return [args.process_name, args.duration, interval]
    else:
        logging.error("The interval cannot be more than the duration! Please give a lower interval.")
        raise ValueError("The interval cannot be more than the duration! Please give a lower interval.")


def format_data_output_to_cmd(metrics):
    """
    Prints the table with the collected values at cmd.

    :param metrics: list of metrics collected
    :returns: None
    """

    logging.info("In format_data_output_to_cmd")

    header = ["CPU usage (%avg)", "Memory (%avg in MB)", "File desc open (%avg)"]

    table = PrettyTable(header)
    table.add_row(metrics)

    print(table, "\n")
