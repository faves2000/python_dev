import wmi
import datetime as dt
 
RESULT_FILE = "inventory"
subnet = '172.19.226.'
OS_LIST = {
    'winsrv 2012 R2': 0,
    'winsrv 2012': 0,
    'winsrv 2016 STD': 0,
    'winsrv 2016 DTC': 0,
    'Windows 10': 0,
    'OTHER': 0,
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
    for ip in range(28,30):
        ip_address = subnet + str(ip)
        #print(ip_address)
        conn = connect_to_server(ip_address)
        if conn:
            os_type = determine_os_type(conn)
            proc = determine_processor(conn)
            if '2012' in os_type[1] and 'R2' in os_type[1]:
                    OS_LIST['winsrv 2012 R2'] += 1
            if '2012' in os_type[1]:
                    OS_LIST['winsrv 2012'] += 1
            elif '2016' in os_type[1]:
                if proc[1] > 8:
                    OS_LIST['ADD_LIC'] += 1
                if 'Standard' in os_type[1]:
                    OS_LIST['winsrv 2016 STD'] += 1
                elif 'Datacenter' in os_type[1]:
                    OS_LIST['winsrv 2016 DTC'] += 1
            elif 'Windows 10' in os_type[1]:
                OS_LIST['Windows 10'] += 1
            else:
                OS_LIST['OTHER'] += 1
            print(f'IP: {ip_address} NAME: {os_type[0]} OS: {os_type[1]} proc type: {proc[0]} CORES: {proc[1]}')
    print(f'Total: 2016 STD: {OS_LIST["winsrv 2016 STD"]}, 2016 DATACENTER: {OS_LIST["winsrv 2016 DTC"]}, ADD LIC: {OS_LIST["ADD_LIC"]}')
    print(f'Total: 2012 R2: {OS_LIST["winsrv 2012 R2"]}, 2012: {OS_LIST["winsrv 2012"]}')
    print(f'Total: Win 10: {OS_LIST["Windows 10"]}')
if __name__ == "__main__":
    main()