import argparse
import threading
import os
import time
import sys
from pywinauto.application import Application
from pywinauto import Desktop
import psutil
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import shutil
###############Without Persian#########################
'''
repository = 'C:/Users/user/Desktop/Pix4D/Image Repository'
path = 'C:/Users/user/Desktop/Pix4D/Pix4D Projects'
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="The filename you want to use.")
args = parser.parse_args()
project_path = f'C:/Users/user/Desktop/Pix4D/Pix4D Projects/{args.filename}'
log_file = os.path.join(project_path, f'{args.filename}.log')
'''
###############With Persian#########################
import pyautogui

repository = 'C:/Users/user/Desktop/Pix4D/Image Repository'
path = 'C:/Users/user/Desktop/Pix4D/Pix4D Projects'
def extract_filename_and_flag(filename):
    main_filename, flag = filename.rsplit('+', 1)
    return main_filename, flag

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="The filename you want to use.")
args = parser.parse_args()
args.filename, flag =  extract_filename_and_flag(args.filename)
if flag =='T':
    print("changing the keyboard name...")
    pyautogui.hotkey('alt', 'shift')
project_path = f'C:/Users/user/Desktop/Pix4D/Pix4D Projects/{args.filename}'
log_file = os.path.join(project_path, f'{args.filename}.log')
################################

def delete_all_folders(path):
    try:
        # Iterate over all items in the directory
        for item in os.listdir(path):
            item_path = os.path.join(path, item)

            # Check if it's a directory
            if os.path.isdir(item_path):
                # Delete the directory and its contents
                shutil.rmtree(item_path)
                print(f'Deleted folder: {item_path}')

        print('All folders deleted successfully.')

    except Exception as e:
        print(f'Error: {e}')
################################
def post_processing_image_generation():
    import os
    import shutil
    # Step 1: Create a new folder named '????' in Repository
    repository = 'C:/Users/user/Desktop/Pix4D/Image Repository'
    folder_path = os.path.join(repository, f'{args.filename}')
    os.makedirs(folder_path, exist_ok=True)

    # Step 2: Move the folder named '????' to the folder created in Step 1
    project_path = f'C:/Users/user/Desktop/Pix4D/Pix4D Projects/{args.filename}'
    path = 'C:/Users/user/Desktop/Pix4D/Pix4D Projects'
    shutil.move(project_path, folder_path)

    # Move the '.jpg' files from step 2 to the folder created in Step 1
    jpg_files = [file for file in os.listdir(path) if file.endswith('.JPG')]
    for jpg_file in jpg_files:
        shutil.move(os.path.join(path, jpg_file), folder_path)

    # Step 3: Create a new folder named 'Image Patches' inside the folder created in Step 1
    image_patches_path = os.path.join(folder_path, 'Image Patches')
    os.makedirs(image_patches_path, exist_ok=True)

    # Move the '.jpg' files from step 2 to the 'Image Patches' folder
    for jpg_file in jpg_files:
        shutil.move(os.path.join(folder_path, jpg_file), image_patches_path)

    image_path = f'C:/Users/user/Desktop/Pix4D/Image Repository/{args.filename}/{args.filename}/3_dsm_ortho/2_mosaic'
    tif_files = [file for file in os.listdir(image_path) if file.endswith('.tif')]
    if len(tif_files) > 0:
        tif_file = tif_files[0]
        tif_file_path = os.path.join(image_path, tif_file)
        final_image_path = os.path.join(folder_path, 'FinalIMG.jpg')
        shutil.move(tif_file_path, final_image_path)

    #make a new folder named by the current date and time and move the FinalIMG.jpg to it
    now = datetime.now()
    date_ = now.strftime("%Y%m%d_%H%M%S")
    date_folder_name = os.path.join(folder_path, date_)
    os.makedirs(date_folder_name, exist_ok=True)
    shutil.move(final_image_path, date_folder_name)
    # Step 5: Go to 'C:/Users/user/Desktop/FLS/Address' and update 'Address.txt' with the image address
    address_folder = 'C:/Users/user/Desktop/FLS/Address'
    address_file = os.path.join(address_folder, 'Address.txt')
    if os.path.exists(address_file):
        with open(address_file, 'a') as f:
            f.write(f"{date_folder_name}\n")
    else:
        with open(address_file, 'w') as f:
            f.write(f"{date_folder_name}\n")
################################
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

#############################    
def check_log_status(log_file, keyword):
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            for line in file:
                if keyword in line:
                    return True
    return False
##############################
def count_jpg_files(directory_path):
    count = 0
    for file_name in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, file_name)) and file_name.endswith('.JPG'):
            count += 1
    return count
