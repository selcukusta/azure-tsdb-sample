'''
    Azure TSDB Sample
'''
import datetime
import json
import sched
import time
import socket

import psutil
from azure.servicebus import ServiceBusService

SERVICE_NAMESPACE = "WRITE_EVENT_HUBS_NAME"
SHARED_ACCESS_KEY_NAME = "WRITE_SHARED_ACCESS_KEY_NAME"
SHARED_ACCESS_KEY_VALUE = "WRITE_SHARED_ACCESS_KEY_VALUE"
EVENT_HUB_NAME = "WRITE_EVENT_HUB_NAME"


def get_cpu_usage():
    '''
        Get CPU usage value
    '''
    write_to_azure(psutil.cpu_percent())
    TIMER.enter(5, 1, get_cpu_usage)


def write_to_azure(cpu_value):
    '''
        Write value to Azure TSDB
    '''
    bus_service = ServiceBusService(service_namespace=SERVICE_NAMESPACE,
                                    shared_access_key_name=SHARED_ACCESS_KEY_NAME,
                                    shared_access_key_value=SHARED_ACCESS_KEY_VALUE)
    message_object = {
        'timestamp' : str(datetime.datetime.utcnow()),
        'machine_name' : socket.gethostname(),
        'value' : cpu_value
    }
    print(message_object)
    message = json.dumps(message_object)
    bus_service.send_event(EVENT_HUB_NAME, message)


if __name__ == "__main__":
    TIMER = sched.scheduler(time.time, time.sleep)
    TIMER.enter(5, 1, get_cpu_usage)
    TIMER.run()
