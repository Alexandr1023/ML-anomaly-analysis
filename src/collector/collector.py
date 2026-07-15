from psutil import cpu_percent, virtual_memory, disk_io_counters, net_io_counters, pids, net_connections
from pandas import Timestamp


def get_timestamp() -> float: # returns current UNIX timestamp
    pd_time = Timestamp.now()
    unix_time = pd_time.timestamp()
    return unix_time

def cpu_usage() -> float: # returns cpu usage percent
    usage = cpu_percent(interval=0.1)
    return usage

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

def tcp_connections() -> int: # returns number of TCP connections
    number_of_connections = len(net_connections("tcp"))
    return number_of_connections

functions_list = [get_timestamp, cpu_usage, memory_percent, disk_read_bytes, 
                  disk_write_bytes, net_bytes_sent, net_bytes_recv, process_count, tcp_connections]

def collect_metrics() -> dict:
    metrics_data = {func.__name__: func() for func in functions_list}
    return metrics_data