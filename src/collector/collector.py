from psutil import cpu_percent, virtual_memory, disk_io_counters, net_io_counters, pids, net_connections
from pandas import Timestamp

def get_timestamp() -> float:
    pd_time = Timestamp.now()
    unix_time = pd_time.timestamp()
    return unix_time

def memory_percent() -> float: # returns RAM usage
    RAM_usage_percent = virtual_memory().percent
    return RAM_usage_percent

def disk_read_bytes() -> int: # returns disk read bytes usage
    bytes_read = disk_io_counters().read_bytes
    return bytes_read

def disk_write_bytes() -> int: # returns disk written bytes
    bytes_written = disk_io_counters().write_bytes
    return bytes_written

def net_bytes_sent() -> int: # returns bytes sent by net
    bytes_sent = net_io_counters().bytes_sent
    return bytes_sent

def net_bytes_recv() -> int: # returns bytes recieved by net
    bytes_recv = net_io_counters().bytes_recv
    return bytes_recv

def process_count() -> int: # returns number of running PIDs
    number_of_processes = len(pids())
    return number_of_processes

def TCP_connections() -> int: # returns number of TCP connections
    number_of_connections = len(net_connections("tcp"))
    return number_of_connections


#----------test----------
def test():
    print(get_timestamp())
    print(memory_percent())
    print(disk_read_bytes())
    print(disk_write_bytes())
    print(net_bytes_sent())
    print(net_bytes_recv())
    print(process_count())
    print(TCP_connections())
test()