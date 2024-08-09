import subprocess
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRunnable, QThreadPool, pyqtSignal, QObject
import os
import os.path
import time
from pywinauto.application import Application
import shutil
import glob
from FLS_Calculator import Ui_Calculator
from Watcher import Watcher_Image, Watcher_OD, Watcher_Buffer, Watcher_Image_Valid, Watcher_OCR_Data
from Ubuntu_Initializations import close_application
from Shared_Folder_Ordering import move_files, create_next_folder,copy_folder,destination_image_address,report_open_delete_address
from Serial import calibrate, check_com_port
from Other_Threads import ShowImageThread#, initFLSDeviceThread
from threading import Lock
import threading
from PyQt5.QtWidgets import QScrollArea

ssh_ip = '192.168.33.142'
ssh_ip2 = '192.168.33.66'
ssh_username = 'user'
ssh_password = '123'
report_path = 'C:/Users/user/Desktop/Shared/report.docx'
address_path = "C:/Users/user/Desktop/FLS/Address/Address.txt"
moved_address_path = 'C:/Users/user/Desktop/Shared/Address.txt'
shared_folder = 'C:/Users/user/Desktop/Shared'
shared_image = 'C:/Users/user/Desktop/Shared/FinalIMG.jpg'
temp_od_path = 'C:/Users/user/Desktop/IC-Images/IC-Images/FinalIMG.jpg'
ic_images = 'C:/Users/user/Desktop/IC-Images'
Path_Data = r'C:\Users\user\Desktop\Data\data.pkl'
Data = 'C:/Users/user/Desktop/Data'
crop_folder = 'C:/Users/user/Desktop/IC-Images/IC-Images\\crops'

####################################################################################
def delete_images_and_text_files(folder_path):
    # Create patterns for .jpg and .txt files
    jpg_pattern = os.path.join(folder_path, '*.jpg')
    txt_pattern = os.path.join(folder_path, '*.txt')

    # Get a list of all .jpg and .txt files in the folder
    jpg_files = glob.glob(jpg_pattern)
    txt_files = glob.glob(txt_pattern)

    # Combine the lists of files
    files_to_delete = jpg_files + txt_files

    # Loop through the files and delete them
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except OSError as e:
            print(f"Error: {file_path} : {e.strerror}")
####################################################################################
def Transfer_crops_to_shared():
    # Set the source and destination directories
    dst_dir = shared_folder        
    #report_path = '/home/user/Documents/PCB-Report/Report-doc/Report.docx'
    src_dir = ic_images
    # Loop through all files in the source directory
    for filename in os.listdir(src_dir):
        # Check if the file is a .jpg file
        if filename.endswith(".JPG") or filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".jpg"):
            # Construct the full path to the file
            src_path = os.path.join(src_dir, filename)
            dst_path = os.path.join(dst_dir, filename)
            # Move the file to the destination directory
            shutil.move(src_path, dst_path)
####################################################################################
def move_and_overwrite(source, destination):
    if os.path.exists(destination):
        os.remove(destination)
    shutil.move(source, destination)
