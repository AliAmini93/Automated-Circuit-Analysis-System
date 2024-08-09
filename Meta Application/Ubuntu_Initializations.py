import paramiko
import psutil
import socket
import os.path
ssh_ip2 = '192.168.33.66'
ssh_ip = '192.168.33.142'
ssh_username = 'user'
ssh_password = '123'
login_username = 'asef2'
login_password = 'Aa12345'
address_path = "C:/Users/user/Desktop/FLS/Address/Address.txt"

def check_valid_image():
    with open(address_path, 'r') as file:
        lines = file.readlines()
        if len(lines) > 0:  # Make sure 'lines' is not empty before accessing its elements
            first_line = lines[0].rstrip('\n')
            image_file_path = os.path.join(first_line, "FinalIMG.jpg")
            if os.path.isfile(image_file_path):
                return 1
            else:
                return 2
        else:
            return 3
def login():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ssh_ip, username=ssh_username, password=ssh_password, timeout=10.0)
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as error:
        print(f"Failed to connect to {ssh_ip} due to {error}")
        return False

    # Change directory to /home/user/Documents
    command = 'cd /home/user/Documents && ./login.sh'
    stdin, stdout, stderr = ssh_client.exec_command(command)

    # Provide login credentials
    stdin.write(login_username + '\n')
    stdin.write(login_password + '\n')
    stdin.flush()

    # Print output and error messages
    output = stdout.read().decode('utf-8').strip()  # Strip the output string
    print("Output:",output)
    print("Error:", stderr.read().decode('utf-8'))
    if output == 'success !':
        ssh_client.close()
        print("Internet logged in successfully.")
        return True
    else:
        ssh_client.close()
        print("Error in the Internet logging in!")
        return False


def ssh_connection_to_ocr_ubuntu():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   
    try:
        ssh_client.connect(hostname=ssh_ip, username=ssh_username, password=ssh_password, timeout=10.0)
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as error:
        print(f"Failed to connect to {ssh_ip} due to {error}")
        return False
    else:
        ssh_client.close()
        return True

def ssh_connection_to_od_ubuntu():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   
    try:
        ssh_client.connect(hostname=ssh_ip2, username=ssh_username, password=ssh_password, timeout=10.0)
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as error:
        print(f"Failed to connect to {ssh_ip} due to {error}")
        return False
    else:
        ssh_client.close()
        return True
def mount_shared():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ssh_ip, username=ssh_username, password=ssh_password, timeout=10.0)
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as error:
        print(f"Failed to connect to {ssh_ip} due to {error}")
        return False
    command = 'echo {} | sudo -S mount -t cifs //192.168.33.50/Shared /home/user/Documents/PCB-Report/Results -o user=user,password=123,dir_mode=0777,file_mode=0777,uid=user,gid=users'.format(ssh_password)
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    ssh_client.close()
    error = error.strip()
    print("Output:", stdout)
    print("Error:", error)
    # Check if the output is empty and the error value
    if not output and error =='[sudo] password for user:' or not output and 'Device or resource busy' in error:
        return True
    else:
        return False
    
def mount_shared_od():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ssh_ip2, username=ssh_username, password=ssh_password, timeout=10.0)
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as error:
        print(f"Failed to connect to {ssh_ip} due to {error}")
        return False
    command = 'echo {} | sudo -S mount -t cifs //192.168.33.50/Shared /home/user/Downloads/images -o user=user,password=123,dir_mode=0777,file_mode=0777,uid=user,gid=users'.format(ssh_password)
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    ssh_client.close()
    error = error.strip()
    print("Output:", stdout)
    print("Error:", error)
    # Check if the output is empty and the error value
    if not output and error =='[sudo] password for user:' or not output and 'Device or resource busy' in error:
        return True
    else:
        return False
    
def mount_ic_images_OCR():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ssh_ip, username=ssh_username, password=ssh_password, timeout=10.0)
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as error:
        print(f"Failed to connect to {ssh_ip} due to {error}")
        return False
    command = 'echo {} | sudo -S mount -t cifs //192.168.33.50/IC-Images /home/user/Documents/PCB-Report/IC-Images -o user=user,password=123,dir_mode=0777,file_mode=0777,uid=user,gid=users'.format(ssh_password)
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    ssh_client.close()
    error = error.strip()
    print("Output:", stdout)
    print("Error:", error)
    # Check if the output is empty and the error value
    if not output and error =='[sudo] password for user:' or not output and 'Device or resource busy' in error:
        return True
    else:
        return False
    
