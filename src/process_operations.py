import psutil
import os
import csv
import time
import logging

from datetime import datetime


def check_if_process_running(process_name):
    """
    Checks if there is any running process that contains the given name process name.

    :param process_name: Process name
    :type process_name: str
    :returns: True or False whether the process is running
    :rtype: bool
    """

    logging.info("In check_if_process_running")

    for proc in psutil.process_iter():
        if process_name.lower() == proc.name().lower():
            return True
    else:
        raise Exception(f"No PROCESS WITH NAME: {process_name} RUNNING!")


def find_process_id_by_name(process_name):
    """
    Get a list of all PIDs, of all running process whose name contains the given string process name.

    :param process_name: Process name
    :type process_name: str
    :returns: The ids of the requested process
    :rtype: list
    """

    logging.info("In find_process_id_by_name")

    processes = []

    try:
        for proc in psutil.process_iter():
            process_info = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            if process_name.lower() == process_info['name'].lower():
                processes.append(process_info)
    except IndexError:
        logging.error(f"FAILED TO FIND PID - PROCESSES LIST INDEX ERROR!", exc_info=True)

    return processes


def get_process_cpu_percent(process):
    """
    Obtains the CPU percentage of the given process.

    :param process: Process name
    :returns: Return the CPU usage of a process for a given interval
    :rtype: float
    """

    logging.info("In get_process_cpu_percent")

    return process.cpu_percent()


def get_process_ram_total(process):
    """
    Obtains the RES amount of RAM in MB.

    :param process: Process name
    :returns: RES (Resident size) memory value.
    :rtype: float
    """

    logging.info("In get_process_ram_total")

    return process.memory_info().rss / 1024 ** 2  # in MB


def get_open_file_descriptors(process):
    """
    Get the process open file descriptors.

    :param process: Process name
    :returns: The open file descriptors
    :rtype: int
    """

    logging.info("In get_open_file_descriptors")

    return process.num_fds()


def collect_metrics_in_csv_for_pid(process_info, duration, interval, filename):
    """
    Collect and store the requested metrics at a given duration in a .csv file.

    :param process_info:
    :param duration:
    :type duration: int
    :param interval:
    :type interval: int
    :param filename:
    :type filename: str
    :returns: Nothing to return, writes data to a .csv file
    :rtype: None
    """

    logging.info(f"In collect metrics trying to open a new file {filename}")

    try:
        with open(filename, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)

            end_time_secs = time.time() + duration
            # Collect the metrics for the given duration
            while time.time() < end_time_secs:
                # Stops the program for n seconds - interval logic
                time.sleep(interval)

                cpu = get_process_cpu_percent(process_info)
                mem = get_process_ram_total(process_info)
                fd = get_open_file_descriptors(process_info)

                current_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
                logging.info(f"In metrics collect - current time: {current_time} /"
                             f" cpu: {cpu} - mem: {mem} - file_desc: {fd}")
                # writing the fields at the csv
                csv_writer.writerow([current_time, cpu, mem, fd])
    except IOError:
        logging.error(f"ERROR WITH THE {filename}.csv FILE!", exc_info=True)
    finally:
        csv_file.close()


def calculate_metrics_average_from_csv(filename):
    """
    Calculates the average of every metric as column 0 value is the time, 1st value is cpu, 3rd value memory.

    :param filename: the name of the csv file
    :type filename: str
    :returns: average rounded to 3 digits cpu and memory and avg file descriptors
    :rtype: list
    """

    logging.info("In calculate_metrics_average_from_csv")

    try:
        file_path = os.path.join(os.getcwd(), filename)

        with open(file_path, 'r') as stats:
            cpu_sum = 0.0
            mem_sum = 0.0
            fd_sum = 0
            ln_count = 0

            for line in stats:
                ln_count += 1
                cpu_sum += float(line.split(',')[1])
                mem_sum += float(line.split(',')[2])
                fd_sum += float(line.split(',')[3])

            cpu_average = cpu_sum / ln_count
            mem_average = mem_sum / ln_count
            fd_average = fd_sum // ln_count

            # round values to 3 digits as assumption
            return [round(cpu_average, 3), round(mem_average, 3), int(fd_average)]
    except IOError:
        logging.error(f"ERROR WITH THE {filename}.csv FILE!", exc_info=True)
    finally:
        stats.close()
