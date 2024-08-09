from PyQt5 import QtCore
import os.path
from Serial import check_com_port
from Ubuntu_Initializations import check_valid_image, ssh_connection_to_ocr_ubuntu, login, mount_shared, mount_shared_od, mount_ic_images_OCR, mount_ic_images_OD, mount_datasheet, MongoDB, ssh_connection_to_od_ubuntu
class Watcher_Image(QtCore.QObject):
    fileReady = QtCore.pyqtSignal(str)
    fileNotGenerated = QtCore.pyqtSignal(str)
    def __init__(self, aFile, checkEvery=1):
        super(Watcher_Image, self).__init__()
        self.file = aFile
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkFile)
    def _checkFile(self):
        if os.path.isfile(self.file):
            self._timer.stop()
            self.fileReady.emit(self.file)
        else:
            self.fileNotGenerated.emit(self.file)
    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()       

######################################################
class Watcher_Image_Valid(QtCore.QObject):
    fileReady = QtCore.pyqtSignal()
    fileNotGenerated = QtCore.pyqtSignal()
    CaptureAgain = QtCore.pyqtSignal()
    def __init__(self, aFile, checkEvery=1):
        super(Watcher_Image_Valid, self).__init__()
        self.file = aFile
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkFile)
    
    def _checkFile(self):
        if check_valid_image()==1:
            self._timer.stop()
            self.fileReady.emit()
        if check_valid_image() ==2:
            self.fileNotGenerated.emit()
        if check_valid_image() ==3:
            self._timer.stop()
            self.CaptureAgain.emit() 
    def start(self):
        self._timer.start()
    def stop(self):
        self._timer.stop()
######################################################
class Watcher_OD(QtCore.QObject):
    fileReady = QtCore.pyqtSignal(str)
    fileNotGenerated = QtCore.pyqtSignal(str)
    timerStarted = QtCore.pyqtSignal()  # New signal

    def __init__(self, aFile, checkEvery=1):
        super(Watcher_OD, self).__init__()
        self.file = aFile
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkFile)
        self.emitFileNotGenerated = True  # New flag
    def _checkFile(self):
        if os.path.isfile(self.file):
            self._timer.stop()
            self.fileReady.emit(self.file)
        elif self.emitFileNotGenerated:  # Check the flag before emitting
            self.fileNotGenerated.emit(self.file)

    def start(self):
        self._timer.start()
        self.timerStarted.emit()  # Emit the signal when the timer starts

    def stop(self):
        self._timer.stop()
'''
######################################################
class Watcher_OD(QtCore.QObject):
    fileReady = QtCore.pyqtSignal(str)
    fileNotGenerated = QtCore.pyqtSignal(str)
    timerStarted = QtCore.pyqtSignal()  # New signal

    def __init__(self, aFile, checkEvery=1):
        super(Watcher_OD, self).__init__()
        self.file = aFile
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkFile)

    def _checkFile(self):
        if os.path.isfile(self.file):
            self._timer.stop()
            self.fileReady.emit(self.file)
        else:
            self.fileNotGenerated.emit(self.file)

    def start(self):
        self._timer.start()
        self.timerStarted.emit()  # Emit the signal when the timer starts

    def stop(self):
        self._timer.stop()
#################################################################
'''
class Watcher_Report(QtCore.QObject):
    fileReady = QtCore.pyqtSignal(str)
    fileNotGenerated = QtCore.pyqtSignal(str)
    timerStarted = QtCore.pyqtSignal()  # New signal

    def __init__(self, aFile, checkEvery=1):
        super(Watcher_Report, self).__init__()
        self.file = aFile
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkFile)

    def _checkFile(self):
        if os.path.isfile(self.file):
            self._timer.stop()
            self.fileReady.emit(self.file)
        else:
            self.fileNotGenerated.emit(self.file)

    def start(self):
        self._timer.start()
        self.timerStarted.emit()  # Emit the signal when the timer starts

    def stop(self):
        self._timer.stop()
