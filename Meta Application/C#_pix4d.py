import threading
import os
import time
import sys
from pywinauto.application import Application
from pywinauto import Desktop
path = 'C:/Users/user/Desktop/New folder/Test Pix4D'
project_path = 'C:/Users/user/Desktop/New folder/Test Pix4D/Taken_from_outside'
log_file = os.path.join(project_path, 'Taken_from_outside.log')
################################
def close_application(application_name):
    ...
#############################    
def check_log_status(log_file, keyword):
    ...
##############################
def count_jpg_files(directory_path):
    ...
##############################
def run_background_code():
    count = count_jpg_files(path)
    if count>=5:        
        app = Application(backend='uia').start(r'C:\Program Files\Pix4Dmapper\pix4dmapper.exe')
        time.sleep(3)  
        main_window = app.window(title='Pix4Denterprise')
        project = main_window.child_window(title="Project", control_type="MenuItem").wrapper_object()
        project.click_input()
        time.sleep(1) 
        main_window.type_keys('{TAB}')
        main_window.type_keys('{ENTER}')
        main_window.type_keys('1')
        main_window.type_keys('{TAB}{TAB}{TAB}', with_spaces=True)
        main_window.type_keys('{ENTER}')
        main_window.type_keys('{TAB}')
        main_window.type_keys('{ENTER}') 
        time.sleep(0.3) 
        app2 = Application(backend='win32').connect(title='Select Images', class_name='#32770')
        select_images_window = app2.window(title='Select Images', class_name='#32770')
        select_images_window.type_keys('{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}', with_spaces=True)
        select_images_window.type_keys('^a')  
        select_images_window.type_keys('{ENTER}')
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
        desktop = Desktop(backend="uia") 
        win = desktop.window(title_re='.*Pix4Denterprise.*')
        win.child_window(title='Start', control_type='Button').click_input()
    else:
        app = Application(backend='uia').start(r'C:\Program Files\Pix4Dmapper\pix4dmapper.exe')
        time.sleep(3)  
        main_window = app.window(title='Pix4Denterprise')
        project = main_window.child_window(title="Project", control_type="MenuItem").wrapper_object()
        project.click_input()
        time.sleep(1) 
        main_window.type_keys('{TAB}')
        main_window.type_keys('{ENTER}')
        main_window.type_keys('1')
        main_window.type_keys('{TAB}{TAB}{TAB}', with_spaces=True)
        main_window.type_keys('{ENTER}')
        main_window.type_keys('{TAB}')
        main_window.type_keys('{ENTER}') 
        time.sleep(0.3) 
        app2 = Application(backend='win32').connect(title='Select Images', class_name='#32770')
        select_images_window = app2.window(title='Select Images', class_name='#32770')
        select_images_window.type_keys('{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}', with_spaces=True)
        select_images_window.type_keys('^a')  
        select_images_window.type_keys('{ENTER}')  
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
        desktop = Desktop(backend="uia") 
        win = desktop.window(title_re='.*Pix4Denterprise.*')
        win.child_window(title='Start', control_type='Button').click_input()
def monitor_log_file():
    while True:
        if check_log_status(log_file, 'Step3Done'):
            close_application("Pix4Dmapper.exe")
            sys.exit(0)
        time.sleep(5)  
def main():
    t1 = threading.Thread(target=run_background_code)
    t2 = threading.Thread(target=monitor_log_file)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
if __name__ == '__main__':
    main()