##############################
def run_background_code():
    count = count_jpg_files(path)
    if count>=5:
        # Start the application
        app = Application(backend='uia').start(r'C:\Program Files\Pix4Dmapper\pix4dmapper.exe')
        time.sleep(5)  # wait for 5 seconds for the application to fully start
        #main_window = app.window(title='Pix4Denterprise')
        
        while True:
            try:
                # Define the main window
                main_window = app.window(title='Pix4Denterprise')
                break  # if the window is found, break the loop
            except Exception:
                print("Window not found. Restarting the application...")
                # Close the application
                close_application('pix4dmapper.exe')
                # Restart the application
                app = Application(backend='uia').start(r'C:\Program Files\Pix4Dmapper\pix4dmapper.exe')
                # Wait for the application to fully start
                time.sleep(5)
        
        ### using the menu item
        # Navigate through the main window
        project = main_window.child_window(title="Project", control_type="MenuItem").wrapper_object()
        project.click_input()
        time.sleep(1) 
        main_window.type_keys('{TAB}')
        main_window.type_keys('{ENTER}')
        '''
        #using just ctrl+N for new project.
        main_window.type_keys('^n')
        '''
        main_window.type_keys(f'{args.filename}')
        main_window.type_keys('{TAB}{TAB}{TAB}', with_spaces=True)
        main_window.type_keys('{ENTER}')

        main_window.type_keys('{TAB}')
        main_window.type_keys('{ENTER}') # At this point, 'Select Images' window should be opened
        time.sleep(0.3) 
        # Define the 'Select Images' window as a separate object
        app2 = Application(backend='win32').connect(title='Select Images', class_name='#32770')
        select_images_window = app2.window(title='Select Images', class_name='#32770')
        # Navigate through the 'Select Images' window
        select_images_window.type_keys('{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}', with_spaces=True)
        select_images_window.type_keys('^a')  # This should select all the images
        select_images_window.type_keys('{ENTER}')  # This should click the 'Open' button
        time.sleep(0.3) 
        main_window.type_keys('{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}', with_spaces=True)
        main_window.type_keys('{ENTER}')
        time.sleep(0.3) 
        
        main_window.type_keys('{ENTER}')
        time.sleep(0.3) 
        
        main_window.type_keys('{TAB}{TAB}{TAB}{TAB}', with_spaces=True)
        main_window.type_keys('{ENTER}')
        time.sleep(0.3) 
        
        main_window.type_keys('{ENTER}')
        time.sleep(0.3) 
        
        main_window.type_keys('{ENTER}')
        time.sleep(8) 
        
        main_window.type_keys('{DOWN}')
        main_window.type_keys('{UP}')
        main_window.type_keys('{ENTER}')
        time.sleep(0.3)
        # Using .click_input()
        # Get the desktop object
        desktop = Desktop(backend="uia") 
        
        # Get the window
        win = desktop.window(title_re='.*Pix4Denterprise.*')
        
        # Interact with the button
        win.child_window(title='Start', control_type='Button').click_input()
    else:
        # Start the application
        app = Application(backend='uia').start(r'C:\Program Files\Pix4Dmapper\pix4dmapper.exe')
        time.sleep(5)  # wait for 5 seconds for the application to fully start
        
        # Define the main window
        #main_window = app.window(title='Pix4Denterprise')  
        while True:
            try:
                # Define the main window
                main_window = app.window(title='Pix4Denterprise')
                break  # if the window is found, break the loop
            except Exception:
                print("Window not found. Restarting the application...")
                # Close the application
                close_application('pix4dmapper.exe')
                # Restart the application
                app = Application(backend='uia').start(r'C:\Program Files\Pix4Dmapper\pix4dmapper.exe')
                # Wait for the application to fully start
                time.sleep(5)
        ### using the menu item
        # Navigate through the main window
        project = main_window.child_window(title="Project", control_type="MenuItem").wrapper_object()
        project.click_input()
        time.sleep(1) 
        main_window.type_keys('{TAB}')
        main_window.type_keys('{ENTER}')
        '''
        #using just ctrl+N for new project.
        main_window.type_keys('^n')
        '''
        main_window.type_keys(f'{args.filename}')
        main_window.type_keys('{TAB}{TAB}{TAB}', with_spaces=True)
        main_window.type_keys('{ENTER}')

        main_window.type_keys('{TAB}')
        main_window.type_keys('{ENTER}') # At this point, 'Select Images' window should be opened
        time.sleep(0.3) 
        # Define the 'Select Images' window as a separate object
        app2 = Application(backend='win32').connect(title='Select Images', class_name='#32770')
        select_images_window = app2.window(title='Select Images', class_name='#32770')
        # Navigate through the 'Select Images' window
        select_images_window.type_keys('{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}', with_spaces=True)
        select_images_window.type_keys('^a')  # This should select all the images
        select_images_window.type_keys('{ENTER}')  # This should click the 'Open' button
        time.sleep(0.3) 
        main_window.type_keys('{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}', with_spaces=True)
        main_window.type_keys('{ENTER}')
        time.sleep(0.3) 
        main_window.type_keys('{TAB}{TAB}{TAB}{TAB}', with_spaces=True)
        main_window.type_keys('{ENTER}')
        time.sleep(0.3) 
        
        main_window.type_keys('{ENTER}')
        time.sleep(8) 
        
        main_window.type_keys('{DOWN}')
        main_window.type_keys('{UP}')
        main_window.type_keys('{ENTER}')
        time.sleep(0.3)
        # Using .click_input()
        # Get the desktop object
        desktop = Desktop(backend="uia") 
        
        # Get the window
        win = desktop.window(title_re='.*Pix4Denterprise.*')
        
        # Interact with the button
        win.child_window(title='Start', control_type='Button').click_input()
def monitor_log_file():
    while True:
        if check_log_status(log_file, 'No calibrated cameras'):
            close_application("Pix4Dmapper.exe")
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", 
                                 "The image patches are not appropriate, please change the circuit position and try again.")
            sys.exit(0)
        if check_log_status(log_file, 'Step3Done'):
            close_application("Pix4Dmapper.exe")
            post_processing_image_generation()
            sys.exit(0)
        time.sleep(5)  # wait for 5 seconds before checking again
def main():
    close_application("Pix4Dmapper.exe")
    delete_all_folders(path)
    print("Is it deleted?")
    print(f'file name:{args.filename}')
    t1 = threading.Thread(target=run_background_code)
    t2 = threading.Thread(target=monitor_log_file)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    main()