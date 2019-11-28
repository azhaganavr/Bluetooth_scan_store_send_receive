import socket
import subprocess
import os
import time
import csv
import itertools
import datetime

# Importing all necessary libraries

time.sleep(10)  # To give a waiting period for the 3G modem to connect

scan_var = 0
j = 0
row_count = 0
RSSI = 00  # Not used just for testing purpose
port = 21
bt_var = 0
scan_data_len = 0
scan_data_array = []
# Necessary variables are initialized

device_name = 'raspi_A'  # Each device is given a unique name to identify itself

hci_dump = subprocess.Popen(["hcidump -a hci"], bufsize=0, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)  # Scanning data is taken from the hcidump

while True:

    filename = 'bt_send_' + str(time.strftime('%d-%m-%Y')) + '.csv'  # This command is used instead.

    print("Scanning for Bluetooth data.....")

    loop_time = time.time() + 60  # Scanning variable is intialized to current time value plus 300 Seconds

    try:

        while time.time() < loop_time:  # A loop is started for scanning the data for the given duration

            flag = 0
            for i in range(0, 30, 1):
                inchar = hci_dump.stdout.readline()  # We store  the dump value in inchar
                char = str(inchar)  # Convert it to string
                a, b, c = char.partition(
                    'bdaddr')  # We store the 'baddr', the string before and  after 'badddr' string in b,a,c

                if (
                c):  # c is the string that contains the MAC address , Mode variable followed by  mode value, class variable followed by classs value, clock offset variable followed by clock offset  and rssi variable followed by rssi value in an array

                    classification = []
                    device_class = []
                    device_class += c.split()[6]  # the 6th element of array C consists of bluetooth class value

                    case_array = {'0': 'Uncategorized', '1': 'Computer', '2': 'Phone', '3': 'LAN',
                                  '4': 'Audio/Video', '5': 'Peripheral', '6': 'Imaging', '7': 'Wearable', '8': 'Toys'}
                    device_type = case_array.get(device_class[5],
                                                 'default')  # the 5th charecter decides the type of device

                    concat = str(device_class[6]) + str(
                        device_class[7])  # the 6th and 7th charecter gives a more detailed classification.

                    if device_class[5] == '0':
                        misc_array = {'00': 'Bluetooth Device'}
                        classification = misc_array.get(concat, 'default')

                    elif device_class[5] == '1':
                        computer_array = {'00': 'unasssigned', '04': 'Desktop Workstation', '08': 'Server class',
                                          '0c': 'Laptop', '10': 'Handheld PCA', '14': 'Palm Sized PDA',
                                          '18': 'Wearable'}
                        classification = computer_array.get(concat, 'default')

                    elif device_class[5] == '2':
                        phone_array = {'00': 'unasssigned', '04': 'Cellular', '08': 'Cordless', '0c': 'Smart',
                                       '10': 'Wired Modem or Access Gateway', '14': 'Common ISDN Access'}
                        classification = phone_array.get(concat, 'default')

                    elif device_class[5] == '4':
                        audio_video_array = {'00': 'unasssigned', '04': 'Wearable Headset', '08': 'Hands-Free',
                                             '10': 'Microphone', '14': 'Loudspeaker', '18': 'Headphones',
                                             '1c': 'Portable ', '20': 'Car Audio', '24': 'Set-Top Box', '28': 'HiFi',
                                             '2c': 'Laptop', '30': 'Video Tape Recorder', '34': 'Video Camera',
                                             '38': 'Camcorder', '3c': 'Video Display and Loudspeaker',
                                             '40': 'Video Conferencing', '44': 'Reserved', '48': 'Game/Toy'}
                        classification = audio_video_array.get(concat, 'default')

                    elif device_class[5] == '5':
                        peripheral_array = {'00': 'unasssigned', '04': 'Joystick', '08': 'Gamepad',
                                            '0c': 'Remote control', '10': 'Sensing device', '14': 'Digitiser Tablet',
                                            '18': 'Card Reader'}
                        classification = peripheral_array.get(concat, 'default')

                    elif device_class[5] == '6':
                        imaging_array = {'00': 'unasssigned', '10': 'Display', '20': 'Camera', '40': 'Scanner',
                                         '80': 'Printer'}
                        classification = imaging_array.get(concat, 'default')

                    elif device_class[5] == '7':
                        wearable_array = {'00': 'unasssigned', '04': 'Wrist Watch', '08': 'Pager', '0c': 'Jacket',
                                          '10': 'Helmet', '14': 'Glasses'}
                        classification = wearable_array.get(concat, 'default')

                    elif device_class[5] == '8':
                        toys_array = {'00': 'unasssigned', '04': 'Robot', '08': 'Vehicle', '0c': 'Character',
                                      '10': 'Controller', '14': 'Game'}
                        classification = toys_array.get(concat, 'default')

                    device = (str(classification) + ' ' + str(
                        device_type))  # concatenate the final accurate classification
                    rssi = []
                    rssi += c.split()[8]  # C array has rssi value in the 8th cell
                    concat_rssi = (str(rssi[0]) + str(rssi[1]) + str(
                        rssi[2]))  # the three charecters constitute the rssi value
                    print(device_name + ',' + str(time.strftime('%d-%m-%Y %H:%M:%S')) + ',' + (
                    c.split()[0]) + ',' + device + ',' + concat_rssi)

                    data_string = device_name + ',' + str(time.strftime('%d-%m-%Y %H:%M:%S')) + ',' + (
                    c.split()[0]) + ',' + device + ',' + concat_rssi

                    scan_data_array.append(data_string)

                    #                     print(scan_data_array[scan_var])
                    scan_var = scan_var + 1  # Just a flag variable used to know whether ther was any scanned value

                    classification = ""

        #         print(len(scan_data_array)) #Actual length of the array
        data_array = list(set(scan_data_array))  # we remove the duplicate data from the array
        scan_data_len = len(data_array)
        #         print(scan_data_len) # reduced Lenth of the array

        if (scan_data_len):
            csv_file_obj = open(filename, 'a')  # Create an object for  open csv file
            print("opening csv file to write data")
            for i in range(scan_data_len):
                bt_var = 1

                csv_file_obj.write(data_array[i] + "\n")  # writing the values to the CSV file one after the other,
                j = 1  # flag to know if any data is written to the file
            csv_file_obj.flush()
            csv_file_obj.close()  # Closing the file

        if j:
            print('Data Written to the file')
            j = 0

        scan_data_array = []
        scan_var = 0

    except Exception as e:  # Incase of any error , it is stored in the syslog file
        filename_log = 'Syslog.csv'
        field_log = ['Error', 'Date & Time']
        csv_syslog_obj = open(filename_log, 'a')
        print("opening csv file to write exception 1")
        log_writer = csv.DictWriter(csv_syslog_obj, fieldnames=field_log)
        log_writer.writerow(
            {'Error': str(e), 'Date & Time': str(time.strftime('%d-%m-%Y %H:%M:%S'))})
        csv_syslog_obj.close()
        print("Error: " + str(e))

    try:
        server_connectivity = 0  # A flag variable used to know whether the device has been connected to the server or not
        if (bt_var == 1):  # As mentioned above the following block is executed only if any values were scanned and until the values are sent

            try:  # Checking for internet connectivity
                host = socket.gethostbyname("www.google.com")
                s = socket.create_connection((host, 80), 2)
                s.close()
                print('internet on.')
                connectivity = 1

            except:
                print("internet off.")
                connectivity = 0
                os.system("sudo /etc/init.d/reconnectnet start")

            if (connectivity == 1):  # only if internet connectivity exists the following connection establishment and data transmission block is executed
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a socket object
                print('Trying to connect.....')
                s.connect(("192.168.0.9", port))  # For RapsberryPi to connect to server
                # s.connect(("10.21.56.201", port))  # For Institute PC to connect to server
                server_connectivity = 1  # flag used to define if connectivity has been established
                print(s.recv(1024).decode())  # Connection establishment acknowledgement is printed from the server

                from itertools import islice  # importing islice from itertools

                with open(filename, "r") as f:
                    send_data = csv.reader(f, delimiter=",")
                    list_data = list(send_data)
                    row_count = len(list_data)
                    print(row_count)

                with open(filename, "r") as myfile:
                    redc_data = list(islice(myfile, row_count))  # it takes the no. of rows and stores in the array
                    # myfile.close()

                if (row_count % 2 == 0):  # If the no. of data is even

                    for even in range(0, row_count - 1, 2):
                        data = redc_data[0 + even] + redc_data[1 + even]
                        s.send(data.encode())

                else:  # if no. of data is odd

                    s.send(redc_data[0].encode())  # we first send one value seperately

                    for odd in range(1, row_count - 1, 2):  # then we send two values together
                        data = redc_data[0 + odd] + redc_data[1 + odd]
                        s.send(data.encode())

                endofdata = "END\n"  # End of data transmission variable
                s.send(endofdata.encode())  # eod variable is transmitted

                time.sleep(1)
                ack = s.recv(2048).decode()  # Once all data is sent the an acknowledgement is received

                if ack:  # Only if acknowledgement is received  we remove the csv file and change the bt_var flag variable
                    # print(''.join(redc_data))
                    print('Data Sent Succssfully')
                    os.remove(filename)
                    bt_var = 0
                data = ""
                s.close()  # Close the socket

    except Exception as g:  # any error in the block above is stored in syslog
        filename_log = 'Syslog.csv'
        field_log = ['Error', 'Date & Time']
        csv_syslog_obj = open(filename_log, 'a')
        print("opening csv file to write exception 2")
        log_writer = csv.DictWriter(csv_syslog_obj, fieldnames=field_log)
        log_writer.writerow(
            {'Error': str(g), 'Date & Time': str(time.strftime('%d-%m-%Y %H:%M:%S'))})
        csv_syslog_obj.close()
        print("Error: " + str(g))

        if (server_connectivity == 1):  # only if connectivity was established we close the socket
            s.close()