def mount_ic_images_OD():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ssh_ip2, username=ssh_username, password=ssh_password, timeout=10.0)
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as error:
        print(f"Failed to connect to {ssh_ip} due to {error}")
        return False
    command = 'echo {} | sudo -S mount -t cifs //192.168.33.50/IC-Images /home/user/Desktop/IC-Images -o user=user,password=123,dir_mode=0777,file_mode=0777,uid=user,gid=users'.format(ssh_password)
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    ssh_client.close()
    error = error.strip()
    print("Output:", stdout)
    print("Error:", error)
    # Check if the output is empty and the error value
    if not output and error =='[sudo] password for user:' or not output and 'Device or resource busy' in error:
        return True
    else:
        return False
    
def mount_datasheet():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ssh_ip, username=ssh_username, password=ssh_password, timeout=10.0)
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as error:
        print(f"Failed to connect to {ssh_ip} due to {error}")
        return False
    command = 'echo {} | sudo -S mount -t cifs //192.168.33.50/Datasheets /home/user/Documents/PCB-Report/Datasheets -o user=user,password=123,dir_mode=0777,file_mode=0777,uid=user,gid=users'.format(ssh_password)
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    ssh_client.close()
    error = error.strip()
    print("Output:", stdout)
    print("Error:", error)
    # Check if the output is empty and the error value
    if not output and error =='[sudo] password for user:' or not output and 'Device or resource busy' in error:
        return True
    else:
        return False
    
def unmount_OCR():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ssh_ip, username=ssh_username, password=ssh_password, timeout=10.0)
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as error:
        print(f"Failed to connect to {ssh_ip} due to {error}")
        return False
    # Change directory to /home/user/Documents
    command1 = 'echo {} | sudo -S umount /home/user/Documents/PCB-Report/Results'.format(ssh_password)
    stdin1, stdout1, stderr1 = ssh_client.exec_command(command1)
    print("Unmount Output1:", stdout1.read().decode('utf-8'))
    print("Unmount Error1:", stderr1.read().decode('utf-8'))
    
    command2 = 'echo {} | sudo -S umount /home/user/Documents/PCB-Report/Datasheets'.format(ssh_password)
    stdin2, stdout2, stderr2 = ssh_client.exec_command(command2)
    print("Unmount Output2:", stdout2.read().decode('utf-8'))
    print("Unmount Error2:", stderr2.read().decode('utf-8'))
    
    command3 = 'echo {} | sudo -S /home/user/Documents/PCB-Report/IC-Images'.format(ssh_password)
    stdin3, stdout3, stderr3 = ssh_client.exec_command(command3)
    print("Unmount Output3:", stdout2.read().decode('utf-8'))
    print("Unmount Error3:", stderr2.read().decode('utf-8'))
    ssh_client.close()


def unmount_OD():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ssh_ip2, username=ssh_username, password=ssh_password, timeout=10.0)
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as error:
        print(f"Failed to connect to {ssh_ip2} due to {error}")
        return False
    # Change directory to /home/user/Documents
    command1 = 'echo {} | sudo -S /home/user/Downloads/images'.format(ssh_password)
    stdin1, stdout1, stderr1 = ssh_client.exec_command(command1)
    print("Unmount Output1:", stdout1.read().decode('utf-8'))
    print("Unmount Error1:", stderr1.read().decode('utf-8'))
    
    command2 = 'echo {} | sudo -S /home/user/Desktop/IC-Images'.format(ssh_password)
    stdin2, stdout2, stderr2 = ssh_client.exec_command(command2)
    print("Unmount Output2:", stdout2.read().decode('utf-8'))
    print("Unmount Error2:", stderr2.read().decode('utf-8'))
    ssh_client.close()
    
def MongoDB():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ssh_ip, username=ssh_username, password=ssh_password, timeout=10.0)
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as error:
        print(f"Failed to connect to {ssh_ip} due to {error}")
        return False

    # Change directory to /home/user/Documents/PCB-Report and start mongod with sudo privileges
    command = 'cd /home/user/Documents/PCB-Report && echo ' + ssh_password + ' | sudo -S systemctl start mongod'
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    ssh_client.close()
    error = error.strip()
    print("Output:", stdout)
    print("Error:", error)
    # Check if the output is empty and the error value
    if not output and error =='[sudo] password for user:':
        return True
    else:
        return False
    
def close_application(application_name):
    for process in psutil.process_iter():
        try:
            if process.name().lower() == application_name.lower():
                process.terminate()
                print(f"{application_name} closed successfully.")
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print(f"{application_name} not found.")