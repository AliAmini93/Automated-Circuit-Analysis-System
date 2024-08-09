import logging

logger = logging.getLogger("logger_Info")
logger.setLevel(logging.INFO)

f_handler = logging.FileHandler('log_Info.txt', 'w+', 'utf-8')
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
logger.propagate = False

logger_Debug = logging.getLogger("logger_Debug")
logger_Debug.setLevel(logging.DEBUG)
f_handler = logging.FileHandler('log_Debug.txt', 'w+', 'utf-8')
f_handler.setLevel(logging.DEBUG)
f_format = logging.Formatter('%(message)s')
f_handler.setFormatter(f_format)
logger_Debug.addHandler(f_handler)
logger_Debug.propagate = False

from database import collection_name
from ic_info.path import Path_Input, Path_UnverifiedFiles, Path_Downloads
from ic_info.search import search_textocr
from ocr import ocr
import time
import cv2
from ui import show_window
from logo_detection import logo_detection
from scipy import ndimage
import shutil
from multiprocessing import Process, Manager
import re
import os
import signal
import psutil
from contextlib import suppress
import numpy as np

start_time = time.time()


def clean_text(text):
    pattern = r'([A-Z|0-9]+[- /.]*)+[A-Z|0-9]'
    try:
        return re.search(pattern, text).group(0)
    except Exception as e:
        logger_Debug.exception(str(e))
        return ''


def sub_create_data(data, check_IC, name):
    print('*********************** Image: %s ***********************' % name)
    logger.info('*********************** Image: %s ***********************' % name)
    logger_Debug.info('*********************** Image: %s ***********************' % name)
    img = cv2.imread(Path_Input + name)
    img2 = img.copy()
    manufacturer = logo_detection(img)
    text_output, angle = ocr(img)
    print('Angle of the image: ', angle)
    logger.info('Angle of the image: %s' % str(angle))
    logger_Debug.info('Angle of the image: %s' % str(angle))
    img2 = ndimage.rotate(img2, angle, reshape=True)
    cv2.imwrite(Path_Input + name, img2)

    detect = False
    count_line = 0
    text = ''
    for j, text in enumerate(text_output):

        text = clean_text(text)
        if len(text) <= 3:
            continue
        count_line += 1

        if count_line > 3:
            break

        print('Part Number: %s' % text)
        logger.info('Part Number: %s' % text)
        logger_Debug.info('Part Number: %s' % text)

        data_IC = collection_name.find_one({"textOCR": {'$regex': '.*' + text + '.*'}})
        if data_IC != None:
            detect = True
            data_IC['picture'] = name
            data.append(data_IC)
            logger.info('This Part Number exists in the database')
            logger_Debug.info('This Part Number exists in the database')
            print('This Part Number exists in the database')
        elif data_IC == None:

            source = 'None'
            if text not in check_IC:
                data_IC, source = search_textocr(text, manufacturer)  # ,source
                check_IC.append(text)

            else:
                data_IC = [d for d in data if d['textOCR'] == text]
                if len(data_IC) != 0:
                    data_IC = data_IC[0].copy()
                else:
                    data_IC = None

            logger.info('This part number exist in the %s' % source)
            logger_Debug.info('This part number exist in the %s' % source)
            print('This part number exist in the %s' % source)

            if data_IC != None:
                detect = True
                data_IC['picture'] = name
                data.append(data_IC)  # += (data_IC,)

    if detect == False:
        data_IC = {'Manufacturer': '',
                   'Description': '',
                   'ManufacturerPartNumber': 'پیدا نشد',
                   'Category': '',
                   'DataSheetUrl': '-',
                   'textOCR': text,
                   'source': '',
                   'picture': name}

        data.append(data_IC)


def create_data():
    if os.path.exists(Path_UnverifiedFiles):
        shutil.rmtree(Path_UnverifiedFiles)
    os.makedirs(Path_UnverifiedFiles)
    if os.path.exists(Path_Downloads):
        shutil.rmtree(Path_Downloads)
    os.makedirs(Path_Downloads)
    pictures_IC = []
    procs = []

    manager = Manager()
    check_IC = manager.list()
    data = manager.list()

    for name in os.listdir(Path_Input):  # range(5,7):
        proc = Process(target=sub_create_data, args=(data, check_IC, name))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()

    PID_list = []
    for process in psutil.process_iter():
        if process.name() == 'chromedriver.exe':
                PID_list.append(process.pid)
        if process.name() == 'chrome.exe' and '--test-type=webdriver' in process.cmdline():
            with suppress(psutil.NoSuchProcess):
                PID_list.append(process.pid)
    for pid in set(PID_list):
        os.kill(pid, signal.SIGTERM)



    data = data.__deepcopy__({})



    for i, data_IC in enumerate(data):
        pictures_IC.append(data_IC['picture'])
        data_IC.pop('picture')

    for i, data_IC in enumerate(data):
        first_index = data.index(data_IC)
        data[i] = data[first_index]

    pictures_IC = np.array(pictures_IC)
    new_data = []
    new_pictures_IC = []
    for name in set(pictures_IC):
        indexes = np.where(pictures_IC == name)[0]
        for i in indexes:
            new_pictures_IC.append(pictures_IC[i])
            new_data.append(data[i])
    return new_data, new_pictures_IC


if __name__ == '__main__':
    data, pictures_IC = create_data()
    logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<< THE DATA IS >>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    logger.info(str(data))
    print('\n' + "<<<<<<<<<<<<<<<<<<<<<<<<<<<< THE DATA IS >>>>>>>>>>>>>>>>>>>>>>>>>>>>" + '\n')

    print("--- %.2f minutes ---" % ((time.time() - start_time) / 60))
    logger.info("--- %.2f minutes ---" % ((time.time() - start_time) / 60))
    show_window(data, pictures_IC)
