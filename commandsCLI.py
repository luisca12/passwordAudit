from netmiko import ConnectHandler
from log import authLog

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
                authLog.info(f"Successfully connected to {validDeviceIP}")
                    
        except Exception as error:
            print(f"An error occurred: {error}\n")
            authLog.error(f"User {username} with password {currentNetDevice['password']} connected to {validDeviceIP} got an error: Authentcation failed.")
            with open(f"failedDevices.txt","a") as failedDevices:
                failedDevices.write(f"User {username} with password {currentNetDevice['password']} connected to {validDeviceIP} got an error: Authentcation failed.\n")

        print(f"Outputs and files successfully created for device {validDeviceIP}.\n")
        print("For any erros or logs please check Logs -> authLog.txt\n")
        print(f"Program finished, all the configuration has been applied.")
