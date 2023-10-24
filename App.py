#!/usr/bin/env python3
import os
import Api
from util.Sentry import Sentry
from config.slave.config import meRaspb,version
import datetime
if __name__ == '__main__':
    print(os.linesep+"#################################################################"+os.linesep)
    print(f"Inicio de App Slave {datetime.datetime.now()} Version {version} "+os.linesep)
    print(f"Raspberry {meRaspb} "+os.linesep)
    print("#################################################################")
    Sentry.init()
    Api.app.run(host='0.0.0.0', port=meRaspb.port)
