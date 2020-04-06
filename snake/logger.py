#!/usr/bin/python

import datetime


class Logger:
    def __init__(self, log_level=2):
        self.__log_level = log_level

    def log_debug(self, message_to_log):
        if self.__log_level > 1:
            print("Application log:", message_to_log)
            log_file = open("log.txt", "a")
            log_file.write(datetime.datetime.now().strftime("%Y/%m/%d_%H:%M:%S ") + message_to_log + "\n")
            log_file.close()