#################################################################
class Watcher_OCR_Data(QtCore.QObject):
    fileReady = QtCore.pyqtSignal(str)
    fileNotGenerated = QtCore.pyqtSignal(str)
    timerStarted = QtCore.pyqtSignal()  # New signal

    def __init__(self, aFile, checkEvery=1):
        super(Watcher_OCR_Data, self).__init__()
        self.file = aFile
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkFile)

    def _checkFile(self):
        if os.path.isfile(self.file):
            self._timer.stop()
            self.fileReady.emit(self.file)
        else:
            self.fileNotGenerated.emit(self.file)

    def start(self):
        self._timer.start()
        self.timerStarted.emit()  # Emit the signal when the timer starts

    def stop(self):
        self._timer.stop()
#################################################################

class Watcher_Buffer(QtCore.QObject):
    bufferReady = QtCore.pyqtSignal(str)
    bufferNotReady = QtCore.pyqtSignal(str)

    def __init__(self, aFile, checkEvery=1):
        super(Watcher_Buffer, self).__init__()
        self.file = aFile
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkFile)

    def _checkFile(self):
        if not os.path.isfile(self.file):
            self._timer.stop()
            self.bufferReady.emit(self.file)
        else:
            self.bufferNotReady.emit(self.file)
    def start(self):
        self._timer.start()
    def stop(self):
        self._timer.stop()
#################################################################
class Watcher_FLS(QtCore.QObject):
    deviceReady = QtCore.pyqtSignal(bool)
    deviceNotReady = QtCore.pyqtSignal(bool)
    def __init__(self, aStatus, checkEvery=1):
        super(Watcher_FLS, self).__init__()
        self.status = aStatus
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkDevice)
    def _checkDevice(self):
        self.status = check_com_port()
        if self.status:
            self._timer.stop()
            self.deviceReady.emit(self.status)
        else:
            self.deviceNotReady.emit(self.status)
    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()
#################################################################
class Watcher_OCR_Server(QtCore.QObject):
    deviceReady = QtCore.pyqtSignal(bool)
    deviceNotReady = QtCore.pyqtSignal(bool)
    def __init__(self, aStatus, checkEvery=1):
        super(Watcher_OCR_Server, self).__init__()
        self.status = aStatus
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkDevice)
    def _checkDevice(self):
        self.status = ssh_connection_to_ocr_ubuntu()
        if self.status:
            self._timer.stop()
            self.deviceReady.emit(self.status)
        else:
            self.deviceNotReady.emit(self.status)
    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()
#################################################################
class Watcher_OD_Server(QtCore.QObject):
    deviceReady = QtCore.pyqtSignal(bool)
    deviceNotReady = QtCore.pyqtSignal(bool)
    def __init__(self, aStatus, checkEvery=1):
        super(Watcher_OD_Server, self).__init__()
        self.status = aStatus
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkDevice)
    def _checkDevice(self):
        self.status = ssh_connection_to_od_ubuntu()
        if self.status:
            self._timer.stop()
            self.deviceReady.emit(self.status)
        else:
            self.deviceNotReady.emit(self.status)
    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()
#################################################################
class Watcher_Internet_Login(QtCore.QObject):
    internetReady = QtCore.pyqtSignal(bool)
    internetNotReady = QtCore.pyqtSignal(bool)
    def __init__(self, aStatus, checkEvery=1):
        super(Watcher_Internet_Login, self).__init__()
        self.status = aStatus
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkDevice)
    def _checkDevice(self):
        self.status = login()
        if self.status:
            self._timer.stop()
            self.internetReady.emit(self.status)
        else:
            self.internetNotReady.emit(self.status)
    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()