####################################################################################
def Making_shared_folder_ready():
    base_directory = "C:\\Users\\user\\Desktop"
    datasheets_folder = os.path.join(base_directory, "Datasheets")
    shared_folder = os.path.join(base_directory, "Shared")
    IC_Images = os.path.join(base_directory, "IC-Images")
    # Share the folders
    command1 = 'net share Datasheets=C:\\Users\\user\\Desktop\\Datasheets /grant:Everyone,FULL'
    command2 = 'net share Shared=C:\\Users\\user\\Desktop\\Shared /grant:Everyone,FULL' 
    command3 = 'net share Shared=C:\\Users\\user\\Desktop\\IC-Images /grant:Everyone,FULL' 
    # Check if folders exist, if not, create them
    if not os.path.exists(datasheets_folder):
        os.makedirs(datasheets_folder)    
        try:
            subprocess.run(['cmd.exe', '/c', command1], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in command1: {e}")
    if not os.path.exists(shared_folder):
        os.makedirs(shared_folder)
        try:
            subprocess.run(['cmd.exe', '/c', command2], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in command2: {e}")
    if not os.path.exists(IC_Images):
        os.makedirs(IC_Images)    
        try:
            subprocess.run(['cmd.exe', '/c', command3], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in command3: {e}")
    if not os.path.exists(Data):
        os.makedirs(Data)
'''
# This function is a part of initialization and finalizing the unfinished process
def checking_image_existence():
    with open(address_path, 'r') as file:
         lines = file.readlines()
         first_line = lines[0].rstrip('\n')
    image_file_path = os.path.join(first_line, "FinalIMG.jpg")
    #image_already_path = os.path.join(shared_folder, "FinalIMG.jpg")
    if os.path.isfile(image_file_path):
        return True
    else:
        os.remove(address_path)
        return False
'''
def post_image_generation_proccessing():
    with open(address_path, 'r') as file:
        lines = file.readlines()
        first_line = lines[0].rstrip('\n')
    image_file_path = os.path.join(first_line, "FinalIMG.jpg")
    if os.path.isfile(image_file_path):
        shutil.move(image_file_path, shared_folder)
        # If there are more than one lines in the file
        if len(lines) > 1:
            # Remove the first line
            lines.pop(0)
            # Write the remaining lines back to the file
            with open(address_path, 'w') as file:
                file.writelines(lines)
            # Create Address.txt in the shared folder and write the image_file_path into it
            with open(os.path.join(shared_folder, 'Address.txt'), 'w') as file:
                file.write(image_file_path + '\n')
        else:
            #move_and_overwrite(address_path, shared_folder)
            shutil.move(address_path, shared_folder)
        return True
    else:
        return False
def init_fls_device():
    app = Application(backend='uia').start('C:\Program Files\ChipScan-Scanner 4.0.32\ChipScan.exe').connect(title='Langer EMV-Technik GmbH ChipScan-Scanner 4.0.32  -  Untitled.csd')
    window = app.LangerEMVTechnikGmbHChipScanScanner4032UntitledCsd
    Float = window.child_window(title="Maximize", control_type="Button").wrapper_object()
    Float.click_input()

    device = window.child_window(title="Devices", control_type="MenuItem").wrapper_object()
    device.click_input()
    # Press Tab key twice to navigate to the "Detect Recently Found Devices" menu item

    window.type_keys('{TAB}{TAB}{TAB}', with_spaces=True)
    # Press Enter key to select the "Detect Recently Found Devices" menu item
    window.type_keys('{ENTER}')
    time.sleep(3)
    ###### using the app calibration is done ########
    call = window.child_window(title="Calibrate", control_type="Button")
    call.click_input()
    time.sleep(5)
def delete_buffer():
    if os.path.isfile(address_path):
        with open(address_path, 'r') as file:
            lines = file.readlines()
            first_line = lines[0].rstrip('\n')
        image_file_path = os.path.join(first_line, "FinalIMG.jpg")
        if os.path.isfile(image_file_path):
            os.remove(address_path)
            os.remove(image_file_path)
        else:
            os.remove(address_path)
    elif os.path.isfile(shared_image):
        os.remove(shared_image)
        
def delete_ic_image_subfolders_and_files():
    for filename in os.listdir(ic_images):
        file_path = os.path.join(ic_images, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
def delete_data():
    if os.path.exists(Path_Data):
        os.remove(Path_Data)
    else:
        return
def delete_ic_crops():
    for filename in os.listdir(shared_folder):
        if filename.endswith('.jpg') and filename != 'FinalIMG.jpg':
        
            os.remove(os.path.join(shared_folder, filename))
def image_buffer():
    if os.path.isfile(address_path):
        with open(address_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >=1:
                return True
            else:
                return False
    if os.path.isfile(shared_image):
        return True
    else:
        return False   
    
def IC_Detection_Post_processing():
    test_dir = 'C:/Users/user/Desktop/IC-Images/IC-Images'
    crops_dir = os.path.join(test_dir, 'crops')
    labels_dir = os.path.join(test_dir, 'labels')
    final_dir = 'C:/Users/user/Desktop/IC-Images'  # Final directory to move images to
    '''
    # Delete .jpg files in test directory
    for item in os.listdir(test_dir):
        if item.endswith('.jpg'):
            os.remove(os.path.join(test_dir, item))
    '''
    for item in os.listdir(test_dir):
        if item.endswith('.jpg'):
            new_name = item.replace('.jpg', 'FinalIMG-IC-Detected.jpg')
            os.rename(os.path.join(test_dir, item), os.path.join(test_dir, new_name))
            shutil.move(os.path.join(test_dir, new_name), shared_folder)
    # Delete 'labels' directory
    shutil.rmtree(labels_dir, ignore_errors=True)

    # Move folders from 'crops' to 'test' directory and delete 'crops' directory
    for folder in os.listdir(crops_dir):
        folder_path = os.path.join(crops_dir, folder)
        index = 0
        for item in os.listdir(folder_path):
            if item.endswith('.jpg'):
                # Rename the file to folder_name_index.jpg
                new_name = f"{folder}_{index}.jpg"
                os.rename(os.path.join(folder_path, item), os.path.join(folder_path, new_name))
                item = new_name  # Update item to the new name
                index += 1  # Increment the index
                destination_path = os.path.join(test_dir, item)
                # Check if file already exists at destination and delete it if it does
                if os.path.exists(destination_path):
                    os.remove(destination_path)
                shutil.move(os.path.join(folder_path, item), test_dir)
        shutil.rmtree(folder_path, ignore_errors=True)
    shutil.rmtree(crops_dir, ignore_errors=True)

    # Move final images from 'test' directory to 'IC-Images' directory
    for item in os.listdir(test_dir):
        if item.endswith('.jpg'):
            shutil.move(os.path.join(test_dir, item), final_dir)
    shutil.rmtree(test_dir, ignore_errors=True)

######################################################
class WorkerSignals(QObject):
    result = pyqtSignal(str, str, bool)

class Worker(QRunnable):
    def __init__(self, func, status_flag, pass_text, fail_text):
        super().__init__()
        self.func = func
        self.status_flag = status_flag
        self.pass_text = pass_text
        self.fail_text = fail_text
        self.signals = WorkerSignals()

    def run(self):
        result = self.func()
        self.signals.result.emit(self.status_flag, self.pass_text if result else self.fail_text, result)
######################################################
from PyQt5.QtCore import QThread, pyqtSignal

class ODWorker(QThread):
    finished = pyqtSignal(str, str)  # Signals to emit output and error

    def __init__(self, cmd):
        super(ODWorker, self).__init__()
        self.cmd = cmd

    def run(self):
        # Execute the command and emit its output and error through a signal
        result = subprocess.run(self.cmd, text=True, capture_output=True, encoding='utf-8')
        output = result.stdout
        error = result.stderr
        self.finished.emit(output, error)  # Emit the output and error
######################################################
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def resizeEvent(self, event):
        self.ui.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, self.width() - 20, self.height() - 20))
        super().resizeEvent(event)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 480, 480))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Meta = QtWidgets.QLabel(self.verticalLayoutWidget)
        ### CSS ###
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Meta.setFont(font)
        self.Meta.setAlignment(QtCore.Qt.AlignCenter)
        self.Meta.setObjectName("Meta")
        self.verticalLayout.addWidget(self.Meta)
        #############################################################################
        self.Run = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Run.setStyleSheet("background-color: #2ABf9E; padding: 10px; font-size: 18px;")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Run.setFont(font)
        self.Run.setObjectName("Run")
        self.verticalLayout.addWidget(self.Run)
        ############################################################################
        self.Run.setEnabled(False)
        self.Run.clicked.connect(self.run)
        ############################################################################
        self.Calculator = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Calculator.setStyleSheet("background-color: #2ABf9E; padding: 10px; font-size: 18px;")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Calculator.setFont(font)
        self.Calculator.setObjectName("Calculator")
        self.verticalLayout.addWidget(self.Calculator)
        self.Calculator.clicked.connect(self.calculate)
        ############################################################################
        self.Browse = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Browse.setStyleSheet("background-color: #2ABf9E; padding: 10px; font-size: 18px;")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Browse.setFont(font)
        self.Browse.setObjectName("Browse Image")
        self.verticalLayout.addWidget(self.Browse)
        self.Browse.clicked.connect(self.browse_image)
        ############################################################################
        # ScrollArea for QTextBrowser
        self.scroll = QScrollArea(self.verticalLayoutWidget)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        ############################################################################
        self.Log = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.Log.setStyleSheet("color: #FFFFFF; background-color: #33373B;")   
        self.Log.setMinimumSize(500, 500)
        self.Log.setObjectName("Log")
        self.verticalLayout.addWidget(self.Log)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 322, 45))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setWindowIcon(QtGui.QIcon('logo.png'))
        ######################### Events ######################################
        MainWindow.closeEvent = self.closeEvent
        # Set the QTextBrowser as the widget for ScrollArea
        self.scroll.setWidget(self.Log)
        self.verticalLayout.addWidget(self.scroll)
        #######################################################################
        # Setup the ODWorker thread
        self.od_worker = None
        
    def resizeEvent(self, event):
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, self.width() - 20, self.height() - 20))
        super().resizeEvent(event)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Meta: Edition 0.1"))
        self.Meta.setText(_translate("MainWindow", "Meta Application"))
        self.Run.setText(_translate("MainWindow", "Run"))
        self.Calculator.setText(_translate("MainWindow", "Calculator"))
        self.Browse.setText(_translate("MainWindow", "Browse Image"))
        #unmount_OCR()
        #unmount_OD()
        Making_shared_folder_ready()
        self.init()
    def browse_image(self):
        t = threading.Thread(target=self._browse_image)
        t.start()
    def _browse_image(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '', 'Image (*.jpg, *.jpeg *.JPG *.png *.tiff)')
        if path:
            #self.Browse.setEnabled(False)
            print("The Image is loaded.")
            self.Log.append("The Image is loaded.")
            # Read the image
            img = cv2.imread(path)
            
            # Get the directory and the extension of the original image
            directory, filename = os.path.split(path)
            basename, _ = os.path.splitext(filename)
            
            # Rename and change format of the image
            new_filename = "FinalIMG.jpg"
            new_path = os.path.join(directory, new_filename)
            
            # Save the image to the same directory
            cv2.imwrite(new_path, img)
            print("The image is saved...")
            self.Log.append("Image Format changing and saving to the directory...")
            
            # Check if the address_path file exists
            if os.path.exists(address_path):
                # If it exists, append the directory to the last line of the address_path
                with open(address_path, 'a') as f:
                    f.write('\n' + directory)
                print("The image is written to Addres.txt")
                self.Log.append("The Image is saved to the buffer(Address.txt)")
            else:
                # If it doesn't exist, create the file and write the directory to the first line
                with open(address_path, 'w') as f:
                    f.write(directory)
                print("The image is written to Addres.txt")
                self.Log.append("The Image is saved to the buffer(Address.txt)")
        else:
            self.Log.append("No Image selected...")
            
    def __init__(self):
        ##### SSH to IC-Detection
        self.lock = Lock()
        self.output_od = None
        self.error_od = None
        self.status = {
            "fls_status": False
        }
        self.buffer_status = image_buffer()
        self.error_occurred = False
        self.init_error_occurred = False
        self.error_messages = []
        self.pool = QThreadPool()
        self.finished_workers = 0
    def remove_log(self,txt):
        # Get the cursor position of the last character
        cursor = self.Log.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.movePosition(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.KeepAnchor)
        # Delete the entire line
        cursor.removeSelectedText() 
        # Move the cursor back to the start of the line
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        # Insert the new text at the same position
        cursor.insertText(txt)

    def init(self):
        self.Log.append('Please wait for the initialization')
        close_application('ChipScan.exe')
        close_application('card communication.exe')
        self.Log.append("The previous open applications are closed successfully...")
        
        init_functions = [(check_com_port, 'fls_status', 'FLS connection passed', 'FLS connection failed')]

        for func, status_flag, pass_text, fail_text in init_functions:
            worker = Worker(func, status_flag, pass_text, fail_text)
            worker.signals.result.connect(self.process_result)
            self.pool.start(worker)
        #self.fls_device_init()
        '''
        init_fls_device()
        close_application('ChipScan.exe')
        time.sleep(2)
        calibrate()
        time.sleep(5)
        '''
        
    def process_result(self, status_flag, message, result):
        print(message)
        self.Log.append(message)
        self.status[status_flag] = result
        if not result:
            self.error_messages.append(message)
        self.finished_workers += 1
        if self.finished_workers == len(self.status):
            if all(self.status.values()):
                self.signalNotifyFlags()
            else:
                self.init_error_occurred = True
                Init_Error = QtWidgets.QMessageBox()
                Init_Error.setIcon(QtWidgets.QMessageBox.Critical)
                Init_Error.setText('Error')
                Init_Error.setInformativeText('The initialization is not finished successfully. Please fix the issue and try again later.')
                Init_Error.setWindowTitle("Error")
                Init_Error.setDetailedText('\n'.join(self.error_messages))  # Display all fail_text messages
                Init_Error.exec_()
                if Init_Error == QtWidgets.QMessageBox.Ok:
                    MainWindow.close()
