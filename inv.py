import wmi
import datetime as dt
 
RESULT_FILE = "inventory"
subnet = '172.19.224.'
OS_LIST = {
    '2012_R2': 0,
    '2012': 0,
    '2016_STD': 0,
    '2016_DTC': 0,
    '2016_OTHER': 0,
    'ADD_LIC': 0
}
 
def connect_to_server(ip_address):
    try:
        conn = wmi.WMI(computer=ip_address, user='trc1\otm_admin', password='234wer@R')
        return conn
    except Exception:
        print(f'Connect failed to {ip_address}')
 
def determine_os_type(connection):
    for os in connection.Win32_OperatingSystem():
        return os.CSName, os.Caption
def determine_processor(connection):
    for proc in connection.Win32_Processor():
        return proc.Name, proc.NumberOfCores
def get_time_date():
    now = dt.datetime.now()
    return now.strftime("%H:%M:%S %d %m %Y")
 
def main():
    result_file_name = RESULT_FILE + '.' + subnet + 'txt'
    with open(result_file_name, 'w') as result_file:
        date  = get_time_date()
        result_file.write(f'File created: {date} \n')
    for ip in range(11,20):
        ip_address = subnet + str(ip)
        #print(ip_address)
        conn = connect_to_server(ip_address)
        if conn:
            os_type = determine_os_type(conn)
            proc = determine_processor(conn)
            if '2012' in os_type[1]:
                if 'R2' in os_type[1]:
                    OS_LIST['2012_R2'] += 1
                else:
                    OS_LIST['2012'] += 1
            elif '2016' in os_type[1]:
                if proc[1] > 8:
                    OS_LIST['ADD_LIC'] += 1
                if 'Standard' in os_type[1]:
                    OS_LIST['2016_STD'] += 1
                elif 'Datacenter' in os_type[1]:
                    OS_LIST['2016_DTC'] += 1
                else:
                    OS_LIST['2016_OTHER'] += 1
            print(f'IP: {ip_address} NAME: {os_type[0]} OS: {os_type[1]} proc type: {proc[0]} CORES: {proc[1]}')
            with open(result_file_name, 'a') as result_file:
                result_file.write(f'IP: {ip_address} NAME: {os_type[0]} OS: {os_type[1]} proc type: {proc[0]} CORES: {proc[1]} \n')
    print(f'Total: 2016 STD: {OS_LIST["2016_STD"]}, 2016 DATACENTER: {OS_LIST["2016_DTC"]}, 2016 OTHER: {OS_LIST["2016_OTHER"]}')
    print(f'Additional 2016 licenses: {OS_LIST["ADD_LIC"]} pcs.')
    print(f'2012 R2: {OS_LIST["2012_R2"]}, 2012 OTHER: {OS_LIST["2012"]}')
    with open(result_file_name, 'a') as result_file:
        result_file.write(f'Total: 2016 STD: {OS_LIST["2016_STD"]}, 2016 DATACENTER: {OS_LIST["2016_DTC"]}, 2016 OTHER: {OS_LIST["2016_OTHER"]} \n')
        result_file.write(f'Additional 2016 licenses: {OS_LIST["ADD_LIC"]} pcs. \n')
        result_file.write(f'2012 R2: {OS_LIST["2012_R2"]}, 2012 OTHER: {OS_LIST["2012"]}')            
 
if __name__ == "__main__":
    main()