#################################################################
class Watcher_Mount_Shared(QtCore.QObject):
    folderReady = QtCore.pyqtSignal(bool)
    folderNotReady = QtCore.pyqtSignal(bool)
    def __init__(self, aStatus, checkEvery=1):
        super(Watcher_Mount_Shared, self).__init__()
        self.status = aStatus
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkDevice)
    def _checkDevice(self):
        self.status = mount_shared()
        if self.status:
            self._timer.stop()
            self.folderReady.emit(self.status)
        else:
            self.folderNotReady.emit(self.status)
    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()
#################################################################
class Watcher_Mount_Shared_OD(QtCore.QObject):
    folderReady = QtCore.pyqtSignal(bool)
    folderNotReady = QtCore.pyqtSignal(bool)
    def __init__(self, aStatus, checkEvery=1):
        super(Watcher_Mount_Shared_OD, self).__init__()
        self.status = aStatus
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkDevice)
    def _checkDevice(self):
        self.status = mount_shared_od()
        if self.status:
            self._timer.stop()
            self.folderReady.emit(self.status)
        else:
            self.folderNotReady.emit(self.status)
    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()
#################################################################
class Watcher_Mount_IC_Images_OCR(QtCore.QObject):
    folderReady = QtCore.pyqtSignal(bool)
    folderNotReady = QtCore.pyqtSignal(bool)
    def __init__(self, aStatus, checkEvery=1):
        super(Watcher_Mount_IC_Images_OCR, self).__init__()
        self.status = aStatus
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkDevice)
    def _checkDevice(self):
        self.status = mount_ic_images_OCR()
        if self.status:
            self._timer.stop()
            self.folderReady.emit(self.status)
        else:
            self.folderNotReady.emit(self.status)
    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()
#################################################################
class Watcher_Mount_IC_Images_OD(QtCore.QObject):
    folderReady = QtCore.pyqtSignal(bool)
    folderNotReady = QtCore.pyqtSignal(bool)
    def __init__(self, aStatus, checkEvery=1):
        super(Watcher_Mount_IC_Images_OD, self).__init__()
        self.status = aStatus
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkDevice)
    def _checkDevice(self):
        self.status = mount_ic_images_OD()
        if self.status:
            self._timer.stop()
            self.folderReady.emit(self.status)
        else:
            self.folderNotReady.emit(self.status)
    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()
#################################################################
class Watcher_Mount_Datasheet(QtCore.QObject):
    folderReady = QtCore.pyqtSignal(bool)
    folderNotReady = QtCore.pyqtSignal(bool)
    def __init__(self, aStatus, checkEvery=1):
        super(Watcher_Mount_Datasheet, self).__init__()
        self.status = aStatus
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkDevice)
    def _checkDevice(self):
        self.status = mount_datasheet()
        if self.status:
            self._timer.stop()
            self.folderReady.emit(self.status)
        else:
            self.folderNotReady.emit(self.status)
    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()
#################################################################
class Watcher_MongoDB(QtCore.QObject):
    mongoReady = QtCore.pyqtSignal(bool)
    mongoNotReady = QtCore.pyqtSignal(bool)
    def __init__(self, aStatus, checkEvery=1):
        super(Watcher_MongoDB, self).__init__()
        self.status = aStatus
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkDevice)
    def _checkDevice(self):
        self.status = MongoDB()
        if self.status:
            self._timer.stop()
            self.mongoReady.emit(self.status)
        else:
            self.mongoNotReady.emit(self.status)
    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()  
#################################################################
'''
class Watcher_Flags(QtCore.QObject):
    flagsReady = QtCore.pyqtSignal(bool)
    flagsNotReady = QtCore.pyqtSignal(bool)
    def __init__(self, aStatus, checkEvery=1):
        super(Watcher_Flags, self).__init__()
        self.status = aStatus
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(checkEvery * 1000)
        self._timer.timeout.connect(self._checkDevice)
    def _checkDevice(self):
        self.status = check_flag()
        if self.status:
            self._timer.stop()
            self.flagsReady.emit(self.status)
        else:
            self.flagsNotReady.emit(self.status)
    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()
'''