ssh_ip = '192.168.33.142'
ssh_username = 'user'
ssh_password = '123'
report_path = 'C:/Users/user/Desktop/Shared/report.docx'
address_path = "C:/Users/user/Desktop/FLS/Address/Address.txt"
shared_folder = 'C:/Users/user/Desktop/Shared'
import os.path
import shutil

def create_next_folder():
    # set the directory path
    directory_path = shared_folder
    # check if the directory exists, create it if not
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    # get a list of existing directories in the directory_path
    existing_folders = [int(folder) for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]
    # determine the next folder name
    if not existing_folders:
        next_folder_name = 1
    else:
        next_folder_name = max(existing_folders) + 1
    # create the new folder
    new_folder_path = os.path.join(directory_path, str(next_folder_name))
    os.makedirs(new_folder_path)
    # return the name of the new folder
    return str(next_folder_name)

def move_files(folder_name):
    # set the directory path
    directory_path = shared_folder
    # create the folder if it doesn't exist
    folder_path = os.path.join(directory_path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # get a list of all files in the directory
    files = os.listdir(directory_path)
    # loop through the files and move them to the folder
    for file in files:
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            shutil.move(file_path, folder_path)
            
def copy_folder(source_path, destination_path):
    destination_path = os.path.join(destination_path, os.path.basename(source_path))
    shutil.copytree(source_path, destination_path)


def destination_image_address(shared_folder):
    address_file = os.path.join(shared_folder, "Address.txt")
    with open(address_file, "r") as f:
        first_line = f.readline().strip()
    return first_line
def report_open_delete_address(destination_folder, num):
    destination_folder = os.path.join(destination_folder, str(num))
    report_path = os.path.join(destination_folder, "report.docx")
    text_path = os.path.join(destination_folder, "Address.txt")
    os.startfile(report_path)
    os.remove(text_path)

