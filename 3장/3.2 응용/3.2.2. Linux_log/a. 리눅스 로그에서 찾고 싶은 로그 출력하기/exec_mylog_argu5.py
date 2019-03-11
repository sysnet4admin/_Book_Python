#!/bin/env python
#-*- coding: utf-8 -*-

import mylog
import os

logfile = "/var/log/messages"
file_length = os.path.getsize(logfile)

mylog.printlog("/var/log/messages", "fail", int(file_length/2), 3, 5)