######################################################################################
    def Do_You_Like_The_Image1(self):
        # Display a confirmation dialog
        reply = QtWidgets.QMessageBox.question(None, 'Take or leave?', "Would you prefer to continue with this image?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            delete_ic_image_subfolders_and_files()
            delete_data()
            self.Log.append("Sending the Image for IC detection part...")
            print("Sending the Image for IC detection part...")
            self.object_detection()
        else:
            ### Delete the image AND the address.txt in the shared folder
            os.remove(shared_image)
            os.remove(moved_address_path)
            self.Log.append("The image has been deleted.")
            print("The image has been deleted.")
            self.Log.append("Checking the buffer for another images.")
            print("Checking the buffer for another images.")
            if image_buffer():
                self.Existing_Image_Processing()
            else:
                self.Log.append("The buffer is empty.")
                print("The buffer is empty.")
                self.setup_watcher_image()     
######################################################################################
    def Do_You_Like_The_Image2(self):
        # Display a confirmation dialog
        reply = QtWidgets.QMessageBox.question(None, 'Take or leave?', "Would you prefer to continue with this image?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            #### Deleting the IC crops #### 
            delete_ic_crops()
            self.Log.append("Sending the Image for IC detection part...")
            print("Sending the Image for IC detection part...")
            self.object_detection()
        else:
            ### Delete the image OR the address.txt in the shared folder
            os.remove(shared_image)
            if os.path.isfile(moved_address_path):
                os.remove(moved_address_path)
            self.Log.append("The image has been deleted.")
            print("The image has been deleted.")
            ### check the buffer for more images...
            self.Log.append("Checking the buffer for another images.")
            print("Checking the buffer for another images.")
            if image_buffer():
                self.Existing_Image_Processing()
            else:      
                self.setup_watcher_image()   
######################################################################################
    def ImageBufferEvent(self):
        # Display a confirmation dialog
        reply = QtWidgets.QMessageBox.question(None, 'Processing Buffer Image', "There are images in the buffer. Would you like to process them?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.Existing_Image_Processing()
        else:
            delete_buffer() 
            delete_images_and_text_files(shared_folder)
            delete_ic_image_subfolders_and_files()
            self.setup_watcher_image()
######################################################################################
    def signalNotifyFlags(self):
        print("The system is ready.")
        self.Log.append("The system is ready.")
        if image_buffer():
            self.ImageBufferEvent()
            self.Run.setEnabled(True)
            self.Browse.setEnabled(True)
        else:  
            self.Run.setEnabled(True)
            self.Browse.setEnabled(True)
            self.setup_watcher_image()
        #self.Log.append('You can press the Run button to start the image capturing program.')   
############################################################################################
    ''' FLS Thraed
    def fls_device_init(self):
        self.fls_init = initFLSDeviceThread()
        self.fls_init.start()
    '''    
######################################################################################
    def Existing_Image_Processing(self):
        if (os.path.isfile(address_path) and not(os.path.isfile(shared_image))):
            self.signalNotifyImage()     
        if (os.path.isfile(shared_image) and os.path.isfile(address_path)) or (os.path.isfile(shared_image) and not(os.path.isfile(address_path))) :
            self.Log.append("There is an existing image on the shared folder...")         
            ############ Delete IC-Images folder files and sub-folders####################
            delete_ic_image_subfolders_and_files()
            delete_data()
            #### Deleting the Report.docx #####
            if os.path.exists(report_path):
                os.remove(report_path)
                print("The Report.docx has been deleted.")
            else:
                print("The Report.docx does not exist.")
            self.Log.append("Showing the existing image...")
            self.image_opening()
            self.Do_You_Like_The_Image2()
            
######################################################################################
    def image_opening(self):
        #im_path = 'C:/Users/user/Desktop/Shared/FinalIMG.jpg'
        self.open_image = ShowImageThread(shared_image)
        self.open_image.start()
######################################################################################
    def setup_watcher_image(self):
        self.watcher_image = Watcher_Image(address_path, checkEvery=5)
        self.watcher_image.fileReady.connect(self.signalNotifyImage)
        self.watcher_image.fileNotGenerated.connect(self.callbackNotifyImage)
        self.watcher_image.start()        
    def callbackNotifyImage(self):      
        print("The Image is not generated yet")
        self.remove_log('Waiting for new image...')      
    def signalNotifyImage(self):
        self.setup_watcher_image_valid()
######################################################################################
    def setup_watcher_image_valid(self):
        self.watcher_image_valid = Watcher_Image_Valid(address_path, checkEvery=10)
        self.watcher_image_valid.fileReady.connect(self.signalNotifyImageValid)
        self.watcher_image_valid.fileNotGenerated.connect(self.callbackNotifyImageValid)
        self.watcher_image_valid.CaptureAgain.connect(self.RemoveAddresstxt)
        self.watcher_image_valid.start()     
    def callbackNotifyImageValid(self):      
        print("The Image is not generated successfully after image capturing by FLS!")
        with open(address_path, 'r') as file:
            lines = file.readlines()
            lines.pop(0)
        with open(address_path, 'w') as file:
            for line in lines:
                file.write(line)
    def RemoveAddresstxt(self):
        os.remove(address_path)
        print("There is no valid Image in the buffer!")
        print("Start capturing new images...")
        self.setup_watcher_image()
    def signalNotifyImageValid(self):
        print("Succeed to another image...")
        self.setup_watcher_buffer()
######################################################################################
    def setup_watcher_buffer(self):
        self.watcher_buffer = Watcher_Buffer(shared_image, checkEvery=5)
        self.watcher_buffer.bufferReady.connect(self.signalNotifyBuffer)
        self.watcher_buffer.bufferNotReady.connect(self.callbackNotifyBuffer)
        self.watcher_buffer.start() 
    def callbackNotifyBuffer(self):
        print("The Buffer is not Ready yet")
        #self.remove_log('Waiting for new image...')
    def signalNotifyBuffer(self,f):
        print("The Buffer is ready.")
        self.Log.append("The Buffer is ready.")
        print("The Image is ready and its address is: ", f)
        self.Log.append("There is a new image on the directory...")
        post_image_generation_proccessing()
        self.Log.append("The new image is on a shared folder")
        self.Log.append("Showing the new image...")
        self.image_opening()
        self.Do_You_Like_The_Image1()
        
######################################################################################
    def object_detection(self):
        self.watcher_od = Watcher_OD(temp_od_path, checkEvery=10)
        self.watcher_od.fileReady.connect(self.signalNotifyOD)
        self.watcher_od.fileNotGenerated.connect(self.callbackNotifyOD)
        self.watcher_od.timerStarted.connect(self.run_od)  # Connect the new signal to run_od
        self.watcher_od.start()
#########################################################################
    def run_od(self):
        # The command string for running the Python script
        commands = "C:\\Users\\user\\anaconda3\\Scripts\\activate venv && cd C:\\Users\\user\\Desktop && yolo predict project=IC-Images name=IC-Images save_txt=true save_crop=true save_conf=true conf=0.4 model=C:/Users/user/Desktop/IC_Detection_Models/best3.pt source=C:/Users/user/Desktop/Shared"
        # Split the commands to pass it as a list to subprocess
        cmd = ['cmd', '/c'] + commands.split()
        # Initialize and start the ODWorker thread
        self.od_worker = ODWorker(cmd)
        self.od_worker.finished.connect(self.on_batch_finished_od)
        self.od_worker.finished.connect(self.od_worker.deleteLater)
        self.od_worker.start()
#########################################################################
    def on_batch_finished_od(self, output, error):
        print("Output:", output)
        print("Error:", error)
        with self.lock:
            self.output_od = output
            self.error_od = error
        if not output and 'Results saved' in error:
            # Do something if the command executed successfully
            print('The IC-Detection is done successfully.')
            self.Log.append("The IC-Detection is done successfully.")
        else:
            # Handle the case when there is an error or unexpected output
            self.error_occurred = True
            print("The IC-detection has NOT been completed.")
            self.Log.append("The IC-detection has NOT been completed.\n")
            Error = QtWidgets.QMessageBox.information(None, 'Error', 'An error has been occured in IC-Detection side. Close the App and fix the problem.', QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            if Error == QtWidgets.QMessageBox.Ok:
                MainWindow.close()
        return output, error
#########################################################################
    def callbackNotifyOD(self):
        print("Waiting for IC detection...")
        self.remove_log('Waiting for IC detection...')   
        
    def signalNotifyOD(self, f):
        with self.lock:
            output_od =  self.output_od 
            error_od  =  self.error_od
        print("The output and error from Batch execution is ready...")
        print("The IC-detection is finished and its address is: ", f)  
        self.Log.append("The IC-detection process is finished.")
        print("The error_od is:",error_od)
        if error_od is not None and '0 label' in error_od and not os.path.exists(crop_folder):
            delete_ic_image_subfolders_and_files()
            print("There is no IC detected in the FinalIMG.")
            self.Log.append("There is no IC detected in the FinalIMG.")
            self.watcher_od.emitFileNotGenerated = False  # Set the flag to False
            # delete the IC-Images image and subfolders
            #delete_ic_image_subfolders_and_files()
            #This part is related to the signalNotifyReport 
            if os.path.isfile(moved_address_path):
                destination_address = destination_image_address(shared_folder)
                num = create_next_folder()
                move_files(num)
                source_address = os.path.join(shared_folder, str(num))
                copy_folder(source_address, destination_address)
                print("The results are ready on the directory, and the specified folder is:"+num)
                self.Log.append("The results are ready on the directory, and the specified folder is:"+num)
                print("The processing of the new image is finished successfully.\n\n")
                self.Log.append("The processing of the new image is finished successfully.\n\n")
            #if the Address.txt is NOT available on the shared folder
            else:
                num = create_next_folder()
                move_files(num)
                self.Log.append("The results are ready on the directory, and the specified folder is:"+num)
                print("The results are ready on the directory, and the specified folder is:"+num)
                self.Log.append("The processing of the new image is finished successfully.\n\n")
                print("The processing of the new image is finished successfully.\n\n")
            if not(image_buffer()):
                self.Log.append('There is no image in the buffer.')
                #self.Run.setEnabled(True)
            self.setup_watcher_image()
        else:
            IC_Detection_Post_processing()
            self.setup_watcher_ocr_data()
#########################################################################  
    def setup_watcher_ocr_data(self):
        self.watcher_ocr_data = Watcher_OCR_Data(report_path, checkEvery=5)
        self.watcher_ocr_data.fileReady.connect(self.signalNotifyOCRData)
        self.watcher_ocr_data.fileNotGenerated.connect(self.callbackNotifyOCRData)
        self.watcher_ocr_data.timerStarted.connect(self.run_ocr_data)  # Connect the new signal to run_report
        self.watcher_ocr_data.start()
#########################################################################
    def run_ocr_data(self):
        subprocess.Popen(['start', 'cmd', '/k', 'C:/Users/user/Desktop/Sharifi6/main.bat'], shell=True)
#########################################################################
    def callbackNotifyOCRData(self):
        print("The Report is not generated yet")
        self.remove_log('Waiting for new report....')  
         
#########################################################################
    def signalNotifyOCRData(self, f):
        print("The report is ready and its address is: ", f)    
        self.Log.append("The report is ready on the shared folder to be opened.")
        #if the Address.txt is available on the shared folder
        Transfer_crops_to_shared()
        #os.remove(Path_Data)
        if os.path.isfile(moved_address_path):
            destination_address = destination_image_address(shared_folder)
            num = create_next_folder()
            move_files(num)
            source_address = os.path.join(shared_folder, str(num))
            copy_folder(source_address, destination_address)
            self.Log.append("The results are ready on the directory, and the specified folder is:"+num)
            self.Log.append("The processing of the new image is finished successfully.\n\n")
            report_open_delete_address(destination_address,num)
        #if the Address.txt is NOT available on the shared folder
        else:
            num = create_next_folder()
            move_files(num)
            f_path = os.path.join(shared_folder, num)
            print(f_path)
            r_path = os.path.join(f_path, "report.docx")
            os.startfile(r_path)
            self.Log.append("The results are ready on the directory, and the specified folder is:"+num)
            self.Log.append("The processing of the new image is finished successfully.\n\n")
        if not(image_buffer()):
            self.Log.append('Please press the Run button to start the process.')
            self.Run.setEnabled(True)
        self.setup_watcher_image()
    '''
#########################################################################
    def setup_watcher_report(self):
        self.watcher_report = Watcher_Report(report_path, checkEvery=5)
        self.watcher_report.fileReady.connect(self.signalNotifyReport)
        self.watcher_report.fileNotGenerated.connect(self.callbackNotifyReport)
        self.watcher_report.timerStarted.connect(self.run_report)  # Connect the new signal to run_report
        self.watcher_report.start()
#########################################################################  
    def run_report(self):
        #subprocess.Popen(['start', 'cmd', '/k', 'C:/Users/user/Desktop/Sharifi/show_ui.bat'], shell=True)
        subprocess.Popen(['C:/Users/user/Desktop/Sharifi/show_ui.bat'], shell=True)

#########################################################################
    def callbackNotifyReport(self):
        print("The Report is not generated yet")
        self.remove_log('Waiting for new report...')             
    def signalNotifyReport(self, f):
        print("The report is ready and its address is: ", f)    
        self.Log.append("The report is ready on the shared folder to be opened.")       
        #if the Address.txt is available on the shared folder
        Transfer_crops_to_shared()
        os.remove(Path_Data)
        if os.path.isfile(moved_address_path):
            destination_address = destination_image_address(shared_folder)
            num = create_next_folder()
            move_files(num)
            source_address = os.path.join(shared_folder, str(num))
            copy_folder(source_address, destination_address)
            self.Log.append("The results are ready on the directory, and the specified folder is:"+num)
            self.Log.append("The processing of the new image is finished successfully.\n\n")
            report_open_delete_address(destination_address,num)
        #if the Address.txt is NOT available on the shared folder
        else:
            num = create_next_folder()
            move_files(num)
            f_path = os.path.join(shared_folder, num)
            print(f_path)
            r_path = os.path.join(f_path, "report.docx")
            os.startfile(r_path)
            self.Log.append("The results are ready on the directory, and the specified folder is:"+num)
            self.Log.append("The processing of the new image is finished successfully.\n\n")
        if not(image_buffer()):
            self.Log.append('Please press the Run button to start the process.')
            self.Run.setEnabled(True)
        self.setup_watcher_image()
        '''
#########################################################################
    def run(self):
        self.Run.setEnabled(False)
        subprocess.Popen(['C:/Users/user/Desktop/FLS/UI/FLS-UI-ed9-server/scanner_program_4.9-Y1/card communication/bin/x64/Debug/card communication.exe'])
        self.Log.append('The FLS app started.')
        '''
        self.Log.append('Please Do not touch the mouse or keyboard!!\n')
        init_fls_device()
        close_application('ChipScan.exe')
        time.sleep(2)
        calibrate()
        time.sleep(5)
        '''
        self.Run.setEnabled(True)
        #self.setup_watcher_image()
    def calculate(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Calculator()
        self.ui.setupUi(self.window)
        self.window.show()
       
    def closeEvent(self, event):
        if not self.error_occurred:
            reply = QtWidgets.QMessageBox.question(None, 'Close Confirmation', 'Are you sure you want to close the app?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                close_application('card communication.exe')
                close_application('ChipScan.exe')
                time.sleep(2)
                calibrate()
            else:
                event.ignore()
        else:
            close_application('card communication.exe')
            close_application('ChipScan.exe')
            time.sleep(2)
            calibrate()        
if __name__ == "__main__":
    '''
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)    
    MainWindow.show()
    sys.exit(app.exec_())
    sys.exit(app.exec_())
    '''
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())  
    