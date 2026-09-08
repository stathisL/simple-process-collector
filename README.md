# Simple Process Collector

## About this project

Version: 1.0.5\
Date: 28.03.2021

This is a small Python application part of exersice/requirement to implement a small process collector for an
operating system of preference. The scenario will be: A user runs Linux cmd and wants to collect process data
(already knowing the process name), for a given time. The results will be available in .csv file and on cmd.

The app collects the average CPU, Memory and File descriptors of a process.

## Environment

1. Fedora Linux 33 Workstation used as dev environment (Not tested with other Unix OSs and versions)
2. Python 3 is supported (more specifically it is implemented with version 3.9)
3. For the code and manual execution venv is suggested.

### Installation

Create a .venv (optional)
```
$ python -m venv .venv
$ source .venv/bin/activate
```

Install Python 3 dependencies:\
`$ pip install -r requirements.txt`

### Run

To run the collector app first we need to know a process name for example checking the ps -ef.
After, from collector/ path we can run:

`$ python src/collector.py <process_name> <overall_duration_in_seconds> -i <collection_interval_in_seconds>`

example:\
```
$ python src/collector.py firefox 10 -i 5

Process: firefox /  PID: 11931 

Please wait 10 seconds until data are collected...

+------------------+---------------------+-----------------------+
| CPU usage (%avg) | Memory (%avg in MB) | File desc open (%avg) |
+------------------+---------------------+-----------------------+
|       0.0        |       490.488       |          153          |
+------------------+---------------------+-----------------------+ 
```

for help:\
`$ python src/collector.py -h`

**NOTE**: For root processes access rights needed.

### Results

A report.csv file is created at the project level:\
`$ cat report.csv`

## Assumptions

1. No packaging needed for this app, but if I had to do then I would use .rpm for RedHat and
a .deb for Debian based, to have the majority of Linux systems covered or Python .whl.
If no package needed direct run is fine.

2. As assumption, I stop the program if the interval > duration it should not return anything.

3. In general, it will not be 100% accurate because of slight delays at the execution:\
    3a) % of cpu metric
        -- I allow the value 0 for interval which is unblocked and gives constantly data\
    3b) private memory metric
        -- I use the RES memory\
    3c) round floats to 3 digits (it is sufficient)

4. Regarding the .csv file:\
   4a) It will be created in the same folder in the collector, of course a configurable path chosen by the user
       can be implemented, but I won't do it in this case.\
   4b) As there are no specific requirements, I assume that one instance will run, otherwise the .csv file needs
       to get a timestamp or new name for every instance because both are writing in the same file.\
   4c) The name of the report file will be report.csv. The format of the .csv file will be in the
       form: time(each_second),cpu,mem,fd one <time_interval> per line. The time is kept as reference if needed to check
       the exact time or for future use (timing can also be done with logging).\
   4d) I will leave the .csv from last execution to override by the next run, of course it can cleaned up in the end
       (no requirement)

5. If the process terminates while collector running the psutil throws exception, I can raise an exception, but
   I leave it as it is to get it from the library.

6. For unit testing I chose to use the systemd as process, otherwise I have to create my own dummy
   initiate/start in test setup and remove/stop at the teardown.

7. I created this structure with modules (except that is a proper one) because I had in mind the deployment, so only
   the /scr can be build and before deploy the /tests dir can be used to test the code in automation CI/CD pipeline.

## Concerns

1. How long the collector can run (forever? years? months? days? hours?) I don't set any restriction
in the user input duration which is in secs.
- I suppose it can get the max int value which for me is:
```
>>> import sys
>>> print(sys.maxsize)
>>> 9223372036854775807
```

2. Not sure about the cpu metric regarding the cores and the total cpu that calculated, 
maybe I have to do something like / num_of_cpus? need to research.\
    2a) I saw cpu 102% for a process based on this I suspect that it's not in total cores.

3. The open file (report.csv) running and writing data if it's for a short time is fine but if it is for example for years
   writing all these data in 1 file is not sufficient. First need to estimate by collecting a process data
   the amount and after, most probably I would go split into multiple files for example per day and store
   them in archive folder.

## Improvements or upgrades

1. A memory leak requirement IS NOT IMPLEMENTED, I would try something with tracemalloc I would do as a next step.
2. List running process to choose as option.
3. Ability to search based on PID.
4. Add more unit tests.
5. Add more stats to collect.
6. Use threading to collect multiple processes data.
7. Give option to the user to set the path and the name of the csv file.
8. To reply at the "additional-extra", if I wanted to make cross-platform as a next step I would go object-oriented
   with classes for different OSs performing a check to get on which system is running and use the appropriate classes
   with overload or os system specific. Example: assert ('linux' in sys.platform). psutil supports different OSs but
   slight different names also the file paths for windows and unix should be taken care and the input of course.
