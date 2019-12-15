
import socket               # Import socket module
# import mysql.connector as apnd
import csv
import subprocess
import os
import time

port=21
terminator = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(("192.168.1.102", port))
# s.bind(("192.168.43.71", port))
s.bind(("localhost", port))

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
print('Server Listening.......')

try:
    client_connectivity = 0
    while True:

        print('Waiting for Connection.....')

        filename = 'data_log.csv'
        c, addr = s.accept()     # Establish connection with client.

        client_connectivity=1

        print ("Connected to :",addr)
        c.send('Connection Established'.encode())


        data = c.recv(4096)

        while(data):

            if data.decode().find("END")>=0:
                print(data.decode().split("END")[0])
                f = open(filename, 'a')
                f.write(data.decode().split("END")[0])
                f.close()
                break
            else:
                f = open(filename, 'a')
                f.write(data.decode())
                f.close()
                print(data.decode())
                data = c.recv(4096)



        if data:
            c.send("Data Received".encode())

            # while(data):
            #
            #     csv_file_obj = open(filename, 'rb')
            #     csv_file = open('sql.csv', 'wb')
            #     wr = csv.writer(csv_file)
            #
            #     for row in csv.reader(csv_file_obj):
            #         if (len(row[0]) > 3):
            #             print(','.join(row))
            #             wr.writerow(row)
            #     csv_file.close()
            #     csv_file_obj.close()



            #     with open('sql.csv', 'r') as file:
            #         nSql = [list(map(str, rec)) for rec in csv.reader(file, delimiter=',')]
            #         servertime=str(time.strftime('%d-%m-%Y %H:%M:%S'))
            #
            #         for ins in nSql:
            #
            #             con = apnd.connect(user='bluetooth', password='admin', database='Bluetooth_test')
            #             cur = con.cursor()
            #             if (ins[0]=='raspi_A'):
            #                 insertstmt = (
            #                 "insert into raspi_A (address, device_class, rssi, device_time, server_time) values ('%s', '%s', '%s', '%s', '%s')" % (
            #                     ins[1], ins[2], ins[3], ins[4], servertime))
            #
            #
            #             if (ins[0]=='raspi_B'):
            #                 insertstmt = (
            #                 "insert into raspi_B (address, device_class, rssi, device_time, server_time) values ('%s', '%s', '%s', '%s', '%s')" % (
            #                     ins[1], ins[2], ins[3], ins[4], servertime))
            #
            #
            #             if (ins[0]=='raspi_C'):
            #                 insertstmt = (
            #                 "insert into raspi_C (address, device_class, rssi, device_time, server_time) values ('%s', '%s', '%s', '%s', '%s')" % (
            #                     ins[1], ins[2], ins[3], ins[4], servertime))
            #
            #
            #             if (ins[0] == 'raspi_D'):
            #                 insertstmt = (
            #                     "insert into raspi_D (address, device_class, rssi, device_time, server_time) values ('%s', '%s', '%s', '%s', '%s')" % (
            #                     ins[1], ins[2], ins[3], ins[4], servertime))
            #
            #             if (ins[0] == 'raspi_E'):
            #                 insertstmt = (
            #                     "insert into raspi_E(address, device_class, rssi, device_time, server_time) values ('%s', '%s', '%s', '%s', '%s')" % (
            #                     ins[1], ins[2], ins[3], ins[4], servertime))
            #
            #             if (ins[0] == 'raspi_F'):
            #                 insertstmt = (
            #                     "insert into raspi_F (address, device_class, rssi, device_time, server_time) values ('%s', '%s', '%s', '%s', '%s')" % (
            #                     ins[1], ins[2], ins[3], ins[4], servertime))
            #
            #             if (ins[0] == 'raspi_G'):
            #                 insertstmt = (
            #                     "insert into raspi_G (address, device_class, rssi, device_time, server_time) values ('%s', '%s', '%s', '%s', '%s')" % (
            #                     ins[1], ins[2], ins[3], ins[4], servertime))
            #
            #             if (ins[0] == 'raspi_H'):
            #                 insertstmt = (
            #                     "insert into raspi_H (address, device_class, rssi, device_time, server_time) values ('%s', '%s', '%s', '%s', '%s')" % (
            #                     ins[1], ins[2], ins[3], ins[4], servertime))
            #
            #             if (ins[0] == 'raspi_I'):
            #                 insertstmt = (
            #                     "insert into raspi_I (address, device_class, rssi, device_time) values ('%s', '%s', '%s', '%s', '%s')" % (
            #                         ins[1], ins[2], ins[3], ins[4]))
            #
            #             if (ins[0] == 'raspi_J'):
            #                 insertstmt = (
            #                     "insert into raspi_J (address, device_class, rssi, device_time, server_time) values ('%s', '%s', '%s', '%s', '%s')" % (
            #                     ins[1], ins[2], ins[3], ins[4], servertime))
            #
            #             if (ins[0] == 'raspi_K'):
            #                 insertstmt = (
            #                     "insert into raspi_K (address, device_class, rssi, device_time, server_time) values ('%s', '%s', '%s', '%s', '%s')" % (
            #                     ins[1], ins[2], ins[3], ins[4], servertime))
            #
            #             cur.execute(insertstmt)
            #             con.commit()
            #             con.close()
            #
            #     file.close()
            #     break
            # print('Successfully received data')
            #
            # os.remove(filename)
            # os.remove('sql.csv')

except Exception as e:
    print("hi")
    filename_log = 'Syslog.csv'
    field_log = ['Error', 'Date & Time']
    csv_syslog_obj = open(filename_log, 'a')
    log_writer = csv.DictWriter(csv_syslog_obj, fieldnames=field_log)
    log_writer.writerow(
        {'Error': str(e), 'Date & Time': str(time.strftime('%d-%m-%Y %H:%M:%S'))})
    csv_syslog_obj.close()
    print("Error : " + str(e))

