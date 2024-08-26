from netmiko import ConnectHandler
from log import authLog

import traceback
import os

def passAudit(validIPs, username, netDevice):
    # This function is to take a show run

    for validDeviceIP in validIPs:
        try:
            currentNetDevice = {
                'device_type': 'cisco_xe',
                'ip': validDeviceIP,
                'username': username,
                'password': netDevice['password'],
                'secret': netDevice['secret'],
                'global_delay_factor': 2.0,
                'timeout': 120,
                'session_log': 'netmikoLog.txt',
                'verbose': True,
                'session_log_file_mode': 'append',
                'keepalive' : 30
            }

            print(f"Connecting to device {validDeviceIP}...")
            with ConnectHandler(**currentNetDevice) as sshAccess:
                try:
                    sshAccess.enable()

                except Exception as error:
                    print(f"An error occurred: {error}\n")
                    authLog.error(f"User {username} with password {currentNetDevice['password']} connected to {validDeviceIP} got an error: Authentcation failed.")
                    with open(f"failedDevices.txt","a") as failedDevices:
                        failedDevices.write(f"User {username} with password {currentNetDevice['password']} connected to {validDeviceIP} got an error: Authentcation failed.\n")

        except Exception as error:
            print(f"ERROR: An error occurred: {error}\n", traceback.format_exc())
            authLog.error(f"User {username} connected to {validDeviceIP} got an error: {error}")
            authLog.error(traceback.format_exc(),"\n")
            with open(f"failedDevices.txt","a") as failedDevices:
                failedDevices.write(f"User {username} connected to {validDeviceIP} got an error.\n")

        print(f"Outputs and files successfully created for device {validDeviceIP}.\n")
        print("For any erros or logs please check Logs -> authLog.txt\n")
        print(f"Program finished, all the configuration has been applied.")
