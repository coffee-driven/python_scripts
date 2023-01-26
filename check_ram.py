import psutil
import sys
import argparse


def ram_stats():
    "Give me memory stats (MODEL)"
    
    mem = psutil.virtual_memory()
    total_mem = mem.total
    avail_mem = mem.available
    active_mem = mem.active
    buff_mem = mem.buffers
    shared_mem = mem.shared
    
    return total_mem, avail_mem, active_mem, buff_mem, shared_mem
        
class Converter: 
    def convert_value():
        "Convert given values to bytes"
        warning_bytes = args.warning / 1024
        critical_bytes = args.critical / 1024
    
        return warning_bytes, critical_bytes
    
    def convert_value_perf():
        "Convert for performance data Mebi Bytes"
        total_mem, avail_mem, active_mem, buff_mem, shared_mem = ram_stats()
        
        hum_total = total_mem / 1024 / 1024
        hum_avail = avail_mem / 1024 / 1024
        hum_active = active_mem / 1024 / 1024
        hum_buff = buff_mem / 1024 / 1024
        hum_shared = shared_mem / 1024 / 1024 

        return hum_total, hum_avail, hum_active, hum_buff, hum_shared


def ram_threshold():
    "Check the ram usage against threshold (CONTROLER)"
    
    stats = ram_stats()
    
    w_thres, c_thres = Converter.convert_value()

    if w_thres > stats[1]:
        return 1, stats[1]
    elif c_thres > stats[1]:
        return 2, stats[1]
    else:
        return 0, stats[1]
    

def main():
        
    actual_state = ram_threshold()
    
    perf = Converter.convert_value_perf()

    if actual_state[0] == 0:
        OUTPUT = "OK"
    elif actual_state[0] == 1:
        OUTPUT = "WARNING"
    elif actual_state[0] == 2:
        OUTPUT = "CRITICAL"
    else:
        OUTPUT = "UNKNOWN"
        
    if args.performance:
        print( "RAM " + OUTPUT + " - Available memory (MiB) = " + str(perf[1]) + " | mem stat=" +
               "total_mem:" + str(perf[0]) + ";available_mem:" + str(perf[1]) + ";active_mem:" + str(perf[2]) +
               ";buffered_mem:" + str(perf[3]) + ";shared_mem:" + str(perf[4]) )
    else:
        print("RAM " + OUTPUT + " - Available memory (MiB) = " + str(perf[1]) )
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-w", "--warning", type=int, required=True, help="Warning threshold. Single value or range in MiB, e.g. '2000:5000'.")
    parser.add_argument("-c", "--critical", type=int, required=True, help="Critical threshold. Single vluae or range in MiB, e.g. '6000:7000'.")
    parser.add_argument("-t", "--timeout", help="Timeout in seconds (default 10s)", type=int, default=10)
    parser.add_argument("-p", "--performance", action='store_true', help="Return performance data")

    args = parser.parse_args()
    
    main()
