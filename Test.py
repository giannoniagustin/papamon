#!/usr/bin/env python3
from model.StatusSlave import StatusSlave
from model.Raspberry import Raspberry
from model.Status import Status
from model.StatusSystem import StatusSystem
from util import TimeUtil
import datetime

  
  
print(TimeUtil.TimeUtil.timeToString(datetime.datetime.now(), TimeUtil.TimeUtil.format_DD_MM_YYYY_HH_MM))
